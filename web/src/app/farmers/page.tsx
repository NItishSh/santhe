import { Card } from "@/components/ui/card";

export default function FarmersPage() {
    return (
        <div className="container mx-auto px-4 py-12 max-w-4xl">
            <h1 className="text-4xl font-bold font-heading mb-6 text-center">Our Farmers</h1>
            <Card className="p-8 bg-white/60 backdrop-blur-md border border-white/50 shadow-sm">
                <p className="text-lg text-muted-foreground text-center mb-10">
                    Meet the hardworking hands that feed us.
                </p>

                <div className="grid md:grid-cols-2 gap-6">
                    {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="flex items-center gap-4 p-4 rounded-xl bg-white/50 border border-white/50 hover:shadow-md transition-all">
                            <div className="w-16 h-16 rounded-full bg-gray-200 flex items-center justify-center text-2xl">
                                👨‍🌾
                            </div>
                            <div>
                                <h3 className="font-bold">Farmer Group {i}</h3>
                                <p className="text-sm text-muted-foreground">Specialist in Organic Vegetables</p>
                            </div>
                        </div>
                    ))}
                </div>
            </Card>
        </div>
    );
}
