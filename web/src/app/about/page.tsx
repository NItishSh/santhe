import { Card } from "@/components/ui/card";

export default function AboutPage() {
    return (
        <div className="container mx-auto px-4 py-12 max-w-4xl">
            <h1 className="text-4xl font-bold font-heading mb-6 text-center">About Santhe</h1>
            <Card className="p-8 bg-white/60 backdrop-blur-md border border-white/50 shadow-sm">
                <div className="prose prose-lg prose-orange mx-auto">
                    <p className="lead text-xl text-muted-foreground mb-6">
                        Santhe is a community-driven marketplace connecting local farmers directly with consumers. We believe in fresh produce, fair prices, and transparency.
                    </p>
                    <div className="grid md:grid-cols-2 gap-8 my-10">
                        <div className="bg-orange-50/50 p-6 rounded-xl">
                            <h3 className="text-xl font-bold mb-2">For Farmers</h3>
                            <p>Direct access to market, better rates, and immediate payments.</p>
                        </div>
                        <div className="bg-green-50/50 p-6 rounded-xl">
                            <h3 className="text-xl font-bold mb-2">For You</h3>
                            <p>Farm-fresh vegetables, fruits, and grains harvested just hours ago.</p>
                        </div>
                    </div>
                    <p>
                        Our mission is to eliminate the middleman inefficiency (while empowering ethical middlemen functionality where needed!) and ensure that the goodness of the farm reaches your plate with love.
                    </p>
                </div>
            </Card>
        </div>
    );
}
