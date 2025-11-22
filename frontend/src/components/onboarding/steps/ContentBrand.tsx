'use client';

import { Select } from '@/components/ui/Select';
import { Textarea } from '@/components/ui/Textarea';
import { UseFormRegister, FieldErrors } from 'react-hook-form';
import type { OnboardingFormData } from '@/types/onboarding';

interface ContentBrandProps {
  register: UseFormRegister<OnboardingFormData>;
  errors: FieldErrors<OnboardingFormData>;
}

export function ContentBrand({ register, errors }: ContentBrandProps) {
  return (
    <div className="space-y-6">
      <Select
        {...register('brandTone')}
        label="Brand Tone"
        hint="How should your AI agent write? This affects all content."
        error={errors.brandTone?.message}
        required
      >
        <option value="">Select your tone...</option>
        <option value="professional">Professional</option>
        <option value="friendly">Friendly</option>
        <option value="witty">Witty</option>
        <option value="luxury">Luxury</option>
        <option value="clinical">Clinical</option>
      </Select>

      <Textarea
        {...register('forbiddenWords')}
        label="Forbidden Words/Claims"
        placeholder="e.g., best, guaranteed, miracle, FDA-approved"
        hint="Words the AI should never use (medical/legal compliance)"
        error={errors.forbiddenWords?.message}
      />

      <Select
        {...register('blogCadence')}
        label="Blog Posting Cadence"
        error={errors.blogCadence?.message}
      >
        <option value="off">Off - No blog posts</option>
        <option value="monthly">Monthly - 1 post per month</option>
        <option value="biweekly">Bi-weekly - 2 posts per month</option>
        <option value="weekly">Weekly - 4 posts per month</option>
      </Select>

      <Select
        {...register('gbpCadence')}
        label="GBP Post Cadence"
        error={errors.gbpCadence?.message}
      >
        <option value="off">Off - No GBP posts</option>
        <option value="weekly">Weekly - 1 post per week</option>
        <option value="biweekly">Bi-weekly - 2 posts per week</option>
        <option value="triweekly">Tri-weekly - 3 posts per week</option>
      </Select>

      <Select
        {...register('socialCadence')}
        label="Social Media Cadence"
        hint="Available when Social Agent launches (V1.1 feature)"
        error={errors.socialCadence?.message}
        disabled
      >
        <option value="off">Off - No social posts</option>
        <option value="3x">3× per week</option>
        <option value="5x">5× per week</option>
        <option value="7x">Daily</option>
      </Select>
    </div>
  );
}
