import { currentUser } from "@clerk/nextjs/server";
import Link from "next/link";

export default async function DashboardPage() {
  const user = await currentUser();

  // Mock data - will be replaced with real API calls
  const mockData = {
    business: {
      name: "My Pizza LLC",
      location: "Chicago, IL",
      primaryGoal: "calls", // calls, bookings, forms, directions
    },
    metrics: {
      callsThisMonth: 127,
      callsLastMonth: 98,
      gbpViews: 3421,
      gbpViewsChange: 15.2,
      directionRequests: 89,
      directionsChange: 8.5,
      websiteClicks: 234,
      clicksChange: 12.3,
      reviews: 47,
      avgRating: 4.8,
    },
    agents: [
      {
        id: "gbp",
        name: "GBP Agent",
        icon: "🗺️",
        status: "active", // active, paused, setup_needed
        mode: "autopilot", // draft, approve, autopilot
        lastActivity: "2 hours ago",
        lastAction: "Posted to Google Business Profile",
        pendingActions: 0,
      },
      {
        id: "nap",
        name: "NAP Agent",
        icon: "📍",
        status: "active",
        mode: "autopilot",
        lastActivity: "1 day ago",
        lastAction: "Verified NAP consistency",
        pendingActions: 0,
      },
      {
        id: "keyword",
        name: "Keyword Agent",
        icon: "🔍",
        status: "active",
        mode: "autopilot",
        lastActivity: "3 hours ago",
        lastAction: "Updated keyword rankings",
        pendingActions: 0,
      },
      {
        id: "blog",
        name: "Blog Agent",
        icon: "✍️",
        status: "active",
        mode: "approve",
        lastActivity: "5 hours ago",
        lastAction: "Created draft: 'Best Pizza Toppings'",
        pendingActions: 2,
      },
      {
        id: "social",
        name: "Social Agent",
        icon: "📱",
        status: "active",
        mode: "approve",
        lastActivity: "1 hour ago",
        lastAction: "Drafted Instagram post",
        pendingActions: 1,
      },
      {
        id: "reporting",
        name: "Reporting Agent",
        icon: "📊",
        status: "active",
        mode: "autopilot",
        lastActivity: "1 day ago",
        lastAction: "Sent weekly report",
        pendingActions: 0,
      },
    ],
    recentActivity: [
      {
        id: 1,
        agent: "GBP Agent",
        action: "Posted to Google Business Profile",
        time: "2 hours ago",
        icon: "🗺️",
      },
      {
        id: 2,
        agent: "Social Agent",
        action: "Drafted Instagram post about new menu items",
        time: "1 hour ago",
        icon: "📱",
      },
      {
        id: 3,
        agent: "Blog Agent",
        action: "Published: 'Top 5 Pizza Styles in Chicago'",
        time: "5 hours ago",
        icon: "✍️",
      },
      {
        id: 4,
        agent: "Keyword Agent",
        action: "Detected ranking improvement: 'best pizza near me' → #2",
        time: "6 hours ago",
        icon: "🔍",
      },
    ],
  };

  const callsChange = mockData.metrics.callsThisMonth - mockData.metrics.callsLastMonth;
  const callsPercentChange = ((callsChange / mockData.metrics.callsLastMonth) * 100).toFixed(1);

  return (
    <div className="min-h-screen bg-cream">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-orange-fire to-orange-hover border-b-3 border-charcoal shadow-brutalist">
        <div className="max-w-[1400px] mx-auto px-6 py-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="font-display text-5xl text-white mb-2">
                {mockData.business.name}
              </h1>
              <p className="text-white/80 text-lg font-medium">
                📍 {mockData.business.location}
              </p>
            </div>
            <div className="text-right">
              <div className="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm border-2 border-white/40 rounded-lg px-4 py-2 mb-2">
                <div className="w-2 h-2 bg-sage-green rounded-full animate-pulse"></div>
                <span className="text-white font-mono text-sm font-bold">
                  ALL SYSTEMS OPERATIONAL
                </span>
              </div>
            </div>
          </div>

          {/* Primary Metric - Calls */}
          <div className="bg-white border-3 border-charcoal rounded-brutalist-lg p-6 shadow-brutalist">
            <div className="flex items-end justify-between">
              <div>
                <p className="text-text-muted font-mono text-sm font-bold uppercase tracking-wider mb-2">
                  📞 This Month's Calls
                </p>
                <div className="flex items-baseline gap-4">
                  <span className="font-display text-6xl text-charcoal">
                    {mockData.metrics.callsThisMonth}
                  </span>
                  <div className={`flex items-center gap-1 px-3 py-1 rounded-full ${
                    callsChange >= 0
                      ? 'bg-sage-green/10 text-sage-green'
                      : 'bg-accent-red/10 text-accent-red'
                  }`}>
                    <span className="text-2xl">{callsChange >= 0 ? '↑' : '↓'}</span>
                    <span className="font-mono font-bold text-lg">
                      +{callsChange} ({callsPercentChange}%)
                    </span>
                  </div>
                </div>
                <p className="text-text-secondary mt-2">
                  vs {mockData.metrics.callsLastMonth} last month
                </p>
              </div>
              <div className="text-right">
                <Link
                  href="/dashboard/reports"
                  className="inline-block px-6 py-3 bg-orange-fire text-white font-heading font-bold rounded-lg border-2 border-charcoal hover:bg-orange-hover transition-all shadow-brutalist-sm no-underline"
                >
                  View Full Report →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-[1400px] mx-auto px-6 py-8">
        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* GBP Views */}
          <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">👀</span>
              <p className="text-text-muted font-mono text-xs font-bold uppercase">
                GBP Views
              </p>
            </div>
            <p className="font-display text-4xl text-charcoal mb-1">
              {mockData.metrics.gbpViews.toLocaleString()}
            </p>
            <div className="flex items-center gap-1 text-sage-green text-sm font-bold">
              <span>↑</span>
              <span>{mockData.metrics.gbpViewsChange}% vs last month</span>
            </div>
          </div>

          {/* Direction Requests */}
          <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">🧭</span>
              <p className="text-text-muted font-mono text-xs font-bold uppercase">
                Directions
              </p>
            </div>
            <p className="font-display text-4xl text-charcoal mb-1">
              {mockData.metrics.directionRequests}
            </p>
            <div className="flex items-center gap-1 text-sage-green text-sm font-bold">
              <span>↑</span>
              <span>{mockData.metrics.directionsChange}% vs last month</span>
            </div>
          </div>

          {/* Website Clicks */}
          <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">🖱️</span>
              <p className="text-text-muted font-mono text-xs font-bold uppercase">
                Website Clicks
              </p>
            </div>
            <p className="font-display text-4xl text-charcoal mb-1">
              {mockData.metrics.websiteClicks}
            </p>
            <div className="flex items-center gap-1 text-sage-green text-sm font-bold">
              <span>↑</span>
              <span>{mockData.metrics.clicksChange}% vs last month</span>
            </div>
          </div>

          {/* Reviews */}
          <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-3xl">⭐</span>
              <p className="text-text-muted font-mono text-xs font-bold uppercase">
                Reviews
              </p>
            </div>
            <div className="flex items-baseline gap-2">
              <p className="font-display text-4xl text-charcoal">
                {mockData.metrics.avgRating}
              </p>
              <p className="text-text-secondary text-lg">
                ({mockData.metrics.reviews} reviews)
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Agent Status - Takes up 2 columns */}
          <div className="lg:col-span-2">
            <h2 className="font-heading text-2xl font-bold text-charcoal mb-4">
              Your AI Agents
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {mockData.agents.map((agent) => (
                <div
                  key={agent.id}
                  className="bg-white border-2 border-charcoal rounded-brutalist p-5 shadow-brutalist-sm hover:shadow-brutalist transition-all"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">{agent.icon}</span>
                      <div>
                        <h3 className="font-heading font-bold text-lg text-charcoal">
                          {agent.name}
                        </h3>
                        <p className="text-xs text-text-muted font-mono font-bold uppercase">
                          {agent.mode}
                        </p>
                      </div>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-mono font-bold ${
                        agent.status === "active"
                          ? "bg-sage-green text-white"
                          : agent.status === "paused"
                          ? "bg-accent-yellow text-charcoal"
                          : "bg-charcoal text-white"
                      }`}
                    >
                      {agent.status.toUpperCase()}
                    </span>
                  </div>

                  <p className="text-sm text-text-secondary mb-2">
                    {agent.lastAction}
                  </p>

                  <div className="flex items-center justify-between pt-3 border-t border-charcoal/10">
                    <span className="text-xs text-text-muted">
                      {agent.lastActivity}
                    </span>
                    {agent.pendingActions > 0 && (
                      <span className="px-2 py-1 bg-orange-fire text-white rounded-full text-xs font-bold">
                        {agent.pendingActions} pending
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Activity - Takes up 1 column */}
          <div>
            <h2 className="font-heading text-2xl font-bold text-charcoal mb-4">
              Recent Activity
            </h2>
            <div className="bg-white border-2 border-charcoal rounded-brutalist p-5 shadow-brutalist-sm">
              <div className="space-y-4">
                {mockData.recentActivity.map((activity) => (
                  <div
                    key={activity.id}
                    className="pb-4 border-b border-charcoal/10 last:border-b-0 last:pb-0"
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-2xl">{activity.icon}</span>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-charcoal mb-1">
                          {activity.action}
                        </p>
                        <p className="text-xs text-text-muted">{activity.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <Link
                href="/dashboard/activity"
                className="block text-center mt-4 pt-4 border-t border-charcoal/10 text-orange-fire font-heading font-bold text-sm hover:text-orange-hover transition-colors no-underline"
              >
                View All Activity →
              </Link>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          <Link
            href="/dashboard/content"
            className="bg-white border-2 border-charcoal rounded-brutalist p-6 text-center hover:shadow-brutalist transition-all group no-underline"
          >
            <span className="text-4xl mb-2 block group-hover:scale-110 transition-transform">
              📝
            </span>
            <h3 className="font-heading font-bold text-charcoal">View Content</h3>
            <p className="text-sm text-text-muted mt-1">Posts & drafts</p>
          </Link>

          <Link
            href="/dashboard/agents"
            className="bg-white border-2 border-charcoal rounded-brutalist p-6 text-center hover:shadow-brutalist transition-all group no-underline"
          >
            <span className="text-4xl mb-2 block group-hover:scale-110 transition-transform">
              ⚙️
            </span>
            <h3 className="font-heading font-bold text-charcoal">Configure Agents</h3>
            <p className="text-sm text-text-muted mt-1">Settings & rules</p>
          </Link>

          <Link
            href="/dashboard/connections"
            className="bg-white border-2 border-charcoal rounded-brutalist p-6 text-center hover:shadow-brutalist transition-all group no-underline"
          >
            <span className="text-4xl mb-2 block group-hover:scale-110 transition-transform">
              🔗
            </span>
            <h3 className="font-heading font-bold text-charcoal">Connections</h3>
            <p className="text-sm text-text-muted mt-1">Google, WordPress</p>
          </Link>

          <Link
            href="/dashboard/reports"
            className="bg-white border-2 border-charcoal rounded-brutalist p-6 text-center hover:shadow-brutalist transition-all group no-underline"
          >
            <span className="text-4xl mb-2 block group-hover:scale-110 transition-transform">
              📊
            </span>
            <h3 className="font-heading font-bold text-charcoal">Reports</h3>
            <p className="text-sm text-text-muted mt-1">Analytics & insights</p>
          </Link>
        </div>
      </div>
    </div>
  );
}
