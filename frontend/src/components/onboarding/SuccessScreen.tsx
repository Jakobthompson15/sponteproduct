'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/Button';

interface SuccessScreenProps {
  userId?: string;
  locationId?: string;
}

export function SuccessScreen({ userId, locationId }: SuccessScreenProps) {
  return (
    <div className="text-center py-16">
      <div className="text-8xl mb-8">🚀</div>

      <h2 className="font-display text-5xl md:text-6xl text-charcoal mb-6">
        Your Agents Are Launching!
      </h2>

      <p className="text-xl text-text-secondary max-w-2xl mx-auto mb-8 leading-relaxed">
        We're setting up your multi-agent system now. You'll receive a
        confirmation email within 5 minutes with next steps.
      </p>

      {userId && locationId && (
        <div className="bg-cream-dark border-2 border-charcoal/10 rounded-lg p-6 max-w-md mx-auto mb-8">
          <p className="text-sm text-text-muted mb-2 font-mono">
            <strong>User ID:</strong> {userId}
          </p>
          <p className="text-sm text-text-muted font-mono">
            <strong>Location ID:</strong> {locationId}
          </p>
        </div>
      )}

      <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <Link href="/dashboard">
          <Button variant="primary">Go to Dashboard →</Button>
        </Link>
        <Link href="/">
          <Button variant="secondary">Back to Home</Button>
        </Link>
      </div>

      <div className="mt-12 p-6 bg-white border-2 border-charcoal rounded-brutalist max-w-2xl mx-auto">
        <h3 className="font-heading font-bold text-lg mb-4 flex items-center justify-center gap-2">
          <span>📧</span>
          <span>Check Your Email</span>
        </h3>
        <p className="text-text-secondary text-sm">
          We've sent a welcome email to your inbox with:
        </p>
        <ul className="mt-4 space-y-2 text-left max-w-md mx-auto text-sm text-text-primary">
          <li className="flex items-start">
            <span className="text-sage-green mr-2">✓</span>
            <span>Your active AI agents list</span>
          </li>
          <li className="flex items-start">
            <span className="text-sage-green mr-2">✓</span>
            <span>Next steps to complete setup</span>
          </li>
          <li className="flex items-start">
            <span className="text-sage-green mr-2">✓</span>
            <span>Link to your dashboard</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
