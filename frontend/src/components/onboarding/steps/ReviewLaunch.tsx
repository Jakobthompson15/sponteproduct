'use client';

import { UseFormWatch } from 'react-hook-form';
import type { OnboardingFormData } from '@/types/onboarding';

interface ReviewLaunchProps {
  watch: UseFormWatch<OnboardingFormData>;
  onEditStep: (step: number) => void;
}

export function ReviewLaunch({ watch, onEditStep }: ReviewLaunchProps) {
  const formData = watch();

  const formatAddress = () => {
    const parts = [
      formData.streetAddress,
      formData.city,
      formData.state,
      formData.zipCode,
    ].filter(Boolean);
    return parts.join(', ') || 'Not set';
  };

  return (
    <div className="space-y-6">
      <p className="text-text-secondary mb-8">
        Review your setup before launching your agents.
      </p>

      {/* Business Profile Section */}
      <div className="bg-cream border-2 border-charcoal/10 rounded-brutalist p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-heading font-bold text-lg">
            Business Profile & NAP
          </h3>
          <button
            type="button"
            onClick={() => onEditStep(1)}
            className="text-sm text-orange-fire font-semibold hover:underline"
          >
            Edit
          </button>
        </div>

        <div className="space-y-3 text-sm">
          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Email Address
            </div>
            <div className="text-text-primary">{formData.email || 'Not set'}</div>
          </div>

          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Legal Business Name
            </div>
            <div className="text-text-primary">
              {formData.businessName || 'Not set'}
            </div>
          </div>

          {formData.dbaName && (
            <div>
              <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
                DBA Name
              </div>
              <div className="text-text-primary">{formData.dbaName}</div>
            </div>
          )}

          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Business Address
            </div>
            <div className="text-text-primary">{formatAddress()}</div>
          </div>

          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Primary Phone
            </div>
            <div className="text-text-primary">{formData.phone || 'Not set'}</div>
          </div>

          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Primary Category
            </div>
            <div className="text-text-primary">
              {formData.primaryCategory || 'Not set'}
            </div>
          </div>
        </div>
      </div>

      {/* Content & Brand Section */}
      <div className="bg-cream border-2 border-charcoal/10 rounded-brutalist p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-heading font-bold text-lg">Content & Brand</h3>
          <button
            type="button"
            onClick={() => onEditStep(3)}
            className="text-sm text-orange-fire font-semibold hover:underline"
          >
            Edit
          </button>
        </div>

        <div className="space-y-3 text-sm">
          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Brand Tone
            </div>
            <div className="text-text-primary capitalize">
              {formData.brandTone || 'Not set'}
            </div>
          </div>

          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Blog Cadence
            </div>
            <div className="text-text-primary capitalize">
              {formData.blogCadence || 'Not set'}
            </div>
          </div>

          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              GBP Post Cadence
            </div>
            <div className="text-text-primary capitalize">
              {formData.gbpCadence || 'Not set'}
            </div>
          </div>
        </div>
      </div>

      {/* Autonomy Section */}
      <div className="bg-cream border-2 border-charcoal/10 rounded-brutalist p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-heading font-bold text-lg">Autonomy</h3>
          <button
            type="button"
            onClick={() => onEditStep(4)}
            className="text-sm text-orange-fire font-semibold hover:underline"
          >
            Edit
          </button>
        </div>

        <div className="space-y-3 text-sm">
          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Global Mode
            </div>
            <div className="text-text-primary capitalize">
              {formData.globalAutonomy || 'approve'}
            </div>
          </div>
        </div>
      </div>

      {/* Goals & Reporting Section */}
      <div className="bg-cream border-2 border-charcoal/10 rounded-brutalist p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-heading font-bold text-lg">Goals & Reporting</h3>
          <button
            type="button"
            onClick={() => onEditStep(5)}
            className="text-sm text-orange-fire font-semibold hover:underline"
          >
            Edit
          </button>
        </div>

        <div className="space-y-3 text-sm">
          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Primary Goal
            </div>
            <div className="text-text-primary capitalize">
              {formData.primaryGoal || 'Not set'}
            </div>
          </div>

          <div>
            <div className="text-text-muted font-semibold uppercase tracking-wide text-xs mb-1">
              Report Recipients
            </div>
            <div className="text-text-primary">
              {formData.reportEmails || 'Not set'}
            </div>
          </div>
        </div>
      </div>

      {/* What Happens Next */}
      <div className="mt-8 p-8 bg-cream-dark border-2 border-orange-fire rounded-brutalist text-center">
        <h3 className="font-display text-2xl text-charcoal mb-3">
          What Happens Next?
        </h3>
        <p className="text-text-secondary mb-6">
          After you launch, your agents will:
        </p>
        <ul className="text-left max-w-lg mx-auto space-y-2 text-text-primary">
          <li className="flex items-start">
            <span className="text-sage-green mr-2">✓</span>
            <span>Verify your GBP listing and sync NAP data</span>
          </li>
          <li className="flex items-start">
            <span className="text-sage-green mr-2">✓</span>
            <span>Pull keyword data from Search Console</span>
          </li>
          <li className="flex items-start">
            <span className="text-sage-green mr-2">✓</span>
            <span>Create your first GBP post draft (within 24 hours)</span>
          </li>
          <li className="flex items-start">
            <span className="text-sage-green mr-2">✓</span>
            <span>Send you a weekly summary next Monday</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
