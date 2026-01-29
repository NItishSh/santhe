import Link from "next/link";

export function Footer() {
    const year = new Date().getFullYear();

    return (
        <footer className="w-full border-t border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 py-12">
            <div className="container px-6 max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
                <div className="flex flex-col items-center md:items-start gap-2">
                    <Link href="/" className="flex items-center gap-2 group">
                        <div className="w-6 h-6 rounded bg-gradient-to-br from-primary to-orange-600 flex items-center justify-center text-white text-xs font-bold shadow-md">
                            S
                        </div>
                        <span className="text-xl font-bold font-heading tracking-tight">Santhe</span>
                    </Link>
                    <p className="text-sm text-muted-foreground text-center md:text-left">
                        Connecting farmers directly to your doorstep.
                    </p>
                </div>

                <div className="flex gap-8 text-sm text-muted-foreground">
                    <Link href="/about" className="hover:text-primary transition-colors">About</Link>
                    <Link href="/farmers" className="hover:text-primary transition-colors">Our Farmers</Link>
                    <Link href="/privacy" className="hover:text-primary transition-colors">Privacy</Link>
                    <Link href="/terms" className="hover:text-primary transition-colors">Terms</Link>
                </div>

                <div className="text-sm text-muted-foreground">
                    &copy; {year} Santhe Marketplace. All rights reserved.
                </div>
            </div>
        </footer>
    );
}
