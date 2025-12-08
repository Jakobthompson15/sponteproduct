export default function Loading() {
  return (
    <div className="min-h-screen bg-cream flex items-center justify-center">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-orange-fire border-t-transparent mb-4"></div>
        <h2 className="font-heading text-2xl font-bold text-charcoal">
          Processing OAuth callback...
        </h2>
      </div>
    </div>
  );
}