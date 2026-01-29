import { Card } from "@/components/ui/card";

export default function PrivacyPage() {
    return (
        <div className="container mx-auto px-4 py-12 max-w-4xl">
            <h1 className="text-3xl font-bold font-heading mb-6">Privacy Policy</h1>
            <Card className="p-8 bg-white/60 backdrop-blur-md border border-white/50 shadow-sm">
                <div className="prose prose-sm max-w-none text-muted-foreground">
                    <p>Last updated: January 2026</p>
                    <h3 className="text-foreground font-semibold mt-4">1. Information We Collect</h3>
                    <p>We collect information you provide directly to us, such as when you create or modify your account, request on-demand services, contact customer support, or otherwise communicate with us.</p>

                    <h3 className="text-foreground font-semibold mt-4">2. How We Use Your Information</h3>
                    <p>We use the information we collect to provide, maintain, and improve our services, such as to facilitate payments, send receipts, provide products and services you request, and send you related information.</p>

                    <h3 className="text-foreground font-semibold mt-4">3. Sharing of Information</h3>
                    <p>We may share the information we collect about you as described in this Statement or as described at the time of collection or sharing.</p>
                </div>
            </Card>
        </div>
    );
}
