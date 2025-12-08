'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@clerk/nextjs';
import { toast } from 'react-hot-toast';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function GoogleOAuthCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { getToken, isLoaded, isSignedIn } = useAuth();
  const [status, setStatus] = useState<'loading' | 'selecting' | 'success' | 'error'>('loading');
  const [accounts, setAccounts] = useState<any[]>([]);
  const [selectedLocation, setSelectedLocation] = useState<string | null>(null);
  const [locationId, setLocationId] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      console.log('[handleCallback] Starting...');
      console.log('[handleCallback] isLoaded:', isLoaded);
      console.log('[handleCallback] isSignedIn:', isSignedIn);

      // Wait for Clerk to load
      if (!isLoaded) {
        return;
      }

      if (!isSignedIn) {
        setStatus('error');
        toast.error('Please sign in to continue');
        setTimeout(() => router.push('/sign-in'), 3000);
        return;
      }

      const oauth_success = searchParams.get('oauth_success');
      const oauth_error = searchParams.get('oauth_error');
      const location_id = searchParams.get('location_id');

      console.log('[handleCallback] URL params:', {
        oauth_success,
        oauth_error,
        location_id,
        allParams: Array.from(searchParams.entries())
      });

      if (oauth_error) {
        setStatus('error');
        toast.error(`OAuth failed: ${oauth_error}`);
        setTimeout(() => router.push('/onboarding'), 3000);
        return;
      }

      if (oauth_success === 'google' && location_id) {
        console.log('[handleCallback] Valid callback, fetching locations for:', location_id);
        setLocationId(location_id);
        // Fetch available GBP locations
        await fetchGBPLocations(location_id);
      } else {
        console.error('[handleCallback] Invalid callback state:', { oauth_success, location_id });
        setStatus('error');
        toast.error('Invalid OAuth callback');
        setTimeout(() => router.push('/onboarding'), 3000);
      }
    };

    handleCallback();
  }, [searchParams, router, isLoaded, isSignedIn, getToken]);

  const fetchGBPLocations = async (locId: string) => {
    try {
      console.log('[fetchGBPLocations] Starting fetch for location:', locId);
      console.log('[fetchGBPLocations] API_URL:', API_URL);

      // Get Clerk token using useAuth hook
      const token = await getToken();
      console.log('[fetchGBPLocations] Got token:', token ? 'yes' : 'no');

      if (!token) {
        throw new Error('Failed to get auth token');
      }

      const url = `${API_URL}/api/oauth/google/accounts/${locId}`;
      console.log('[fetchGBPLocations] Fetching from:', url);

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('[fetchGBPLocations] Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('[fetchGBPLocations] Error response:', errorText);
        throw new Error(`Failed to fetch GBP accounts: ${response.status}`);
      }

      const data = await response.json();
      console.log('[fetchGBPLocations] Got accounts:', data);
      setAccounts(data.accounts || []);
      setStatus('selecting');
    } catch (error) {
      console.error('[fetchGBPLocations] Error:', error);
      toast.error('Failed to load your Google Business Profile locations');
      setStatus('error');
    }
  };

  const handleSaveLocation = async () => {
    if (!selectedLocation || !locationId) {
      toast.error('Please select a location');
      return;
    }

    try {
      // Get Clerk token using useAuth hook
      const token = await getToken();
      if (!token) {
        throw new Error('Failed to get auth token');
      }

      const response = await fetch(`${API_URL}/api/locations/${locationId}/gbp-location`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          gbp_location_name: selectedLocation,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save location');
      }

      setStatus('success');
      toast.success('Google Business Profile connected successfully!');

      // Redirect back to onboarding after 2 seconds
      setTimeout(() => {
        router.push('/onboarding');
      }, 2000);
    } catch (error) {
      console.error('Error saving location:', error);
      toast.error('Failed to save location. Please try again.');
    }
  };

  if (status === 'loading') {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-orange-fire border-t-transparent mb-4"></div>
          <h2 className="font-heading text-2xl font-bold text-charcoal">
            Connecting your Google Business Profile...
          </h2>
        </div>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="max-w-md text-center">
          <div className="text-6xl mb-4">❌</div>
          <h2 className="font-heading text-2xl font-bold text-charcoal mb-2">
            Connection Failed
          </h2>
          <p className="text-text-secondary mb-4">
            We couldn't connect your Google Business Profile. Redirecting back...
          </p>
        </div>
      </div>
    );
  }

  if (status === 'success') {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="max-w-md text-center">
          <div className="text-6xl mb-4">✅</div>
          <h2 className="font-heading text-2xl font-bold text-charcoal mb-2">
            Connected Successfully!
          </h2>
          <p className="text-text-secondary">
            Redirecting you back to onboarding...
          </p>
        </div>
      </div>
    );
  }

  // Status === 'selecting'
  return (
    <div className="min-h-screen bg-cream py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white border-3 border-charcoal rounded-brutalist-lg p-8 shadow-brutalist">
          <h2 className="font-heading text-3xl font-bold text-charcoal mb-2">
            Select Your Business Location
          </h2>
          <p className="text-text-secondary mb-8">
            Choose which Google Business Profile location you want to manage with Sponte AI.
          </p>

          {accounts.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-text-secondary">
                No Google Business Profile locations found for this account.
              </p>
              <p className="text-sm text-text-muted mt-2">
                Make sure you have access to at least one Google Business Profile.
              </p>
            </div>
          ) : (
            <div className="space-y-4 mb-8">
              {accounts.map((account) => (
                <div key={account.resource_name} className="space-y-3">
                  <h3 className="font-heading font-bold text-lg text-charcoal">
                    {account.account_name}
                  </h3>

                  {account.locations.map((location: any) => (
                    <div
                      key={location.resource_name}
                      className={`border-2 rounded-brutalist p-4 cursor-pointer transition-all ${
                        selectedLocation === location.resource_name
                          ? 'border-orange-fire bg-orange-fire/5'
                          : 'border-charcoal hover:border-orange-fire'
                      }`}
                      onClick={() => setSelectedLocation(location.resource_name)}
                    >
                      <div className="flex items-start gap-3">
                        <input
                          type="radio"
                          checked={selectedLocation === location.resource_name}
                          onChange={() => setSelectedLocation(location.resource_name)}
                          className="mt-1"
                        />
                        <div className="flex-1">
                          <h4 className="font-heading font-bold text-charcoal">
                            {location.title}
                          </h4>
                          <p className="text-sm text-text-secondary mt-1">
                            {location.address || 'No address available'}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}

          <div className="flex gap-4">
            <button
              onClick={() => router.push('/onboarding')}
              className="flex-1 px-6 py-3 border-2 border-charcoal rounded-brutalist font-heading font-bold hover:bg-cream-dark transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSaveLocation}
              disabled={!selectedLocation}
              className="flex-1 px-6 py-3 bg-orange-fire text-white border-2 border-charcoal rounded-brutalist font-heading font-bold hover:bg-orange-hover transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-brutalist-sm"
            >
              Connect This Location
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function GoogleOAuthCallback() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-orange-fire border-t-transparent mb-4"></div>
          <h2 className="font-heading text-2xl font-bold text-charcoal">
            Loading OAuth callback...
          </h2>
        </div>
      </div>
    }>
      <GoogleOAuthCallbackContent />
    </Suspense>
  );
}
