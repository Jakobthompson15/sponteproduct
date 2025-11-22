'use client';

import { useUser } from '@clerk/nextjs';
import { useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function TestOAuthPage() {
  const { isLoaded, isSignedIn, user } = useUser();
  const [locationId, setLocationId] = useState('cbf5f016-fcb8-4245-a32f-0156ac615177');

  const handleConnectOAuth = async () => {
    if (!isSignedIn) {
      alert('Please sign in first!');
      return;
    }

    try {
      // Get Clerk session token
      const token = await (window as any).Clerk.session.getToken();

      // Make authenticated request to OAuth connect endpoint
      const response = await fetch(`${API_URL}/api/oauth/google/connect?location_id=${locationId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        redirect: 'manual' // Don't follow redirect automatically
      });

      // The backend will return a 307 redirect to Google OAuth
      // We need to get the redirect URL and navigate to it
      const redirectUrl = response.headers.get('Location');

      if (redirectUrl) {
        window.location.href = redirectUrl;
      } else {
        alert('No redirect URL received');
      }
    } catch (error) {
      console.error('OAuth error:', error);
      alert('Failed to initiate OAuth: ' + error);
    }
  };

  if (!isLoaded) {
    return <div className="p-8">Loading...</div>;
  }

  if (!isSignedIn) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Test OAuth Flow</h1>
        <p className="text-red-600">Please sign in first to test OAuth!</p>
        <a href="/" className="text-blue-600 underline">Go to sign in</a>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Test Google OAuth Connection</h1>

      <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-6">
        <p className="mb-2">
          <strong>Signed in as:</strong> {user.primaryEmailAddress?.emailAddress}
        </p>
        <p className="text-sm text-gray-600">
          Clerk User ID: {user.id}
        </p>
      </div>

      <div className="mb-6">
        <label className="block mb-2 font-medium">
          Location ID to connect:
        </label>
        <input
          type="text"
          value={locationId}
          onChange={(e) => setLocationId(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded"
          placeholder="Enter location UUID"
        />
        <p className="text-sm text-gray-500 mt-1">
          Default: cbf5f016-fcb8-4245-a32f-0156ac615177 (jakobnthompson@gmail.com's location)
        </p>
      </div>

      <button
        onClick={handleConnectOAuth}
        className="bg-blue-600 text-white px-6 py-3 rounded font-medium hover:bg-blue-700"
      >
        Connect Google Business Profile
      </button>

      <div className="mt-8 p-4 bg-gray-50 rounded">
        <h2 className="font-bold mb-2">How this works:</h2>
        <ol className="list-decimal list-inside space-y-1 text-sm">
          <li>You're signed in via Clerk</li>
          <li>Click the button to start OAuth</li>
          <li>We fetch your Clerk JWT token</li>
          <li>We send it to the backend with the OAuth request</li>
          <li>Backend redirects you to Google for authorization</li>
          <li>After authorizing, you'll see your GBP locations to select</li>
        </ol>
      </div>
    </div>
  );
}
