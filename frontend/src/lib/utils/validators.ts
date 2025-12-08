/**
 * Zod validation schemas for onboarding form
 */

import { z } from 'zod';

// Step 1: Business Profile validation
export const businessProfileSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  businessName: z.string().min(2, 'Business name must be at least 2 characters'),
  dbaName: z.string().optional(),
  streetAddress: z.string().min(5, 'Please enter a valid street address'),
  city: z.string().min(2, 'Please enter a valid city'),
  state: z.string().min(2, 'Please enter a valid state'),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/, 'Please enter a valid ZIP code'),
  phone: z.string().regex(/^\(\d{3}\) \d{3}-\d{4}$/, 'Format: (XXX) XXX-XXXX'),
  phoneSecondary: z.string().optional(),
  websiteUrl: z.string().url('Please enter a valid URL').optional().or(z.literal('')),
  cmsPlatform: z.string().optional(),
  primaryCategory: z.string().min(2, 'Please enter your business category'),
  services: z.string().optional(),
  coverageRadius: z.number().min(1).max(100).optional(),
});

// Step 3: Content & Brand validation
export const contentBrandSchema = z.object({
  brandTone: z.string().optional(),
  forbiddenWords: z.string().optional(),
  forbiddenTopics: z.string().optional(),
  blogCadence: z.enum(['off', 'monthly', 'biweekly', 'weekly']).optional(),
  gbpCadence: z.enum(['off', 'weekly', 'biweekly', 'triweekly']).optional(),
  socialCadence: z.enum(['off', '3x', '5x', '7x']).optional(),
});

// Step 4: Autonomy & Control validation
export const autonomyControlSchema = z.object({
  globalAutonomy: z.enum(['draft', 'autopilot']).optional(),
  blackoutStart: z.string().optional(),
  blackoutEnd: z.string().optional(),
});

// Step 5: Goals & Reporting validation
export const goalsReportingSchema = z.object({
  primaryGoal: z.enum(['calls', 'forms', 'bookings', 'directions']).optional(),
  weeklyReport: z.boolean().optional(),
  monthlyReport: z.boolean().optional(),
  reportEmails: z.string().email('Please enter a valid email').optional().or(z.literal('')),
  utmCampaign: z.string().optional(),
});

// Complete form validation (all steps combined)
export const completeOnboardingSchema = businessProfileSchema
  .merge(contentBrandSchema)
  .merge(autonomyControlSchema)
  .merge(goalsReportingSchema);

export type BusinessProfileData = z.infer<typeof businessProfileSchema>;
export type ContentBrandData = z.infer<typeof contentBrandSchema>;
export type AutonomyControlData = z.infer<typeof autonomyControlSchema>;
export type GoalsReportingData = z.infer<typeof goalsReportingSchema>;
export type CompleteOnboardingData = z.infer<typeof completeOnboardingSchema>;
