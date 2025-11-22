/**
 * Onboarding Form Data Types
 * Matches the backend API schema
 */

export interface OnboardingFormData {
  // Step 1: Business Profile & NAP
  email: string;
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
  services?: string;
  coverageRadius?: number;

  // Step 2: OAuth Connections (stored separately, not in this form)
  // GBP, GSC, GA4, WordPress tokens handled via OAuth flow

  // Step 3: Content & Brand
  brandTone?: string;
  forbiddenWords?: string;
  forbiddenTopics?: string;
  blogCadence?: 'off' | 'monthly' | 'biweekly' | 'weekly';
  gbpCadence?: 'off' | 'weekly' | 'biweekly' | 'triweekly';
  socialCadence?: 'off' | '3x' | '5x' | '7x';

  // Step 4: Autonomy & Control
  globalAutonomy?: 'draft' | 'autopilot';
  blackoutStart?: string;
  blackoutEnd?: string;

  // Step 5: Goals & Reporting
  primaryGoal?: 'calls' | 'forms' | 'bookings' | 'directions';
  weeklyReport?: boolean;
  monthlyReport?: boolean;
  reportEmails?: string;
  utmCampaign?: string;
}

export type OnboardingStep = 1 | 2 | 3 | 4 | 5 | 6;

export interface StepConfig {
  title: string;
  description: string;
}

export const STEP_TITLES: Record<OnboardingStep, string> = {
  1: 'Business Profile',
  2: 'Connect Your Accounts',
  3: 'Content & Brand',
  4: 'Autonomy & Control',
  5: 'Goals & Reporting',
  6: 'Review & Launch',
};

export const STEP_DESCRIPTIONS: Record<OnboardingStep, string> = {
  1: "We'll use this information to verify your NAP (Name, Address, Phone) consistency across all platforms.",
  2: 'Connect your accounts so Sponte can manage your local SEO automatically.',
  3: 'Configure how your AI agents will create content for your brand.',
  4: 'Choose how much control you want. You can change this anytime.',
  5: 'Set your business goals and reporting preferences.',
  6: 'Review your setup before launching your agents.',
};

export type AutonomyMode = 'draft' | 'autopilot';

export interface AutonomyOption {
  mode: AutonomyMode;
  badge: string;
  label: string;
  description: string;
}

export const AUTONOMY_OPTIONS: AutonomyOption[] = [
  {
    mode: 'draft',
    badge: 'DRAFT',
    label: 'Manual Control',
    description: 'Agents create drafts. You review and publish manually. Full control over every piece of content.',
  },
  {
    mode: 'autopilot',
    badge: 'AUTO',
    label: 'Full Autopilot',
    description: 'Agents create and publish automatically. You get reports. Set it and forget it.',
  },
];
