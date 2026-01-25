import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-background text-foreground">
      <div className="max-w-5xl w-full flex flex-col items-center text-center gap-8">
        <h1 className="text-6xl font-bold tracking-tight text-primary">
          Santhe
        </h1>
        <p className="text-2xl text-muted-foreground">
          A premium marketplace for everyone.
        </p>
        <div className="flex gap-4 mt-8">
          <Button size="lg">Get Started</Button>
          <Button variant="secondary" size="lg">Learn More</Button>
          <Link href="/login">
            <Button variant="outline" size="lg">Log In</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
