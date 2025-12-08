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

// Agent & Draft Types
export type GbpCta =
  | 'BOOK'
  | 'CALL'
  | 'ORDER'
  | 'LEARN_MORE'
  | 'SHOP'
  | 'SIGN_UP';

export interface GbpDraft {
  id: string; // This is the AgentOutput ID
  content: string;
  call_to_action: GbpCta;
  status: 'DRAFT' | 'APPROVED' | 'REJECTED' | 'POSTED';
  created_at: string;
}

export interface AgentOutput {
  id: string;
  task_id: string;
  location_id: string;
  output_type: string;
  status: string;
  content: string;
  call_to_action?: GbpCta;
  platform_post_id?: string;
  output_metadata?: Record<string, unknown>;
  created_at: string;
  posted_at?: string;
}
