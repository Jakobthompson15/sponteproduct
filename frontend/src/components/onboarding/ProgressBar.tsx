'use client';

import { STEP_TITLES } from '@/types/onboarding';
import type { OnboardingStep } from '@/types/onboarding';

interface ProgressBarProps {
  currentStep: OnboardingStep;
  totalSteps: number;
}

export function ProgressBar({ currentStep, totalSteps }: ProgressBarProps) {
  const percentage = (currentStep / totalSteps) * 100;

  return (
    <div className="mb-16">
      <div className="flex justify-between items-center mb-4">
        <span className="font-mono text-sm font-bold text-orange-fire tracking-wide">
          STEP {currentStep} OF {totalSteps}
        </span>
      </div>

      <h1 className="font-display text-5xl md:text-6xl text-charcoal mb-6 leading-tight">
        {STEP_TITLES[currentStep]}
      </h1>

      <div className="h-2 bg-cream-dark border-2 border-charcoal rounded-full overflow-hidden">
        <div
          className="h-full bg-orange-fire transition-all duration-300 ease-out rounded-full"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
