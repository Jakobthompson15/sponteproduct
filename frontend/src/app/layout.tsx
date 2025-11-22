import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import { Toaster } from "react-hot-toast";
import { DM_Serif_Display, Manrope, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const dmSerifDisplay = DM_Serif_Display({
  weight: ['400'],
  style: ['normal', 'italic'],
  subsets: ['latin'],
  variable: '--font-display',
});

const manrope = Manrope({
  weight: ['400', '500', '600', '700', '800'],
  subsets: ['latin'],
  variable: '--font-heading',
});

const inter = Inter({
  weight: ['400', '500', '600', '700'],
  subsets: ['latin'],
  variable: '--font-body',
});

const jetBrainsMono = JetBrains_Mono({
  weight: ['500', '700'],
  subsets: ['latin'],
  variable: '--font-mono',
});

export const metadata: Metadata = {
  title: "Sponte AI - Autonomous Local SEO",
  description: "AI agents that manage your local SEO automatically",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en" className={`${dmSerifDisplay.variable} ${manrope.variable} ${inter.variable} ${jetBrainsMono.variable}`}>
        <body className="antialiased">
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              // Brutalist toast styling
              style: {
                border: '2px solid #1A1D2E',
                padding: '16px',
                color: '#1A1D2E',
                fontFamily: 'Manrope, system-ui, sans-serif',
                fontWeight: 600,
              },
              success: {
                iconTheme: {
                  primary: '#10B981',
                  secondary: 'white',
                },
                style: {
                  background: '#FFFBF5',
                  border: '2px solid #10B981',
                },
              },
              error: {
                iconTheme: {
                  primary: '#EF4444',
                  secondary: 'white',
                },
                style: {
                  background: '#FFFBF5',
                  border: '2px solid #EF4444',
                },
              },
            }}
          />
        </body>
      </html>
    </ClerkProvider>
  );
}
