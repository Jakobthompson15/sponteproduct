'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@clerk/nextjs';
import { toast } from 'react-hot-toast';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function TestGBPOAuth() {
  const { getToken, isLoaded, isSignedIn } = useAuth();
  const [locationId, setLocationId] = useState<string>('');
  const [connectionStatus, setConnectionStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Example location ID - you'll need to get this from your database
  const EXAMPLE_LOCATION_ID = 'YOUR_LOCATION_ID_HERE';

  useEffect(() => {
    // Try to get location ID from localStorage (if saved from onboarding)
    const savedLocationId = localStorage.getItem('test_location_id');
    if (savedLocationId) {
      setLocationId(savedLocationId);
    }
  }, []);

  const checkConnectionStatus = async () => {
    if (!locationId) {
      toast.error('Please enter a location ID');
      return;
    }

    setLoading(true);
    try {
      const token = await getToken();
      const response = await fetch(`${API_URL}/api/oauth/google/status/${locationId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to check status');
      }

      const data = await response.json();
      setConnectionStatus(data);
      toast.success('Status checked successfully');
    } catch (error) {
      console.error('Error checking status:', error);
      toast.error('Failed to check connection status');
    } finally {
      setLoading(false);
    }
  };

  const startOAuthFlow = () => {
    if (!locationId) {
      toast.error('Please enter a location ID');
      return;
    }

    // Save location ID for later
    localStorage.setItem('test_location_id', locationId);

    // Start OAuth flow
    window.location.href = `${API_URL}/api/oauth/google/connect?location_id=${locationId}`;
  };

  const disconnectGoogle = async () => {
    if (!locationId) {
      toast.error('Please enter a location ID');
      return;
    }

    setLoading(true);
    try {
      const token = await getToken();
      const response = await fetch(`${API_URL}/api/oauth/google/disconnect/${locationId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to disconnect');
      }

      toast.success('Disconnected successfully');
      setConnectionStatus(null);
    } catch (error) {
      console.error('Error disconnecting:', error);
      toast.error('Failed to disconnect');
    } finally {
      setLoading(false);
    }
  };

  const testCreatePost = async () => {
    if (!locationId) {
      toast.error('Please enter a location ID');
      return;
    }

    setLoading(true);
    try {
      const token = await getToken();

      // Create a test task
      const response = await fetch(`${API_URL}/api/agents/gbp/tasks`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          location_id: locationId,
          context: 'Test post from OAuth debugging'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create task');
      }

      const task = await response.json();
      toast.success(`Task created: ${task.id}`);

      // Process the task
      const processResponse = await fetch(`${API_URL}/api/agents/gbp/tasks/${task.id}/process`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!processResponse.ok) {
        throw new Error('Failed to process task');
      }

      const output = await processResponse.json();
      toast.success('Post generated successfully!');
      console.log('Generated post:', output);
    } catch (error) {
      console.error('Error creating post:', error);
      toast.error('Failed to create test post');
    } finally {
      setLoading(false);
    }
  };

  if (!isLoaded || !isSignedIn) {
    return (
      <div className="min-h-screen bg-cream flex items-center justify-center">
        <div className="text-center">
          <h2 className="font-heading text-2xl font-bold text-charcoal">
            Please sign in to test GBP OAuth
          </h2>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cream py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white border-3 border-charcoal rounded-brutalist-lg p-8 shadow-brutalist mb-8">
          <h1 className="font-heading text-3xl font-bold text-charcoal mb-2">
            GBP OAuth Test Page
          </h1>
          <p className="text-text-secondary mb-8">
            Debug and test your Google Business Profile OAuth integration
          </p>

          {/* Location ID Input */}
          <div className="mb-8">
            <label className="block font-heading font-bold text-charcoal mb-2">
              Location ID
            </label>
            <input
              type="text"
              value={locationId}
              onChange={(e) => setLocationId(e.target.value)}
              placeholder="Enter your location UUID (e.g., 123e4567-e89b-12d3-a456-426614174000)"
              className="w-full px-4 py-3 border-2 border-charcoal rounded-brutalist focus:border-orange-fire focus:outline-none"
            />
            <p className="text-sm text-text-muted mt-2">
              You can find this in your database or from the onboarding response
            </p>
          </div>

          {/* Action Buttons */}
          <div className="grid grid-cols-2 gap-4 mb-8">
            <button
              onClick={checkConnectionStatus}
              disabled={loading || !locationId}
              className="px-6 py-3 border-2 border-charcoal rounded-brutalist font-heading font-bold hover:bg-cream-dark transition-colors disabled:opacity-50"
            >
              Check Connection Status
            </button>

            <button
              onClick={startOAuthFlow}
              disabled={loading || !locationId}
              className="px-6 py-3 bg-orange-fire text-white border-2 border-charcoal rounded-brutalist font-heading font-bold hover:bg-orange-hover transition-colors disabled:opacity-50 shadow-brutalist-sm"
            >
              Connect Google Business Profile
            </button>

            <button
              onClick={disconnectGoogle}
              disabled={loading || !locationId || !connectionStatus?.connected}
              className="px-6 py-3 border-2 border-red-500 text-red-500 rounded-brutalist font-heading font-bold hover:bg-red-50 transition-colors disabled:opacity-50"
            >
              Disconnect
            </button>

            <button
              onClick={testCreatePost}
              disabled={loading || !locationId || !connectionStatus?.connected}
              className="px-6 py-3 bg-green-500 text-white border-2 border-charcoal rounded-brutalist font-heading font-bold hover:bg-green-600 transition-colors disabled:opacity-50 shadow-brutalist-sm"
            >
              Test Create Post
            </button>
          </div>

          {/* Connection Status */}
          {connectionStatus && (
            <div className="bg-cream border-2 border-charcoal rounded-brutalist p-6">
              <h3 className="font-heading font-bold text-xl mb-4">Connection Status</h3>
              <div className="space-y-2">
                <p>
                  <span className="font-bold">Connected:</span>{' '}
                  <span className={connectionStatus.connected ? 'text-green-600' : 'text-red-600'}>
                    {connectionStatus.connected ? '✅ Yes' : '❌ No'}
                  </span>
                </p>
                {connectionStatus.email && (
                  <p>
                    <span className="font-bold">Email:</span> {connectionStatus.email}
                  </p>
                )}
                {connectionStatus.accounts_count !== undefined && (
                  <p>
                    <span className="font-bold">GBP Accounts:</span> {connectionStatus.accounts_count}
                  </p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="bg-white border-3 border-charcoal rounded-brutalist-lg p-8 shadow-brutalist">
          <h2 className="font-heading text-2xl font-bold text-charcoal mb-4">
            How to Use This Test Page
          </h2>
          <ol className="list-decimal list-inside space-y-3 text-text-secondary">
            <li>Get a location ID from your database (check the locations table in Supabase)</li>
            <li>Enter the location ID in the input field above</li>
            <li>Click "Check Connection Status" to see if Google is already connected</li>
            <li>If not connected, click "Connect Google Business Profile" to start OAuth flow</li>
            <li>After connecting, you can test creating a post with "Test Create Post"</li>
          </ol>

          <div className="mt-6 p-4 bg-yellow-50 border-2 border-yellow-400 rounded-brutalist">
            <h3 className="font-heading font-bold text-charcoal mb-2">⚠️ Important Notes:</h3>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Make sure your backend is running on http://localhost:8000</li>
              <li>Frontend should be on http://localhost:3001</li>
              <li>Google OAuth redirect URI must be: http://localhost:8000/api/oauth/google/callback</li>
              <li>Check Google Cloud Console that your OAuth app is configured correctly</li>
              <li>The app needs these scopes: business.manage, userinfo.email, userinfo.profile</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}