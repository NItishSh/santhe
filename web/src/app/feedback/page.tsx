"use client"

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { supportService } from "@/services/support.service";

export default function FeedbackPage() {
    const router = useRouter();
    const [category, setCategory] = useState("general");
    const [message, setMessage] = useState("");
    const [rating, setRating] = useState(5);
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await supportService.sendFeedback({ category, message, rating });
            setSubmitted(true);
        } catch (error) {
            console.error("Failed to send feedback", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen flex-col items-center bg-gray-50/50 p-6">
            <div className="w-full max-w-2xl">
                <div className="mb-8 flex items-center justify-between">
                    <h1 className="text-3xl font-bold tracking-tight">Feedback</h1>
                    <Button variant="outline" onClick={() => router.push('/')}>
                        Back to Home
                    </Button>
                </div>

                <div className="grid gap-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Share Your Feedback</CardTitle>
                            <CardDescription>We value your opinion. Let us know how we can improve.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            {submitted ? (
                                <div className="text-center py-10 space-y-4">
                                    <div className="text-4xl">🎉</div>
                                    <h3 className="text-xl font-semibold">Thank you for your feedback!</h3>
                                    <p className="text-muted-foreground">Your input helps us make Santhe better.</p>
                                    <Button onClick={() => router.push('/')}>Return Home</Button>
                                </div>
                            ) : (
                                <form onSubmit={handleSubmit} className="space-y-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="category">Category</Label>
                                        <select
                                            id="category"
                                            className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm"
                                            value={category}
                                            onChange={(e) => setCategory(e.target.value)}
                                        >
                                            <option value="general">General</option>
                                            <option value="bug">Report a Bug</option>
                                            <option value="feature">Feature Request</option>
                                            <option value="order">Order Issue</option>
                                        </select>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="message">Message</Label>
                                        <Textarea
                                            id="message"
                                            placeholder="Tell us what you think..."
                                            value={message}
                                            onChange={(e) => setMessage(e.target.value)}
                                            required
                                            className="min-h-[100px]"
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="rating">Rating</Label>
                                        <div className="flex gap-2">
                                            {[1, 2, 3, 4, 5].map((star) => (
                                                <Button
                                                    key={star}
                                                    type="button"
                                                    variant={rating === star ? "default" : "outline"}
                                                    size="sm"
                                                    onClick={() => setRating(star)}
                                                    className="w-10 h-10"
                                                >
                                                    {star}
                                                </Button>
                                            ))}
                                        </div>
                                    </div>

                                    <Button type="submit" className="w-full" disabled={loading}>
                                        {loading ? "Sending..." : "Submit Feedback"}
                                    </Button>
                                </form>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
