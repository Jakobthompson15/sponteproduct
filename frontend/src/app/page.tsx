import {
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/nextjs";
import Link from "next/link";
import BounceCards from "@/components/ui/BounceCards";
import AgentCard from "@/components/ui/AgentCard";
import IndustryCarousel from "@/components/ui/IndustryCarousel";
import Cubes from "@/components/ui/Cubes";

export default function Home() {
  return (
    <>
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-[1000] bg-cream/95 backdrop-blur-[20px] border-b-2 border-charcoal/[0.08] px-xl py-md">
        <div className="max-w-[1400px] mx-auto flex justify-between items-center">
          <Link
            href="/"
            className="flex items-center font-display text-[32px] font-normal text-charcoal no-underline"
          >
            Sponte
          </Link>

          <div className="flex gap-lg items-center">
            <SignedOut>
              <SignInButton mode="modal">
                <button className="font-heading font-semibold text-[15px] text-text-secondary hover:text-orange-fire transition-colors duration-200">
                  Sign In
                </button>
              </SignInButton>
              <SignUpButton mode="modal">
                <button className="bg-orange-fire text-white px-[28px] py-3 rounded-lg font-heading font-bold text-[15px] border-none cursor-pointer transition-all duration-300 shadow-[0_4px_16px_rgba(255,88,16,0.3)] hover:-translate-y-0.5 hover:shadow-[0_8px_24px_rgba(255,88,16,0.4)] hover:bg-orange-hover">
                  Get Started
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <Link
                href="/dashboard"
                className="font-heading font-semibold text-[15px] text-text-secondary hover:text-orange-fire transition-colors duration-200 no-underline"
              >
                Dashboard
              </Link>
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
          </div>
        </div>
      </nav>

      {/* Hero Section - Split Screen */}
      <section className="min-h-screen grid grid-cols-1 lg:grid-cols-[1.2fr_1fr] gap-3xl items-center px-xl py-4xl lg:py-[128px] max-w-[1400px] mx-auto relative z-[2] pt-[128px]">
        <div className="pt-3xl">
          <div className="inline-flex items-center gap-xs bg-white border-2 border-charcoal px-5 py-2 rounded-full font-mono text-[13px] font-bold text-charcoal mb-lg uppercase tracking-wider shadow-[4px_4px_0_var(--charcoal)] hover:translate-x-0.5 hover:translate-y-0.5 hover:shadow-[2px_2px_0_var(--charcoal)] transition-all duration-200">
            ⚡ AI-POWERED SEO AGENT
          </div>

          <h1 className="font-display text-[clamp(48px,7vw,92px)] leading-[1.05] text-charcoal mb-lg tracking-tight">
            Set it up once.
            <br />
            <span className="text-orange-fire italic relative inline-block">
              Local SEO forever.
              <span className="absolute bottom-2 left-0 w-full h-3 bg-accent-yellow -z-10 opacity-50 -skew-y-1"></span>
            </span>
          </h1>

          <p className="text-[22px] leading-[1.7] text-text-secondary mb-xl max-w-[560px]">
            A multi-agent system that runs local SEO (GBP, NAP, on-site, posts, social) on autopilot. You choose: Draft-only → Approve-to-publish → Full autopilot.
          </p>

          <div className="flex gap-md mb-xl flex-wrap">
            <SignedOut>
              <SignUpButton mode="modal">
                <button className="bg-orange-fire text-white px-10 py-4 rounded-lg font-heading font-bold text-[15px] border-none cursor-pointer transition-all duration-300 shadow-[0_4px_16px_rgba(255,88,16,0.3)] hover:-translate-y-0.5 hover:shadow-[0_8px_24px_rgba(255,88,16,0.4)] hover:bg-orange-hover">
                  Start Your Agent
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <Link
                href="/onboarding"
                className="inline-block bg-orange-fire text-white px-10 py-4 rounded-lg font-heading font-bold text-[15px] no-underline cursor-pointer transition-all duration-300 shadow-[0_4px_16px_rgba(255,88,16,0.3)] hover:-translate-y-0.5 hover:shadow-[0_8px_24px_rgba(255,88,16,0.4)] hover:bg-orange-hover"
              >
                Start Your Agent
              </Link>
            </SignedIn>
            <a
              href="#features"
              className="bg-white text-charcoal px-7 py-3 rounded-lg font-heading font-bold text-[15px] border-2 border-charcoal cursor-pointer transition-all duration-200 shadow-[4px_4px_0_var(--charcoal)] hover:translate-x-0.5 hover:translate-y-0.5 hover:shadow-[2px_2px_0_var(--charcoal)] no-underline inline-block"
            >
              See How It Works
            </a>
          </div>

          <div className="flex gap-xl pt-lg border-t-2 border-charcoal/10 flex-wrap">
            <div className="text-left">
              <span className="font-mono text-4xl font-bold text-orange-fire block leading-none mb-1">
                10 min
              </span>
              <span className="text-sm text-text-muted font-medium">Setup Time</span>
            </div>
            <div className="text-left">
              <span className="font-mono text-4xl font-bold text-orange-fire block leading-none mb-1">
                24/7
              </span>
              <span className="text-sm text-text-muted font-medium">Always Working</span>
            </div>
            <div className="text-left">
              <span className="font-mono text-4xl font-bold text-orange-fire block leading-none mb-1">
                50%
              </span>
              <span className="text-sm text-text-muted font-medium">Less Than Agencies</span>
            </div>
          </div>
        </div>

        {/* Hero Visual - Industry Carousel */}
        <IndustryCarousel />
      </section>

      {/* Features - Bounce Cards */}
      <section className="py-4xl px-xl bg-cream" id="features">
        <div className="max-w-[1400px] mx-auto">
          <div className="text-center mb-3xl">
            <h2 className="font-display text-[clamp(40px,5vw,64px)] text-charcoal mb-md leading-[1.1]">
              Meet Your Multi-Agent Team
            </h2>
            <p className="text-xl text-text-secondary max-w-[600px] mx-auto">
              Specialized AI agents working together. One Orchestrator coordinates everything.
            </p>
          </div>

          {/* Bounce Cards Display */}
          <BounceCards
            cards={[
              <AgentCard
                key="gbp"
                badge="GBP AGENT"
                badgeColor="bg-charcoal"
                title="Google Business Profile"
                description="Syncs hours, NAP, categories. Writes & schedules GBP posts with UTM links. Monitors Performance insights."
                emoji="🗺️"
                bgColor="bg-orange-fire"
                textColor="text-white"
              />,
              <AgentCard
                key="keyword"
                badge="KW"
                badgeColor="bg-charcoal"
                title="Keyword Agent"
                description="Clusters keywords, recommends categories, builds topic queues."
                emoji="🔍"
                bgColor="bg-white"
              />,
              <AgentCard
                key="nap"
                badge="NAP"
                badgeColor="bg-sage-green"
                title="NAP Agent"
                description="Checks footer, Contact page, schema, GBP. Auto-fixes issues."
                emoji="📍"
                bgColor="bg-white"
              />,
              <AgentCard
                key="orchestrator"
                badge="ORCHESTRATOR"
                badgeColor="bg-charcoal"
                title="Always On"
                description="Assigns tasks, enforces guardrails, assembles weekly plans. Your command center."
                emoji="⚙️"
                bgColor="bg-accent-yellow"
              />,
              <AgentCard
                key="blog"
                badge="BLOG"
                badgeColor="bg-charcoal"
                title="Blog Agent"
                description="Creates localized posts with FAQs and schema. Drafts or publishes."
                emoji="✍️"
                bgColor="bg-sage-green"
                textColor="text-white"
              />,
              <AgentCard
                key="social"
                badge="SOC"
                badgeColor="bg-sage-green"
                title="Social Agent"
                description="Turns updates into FB, IG, LinkedIn, TikTok posts. Auto-schedules."
                emoji="📱"
                bgColor="bg-white"
              />,
              <AgentCard
                key="reporting"
                badge="REPORT"
                badgeColor="bg-charcoal"
                title="Reporting Agent"
                description="Weekly digest + monthly narrative. Plain English explanations."
                emoji="📊"
                bgColor="bg-white"
              />
            ]}
            containerWidth={1200}
            containerHeight={520}
            enableHover={true}
            animationDelay={0.3}
            animationStagger={0.1}
          />
        </div>
      </section>

      {/* Final CTA */}
      <section className="bg-orange-fire py-4xl px-xl relative overflow-hidden">
        {/* Interactive Cube Grid Background */}
        <div className="absolute inset-0 opacity-20 pointer-events-auto">
          <Cubes
            gridSize={14}
            faceColor="#FFFFFF"
            rippleColor="#FCD34D"
            maxAngle={30}
            autoAnimate={true}
            rippleOnClick={true}
            cellGap={4}
            shadow={false}
            borderStyle="2px solid #1A1D2E"
            rippleSpeed={1.5}
          />
        </div>
        <div className="max-w-[900px] mx-auto text-center relative z-[2]">
          <h2 className="font-display text-[clamp(40px,6vw,80px)] text-white leading-[1.1] mb-lg">
            Ready to Set It and Forget It?
          </h2>
          <p className="text-2xl text-white/90 mb-xl">
            10-minute setup. Then your agents run local SEO forever.
          </p>
          <div className="flex gap-md justify-center flex-wrap">
            <SignedOut>
              <SignUpButton mode="modal">
                <button className="bg-white text-orange-fire px-10 py-4 rounded-lg font-heading font-extrabold text-lg border-none cursor-pointer transition-all duration-300 shadow-[0_8px_24px_rgba(0,0,0,0.2)] hover:-translate-y-1 hover:shadow-[0_12px_32px_rgba(0,0,0,0.3)]">
                  Start Your Agent Today
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <Link
                href="/onboarding"
                className="inline-block bg-white text-orange-fire px-10 py-4 rounded-lg font-heading font-extrabold text-lg no-underline cursor-pointer transition-all duration-300 shadow-[0_8px_24px_rgba(0,0,0,0.2)] hover:-translate-y-1 hover:shadow-[0_12px_32px_rgba(0,0,0,0.3)]"
              >
                Start Your Agent Today
              </Link>
            </SignedIn>
          </div>
        </div>
      </section>
    </>
  );
}
