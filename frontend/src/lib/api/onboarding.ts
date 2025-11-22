/**
 * Onboarding API Functions
 */

import apiClient from './client';
import type { OnboardingFormData } from '@/types/onboarding';
import type { OnboardingSubmitResponse } from '@/types/api';

/**
 * Submit onboarding form data to backend
 */
export async function submitOnboarding(
  data: OnboardingFormData
): Promise<OnboardingSubmitResponse> {
  const response = await apiClient.post<OnboardingSubmitResponse>(
    '/api/onboarding/submit',
    data
  );
  return response.data;
}

/**
 * Create draft location after step 1 (Business Profile)
 */
export async function createDraftLocation(data: {
  businessName: string;
  dbaName?: string;
  streetAddress: string;
  city: string;
  state: string;
  zipCode: string;
  phone: string;
  phoneSecondary?: string;
  websiteUrl?: string;
  cmsPlatform?: string;
  primaryCategory: string;
  services?: string | string[];
}): Promise<{ success: boolean; location_id: string; message: string }> {
  const response = await apiClient.post('/api/onboarding/create-location', data);
  return response.data;
}

/**
 * Health check endpoint
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await apiClient.get('/health');
  return response.data;
}
