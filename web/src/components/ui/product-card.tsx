"use client";

import { motion } from "framer-motion";
import { Product } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ShoppingCart } from "lucide-react";
import Image from "next/image";

interface ProductCardProps {
    product: Product;
    onAddToCart: (product: Product) => void;
    isAdding: boolean;
}

export function ProductCard({ product, onAddToCart, isAdding }: ProductCardProps) {
    return (
        <motion.div
            whileHover={{ y: -5 }}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
        >
            <Card className="h-full border-none shadow-sm hover:shadow-xl transition-shadow duration-300 overflow-hidden bg-white/60 backdrop-blur-md group">
                <div className="relative h-48 w-full bg-gradient-to-br from-orange-50 to-orange-100 flex items-center justify-center overflow-hidden">
                    {/* Placeholder for Product Image - Using dynamic text for now or real image if available */}
                    {product.image_url ? (
                        <Image
                            src={product.image_url}
                            alt={product.name}
                            fill
                            className="object-cover group-hover:scale-110 transition-transform duration-500"
                        />
                    ) : (
                        <span className="text-4xl">🥦</span>
                    )}
                    <Badge className="absolute top-3 right-3 bg-white/90 text-primary hover:bg-white shadow-sm backdrop-blur">
                        Fresh
                    </Badge>
                </div>

                <CardHeader className="p-4 pb-0">
                    <div className="flex justify-between items-start">
                        <div>
                            <h3 className="font-bold text-lg text-foreground line-clamp-1 group-hover:text-primary transition-colors">
                                {product.name}
                            </h3>
                            <p className="text-sm text-muted-foreground line-clamp-2 mt-1 min-h-[2.5em]">
                                {product.description}
                            </p>
                        </div>
                    </div>
                </CardHeader>

                <CardContent className="p-4 pt-2">
                    <div className="flex items-baseline gap-1">
                        <span className="text-2xl font-bold text-primary">₹{product.price}</span>
                        <span className="text-sm text-muted-foreground">/ kg</span>
                    </div>
                </CardContent>

                <CardFooter className="p-4 pt-0">
                    <Button
                        className="w-full gap-2 font-semibold"
                        size="lg"
                        onClick={() => onAddToCart(product)}
                        disabled={isAdding}
                    >
                        <ShoppingCart className="w-4 h-4" />
                        {isAdding ? "Adding..." : "Add to Cart"}
                    </Button>
                </CardFooter>
            </Card>
        </motion.div>
    );
}
