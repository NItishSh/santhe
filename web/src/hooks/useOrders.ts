import { useState, useEffect } from 'react';
import { orderService, Order } from '@/services/order.service';

export function useOrders() {
    const [orders, setOrders] = useState<Order[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                setLoading(true);
                const data = await orderService.getMyOrders();
                setOrders(data);
            } catch (err: any) {
                setError(err.message || 'Failed to fetch orders');
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, []);

    return {
        orders,
        loading,
        error
    };
}
