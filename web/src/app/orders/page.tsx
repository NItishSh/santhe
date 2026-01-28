"use client"

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useOrders } from "@/hooks/useOrders";

export default function OrdersPage() {
    const router = useRouter();
    const { orders, loading, error } = useOrders();

    return (
        <div className="flex min-h-screen flex-col items-center bg-gray-50/50 p-6">
            <div className="w-full max-w-2xl">
                <div className="mb-8 flex items-center justify-between">
                    <h1 className="text-3xl font-bold tracking-tight">Orders</h1>
                    <Button variant="outline" onClick={() => router.push('/')}>
                        Back to Home
                    </Button>
                </div>

                <div className="grid gap-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Your Orders</CardTitle>
                            <CardDescription>View and track your current and past orders.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            {loading ? (
                                <div className="text-center py-10">Loading orders...</div>
                            ) : error ? (
                                <div className="text-center py-10 text-red-500">{error}</div>
                            ) : orders.length === 0 ? (
                                <p className="text-muted-foreground text-center py-10">
                                    No orders found. Start shopping to see your orders here!
                                </p>
                            ) : (
                                <div className="space-y-4">
                                    {orders.map((order) => (
                                        <div key={order.id} className="border rounded-lg p-4 flex flex-col md:flex-row justify-between gap-4">
                                            <div>
                                                <div className="font-semibold">Order #{order.id}</div>
                                                <div className="text-sm text-muted-foreground">{order.date}</div>
                                                <div className="mt-2 space-y-1">
                                                    {order.items.map(item => (
                                                        <div key={item.id} className="text-sm">
                                                            {item.quantity}x {item.product_name}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                            <div className="flex flex-col items-end gap-2">
                                                <Badge variant={order.status === 'delivered' ? 'default' : 'secondary'}>
                                                    {order.status}
                                                </Badge>
                                                <div className="font-medium">₹{order.total}</div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
