"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useAuth } from "@/hooks/useAuth"
import { toast } from "sonner"
import { motion } from "framer-motion"
import { CreditCard, Smartphone, CheckCircle2, User as UserIcon, MapPin, Phone } from "lucide-react"

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

            // 1. Create Order for EACH item
            const orderPromises = cartItems.map(item => {
                return fetch('/api/orders', {
                    method: 'POST',
                    headers,
                    body: JSON.stringify({
                        farmer_id: 1,
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
            const deletePromises = cartItems.map(item =>
                fetch(`/api/cart/items/${item.id}`, { method: 'DELETE', headers })
            )
            await Promise.all(deletePromises)

            toast.success("Order placed successfully!")
            // Small delay to allow toast to be seen
            await new Promise(resolve => setTimeout(resolve, 1500))
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
            <div className="flex items-center justify-center min-h-screen bg-orange-50/30">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
            </div>
        )
    }

    const total = calculateTotal()

    return (
        <div className="min-h-screen bg-orange-50/30 py-12">
            <div className="container mx-auto px-4 max-w-5xl">
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-8"
                >
                    <h1 className="text-3xl font-bold font-heading text-gray-800">Checkout</h1>
                    <p className="text-muted-foreground">Detailed summary of your order</p>
                </motion.div>

                <div className="grid md:grid-cols-3 gap-8">
                    {/* Left Column: Forms */}
                    <div className="md:col-span-2 space-y-6">

                        {/* Shipping Info */}
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.1 }}
                            className="bg-white/70 backdrop-blur-md rounded-2xl p-6 border border-white/50 shadow-sm"
                        >
                            <h2 className="text-xl font-bold font-heading mb-4 flex items-center gap-2">
                                <MapPin className="text-primary w-5 h-5" /> Shipping Details
                            </h2>
                            <div className="space-y-4">
                                <div className="space-y-2">
                                    <Label className="text-muted-foreground flex items-center gap-2">
                                        <UserIcon className="w-4 h-4" /> Full Name
                                    </Label>
                                    <Input value={user?.username || ""} disabled className="bg-gray-50/50" />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-muted-foreground flex items-center gap-2">
                                        <MapPin className="w-4 h-4" /> Address
                                    </Label>
                                    <Input
                                        value={address}
                                        onChange={(e) => setAddress(e.target.value)}
                                        placeholder="123 Farm Road, Village..."
                                        className="h-12"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-muted-foreground flex items-center gap-2">
                                        <Phone className="w-4 h-4" /> Phone Number
                                    </Label>
                                    <Input
                                        value={phone}
                                        onChange={(e) => setPhone(e.target.value)}
                                        placeholder="+91..."
                                        className="h-12"
                                    />
                                </div>
                            </div>
                        </motion.div>

                        {/* Payment Selection */}
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.2 }}
                            className="bg-white/70 backdrop-blur-md rounded-2xl p-6 border border-white/50 shadow-sm"
                        >
                            <h2 className="text-xl font-bold font-heading mb-4 flex items-center gap-2">
                                <CreditCard className="text-primary w-5 h-5" /> Payment Method
                            </h2>
                            <div className="grid grid-cols-2 gap-4">
                                <div
                                    className={`relative border rounded-xl p-4 cursor-pointer flex flex-col items-center justify-center gap-2 transition-all duration-300 ${paymentMethod === 'upi' ? 'border-primary bg-primary/5 shadow-md scale-[1.02]' : 'border-gray-200 hover:border-primary/50 hover:bg-white'}`}
                                    onClick={() => setPaymentMethod('upi')}
                                >
                                    {paymentMethod === 'upi' && (
                                        <div className="absolute top-2 right-2 text-primary">
                                            <CheckCircle2 className="w-5 h-5 fill-primary/10" />
                                        </div>
                                    )}
                                    <Smartphone className={`w-8 h-8 ${paymentMethod === 'upi' ? 'text-primary' : 'text-gray-400'}`} />
                                    <span className="font-semibold">UPI</span>
                                </div>
                                <div
                                    className={`relative border rounded-xl p-4 cursor-pointer flex flex-col items-center justify-center gap-2 transition-all duration-300 ${paymentMethod === 'card' ? 'border-primary bg-primary/5 shadow-md scale-[1.02]' : 'border-gray-200 hover:border-primary/50 hover:bg-white'}`}
                                    onClick={() => setPaymentMethod('card')}
                                >
                                    {paymentMethod === 'card' && (
                                        <div className="absolute top-2 right-2 text-primary">
                                            <CheckCircle2 className="w-5 h-5 fill-primary/10" />
                                        </div>
                                    )}
                                    <CreditCard className={`w-8 h-8 ${paymentMethod === 'card' ? 'text-primary' : 'text-gray-400'}`} />
                                    <span className="font-semibold">Card</span>
                                </div>
                            </div>
                        </motion.div>
                    </div>

                    {/* Right Column: Order Summary */}
                    <div className="relative">
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.3 }}
                            className="sticky top-24 bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-white/60 shadow-lg"
                        >
                            <h2 className="text-xl font-bold font-heading mb-6 border-b pb-4">Order Summary</h2>

                            <div className="space-y-4 mb-6 max-h-[300px] overflow-y-auto custom-scrollbar pr-2">
                                {cartItems.map(item => {
                                    const product = products.get(item.product_id)
                                    return (
                                        <div key={item.id} className="flex justify-between text-sm py-2 border-b border-dashed border-gray-100 last:border-0">
                                            <div className="flex flex-col">
                                                <span className="font-medium">{product?.name || "Item"}</span>
                                                <span className="text-xs text-muted-foreground">Qty: {item.quantity}</span>
                                            </div>
                                            <span className="font-medium">₹{((product?.price || 0) * item.quantity).toFixed(2)}</span>
                                        </div>
                                    )
                                })}
                            </div>

                            <div className="space-y-2 pt-4 border-t">
                                <div className="flex justify-between text-sm">
                                    <span className="text-muted-foreground">Subtotal</span>
                                    <span>₹{total.toFixed(2)}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-muted-foreground">Delivery</span>
                                    <span className="text-green-600 font-medium">Free</span>
                                </div>
                                <div className="flex justify-between font-bold text-xl pt-2 text-primary">
                                    <span>Total</span>
                                    <span>₹{total.toFixed(2)}</span>
                                </div>
                            </div>

                            <Button
                                className="w-full mt-6 shadow-lg shadow-orange-500/20 text-lg py-6"
                                size="lg"
                                onClick={handlePlaceOrder}
                                disabled={isProcessing}
                            >
                                {isProcessing ? (
                                    <span className="flex items-center gap-2">
                                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white/50 border-t-white"></div>
                                        Processing...
                                    </span>
                                ) : (
                                    `Pay ₹${total.toFixed(2)}`
                                )}
                            </Button>
                        </motion.div>
                    </div>
                </div>
            </div>
        </div>
    )
}
