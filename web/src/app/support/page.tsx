"use client"

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function SupportPage() {
    const router = useRouter();

    return (
        <div className="flex min-h-screen flex-col items-center bg-gray-50/50 p-6">
            <div className="w-full max-w-2xl">
                <div className="mb-8 flex items-center justify-between">
                    <h1 className="text-3xl font-bold tracking-tight">Support</h1>
                    <Button variant="outline" onClick={() => router.push('/')}>
                        Back to Home
                    </Button>
                </div>

                <div className="grid gap-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Help & Support</CardTitle>
                            <CardDescription>Get assistance with your orders and account.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground text-center py-10">
                                Support resources coming soon. For urgent matters, please contact support@example.com.
                            </p>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
