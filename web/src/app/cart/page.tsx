"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/hooks/useAuth"

interface CartItem {
    id: number;
    product_id: number;
    product_name: string;
    quantity: number;
    unit_price: number;
    total_price: number;
}

interface Cart {
    id: number;
    user_id: number;
    items: CartItem[];
    total: number;
}

export default function CartPage() {
    const { isAuthenticated, isLoading: authLoading } = useAuth()
    const router = useRouter()
    const [cart, setCart] = useState<Cart | null>(null)
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            router.push('/login')
            return
        }

        if (isAuthenticated) {
            fetchCart()
        }
    }, [isAuthenticated, authLoading, router])

    const fetchCart = async () => {
        try {
            const token = localStorage.getItem('token')
            const response = await fetch('/api/cart', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })

            if (response.ok) {
                const data = await response.json()
                setCart(data)
            } else if (response.status === 404) {
                // No cart yet - that's okay
                setCart({ id: 0, user_id: 0, items: [], total: 0 })
            } else {
                setError('Failed to load cart')
            }
        } catch (err) {
            setError('Failed to connect to cart service')
        } finally {
            setIsLoading(false)
        }
    }

    const updateQuantity = async (itemId: number, newQuantity: number) => {
        if (newQuantity < 1) {
            await removeItem(itemId)
            return
        }

        try {
            const token = localStorage.getItem('token')
            await fetch(`/api/cart/items/${itemId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: newQuantity })
            })
            fetchCart()
        } catch (err) {
            setError('Failed to update quantity')
        }
    }

    const removeItem = async (itemId: number) => {
        try {
            const token = localStorage.getItem('token')
            await fetch(`/api/cart/items/${itemId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            fetchCart()
        } catch (err) {
            setError('Failed to remove item')
        }
    }

    if (authLoading || isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-600"></div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
            <header className="bg-white shadow-sm sticky top-0 z-40">
                <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                    <h1
                        className="text-2xl font-bold text-green-700 cursor-pointer"
                        onClick={() => router.push('/')}
                    >
                        🛒 Santhe
                    </h1>
                    <Button variant="outline" onClick={() => router.push('/')}>
                        Continue Shopping
                    </Button>
                </div>
            </header>

            <main className="container mx-auto px-4 py-8">
                <h2 className="text-3xl font-bold text-gray-800 mb-8">Your Cart</h2>

                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
                        {error}
                    </div>
                )}

                {cart && cart.items.length === 0 ? (
                    <Card className="text-center py-12">
                        <CardContent>
                            <div className="text-6xl mb-4">🛒</div>
                            <h3 className="text-xl font-semibold text-gray-700 mb-2">Your cart is empty</h3>
                            <p className="text-gray-500 mb-6">Add some fresh products to get started!</p>
                            <Button onClick={() => router.push('/')}>
                                Browse Products
                            </Button>
                        </CardContent>
                    </Card>
                ) : (
                    <div className="grid md:grid-cols-3 gap-8">
                        {/* Cart Items */}
                        <div className="md:col-span-2 space-y-4">
                            {cart?.items.map((item) => (
                                <Card key={item.id}>
                                    <CardContent className="flex items-center justify-between py-4">
                                        <div className="flex-1">
                                            <h3 className="font-semibold text-lg">{item.product_name}</h3>
                                            <p className="text-gray-500">₹{(item.unit_price ?? 0).toFixed(2)} each</p>
                                        </div>

                                        <div className="flex items-center gap-4">
                                            <div className="flex items-center gap-2">
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                                >
                                                    -
                                                </Button>
                                                <span className="w-8 text-center font-medium">{item.quantity}</span>
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                                >
                                                    +
                                                </Button>
                                            </div>

                                            <p className="font-semibold w-24 text-right">
                                                ₹{(item.total_price ?? 0).toFixed(2)}
                                            </p>

                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                className="text-red-500 hover:text-red-700"
                                                onClick={() => removeItem(item.id)}
                                            >
                                                ✕
                                            </Button>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>

                        {/* Order Summary */}
                        <div>
                            <Card>
                                <CardHeader>
                                    <CardTitle>Order Summary</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="flex justify-between">
                                        <span>Subtotal</span>
                                        <span>₹{(cart?.total ?? 0).toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span>Delivery</span>
                                        <span className="text-green-600">FREE</span>
                                    </div>
                                    <div className="border-t pt-4 flex justify-between font-bold text-lg">
                                        <span>Total</span>
                                        <span>₹{(cart?.total ?? 0).toFixed(2)}</span>
                                    </div>
                                </CardContent>
                                <CardFooter>
                                    <Button className="w-full bg-green-600 hover:bg-green-700">
                                        Proceed to Checkout
                                    </Button>
                                </CardFooter>
                            </Card>
                        </div>
                    </div>
                )}
            </main>
        </div>
    )
}
