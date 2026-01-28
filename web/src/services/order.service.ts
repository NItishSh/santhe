import { httpClient } from "@/lib/http-client";

export interface OrderItem {
    id: number;
    product_name: string;
    quantity: number;
    price: number;
}

export interface Order {
    id: number;
    date: string;
    status: 'pending' | 'shipped' | 'delivered' | 'cancelled';
    total: number;
    items: OrderItem[];
}

export const orderService = {
    getMyOrders: async (): Promise<Order[]> => {
        // Implementation once backend is ready
        // return httpClient.get<Order[]>('/orders');

        // Mock data for now to satisfy task: "Implement Orders Page"
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve([
                    {
                        id: 101,
                        date: '2023-11-20',
                        status: 'delivered',
                        total: 1250,
                        items: [
                            { id: 1, product_name: 'Organic Rice', quantity: 1, price: 1250 }
                        ]
                    },
                    {
                        id: 102,
                        date: '2023-12-05',
                        status: 'pending',
                        total: 450,
                        items: [
                            { id: 2, product_name: 'Fresh Tomatoes', quantity: 2, price: 225 }
                        ]
                    }
                ]);
            }, 800);
        });
    }
};
