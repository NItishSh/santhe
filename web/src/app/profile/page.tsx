"use client"

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { useUser } from "@/hooks/useUser";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function ProfilePage() {
    const { user, loading } = useUser();
    const { logout, isAuthenticated, isLoading: authLoading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            router.push('/login');
        }
    }, [isAuthenticated, authLoading, router]);

    if (loading || authLoading) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-muted-foreground">Loading profile...</p>
                </div>
            </div>
        );
    }

    if (!user) return null;

    return (
        <div className="flex min-h-screen flex-col items-center bg-gray-50/50 p-6">
            <div className="w-full max-w-2xl">
                <div className="mb-8 flex items-center justify-between">
                    <h1 className="text-3xl font-bold tracking-tight">My Profile</h1>
                    <Button variant="outline" onClick={() => router.push('/')}>
                        Back to Home
                    </Button>
                </div>

                <div className="grid gap-6">
                    <Card>
                        <CardHeader className="flex flex-row items-center gap-4 space-y-0">
                            <Avatar className="h-20 w-20">
                                <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${user.first_name} ${user.last_name}`} />
                                <AvatarFallback>{user.first_name?.[0]?.toUpperCase()}{user.last_name?.[0]?.toUpperCase()}</AvatarFallback>
                            </Avatar>
                            <div className="flex-1">
                                <CardTitle className="text-2xl">{user.first_name} {user.last_name}</CardTitle>
                                <CardDescription className="text-base">{user.email}</CardDescription>
                                <div className="mt-2">
                                    <Badge variant="secondary" className="capitalize">
                                        {user.role}
                                    </Badge>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="mt-6 space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="grid gap-2">
                                    <h3 className="text-sm font-medium text-muted-foreground">Full Name</h3>
                                    <p className="text-lg font-medium">{user.first_name} {user.last_name}</p>
                                </div>
                                <div className="grid gap-2">
                                    <h3 className="text-sm font-medium text-muted-foreground">Username</h3>
                                    <p className="text-lg font-medium">{user.username}</p>
                                </div>
                                <div className="grid gap-2">
                                    <h3 className="text-sm font-medium text-muted-foreground">Date of Birth</h3>
                                    <p className="text-lg font-medium">{user.date_of_birth || "Not provided"}</p>
                                </div>
                                <div className="grid gap-2">
                                    <h3 className="text-sm font-medium text-muted-foreground">Phone</h3>
                                    <p className="text-lg font-medium">{user.phone_number || "Not provided"}</p>
                                </div>
                            </div>

                            <div className="grid gap-2">
                                <h3 className="text-sm font-medium text-muted-foreground">Address</h3>
                                <p className="text-lg font-medium">{user.address || "Not provided"}</p>
                            </div>

                            <div className="grid gap-2">
                                <h3 className="text-sm font-medium text-muted-foreground">Payment Info (UPI)</h3>
                                <p className="text-lg font-medium font-mono bg-muted p-2 rounded w-fit">
                                    {user.payment_method_token || "Not linked"}
                                </p>
                            </div>

                            <div className="grid gap-2">
                                <h3 className="text-sm font-medium text-muted-foreground">Email Address</h3>
                                <p className="text-lg font-medium">{user.email}</p>
                            </div>
                        </CardContent>
                        <CardFooter className="flex justify-between border-t bg-muted/50 p-6">
                            <div className="text-sm text-muted-foreground">
                                Member since {new Date().getFullYear()}
                            </div>
                            <Button variant="destructive" onClick={logout}>
                                Log Out
                            </Button>
                        </CardFooter>
                    </Card>

                    {/* Placeholder for future sections */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Account Settings</CardTitle>
                            <CardDescription>Manage your account preferences and security.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-sm text-muted-foreground">
                                Settings like password change and notification preferences will appear here.
                            </p>
                        </CardContent>
                        <CardFooter>
                            <Button variant="outline" disabled>Coming Soon</Button>
                        </CardFooter>
                    </Card>
                </div>
            </div>
        </div>
    );
}
