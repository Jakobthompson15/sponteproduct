'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getReports } from '@/lib/api/reports';
import type { Report, ReportType } from '@/types/api';

type TabType = 'weekly' | 'monthly' | 'all';

export default function ReportsPage() {
  const [activeTab, setActiveTab] = useState<TabType>('all');
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalReports, setTotalReports] = useState(0);
  const pageSize = 10;

  // Mock location ID - in production, this would come from user context
  const locationId = '30eec932-b6e1-4717-a6a6-ab790e3d286d';

  useEffect(() => {
    loadReports();
  }, [activeTab, page]);

  const loadReports = async () => {
    setLoading(true);
    setError(null);

    try {
      const reportType: ReportType | undefined =
        activeTab === 'weekly'
          ? 'weekly'
          : activeTab === 'monthly'
          ? 'monthly'
          : undefined;

      const response = await getReports(locationId, reportType, page, pageSize);
      setReports(response.reports);
      setTotalReports(response.total);
    } catch (err: any) {
      console.error('Error loading reports:', err);
      setError(err.response?.data?.detail || 'Failed to load reports');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getMetricDisplay = (report: Report) => {
    const { metrics } = report.data;

    // Primary metric - calls
    const calls = metrics?.calls;
    if (calls) {
      return {
        label: 'Calls',
        value: calls.current,
        change: calls.change,
      };
    }

    // Fallback to GBP views
    const gbpViews = metrics?.gbpViews;
    if (gbpViews) {
      return {
        label: 'GBP Views',
        value: gbpViews.current,
        change: gbpViews.change,
      };
    }

    return null;
  };

  const totalPages = Math.ceil(totalReports / pageSize);

  return (
    <div className="min-h-screen bg-cream">
      <div className="max-w-[1400px] mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-display text-5xl text-charcoal mb-3">
            Reports
          </h1>
          <p className="text-text-secondary text-lg">
            View your weekly and monthly performance summaries
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 border-b-2 border-charcoal/20">
          <button
            onClick={() => {
              setActiveTab('all');
              setPage(1);
            }}
            className={`px-6 py-3 font-heading font-bold text-sm transition-all border-b-3 ${
              activeTab === 'all'
                ? 'border-orange-fire text-orange-fire'
                : 'border-transparent text-text-muted hover:text-charcoal'
            }`}
          >
            ALL REPORTS
          </button>
          <button
            onClick={() => {
              setActiveTab('weekly');
              setPage(1);
            }}
            className={`px-6 py-3 font-heading font-bold text-sm transition-all border-b-3 ${
              activeTab === 'weekly'
                ? 'border-orange-fire text-orange-fire'
                : 'border-transparent text-text-muted hover:text-charcoal'
            }`}
          >
            WEEKLY
          </button>
          <button
            onClick={() => {
              setActiveTab('monthly');
              setPage(1);
            }}
            className={`px-6 py-3 font-heading font-bold text-sm transition-all border-b-3 ${
              activeTab === 'monthly'
                ? 'border-orange-fire text-orange-fire'
                : 'border-transparent text-text-muted hover:text-charcoal'
            }`}
          >
            MONTHLY
          </button>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-charcoal border-t-transparent"></div>
            <p className="mt-4 text-text-muted font-mono">Loading reports...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-accent-red/10 border-2 border-accent-red rounded-brutalist p-6 mb-6">
            <p className="text-accent-red font-heading font-bold">{error}</p>
          </div>
        )}

        {/* Reports Grid */}
        {!loading && !error && (
          <>
            {reports.length === 0 ? (
              <div className="bg-white border-2 border-charcoal rounded-brutalist p-12 text-center">
                <span className="text-6xl mb-4 block">📊</span>
                <h3 className="font-heading text-2xl text-charcoal mb-2">
                  No reports yet
                </h3>
                <p className="text-text-muted">
                  Reports will appear here once they are generated
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reports.map((report) => {
                  const metric = getMetricDisplay(report);
                  const isPositive = metric && metric.change >= 0;

                  return (
                    <div
                      key={report.id}
                      className="bg-white border-2 border-charcoal rounded-brutalist p-6 shadow-brutalist-sm hover:shadow-brutalist transition-all"
                    >
                      {/* Report Header */}
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <div className="flex items-center gap-2 mb-2">
                            <span
                              className={`px-3 py-1 rounded-full text-xs font-mono font-bold ${
                                report.report_type === 'weekly'
                                  ? 'bg-sage-green/20 text-sage-green'
                                  : report.report_type === 'monthly'
                                  ? 'bg-orange-fire/20 text-orange-fire'
                                  : 'bg-charcoal/20 text-charcoal'
                              }`}
                            >
                              {report.report_type.toUpperCase()}
                            </span>
                            {report.email_sent && (
                              <span className="text-sm text-text-muted">
                                ✉️ Emailed
                              </span>
                            )}
                          </div>
                          <h3 className="font-heading text-lg font-bold text-charcoal">
                            {report.data.period}
                          </h3>
                          <p className="text-sm text-text-muted mt-1">
                            Generated {formatDate(report.created_at)}
                          </p>
                        </div>
                      </div>

                      {/* Key Metric */}
                      {metric && (
                        <div className="bg-cream rounded-lg p-4 mb-4">
                          <p className="text-xs text-text-muted font-mono font-bold uppercase mb-1">
                            {metric.label}
                          </p>
                          <div className="flex items-baseline gap-3">
                            <span className="font-display text-3xl text-charcoal">
                              {metric.value.toLocaleString()}
                            </span>
                            <span
                              className={`flex items-center gap-1 text-sm font-bold ${
                                isPositive ? 'text-sage-green' : 'text-accent-red'
                              }`}
                            >
                              <span>{isPositive ? '↑' : '↓'}</span>
                              <span>{Math.abs(metric.change).toFixed(1)}%</span>
                            </span>
                          </div>
                        </div>
                      )}

                      {/* Insights Preview */}
                      {report.data.insights && report.data.insights.length > 0 && (
                        <div className="mb-4">
                          <p className="text-sm text-text-secondary line-clamp-2">
                            {report.data.insights[0]}
                          </p>
                        </div>
                      )}

                      {/* View Button */}
                      <Link
                        href={`/dashboard/reports/${report.id}`}
                        className="block w-full text-center px-4 py-2 bg-orange-fire text-white font-heading font-bold rounded-lg border-2 border-charcoal hover:bg-orange-hover transition-all shadow-brutalist-sm no-underline"
                      >
                        View Full Report →
                      </Link>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center gap-4 mt-8">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-4 py-2 bg-white border-2 border-charcoal rounded-lg font-heading font-bold text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-cream transition-colors"
                >
                  ← Previous
                </button>
                <span className="text-text-secondary font-mono">
                  Page {page} of {totalPages}
                </span>
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-4 py-2 bg-white border-2 border-charcoal rounded-lg font-heading font-bold text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-cream transition-colors"
                >
                  Next →
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
