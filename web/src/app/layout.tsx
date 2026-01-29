import type { Metadata } from "next";
import { Rubik, Nunito_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Toaster } from "sonner";
import { AuthProvider } from "@/context/AuthContext";

const rubik = Rubik({
  variable: "--font-heading",
  subsets: ["latin"],
});

const nunito = Nunito_Sans({
  variable: "--font-body",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Santhe",
  description: "A premium marketplace for everyone",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${rubik.variable} ${nunito.variable} antialiased font-body bg-background text-foreground`}
      >
        <AuthProvider>
          <Navbar />
          <main className="pt-24 min-h-screen">
            {children}
          </main>
          <Footer />
          <Toaster />
        </AuthProvider>
      </body>
    </html>
  );
}
