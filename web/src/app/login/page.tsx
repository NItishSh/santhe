"use client"

import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import Link from "next/link"
import { useState } from "react"
import { api } from "@/lib/api"
import { useRouter } from "next/navigation"

export default function LoginPage() {
    const router = useRouter()
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!email || !password) {
            setError("Please fill in all fields")
            return
        }

        try {
            const data = await api.auth.login(email.split('@')[0], password); // Using email part as username 

            localStorage.setItem('token', data.access_token)
            // alert("Login successful!") // Removed as per user request
            router.push("/")
            window.dispatchEvent(new Event("storage")) // Trigger storage event for other components if needed (though local state might need context)
        } catch (err: any) {
            setError(err.message || "Invalid credentials")
        }
    }

    return (
        <div className="flex min-h-screen items-center justify-center bg-muted/40 p-4">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle className="text-2xl">Login</CardTitle>
                    <CardDescription>
                        Enter your email below to login to your account.
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="grid gap-4">
                        <div className="grid gap-2">
                            <Label htmlFor="email">Username or Email</Label>
                            <Input
                                id="email"
                                type="text"
                                placeholder="Username or m@example.com"
                                required
                                value={email}
                                onChange={(e) => {
                                    setEmail(e.target.value)
                                    setError("")
                                }}
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label htmlFor="password">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                required
                                value={password}
                                onChange={(e) => {
                                    setPassword(e.target.value)
                                    setError("")
                                }}
                            />
                        </div>
                        {error && (
                            <p className="text-sm text-red-500 font-medium">{error}</p>
                        )}
                    </CardContent>
                    <CardFooter className="flex flex-col gap-4">
                        <Button className="w-full" type="submit">Sign in</Button>
                        <div className="text-center text-sm text-muted-foreground">
                            Don&apos;t have an account?{" "}
                            <Link href="/register" className="underline hover:text-primary">
                                Sign up
                            </Link>
                        </div>
                    </CardFooter>
                </form>
            </Card>
        </div>
    )
}
