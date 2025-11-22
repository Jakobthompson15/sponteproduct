'use client';

import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { UseFormRegister, FieldErrors } from 'react-hook-form';
import type { OnboardingFormData } from '@/types/onboarding';

interface GoalsReportingProps {
  register: UseFormRegister<OnboardingFormData>;
  errors: FieldErrors<OnboardingFormData>;
}

export function GoalsReporting({ register, errors }: GoalsReportingProps) {
  return (
    <div className="space-y-6">
      <Select
        {...register('primaryGoal')}
        label="Primary Business Goal"
        hint="We'll optimize and report on this metric"
        error={errors.primaryGoal?.message}
        required
      >
        <option value="">What matters most to your business?</option>
        <option value="calls">Phone Calls</option>
        <option value="forms">Form Fills / Contact Requests</option>
        <option value="bookings">Bookings / Appointments</option>
        <option value="directions">Direction Requests</option>
      </Select>

      <div className="border-2 border-charcoal/10 rounded-lg p-6">
        <h3 className="font-heading font-semibold text-base mb-4">
          Report Frequency
        </h3>
        <div className="space-y-3">
          <label className="flex items-center gap-3 cursor-pointer">
            <input
              {...register('weeklyReport')}
              type="checkbox"
              className="w-5 h-5 border-2 border-charcoal rounded accent-orange-fire cursor-pointer"
              defaultChecked
            />
            <span className="text-text-primary">
              Weekly Summary (every Monday)
            </span>
          </label>
          <label className="flex items-center gap-3 cursor-pointer">
            <input
              {...register('monthlyReport')}
              type="checkbox"
              className="w-5 h-5 border-2 border-charcoal rounded accent-orange-fire cursor-pointer"
              defaultChecked
            />
            <span className="text-text-primary">
              Monthly Deep-Dive (first Monday of month)
            </span>
          </label>
        </div>
      </div>

      <Input
        {...register('reportEmails')}
        type="email"
        label="Report Recipients"
        placeholder="you@example.com"
        hint="Separate multiple emails with commas"
        error={errors.reportEmails?.message}
        required
      />

      <Input
        {...register('utmCampaign')}
        label="UTM Campaign Name"
        placeholder="sponte_local_seo"
        hint="Track all Sponte-generated links in Analytics (optional)"
        error={errors.utmCampaign?.message}
      />
    </div>
  );
}
