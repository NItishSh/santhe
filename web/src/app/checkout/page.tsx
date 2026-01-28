"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { useAuth } from "@/hooks/useAuth"
import { toast } from "sonner"

interface Product {
    id: number;
    name: string;
    price: number;
}

interface CartItem {
    id: number;
    product_id: number;
    quantity: number;
}

interface CartItemWithProduct extends CartItem {
    product?: Product;
}

interface UserProfile {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
    address?: string;
    phone_number?: string;
}

export default function CheckoutPage() {
    const { isAuthenticated, isLoading: authLoading } = useAuth()
    const router = useRouter()

    const [cartItems, setCartItems] = useState<CartItemWithProduct[]>([])
    const [products, setProducts] = useState<Map<number, Product>>(new Map())
    const [user, setUser] = useState<UserProfile | null>(null)
    const [isLoading, setIsLoading] = useState(true)
    const [isProcessing, setIsProcessing] = useState(false)

    // Form Stats
    const [address, setAddress] = useState("")
    const [phone, setPhone] = useState("")
    const [paymentMethod, setPaymentMethod] = useState("upi")

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            router.push('/login')
            return
        }

        if (isAuthenticated) {
            initializeCheckout()
        }
    }, [isAuthenticated, authLoading, router])

    const initializeCheckout = async () => {
        try {
            const token = localStorage.getItem('token')
            const headers = { 'Authorization': `Bearer ${token}` }

            // 1. Fetch User Profile
            const userRes = await fetch('/api/users/me', { headers })
            if (userRes.ok) {
                const userData = await userRes.json()
                setUser(userData)
                setAddress(userData.address || "")
                setPhone(userData.phone_number || "")
            }

            // 2. Fetch Cart
            const cartRes = await fetch('/api/cart', { headers })
            if (cartRes.ok) {
                const cartData = await cartRes.json()
                const items = cartData.items || []

                if (items.length === 0) {
                    router.push('/cart') // Redirect if empty
                    return
                }

                setCartItems(items)

                // 3. Fetch Product Details
                const productIds = items.map((i: CartItem) => i.product_id)
                await fetchProductDetails(productIds)
            }
        } catch (error) {
            console.error("Init failed", error)
            toast.error("Failed to load checkout details")
        } finally {
            setIsLoading(false)
        }
    }

    const fetchProductDetails = async (productIds: number[]) => {
        try {
            const response = await fetch('/api/products/search')
            if (response.ok) {
                const allProducts: Product[] = await response.json()
                const productMap = new Map<number, Product>()
                allProducts.forEach(p => {
                    if (productIds.includes(p.id)) {
                        productMap.set(p.id, p)
                    }
                })
                setProducts(productMap)
            }
        } catch (err) {
            console.error('Failed to fetch products', err)
        }
    }

    const calculateTotal = () => {
        return cartItems.reduce((sum, item) => {
            const product = products.get(item.product_id)
            return sum + (product ? product.price * item.quantity : 0)
        }, 0)
    }

    const handlePlaceOrder = async () => {
        if (!user) return
        setIsProcessing(true)

        try {
            const token = localStorage.getItem('token')
            const headers = {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }

            // 1. Create Order for EACH item (Backend limitation: Order = Single Item)
            // In a real app, backend should support multi-item orders.
            // We use Promise.all to do this concurrently.

            const orderPromises = cartItems.map(item => {
                return fetch('/api/orders', {
                    method: 'POST',
                    headers,
                    body: JSON.stringify({
                        farmer_id: 1, // Default Placeholder as per plan
                        middleman_id: user.id,
                        product_id: item.product_id,
                        quantity: item.quantity
                    })
                })
            })

            const orderResults = await Promise.all(orderPromises)
            const failedOrders = orderResults.filter(r => !r.ok)

            if (failedOrders.length > 0) {
                throw new Error("Failed to create some orders")
            }

            // 2. Process Payment
            const totalAmount = calculateTotal()
            const paymentRes = await fetch('/api/payments', {
                method: 'POST',
                headers,
                body: JSON.stringify({
                    user_id: user.id,
                    amount: totalAmount
                })
            })

            if (!paymentRes.ok) {
                throw new Error("Payment failed")
            }

            // 3. Clear Cart
            // Since our backend doesn't allow bulk delete yet, delete items individually
            const deletePromises = cartItems.map(item =>
                fetch(`/api/cart/items/${item.id}`, { method: 'DELETE', headers })
            )
            await Promise.all(deletePromises)

            // Success!
            toast.success("Order placed successfully!")
            router.push('/') // Or a success page

        } catch (error) {
            console.error("Order placement failed", error)
            toast.error("Failed to place order. Please try again.")
        } finally {
            setIsProcessing(false)
        }
    }

    if (authLoading || isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-600"></div>
            </div>
        )
    }

    const total = calculateTotal()

    return (
        <div className="min-h-screen bg-gray-50 py-12">
            <div className="container mx-auto px-4 max-w-4xl">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>

                <div className="grid md:grid-cols-3 gap-8">
                    {/* Left Column: Details */}
                    <div className="md:col-span-2 space-y-6">

                        {/* Shipping Address */}
                        <Card>
                            <CardHeader>
                                <CardTitle>Shipping Details</CardTitle>
                                <CardDescription>Confirm where you want your order delivered.</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="name">Full Name</Label>
                                    <Input id="name" value={user?.username || ""} disabled />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="address">Address</Label>
                                    <Input
                                        id="address"
                                        value={address}
                                        onChange={(e) => setAddress(e.target.value)}
                                        placeholder="123 Farm Road, Village..."
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="phone">Phone Number</Label>
                                    <Input
                                        id="phone"
                                        value={phone}
                                        onChange={(e) => setPhone(e.target.value)}
                                        placeholder="+91..."
                                    />
                                </div>
                            </CardContent>
                        </Card>

                        {/* Payment Method */}
                        <Card>
                            <CardHeader>
                                <CardTitle>Payment Method</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="grid grid-cols-2 gap-4">
                                    <div
                                        className={`border rounded-lg p-4 cursor-pointer flex flex-col items-center gap-2 ${paymentMethod === 'upi' ? 'border-green-600 bg-green-50' : 'hover:bg-gray-50'}`}
                                        onClick={() => setPaymentMethod('upi')}
                                    >
                                        <span className="text-2xl">📱</span>
                                        <span className="font-medium">UPI</span>
                                    </div>
                                    <div
                                        className={`border rounded-lg p-4 cursor-pointer flex flex-col items-center gap-2 ${paymentMethod === 'card' ? 'border-green-600 bg-green-50' : 'hover:bg-gray-50'}`}
                                        onClick={() => setPaymentMethod('card')}
                                    >
                                        <span className="text-2xl">💳</span>
                                        <span className="font-medium">Card</span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                    </div>

                    {/* Right Column: Summary */}
                    <div>
                        <Card className="sticky top-4">
                            <CardHeader>
                                <CardTitle>Order Summary</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-2 max-h-60 overflow-y-auto">
                                    {cartItems.map(item => {
                                        const product = products.get(item.product_id)
                                        return (
                                            <div key={item.id} className="flex justify-between text-sm">
                                                <span>{product?.name || "Unknown Item"} (x{item.quantity})</span>
                                                <span className="font-medium">₹{((product?.price || 0) * item.quantity).toFixed(2)}</span>
                                            </div>
                                        )
                                    })}
                                </div>
                                <Separator />
                                <div className="flex justify-between font-medium">
                                    <span>Subtotal</span>
                                    <span>₹{total.toFixed(2)}</span>
                                </div>
                                <div className="flex justify-between text-green-600">
                                    <span>Delivery</span>
                                    <span>Free</span>
                                </div>
                                <Separator />
                                <div className="flex justify-between font-bold text-lg">
                                    <span>Total</span>
                                    <span>₹{total.toFixed(2)}</span>
                                </div>
                            </CardContent>
                            <CardFooter>
                                <Button
                                    className="w-full bg-green-600 hover:bg-green-700"
                                    size="lg"
                                    onClick={handlePlaceOrder}
                                    disabled={isProcessing}
                                >
                                    {isProcessing ? "Processing..." : `Pay ₹${total.toFixed(2)}`}
                                </Button>
                            </CardFooter>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    )
}
