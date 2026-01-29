"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/hooks/useAuth"
import { motion, AnimatePresence } from "framer-motion"
import { Trash2, Plus, Minus, ShoppingCart } from "lucide-react"

interface Product {
    id: number;
    name: string;
    price: number;
    image_url?: string;
}

interface CartItem {
    id: number;
    product_id: number;
    quantity: number;
}

interface CartItemWithProduct extends CartItem {
    product?: Product;
}

interface CartResponse {
    id: number;
    items: CartItem[];
}

export default function CartPage() {
    const { isAuthenticated, isLoading: authLoading } = useAuth()
    const router = useRouter()
    const [cartItems, setCartItems] = useState<CartItemWithProduct[]>([])
    const [products, setProducts] = useState<Map<number, Product>>(new Map())
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
                headers: { 'Authorization': `Bearer ${token}` }
            })

            if (response.ok) {
                const data: CartResponse = await response.json()
                const sortedItems = [...(data.items || [])].sort((a, b) => a.id - b.id)
                setCartItems(sortedItems)

                if (data.items && data.items.length > 0) {
                    await fetchProductDetails(data.items.map(item => item.product_id))
                }
            } else if (response.status === 404) {
                setCartItems([])
            } else {
                setError('Failed to load cart')
            }
        } catch (err) {
            setError('Failed to connect to cart service')
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
            console.error('Failed to fetch product details', err)
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
                method: 'PATCH',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
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
                headers: { 'Authorization': `Bearer ${token}` }
            })
            fetchCart()
        } catch (err) {
            setError('Failed to remove item')
        }
    }

    const getItemTotal = (item: CartItemWithProduct): number => {
        const product = products.get(item.product_id)
        return product ? product.price * item.quantity : 0
    }

    const getCartTotal = (): number => {
        return cartItems.reduce((sum, item) => sum + getItemTotal(item), 0)
    }

    if (authLoading || isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-orange-50/30">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-orange-50/30 py-12">
            <div className="container mx-auto px-4 max-w-6xl">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <h1 className="text-4xl font-bold font-heading mb-8 flex items-center gap-3">
                        <ShoppingCart className="w-8 h-8 text-primary" />
                        Your Cart
                    </h1>

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6 backdrop-blur-sm">
                            {error}
                        </div>
                    )}

                    {cartItems.length === 0 ? (
                        <div className="text-center py-20 bg-white/60 backdrop-blur-md rounded-2xl border border-white/50 shadow-sm">
                            <div className="text-6xl mb-6">🛒</div>
                            <h3 className="text-2xl font-bold font-heading text-gray-800 mb-2">Your cart is empty</h3>
                            <p className="text-muted-foreground mb-8">Looks like you haven't added anything yet.</p>
                            <Button size="lg" onClick={() => router.push('/')}>
                                Start Shopping
                            </Button>
                        </div>
                    ) : (
                        <div className="grid md:grid-cols-3 gap-8">
                            {/* Cart Items */}
                            <div className="md:col-span-2 space-y-4">
                                <AnimatePresence>
                                    {cartItems.map((item) => {
                                        const product = products.get(item.product_id)
                                        return (
                                            <motion.div
                                                key={item.id}
                                                layout
                                                initial={{ opacity: 0, x: -20 }}
                                                animate={{ opacity: 1, x: 0 }}
                                                exit={{ opacity: 0, x: -20 }}
                                                className="bg-white/70 backdrop-blur-md rounded-xl p-4 border border-white/50 shadow-sm hover:shadow-md transition-shadow"
                                            >
                                                <div className="flex items-center justify-between gap-4">
                                                    <div className="flex-1">
                                                        <h3 className="font-bold text-lg text-foreground">
                                                            {product?.name || `Product #${item.product_id}`}
                                                        </h3>
                                                        <p className="text-sm text-muted-foreground">
                                                            ₹{(product?.price ?? 0).toFixed(2)} / unit
                                                        </p>
                                                    </div>

                                                    <div className="flex items-center gap-6">
                                                        <div className="flex items-center bg-white rounded-lg border shadow-sm">
                                                            <Button
                                                                variant="ghost"
                                                                size="icon"
                                                                className="h-8 w-8 rounded-r-none hover:bg-gray-100"
                                                                onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                                            >
                                                                <Minus className="w-3 h-3" />
                                                            </Button>
                                                            <span className="w-8 text-center font-medium text-sm">{item.quantity}</span>
                                                            <Button
                                                                variant="ghost"
                                                                size="icon"
                                                                className="h-8 w-8 rounded-l-none hover:bg-gray-100"
                                                                onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                                            >
                                                                <Plus className="w-3 h-3" />
                                                            </Button>
                                                        </div>

                                                        <div className="text-right min-w-[80px]">
                                                            <p className="font-bold text-lg text-primary">
                                                                ₹{getItemTotal(item).toFixed(2)}
                                                            </p>
                                                        </div>

                                                        <Button
                                                            variant="ghost"
                                                            size="icon"
                                                            className="text-muted-foreground hover:text-red-500 hover:bg-red-50"
                                                            onClick={() => removeItem(item.id)}
                                                        >
                                                            <Trash2 className="w-4 h-4" />
                                                        </Button>
                                                    </div>
                                                </div>
                                            </motion.div>
                                        )
                                    })}
                                </AnimatePresence>
                            </div>

                            {/* Order Summary */}
                            <div className="relative">
                                <div className="sticky top-24">
                                    <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-white/60 shadow-lg">
                                        <h2 className="text-xl font-bold font-heading mb-6 border-b pb-4">Order Summary</h2>

                                        <div className="space-y-4 mb-6">
                                            <div className="flex justify-between text-sm">
                                                <span className="text-muted-foreground">Subtotal</span>
                                                <span className="font-medium">₹{getCartTotal().toFixed(2)}</span>
                                            </div>
                                            <div className="flex justify-between text-sm">
                                                <span className="text-muted-foreground">Delivery</span>
                                                <span className="text-green-600 font-medium">Free</span>
                                            </div>
                                            <div className="pt-4 border-t flex justify-between items-end">
                                                <span className="font-bold text-lg">Total</span>
                                                <span className="font-bold text-2xl text-primary">₹{getCartTotal().toFixed(2)}</span>
                                            </div>
                                        </div>

                                        <Button
                                            size="lg"
                                            className="w-full shadow-lg shadow-orange-500/20 text-lg py-6"
                                            onClick={() => router.push('/checkout')}
                                        >
                                            Proceed to Checkout
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </motion.div>
            </div>
        </div>
    )
}
