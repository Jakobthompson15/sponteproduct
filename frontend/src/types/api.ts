/**
 * API Response Types
 * Matches FastAPI backend responses
 */

export interface OnboardingSubmitResponse {
  success: boolean;
  message: string;
  user_id: string;
  location_id: string;
  next_steps: string[];
}

export interface ApiError {
  detail: string;
  status?: number;
}

export interface HealthCheckResponse {
  status: string;
  timestamp: string;
  database: string;
}

// OAuth Types
export interface OAuthConnectionStatus {
  provider: 'gbp' | 'gsc' | 'ga4' | 'wordpress';
  connected: boolean;
  email?: string;
  connectedAt?: string;
}

export interface OAuthTokenResponse {
  access_token: string;
  refresh_token?: string;
  expires_in?: number;
  token_type?: string;
  scope?: string;
}

// Report Types
export enum ReportType {
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  CUSTOM = 'custom',
}

export interface ReportMetric {
  current: number;
  previous: number;
  change: number; // Percentage change
}

export interface ReviewMetric {
  count: number;
  avgRating: number;
  newReviews: number;
}

export interface AgentActivityMetric {
  postsCreated?: number;
  postsPublished?: number;
  citationsChecked?: number;
  citationsFixed?: number;
  keywordsTracked?: number;
  rankingImprovements?: number;
  draftsCreated?: number;
  articlesPublished?: number;
  reportsGenerated?: number;
  emailsSent?: number;
  tasksCompleted?: number;
}

export interface ReportData {
  period: string;
  metrics: {
    calls?: ReportMetric;
    gbpViews?: ReportMetric;
    directionRequests?: ReportMetric;
    websiteClicks?: ReportMetric;
    reviews?: ReviewMetric;
  };
  agentActivity?: {
    [key: string]: AgentActivityMetric;
  };
  insights?: string[];
  recommendations?: string[];
}

export interface Report {
  id: string;
  location_id: string;
  report_type: ReportType;
  period_start: string;
  period_end: string;
  data: ReportData;
  email_sent: string | null;
  email_recipients: string | null;
  created_at: string;
}

export interface ReportListResponse {
  reports: Report[];
  total: number;
  page: number;
  page_size: number;
}

export interface LatestReportsResponse {
  weekly: Report | null;
  monthly: Report | null;
}
