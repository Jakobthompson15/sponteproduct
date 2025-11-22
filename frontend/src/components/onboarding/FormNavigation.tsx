'use client';

import { Button } from '@/components/ui/Button';

interface FormNavigationProps {
  currentStep: number;
  totalSteps: number;
  onPrevious: () => void;
  onNext: () => void;
  isSubmitting?: boolean;
}

export function FormNavigation({
  currentStep,
  totalSteps,
  onPrevious,
  onNext,
  isSubmitting,
}: FormNavigationProps) {
  const isFirstStep = currentStep === 1;
  const isLastStep = currentStep === totalSteps;

  return (
    <div className="flex justify-between gap-4 mt-12">
      {!isFirstStep && (
        <Button
          type="button"
          variant="secondary"
          onClick={onPrevious}
          disabled={isSubmitting}
        >
          ← Back
        </Button>
      )}

      <Button
        type="button"
        variant="primary"
        onClick={onNext}
        isLoading={isSubmitting}
        className={isFirstStep ? 'ml-auto' : ''}
      >
        {isLastStep ? 'Launch My Agents 🚀' : 'Continue →'}
      </Button>
    </div>
  );
}
