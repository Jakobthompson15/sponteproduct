'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { toast } from 'react-hot-toast';
import Link from 'next/link';

// Components
import { ProgressBar } from '@/components/onboarding/ProgressBar';
import { FormNavigation } from '@/components/onboarding/FormNavigation';
import { BusinessProfile } from '@/components/onboarding/steps/BusinessProfile';
import { ConnectAccounts } from '@/components/onboarding/steps/ConnectAccounts';
import { ContentBrand } from '@/components/onboarding/steps/ContentBrand';
import { AutonomyControl } from '@/components/onboarding/steps/AutonomyControl';
import { GoalsReporting } from '@/components/onboarding/steps/GoalsReporting';
import { ReviewLaunch } from '@/components/onboarding/steps/ReviewLaunch';
import { SuccessScreen } from '@/components/onboarding/SuccessScreen';

// Types & Validation
import type { OnboardingFormData, OnboardingStep } from '@/types/onboarding';
import { STEP_DESCRIPTIONS } from '@/types/onboarding';
import { completeOnboardingSchema } from '@/lib/utils/validators';

// API
import { submitOnboarding, createDraftLocation } from '@/lib/api/onboarding';

const TOTAL_STEPS = 6;
const STORAGE_KEY = 'sponte_onboarding_draft';

export default function OnboardingPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<OnboardingStep>(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [submissionData, setSubmissionData] = useState<{
    userId?: string;
    locationId?: string;
  }>({});

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    trigger,
    formState: { errors },
  } = useForm<OnboardingFormData>({
    resolver: zodResolver(completeOnboardingSchema),
    mode: 'onBlur',
    defaultValues: {
      globalAutonomy: 'approve', // Default to approve mode
      blogCadence: 'monthly',
      gbpCadence: 'weekly',
      weeklyReport: true,
      monthlyReport: true,
    },
  });

  // Load saved data from localStorage on mount
  useEffect(() => {
    const savedData = localStorage.getItem(STORAGE_KEY);
    if (savedData) {
      try {
        const parsed = JSON.parse(savedData);
        Object.keys(parsed).forEach((key) => {
          setValue(key as keyof OnboardingFormData, parsed[key]);
        });
        toast.success('Loaded your saved progress');
      } catch (error) {
        console.error('Error loading saved data:', error);
      }
    }
  }, [setValue]);

  // Save to localStorage whenever form data changes
  useEffect(() => {
    const subscription = watch((formData) => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(formData));
      } catch (error) {
        console.error('Error saving to localStorage:', error);
      }
    });
    return () => subscription.unsubscribe();
  }, [watch]);

  const handleNext = async () => {
    // Validate current step before proceeding
    const isValid = await trigger();

    if (!isValid) {
      toast.error('Please fill in all required fields correctly');
      return;
    }

    // If moving from step 1 to step 2, create draft location
    if (currentStep === 1) {
      try {
        const formData = watch();
        const response = await createDraftLocation({
          businessName: formData.businessName,
          dbaName: formData.dbaName,
          streetAddress: formData.streetAddress,
          city: formData.city,
          state: formData.state,
          zipCode: formData.zipCode,
          phone: formData.phone,
          phoneSecondary: formData.phoneSecondary,
          websiteUrl: formData.websiteUrl,
          cmsPlatform: formData.cmsPlatform,
          primaryCategory: formData.primaryCategory,
          services: formData.services,
        });

        // Save location_id to localStorage
        const savedData = localStorage.getItem(STORAGE_KEY);
        if (savedData) {
          const parsed = JSON.parse(savedData);
          parsed.locationId = response.location_id;
          localStorage.setItem(STORAGE_KEY, JSON.stringify(parsed));
        } else {
          localStorage.setItem(STORAGE_KEY, JSON.stringify({ locationId: response.location_id }));
        }

        console.log('Draft location created:', response.location_id);
      } catch (error) {
        console.error('Error creating draft location:', error);
        toast.error('Failed to save business profile. Please try again.');
        return;
      }
    }

    if (currentStep < TOTAL_STEPS) {
      setCurrentStep((prev) => (prev + 1) as OnboardingStep);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (currentStep === TOTAL_STEPS) {
      // Final step - submit form
      await handleFinalSubmit();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep((prev) => (prev - 1) as OnboardingStep);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleEditStep = (step: number) => {
    setCurrentStep(step as OnboardingStep);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleFinalSubmit = async () => {
    setIsSubmitting(true);

    try {
      const formData = watch();

      // Submit to backend API
      const response = await submitOnboarding(formData);

      console.log('Onboarding successful:', response);

      // Store response data
      setSubmissionData({
        userId: response.user_id,
        locationId: response.location_id,
      });

      // Show success screen
      setShowSuccess(true);

      // Clear localStorage after successful completion
      // (location_id is already saved during step 1, but we can clear the rest)
      localStorage.removeItem(STORAGE_KEY);

      // Success toast
      toast.success('Your agents are launching! 🚀');
    } catch (error) {
      console.error('Onboarding error:', error);
      toast.error('Failed to submit onboarding. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Show success screen
  if (showSuccess) {
    return (
      <div className="min-h-screen bg-cream">
        <nav className="fixed top-0 left-0 right-0 z-50 bg-cream/95 backdrop-blur-md border-b-2 border-charcoal/10 px-12 py-6">
          <div className="max-w-4xl mx-auto">
            <Link
              href="/"
              className="font-display text-4xl text-charcoal hover:text-orange-fire transition-colors"
            >
              Sponte
            </Link>
          </div>
        </nav>

        <div className="pt-32 pb-20 px-8">
          <div className="max-w-4xl mx-auto">
            <SuccessScreen
              userId={submissionData.userId}
              locationId={submissionData.locationId}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cream">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-cream/95 backdrop-blur-md border-b-2 border-charcoal/10 px-12 py-6">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <Link
            href="/"
            className="font-display text-4xl text-charcoal hover:text-orange-fire transition-colors"
          >
            Sponte
          </Link>
          <Link
            href="/"
            className="font-heading font-semibold text-text-secondary hover:text-orange-fire transition-colors"
          >
            ← Back to home
          </Link>
        </div>
      </nav>

      {/* Main Content */}
      <div className="pt-32 pb-20 px-8">
        <div className="max-w-4xl mx-auto">
          {/* Progress Bar */}
          <ProgressBar currentStep={currentStep} totalSteps={TOTAL_STEPS} />

          {/* Form Card */}
          <div className="bg-white border-3 border-charcoal rounded-brutalist-lg p-8 md:p-12 shadow-brutalist">
            <p className="text-text-secondary mb-8">
              {STEP_DESCRIPTIONS[currentStep]}
            </p>

            <form onSubmit={handleSubmit(handleNext)}>
              {/* Step 1: Business Profile */}
              {currentStep === 1 && (
                <BusinessProfile register={register} errors={errors} setValue={setValue} />
              )}

              {/* Step 2: Connect Accounts */}
              {currentStep === 2 && <ConnectAccounts />}

              {/* Step 3: Content & Brand */}
              {currentStep === 3 && (
                <ContentBrand register={register} errors={errors} />
              )}

              {/* Step 4: Autonomy & Control */}
              {currentStep === 4 && (
                <AutonomyControl
                  register={register}
                  errors={errors}
                  watch={watch}
                  setValue={setValue}
                />
              )}

              {/* Step 5: Goals & Reporting */}
              {currentStep === 5 && (
                <GoalsReporting register={register} errors={errors} />
              )}

              {/* Step 6: Review & Launch */}
              {currentStep === 6 && (
                <ReviewLaunch watch={watch} onEditStep={handleEditStep} />
              )}

              {/* Navigation */}
              <FormNavigation
                currentStep={currentStep}
                totalSteps={TOTAL_STEPS}
                onPrevious={handlePrevious}
                onNext={handleNext}
                isSubmitting={isSubmitting}
              />
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
