/**
 * Connections API Functions
 */

import apiClient from './client';

export interface ConnectionStatus {
  provider: string;
  connected: boolean;
  connected_at?: string;
  expires_at?: string;
  needs_reconnection: boolean;
}

export interface ConnectionsStatusResponse {
  location_id: string;
  google_business_profile: ConnectionStatus;
  google_search_console: ConnectionStatus;
  google_analytics: ConnectionStatus;
  wordpress: ConnectionStatus;
  meta: ConnectionStatus;
  linkedin: ConnectionStatus;
}

/**
 * Get status of all OAuth connections
 */
export async function getConnectionsStatus(): Promise<ConnectionsStatusResponse> {
  const response = await apiClient.get<ConnectionsStatusResponse>(
    '/api/oauth/connections/status'
  );
  return response.data;
}

/**
 * Disconnect Google OAuth
 */
export async function disconnectGoogle(locationId: string): Promise<{ message: string }> {
  const response = await apiClient.post<{ message: string }>(
    `/api/oauth/google/disconnect/${locationId}`
  );
  return response.data;
}
