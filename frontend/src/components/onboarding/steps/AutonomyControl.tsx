'use client';

import { Input } from '@/components/ui/Input';
import { UseFormRegister, FieldErrors, UseFormWatch, UseFormSetValue } from 'react-hook-form';
import type { OnboardingFormData, AutonomyMode } from '@/types/onboarding';
import { AUTONOMY_OPTIONS } from '@/types/onboarding';
import { cn } from '@/lib/utils/cn';

interface AutonomyControlProps {
  register: UseFormRegister<OnboardingFormData>;
  errors: FieldErrors<OnboardingFormData>;
  watch: UseFormWatch<OnboardingFormData>;
  setValue: UseFormSetValue<OnboardingFormData>;
}

export function AutonomyControl({ register, errors, watch, setValue }: AutonomyControlProps) {
  const selectedAutonomy = watch('globalAutonomy') || 'draft';

  const handleAutonomySelect = (mode: AutonomyMode) => {
    setValue('globalAutonomy', mode);
  };

  return (
    <div className="space-y-6">
      <p className="text-text-secondary mb-8">
        Choose how much control you want. You can change this anytime.
      </p>

      <div className="grid md:grid-cols-3 gap-4 mb-8">
        {AUTONOMY_OPTIONS.map((option) => (
          <button
            key={option.mode}
            type="button"
            onClick={() => handleAutonomySelect(option.mode)}
            className={cn(
              'bg-cream border-3 border-charcoal rounded-brutalist p-6 cursor-pointer transition-all text-center',
              'hover:translate-y-[-2px] hover:shadow-brutalist-sm',
              selectedAutonomy === option.mode &&
                'bg-orange-fire border-charcoal shadow-brutalist'
            )}
          >
            <div
              className={cn(
                'inline-block px-4 py-2 bg-charcoal text-white font-mono text-xs font-bold rounded-md mb-3',
                selectedAutonomy === option.mode && 'bg-white text-orange-fire'
              )}
            >
              {option.badge}
            </div>
            <h3
              className={cn(
                'font-heading font-bold text-lg mb-2',
                selectedAutonomy === option.mode ? 'text-white' : 'text-charcoal'
              )}
            >
              {option.label}
            </h3>
            <p
              className={cn(
                'text-sm',
                selectedAutonomy === option.mode ? 'text-white/90' : 'text-text-secondary'
              )}
            >
              {option.description}
            </p>
          </button>
        ))}
      </div>

      {/* Hidden input for form state */}
      <input type="hidden" {...register('globalAutonomy')} />

      <div className="border-t-2 border-charcoal/10 pt-6">
        <h3 className="font-heading font-semibold text-lg mb-4">
          Blackout Hours (Optional)
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          <Input
            {...register('blackoutStart')}
            type="time"
            label="Don't publish after"
            placeholder="23:00"
            error={errors.blackoutStart?.message}
          />
          <Input
            {...register('blackoutEnd')}
            type="time"
            label="Resume publishing after"
            placeholder="07:00"
            error={errors.blackoutEnd?.message}
          />
        </div>
      </div>

      <div className="mt-6 p-4 bg-cream-dark rounded-lg border-2 border-charcoal/20">
        <p className="text-sm text-text-secondary">
          <strong>💡 Pro tip:</strong> Start with "Manual Control" to see
          what agents create, then switch to Autopilot once you're comfortable with the quality.
        </p>
      </div>
    </div>
  );
}
