"use client"

import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useEffect, useState } from "react";
import { api, Product, User } from "@/lib/api";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { UserMenu } from "@/components/UserMenu";

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const init = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await api.users.me();
          setUser(userData);
        } catch (e) {
          console.error("Failed to fetch user", e);
          // process.env.NODE_ENV === 'development' && setUser({ username: 'Dev', email: 'dev@example.com', role: 'farmer', full_name: 'Dev User' }); // fallback for dev? No, failing silently is better or logout.
          localStorage.removeItem('token'); // Invalid token?
        }
      }

      try {
        const data = await api.products.list();
        setProducts(data);
      } catch (err) {
        console.error("Failed to load products", err);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    window.location.reload();
  };

  return (
    <div className="flex min-h-screen flex-col items-center p-4 bg-background text-foreground">
      <header className="w-full max-w-6xl flex justify-between items-center py-6 mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-primary">Santhe</h1>
        <div className="flex gap-4">
          {user ? (
            <UserMenu user={user} onLogout={handleLogout} />
          ) : (
            <>
              <Link href="/login">
                <Button variant="outline">Log In</Button>
              </Link>
              <Link href="/register">
                <Button>Sign Up</Button>
              </Link>
            </>
          )}
        </div>
      </header>

      <main className="w-full max-w-6xl">
        <section className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Fresh Direct from Farmers</h2>
          <p className="text-xl text-muted-foreground">Marketplace for everyone.</p>
        </section>

        {loading ? (
          <div className="text-center py-20">Loading fresh produce...</div>
        ) : products.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {products.map((product) => (
              <Card key={product.id} className="flex flex-col">
                <CardHeader>
                  <CardTitle>{product.name}</CardTitle>
                </CardHeader>
                <CardContent className="flex-1">
                  <p className="text-sm text-muted-foreground mb-4">{product.description}</p>
                  <p className="text-lg font-bold text-primary">₹{product.price}</p>
                </CardContent>
                <CardFooter>
                  <Button className="w-full" variant="secondary">Add to Cart</Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        ) : (
          <div className="text-center py-20 border rounded-lg bg-muted/20">
            <h3 className="text-xl font-semibold mb-2">No products found</h3>
            <p className="text-muted-foreground">The market is currently empty. Be the first to sell!</p>
          </div>
        )}
      </main>
    </div>
  );
}
