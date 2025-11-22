'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { getReport } from '@/lib/api/reports';
import type { Report } from '@/types/api';

export default function ReportDetailPage() {
  const params = useParams();
  const reportId = params.id as string;

  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadReport();
  }, [reportId]);

  const loadReport = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await getReport(reportId);
      setReport(data);
    } catch (err: any) {
      console.error('Error loading report:', err);
      setError(err.response?.data?.detail || 'Failed to load report');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-charcoal border-t-transparent mb-4"></div>
          <p className="text-text-muted font-mono">Loading report...</p>
        </div>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="min-h-screen bg-cream">
        <div className="max-w-[1400px] mx-auto px-6 py-8">
          <div className="bg-accent-red/10 border-2 border-accent-red rounded-brutalist p-8 text-center">
            <span className="text-6xl mb-4 block">⚠️</span>
            <h2 className="font-heading text-2xl text-charcoal mb-2">
              Report Not Found
            </h2>
            <p className="text-text-muted mb-6">{error || 'This report does not exist'}</p>
            <Link
              href="/dashboard/reports"
              className="inline-block px-6 py-3 bg-orange-fire text-white font-heading font-bold rounded-lg border-2 border-charcoal hover:bg-orange-hover transition-all shadow-brutalist-sm no-underline"
            >
              ← Back to Reports
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const { metrics, agentActivity, insights, recommendations } = report.data;

  return (
    <div className="min-h-screen bg-cream">
      <div className="max-w-[1400px] mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link
            href="/dashboard/reports"
            className="inline-flex items-center gap-2 text-orange-fire font-heading font-bold hover:text-orange-hover transition-colors mb-4 no-underline"
          >
            <span>←</span> Back to Reports
          </Link>

          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-mono font-bold ${
                    report.report_type === 'weekly'
                      ? 'bg-sage-green/20 text-sage-green'
                      : report.report_type === 'monthly'
                      ? 'bg-orange-fire/20 text-orange-fire'
                      : 'bg-charcoal/20 text-charcoal'
                  }`}
                >
                  {report.report_type.toUpperCase()} REPORT
                </span>
                {report.email_sent && (
                  <span className="text-sm text-text-muted">
                    ✉️ Emailed on {formatDate(report.email_sent)}
                  </span>
                )}
              </div>
              <h1 className="font-display text-4xl text-charcoal mb-2">
                {report.data.period}
              </h1>
              <p className="text-text-muted">
                Generated {formatDate(report.created_at)}
              </p>
            </div>

            <button
              onClick={() => window.print()}
              className="px-6 py-3 bg-white text-charcoal font-heading font-bold rounded-lg border-2 border-charcoal hover:bg-cream transition-all shadow-brutalist-sm"
            >
              🖨️ Print Report
            </button>
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {metrics?.calls && (
            <MetricCard
              icon="📞"
              label="Calls"
              current={metrics.calls.current}
              previous={metrics.calls.previous}
              change={metrics.calls.change}
            />
          )}
          {metrics?.gbpViews && (
            <MetricCard
              icon="👀"
              label="GBP Views"
              current={metrics.gbpViews.current}
              previous={metrics.gbpViews.previous}
              change={metrics.gbpViews.change}
            />
          )}
          {metrics?.directionRequests && (
            <MetricCard
              icon="🧭"
              label="Directions"
              current={metrics.directionRequests.current}
              previous={metrics.directionRequests.previous}
              change={metrics.directionRequests.change}
            />
          )}
          {metrics?.websiteClicks && (
            <MetricCard
              icon="🖱️"
              label="Website Clicks"
              current={metrics.websiteClicks.current}
              previous={metrics.websiteClicks.previous}
              change={metrics.websiteClicks.change}
            />
          )}
        </div>

        {/* Reviews */}
        {metrics?.reviews && (
          <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm mb-8">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-4xl">⭐</span>
              <h2 className="font-heading text-2xl font-bold text-charcoal">
                Reviews & Ratings
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <p className="text-text-muted text-sm font-mono font-bold uppercase mb-1">
                  Average Rating
                </p>
                <p className="font-display text-4xl text-charcoal">
                  {metrics.reviews.avgRating}
                </p>
              </div>
              <div>
                <p className="text-text-muted text-sm font-mono font-bold uppercase mb-1">
                  Total Reviews
                </p>
                <p className="font-display text-4xl text-charcoal">
                  {metrics.reviews.count}
                </p>
              </div>
              <div>
                <p className="text-text-muted text-sm font-mono font-bold uppercase mb-1">
                  New This Period
                </p>
                <p className="font-display text-4xl text-sage-green">
                  +{metrics.reviews.newReviews}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Agent Activity */}
        {agentActivity && Object.keys(agentActivity).length > 0 && (
          <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm mb-8">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-4xl">🤖</span>
              <h2 className="font-heading text-2xl font-bold text-charcoal">
                AI Agent Activity
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(agentActivity).map(([agentKey, activity]) => (
                <AgentActivityCard key={agentKey} agentKey={agentKey} activity={activity} />
              ))}
            </div>
          </div>
        )}

        {/* Insights & Recommendations */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Insights */}
          {insights && insights.length > 0 && (
            <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl">💡</span>
                <h2 className="font-heading text-xl font-bold text-charcoal">
                  Key Insights
                </h2>
              </div>
              <ul className="space-y-3">
                {insights.map((insight, index) => (
                  <li key={index} className="flex gap-3">
                    <span className="text-sage-green font-bold mt-1">✓</span>
                    <span className="text-text-secondary flex-1">{insight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          {recommendations && recommendations.length > 0 && (
            <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl">🎯</span>
                <h2 className="font-heading text-xl font-bold text-charcoal">
                  Recommendations
                </h2>
              </div>
              <ul className="space-y-3">
                {recommendations.map((rec, index) => (
                  <li key={index} className="flex gap-3">
                    <span className="text-orange-fire font-bold mt-1">→</span>
                    <span className="text-text-secondary flex-1">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// MetricCard Component
function MetricCard({
  icon,
  label,
  current,
  previous,
  change,
}: {
  icon: string;
  label: string;
  current: number;
  previous: number;
  change: number;
}) {
  const isPositive = change >= 0;

  return (
    <div className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm">
      <div className="flex items-center gap-3 mb-3">
        <span className="text-3xl">{icon}</span>
        <p className="text-text-muted font-mono text-xs font-bold uppercase">
          {label}
        </p>
      </div>
      <div className="mb-2">
        <p className="font-display text-4xl text-charcoal">
          {current.toLocaleString()}
        </p>
      </div>
      <div className="flex items-center gap-2">
        <span
          className={`flex items-center gap-1 text-sm font-bold ${
            isPositive ? 'text-sage-green' : 'text-accent-red'
          }`}
        >
          <span>{isPositive ? '↑' : '↓'}</span>
          <span>{Math.abs(change).toFixed(1)}%</span>
        </span>
        <span className="text-text-muted text-sm">
          vs {previous.toLocaleString()}
        </span>
      </div>
    </div>
  );
}

// AgentActivityCard Component
function AgentActivityCard({
  agentKey,
  activity,
}: {
  agentKey: string;
  activity: any;
}) {
  const agentNames: Record<string, { name: string; icon: string }> = {
    gbp: { name: 'GBP Agent', icon: '🗺️' },
    nap: { name: 'NAP Agent', icon: '📍' },
    keyword: { name: 'Keyword Agent', icon: '🔍' },
    blog: { name: 'Blog Agent', icon: '✍️' },
    social: { name: 'Social Agent', icon: '📱' },
    reporting: { name: 'Reporting Agent', icon: '📊' },
  };

  const agent = agentNames[agentKey] || { name: agentKey, icon: '🤖' };

  return (
    <div className="bg-cream rounded-lg p-4">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">{agent.icon}</span>
        <h3 className="font-heading font-bold text-charcoal">{agent.name}</h3>
      </div>
      <div className="space-y-2">
        {Object.entries(activity).map(([key, value]) => {
          // Convert camelCase to Title Case
          const label = key
            .replace(/([A-Z])/g, ' $1')
            .replace(/^./, (str) => str.toUpperCase());

          return (
            <div key={key} className="flex justify-between items-center">
              <span className="text-sm text-text-secondary">{label}</span>
              <span className="font-mono font-bold text-charcoal">{value as number}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
