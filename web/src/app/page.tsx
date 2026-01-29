"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { api, Product, User } from "@/lib/api";
import { ProductCard } from "@/components/ui/product-card";
import { Button } from "@/components/ui/button";
import { ArrowRight, Leaf, Truck, ShieldCheck } from "lucide-react";

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [addingToCart, setAddingToCart] = useState<number | null>(null);
  const [cartMessage, setCartMessage] = useState<string | null>(null);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const data = await api.products.list();
        setProducts(data);
      } catch (err) {
        console.error("Failed to load products", err);
      } finally {
        setLoading(false);
      }
    };
    loadProducts();
  }, []);

  const handleAddToCart = async (product: Product) => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    setAddingToCart(product.id);
    setCartMessage(null);

    try {
      await api.cart.addItem(product.id, 1);
      setCartMessage(`✅ ${product.name} added to cart!`);
      setTimeout(() => setCartMessage(null), 3000);
    } catch (err) {
      setCartMessage(`❌ Failed to add ${product.name}`);
      setTimeout(() => setCartMessage(null), 3000);
    } finally {
      setAddingToCart(null);
    }
  };

  const categories = [
    { name: "Vegetables", color: "bg-green-100/50", icon: "🥦" },
    { name: "Fruits", color: "bg-orange-100/50", icon: "🍎" },
    { name: "Grains", color: "bg-yellow-100/50", icon: "🌾" },
    { name: "Dairy", color: "bg-blue-100/50", icon: "🥛" },
  ];

  const features = [
    { title: "Farm Fresh", desc: "Harvested this morning", icon: Leaf },
    { title: "Fast Delivery", desc: "To your door in hours", icon: Truck },
    { title: "Quality Check", desc: "Hand-picked produce", icon: ShieldCheck },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      {/* Toast */}
      {cartMessage && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className="fixed top-24 right-6 z-50 bg-white/90 backdrop-blur border border-green-200 shadow-xl rounded-lg px-6 py-4 flex items-center gap-2"
        >
          {cartMessage}
        </motion.div>
      )}

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        {/* Abstract Background Blobs */}
        <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-orange-200/30 rounded-full blur-3xl -z-10 translate-x-1/3 -translate-y-1/3 animate-pulse duration-10000" />
        <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-green-200/30 rounded-full blur-3xl -z-10 -translate-x-1/3 translate-y-1/3" />

        <div className="container px-6 max-w-7xl mx-auto flex flex-col items-center text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-block py-1 px-3 rounded-full bg-orange-100 text-orange-600 text-sm font-semibold mb-6 border border-orange-200">
              🚀 New Harvest Arrived
            </span>
            <h1 className="text-5xl md:text-7xl font-bold font-heading mb-6 bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">
              Fresh from the Farm,<br />
              <span className="text-primary">Designed for You.</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
              Experience the freshest produce delivered directly to your doorstep. Supporting local farmers, ensuring premium quality.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="rounded-full shadow-lg shadow-orange-500/20 px-8 text-lg h-14" onClick={() => document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' })}>
                Shop Fresh <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
              <Link href="/about">
                <Button variant="outline" size="lg" className="rounded-full px-8 text-lg h-14 bg-white/50 backdrop-blur border-gray-200 hover:bg-white/80">
                  Our Story
                </Button>
              </Link>
            </div>
          </motion.div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 w-full">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="p-6 rounded-2xl bg-white/50 backdrop-blur border border-white/50 shadow-sm hover:shadow-md transition-all text-left group"
              >
                <div className="w-12 h-12 rounded-xl bg-orange-50 text-primary flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <feature.icon className="w-6 h-6" />
                </div>
                <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Bento (Visual only for now) */}
      <section className="py-16 bg-white/30" id="categories">
        <div className="container px-6 max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold font-heading mb-10 text-center">Browse Categories</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {categories.map((cat, i) => (
              <motion.div
                key={cat.name}
                whileHover={{ scale: 1.05 }}
                className={`h-32 rounded-2xl ${cat.color} backdrop-blur border border-white/20 flex flex-col items-center justify-center cursor-pointer shadow-sm hover:shadow-md transition-all`}
              >
                <span className="text-4xl mb-2">{cat.icon}</span>
                <span className="font-semibold text-gray-800">{cat.name}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Products Section */}
      <section className="py-20" id="products">
        <div className="container px-6 max-w-7xl mx-auto">
          <div className="flex justify-between items-end mb-10">
            <div>
              <span className="text-primary font-semibold uppercase tracking-wider text-sm">Our Selection</span>
              <h2 className="text-3xl md:text-4xl font-bold font-heading mt-2">Trending Produce</h2>
            </div>
            <Button variant="link" className="text-primary hidden md:inline-flex">View All</Button>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-80 rounded-2xl bg-gray-100 animate-pulse" />
              ))}
            </div>
          ) : products.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {products.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAddToCart={handleAddToCart}
                  isAdding={addingToCart === product.id}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-20 border-2 border-dashed rounded-3xl bg-gray-50/50">
              <h3 className="text-xl font-semibold mb-2 text-gray-400">No products found</h3>
              <p className="text-muted-foreground">The market is quiet today.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
