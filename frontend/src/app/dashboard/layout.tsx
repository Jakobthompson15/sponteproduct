import { UserButton } from "@clerk/nextjs";
import Link from "next/link";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-cream">
      {/* Dashboard Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b-3 border-charcoal shadow-brutalist-sm">
        <div className="max-w-[1400px] mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <Link
              href="/dashboard"
              className="font-display text-3xl text-charcoal hover:text-orange-fire transition-colors no-underline"
            >
              Sponte
            </Link>

            <div className="flex items-center gap-6">
              <Link
                href="/dashboard"
                className="text-charcoal font-heading font-semibold text-[15px] hover:text-orange-fire transition-colors no-underline"
              >
                Dashboard
              </Link>
              <Link
                href="/dashboard/content"
                className="text-charcoal font-heading font-semibold text-[15px] hover:text-orange-fire transition-colors no-underline"
              >
                Content
              </Link>
              <Link
                href="/dashboard/agents"
                className="text-charcoal font-heading font-semibold text-[15px] hover:text-orange-fire transition-colors no-underline"
              >
                Agents
              </Link>
              <Link
                href="/dashboard/connections"
                className="text-charcoal font-heading font-semibold text-[15px] hover:text-orange-fire transition-colors no-underline"
              >
                Connections
              </Link>
              <Link
                href="/dashboard/reports"
                className="text-charcoal font-heading font-semibold text-[15px] hover:text-orange-fire transition-colors no-underline"
              >
                Reports
              </Link>
              <UserButton afterSignOutUrl="/" />
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard Content */}
      <main className="pt-20">
        {children}
      </main>
    </div>
  );
}
