'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { gsap } from 'gsap';
import { industries } from '@/data/industryKeywords';

export default function IndustryCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const isTransitioningRef = useRef(false);

  const currentIndustry = industries[currentIndex];

  const nextIndustry = useCallback(() => {
    if (isTransitioningRef.current) return;

    isTransitioningRef.current = true;
    setIsTransitioning(true);

    // Kill any existing animations to prevent overlaps
    gsap.killTweensOf('.keyword-item');
    gsap.killTweensOf('.industry-name');

    // Slide out current keywords
    const slideOutTimeline = gsap.timeline({
      onComplete: () => {
        // Update to next industry
        setCurrentIndex((prevIndex) => (prevIndex + 1) % industries.length);

        // Wait a frame for React to re-render with new content
        requestAnimationFrame(() => {
          // Slide in new keywords
          gsap.fromTo(
            '.keyword-item',
            { x: 100, opacity: 0 },
            {
              x: 0,
              opacity: 1,
              duration: 0.5,
              stagger: 0.1,
              ease: 'power2.out',
              delay: 0.1,
              onComplete: () => {
                isTransitioningRef.current = false;
                setIsTransitioning(false);
              }
            }
          );
        });
      }
    });

    slideOutTimeline.to('.keyword-item', {
      x: -100,
      opacity: 0,
      duration: 0.4,
      stagger: 0.05,
      ease: 'power2.in'
    });

    // Fade out/in industry name
    slideOutTimeline.to('.industry-name', {
      opacity: 0,
      y: -10,
      duration: 0.3,
      ease: 'power2.in'
    }, 0); // Start at the same time as keyword slide out

    slideOutTimeline.add(() => {
      gsap.fromTo(
        '.industry-name',
        { opacity: 0, y: 10 },
        { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' }
      );
    }, '+=0.2'); // After keywords slide out
  }, []);

  // Auto-rotation effect
  useEffect(() => {
    const intervalId = setInterval(() => {
      nextIndustry();
    }, 3000); // 3 seconds per industry

    return () => {
      clearInterval(intervalId);
    };
  }, [nextIndustry]);

  return (
    <div className="relative h-[400px] lg:h-[600px]">
      <div
        ref={containerRef}
        className="relative w-full h-full bg-white rounded-3xl border-3 border-charcoal shadow-[12px_12px_0_var(--charcoal)] overflow-hidden p-lg"
      >
        {/* Browser Chrome Dots */}
        <div className="flex gap-2 mb-md">
          <div className="w-3 h-3 rounded-full border-2 border-charcoal bg-accent-red"></div>
          <div className="w-3 h-3 rounded-full border-2 border-charcoal bg-accent-yellow"></div>
          <div className="w-3 h-3 rounded-full border-2 border-charcoal bg-sage-green"></div>
        </div>

        {/* Industry Name Label */}
        <div className="mb-sm">
          <span className="industry-name inline-block px-4 py-2 bg-charcoal text-white font-mono text-xs font-bold rounded-lg uppercase tracking-wider">
            {currentIndustry.name}
          </span>
        </div>

        {/* Keywords List */}
        <div className="mt-md space-y-sm">
          {currentIndustry.keywords.map((item, i) => (
            <div
              key={`${currentIndex}-${i}`}
              className="keyword-item flex items-center justify-between p-sm bg-cream border-2 border-charcoal rounded-lg"
            >
              <span className="font-mono font-bold text-lg text-sage-green">
                {item.pos}
              </span>
              <span className="flex-1 font-semibold text-charcoal mx-sm">
                {item.keyword}
              </span>
              <span className="bg-sage-green text-white px-3 py-1 rounded-full text-xs font-bold font-mono">
                ↑ LIVE
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
