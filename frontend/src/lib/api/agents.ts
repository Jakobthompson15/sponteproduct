/**
 * Agent API Functions
 */

import apiClient from './client';
import type { AgentOutput, GbpDraft } from '@/types/api';

/**
 * Get all GBP drafts for a location
 */
export async function getGbpDrafts(
  locationId: string
): Promise<GbpDraft[]> {
  const response = await apiClient.get<{ drafts: GbpDraft[] }>(
    `/api/agents/gbp/drafts/${locationId}`
  );
  return response.data.drafts;
}

/**
 * Approve an agent output
 */
export async function approveAgentOutput(outputId: string): Promise<AgentOutput> {
  const response = await apiClient.patch<AgentOutput>(
    `/api/agents/outputs/${outputId}/approve`
  );
  return response.data;
}

/**
 * Reject an agent output
 */
export async function rejectAgentOutput(
  outputId: string,
  reason: string
): Promise<AgentOutput> {
  const response = await apiClient.patch<AgentOutput>(
    `/api/agents/outputs/${outputId}/reject`,
    { reason }
  );
  return response.data;
}

/**
 * Update an agent output
 */
export async function updateAgentOutput(
  outputId: string,
  content: string,
  callToAction: string
): Promise<AgentOutput> {
  const response = await apiClient.patch<AgentOutput>(
    `/api/agents/outputs/${outputId}`,
    { content, call_to_action: callToAction }
  );
  return response.data;
}
