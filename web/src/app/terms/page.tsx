import { Card } from "@/components/ui/card";

export default function TermsPage() {
    return (
        <div className="container mx-auto px-4 py-12 max-w-4xl">
            <h1 className="text-3xl font-bold font-heading mb-6">Terms of Service</h1>
            <Card className="p-8 bg-white/60 backdrop-blur-md border border-white/50 shadow-sm">
                <div className="prose prose-sm max-w-none text-muted-foreground">
                    <p>Last updated: January 2026</p>
                    <h3 className="text-foreground font-semibold mt-4">1. Acceptance of Terms</h3>
                    <p>By accessing or using our Services, you agree to be bound by these Terms. If you do not agree to these Terms, you may not access or use the Services.</p>

                    <h3 className="text-foreground font-semibold mt-4">2. Description of Services</h3>
                    <p>Santhe provides a marketplace platform connecting farmers and consumers. We are not a party to any transaction between buyers and sellers.</p>

                    <h3 className="text-foreground font-semibold mt-4">3. User Conduct</h3>
                    <p>You agree to use the Services only for purposes that are permitted by these Terms and any applicable law, regulation or generally accepted practices or guidelines in the relevant jurisdictions.</p>
                </div>
            </Card>
        </div>
    );
}
