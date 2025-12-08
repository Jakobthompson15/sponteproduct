#!/bin/bash

# Add environment variables to Vercel
echo "Adding environment variables to Vercel..."

# Add each variable for production, preview, and development
echo "pk_test_aW1tdW5lLXN1bmZpc2gtNTUuY2xlcmsuYWNjb3VudHMuZGV2JA" | vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY production --yes
echo "pk_test_aW1tdW5lLXN1bmZpc2gtNTUuY2xlcmsuYWNjb3VudHMuZGV2JA" | vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY preview --yes
echo "pk_test_aW1tdW5lLXN1bmZpc2gtNTUuY2xlcmsuYWNjb3VudHMuZGV2JA" | vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY development --yes

echo "sk_test_PElmNRoWmsJZUlZILClOgRhJAHMD9EfQjapmqZUliX" | vercel env add CLERK_SECRET_KEY production --yes
echo "sk_test_PElmNRoWmsJZUlZILClOgRhJAHMD9EfQjapmqZUliX" | vercel env add CLERK_SECRET_KEY preview --yes
echo "sk_test_PElmNRoWmsJZUlZILClOgRhJAHMD9EfQjapmqZUliX" | vercel env add CLERK_SECRET_KEY development --yes

echo "http://localhost:8000" | vercel env add NEXT_PUBLIC_API_URL production --yes
echo "http://localhost:8000" | vercel env add NEXT_PUBLIC_API_URL preview --yes
echo "http://localhost:8000" | vercel env add NEXT_PUBLIC_API_URL development --yes

echo "/sign-in" | vercel env add NEXT_PUBLIC_CLERK_SIGN_IN_URL production --yes
echo "/sign-in" | vercel env add NEXT_PUBLIC_CLERK_SIGN_IN_URL preview --yes
echo "/sign-in" | vercel env add NEXT_PUBLIC_CLERK_SIGN_IN_URL development --yes

echo "/sign-up" | vercel env add NEXT_PUBLIC_CLERK_SIGN_UP_URL production --yes
echo "/sign-up" | vercel env add NEXT_PUBLIC_CLERK_SIGN_UP_URL preview --yes
echo "/sign-up" | vercel env add NEXT_PUBLIC_CLERK_SIGN_UP_URL development --yes

echo "/dashboard" | vercel env add NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL production --yes
echo "/dashboard" | vercel env add NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL preview --yes
echo "/dashboard" | vercel env add NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL development --yes

echo "/onboarding" | vercel env add NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL production --yes
echo "/onboarding" | vercel env add NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL preview --yes
echo "/onboarding" | vercel env add NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL development --yes

echo "Environment variables added successfully!"
echo "Now redeploying..."
vercel --prod --yes