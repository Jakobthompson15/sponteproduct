/**
 * Reports API Functions
 */

import apiClient from './client';
import type {
  Report,
  ReportListResponse,
  LatestReportsResponse,
  ReportType,
} from '@/types/api';

/**
 * Get all reports for a location with optional filtering
 */
export async function getReports(
  locationId: string,
  reportType?: ReportType,
  page: number = 1,
  pageSize: number = 20
): Promise<ReportListResponse> {
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  });

  if (reportType) {
    params.append('report_type', reportType);
  }

  const response = await apiClient.get<ReportListResponse>(
    `/api/reports/${locationId}?${params.toString()}`
  );
  return response.data;
}

/**
 * Get the latest weekly and monthly reports for a location
 */
export async function getLatestReports(
  locationId: string
): Promise<LatestReportsResponse> {
  const response = await apiClient.get<LatestReportsResponse>(
    `/api/reports/${locationId}/latest`
  );
  return response.data;
}

/**
 * Get a specific report by ID
 */
export async function getReport(reportId: string): Promise<Report> {
  const response = await apiClient.get<Report>(`/api/reports/report/${reportId}`);
  return response.data;
}

/**
 * Generate a new report
 */
export async function generateReport(
  locationId: string,
  reportType: ReportType,
  periodStart: Date,
  periodEnd: Date,
  sendEmail: boolean = false
): Promise<Report> {
  const response = await apiClient.post<Report>('/api/reports/generate', {
    location_id: locationId,
    report_type: reportType,
    period_start: periodStart.toISOString(),
    period_end: periodEnd.toISOString(),
    send_email: sendEmail,
  });
  return response.data;
}
