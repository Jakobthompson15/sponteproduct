'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@clerk/nextjs';
import { toast } from 'react-hot-toast';
import { ConnectAccounts } from '@/components/onboarding/steps/ConnectAccounts';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function ConnectionsPage() {
  const router = useRouter();
  const { getToken, isLoaded, isSignedIn } = useAuth();
  const [locationId, setLocationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      fetchLocation();
    } else if (isLoaded && !isSignedIn) {
      toast.error('Please sign in');
      setIsLoading(false);
    }
  }, [isLoaded, isSignedIn]);

  const fetchLocation = async () => {
    try {
      // Get token using Clerk's useAuth hook
      const token = await getToken();
      
      if (!token) {
        toast.error('Authentication failed');
        setIsLoading(false);
        return;
      }

      // Fetch user's location
      const response = await fetch(`${API_URL}/api/locations/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      if (!data || !data.id) {
        // User hasn't completed onboarding yet
        toast.error('Please complete onboarding first');
        router.push('/onboarding');
        return;
      }

      setLocationId(data.id);
    } catch (error) {
      console.error('Error fetching location:', error);
      toast.error('Failed to load location');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin text-6xl mb-4">⚙️</div>
          <p className="text-text-secondary font-heading">Loading...</p>
        </div>
      </div>
    );
  }

  if (!locationId) {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="text-center">
          <p className="text-text-secondary font-heading">Redirecting to onboarding...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cream">
      <div className="max-w-4xl mx-auto px-6 py-12">
        <div className="mb-8">
          <h1 className="font-display text-5xl text-charcoal mb-3">Connections</h1>
          <p className="text-text-secondary text-lg">
            Manage your integrations with Google, WordPress, and social media platforms
          </p>
        </div>

        {/* Reuse the ConnectAccounts component from onboarding */}
        <ConnectAccounts locationId={locationId} />
      </div>
    </div>
  );
}
