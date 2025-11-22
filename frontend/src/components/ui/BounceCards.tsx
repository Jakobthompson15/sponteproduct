'use client';

import { useEffect, ReactNode } from 'react';
import { gsap } from 'gsap';
import './BounceCards.css';

interface BounceCardsProps {
  className?: string;
  cards: ReactNode[];
  containerWidth?: number;
  containerHeight?: number;
  animationDelay?: number;
  animationStagger?: number;
  easeType?: string;
  transformStyles?: string[];
  enableHover?: boolean;
}

export default function BounceCards({
  className = '',
  cards = [],
  containerWidth = 1200,
  containerHeight = 500,
  animationDelay = 0.5,
  animationStagger = 0.08,
  easeType = 'elastic.out(1, 0.8)',
  transformStyles = [
    'rotate(16deg) translate(-480px)',
    'rotate(10deg) translate(-320px)',
    'rotate(5deg) translate(-160px)',
    'rotate(0deg)',
    'rotate(-5deg) translate(160px)',
    'rotate(-10deg) translate(320px)',
    'rotate(-16deg) translate(480px)'
  ],
  enableHover = true
}: BounceCardsProps) {
  useEffect(() => {
    gsap.fromTo(
      '.bounce-card',
      { scale: 0, opacity: 1 },
      {
        scale: 1,
        opacity: 1,
        stagger: animationStagger,
        ease: easeType,
        delay: animationDelay
      }
    );
  }, [animationStagger, easeType, animationDelay]);

  const getNoRotationTransform = (transformStr: string): string => {
    const hasRotate = /rotate\([\s\S]*?\)/.test(transformStr);
    if (hasRotate) {
      return transformStr.replace(/rotate\([\s\S]*?\)/, 'rotate(0deg)');
    } else if (transformStr === 'none') {
      return 'rotate(0deg)';
    } else {
      return `${transformStr} rotate(0deg)`;
    }
  };

  const getPushedTransform = (baseTransform: string, offsetX: number): string => {
    const translateRegex = /translate\(([-0-9.]+)px\)/;
    const match = baseTransform.match(translateRegex);
    if (match) {
      const currentX = parseFloat(match[1]);
      const newX = currentX + offsetX;
      return baseTransform.replace(translateRegex, `translate(${newX}px)`);
    } else {
      return baseTransform === 'none' ? `translate(${offsetX}px)` : `${baseTransform} translate(${offsetX}px)`;
    }
  };

  const pushSiblings = (hoveredIdx: number) => {
    if (!enableHover) return;

    cards.forEach((_, i) => {
      gsap.killTweensOf(`.bounce-card-${i}`);

      const baseTransform = transformStyles[i] || 'none';

      if (i === hoveredIdx) {
        const noRotation = getNoRotationTransform(baseTransform);
        gsap.to(`.bounce-card-${i}`, {
          transform: noRotation,
          duration: 0.5,
          ease: 'back.out(1.7)',
          overwrite: 'auto',
          scale: 1.05,
          zIndex: 100
        });
      } else {
        const offsetX = i < hoveredIdx ? -200 : 200;
        const pushedTransform = getPushedTransform(baseTransform, offsetX);

        const distance = Math.abs(hoveredIdx - i);
        const delay = distance * 0.06;

        gsap.to(`.bounce-card-${i}`, {
          transform: pushedTransform,
          duration: 0.5,
          ease: 'back.out(1.7)',
          delay,
          overwrite: 'auto',
          scale: 0.95,
          opacity: 0.7
        });
      }
    });
  };

  const resetSiblings = () => {
    if (!enableHover) return;

    cards.forEach((_, i) => {
      gsap.killTweensOf(`.bounce-card-${i}`);
      const baseTransform = transformStyles[i] || 'none';
      gsap.to(`.bounce-card-${i}`, {
        transform: baseTransform,
        duration: 0.4,
        ease: 'power2.out',
        overwrite: true,
        scale: 1,
        opacity: 1,
        zIndex: i
      });
    });
  };

  return (
    <div
      className={`bounceCardsContainer ${className}`}
      style={{
        position: 'relative',
        width: containerWidth,
        height: containerHeight,
        margin: '0 auto'
      }}
    >
      {cards.map((card, idx) => (
        <div
          key={idx}
          className={`bounce-card bounce-card-${idx}`}
          style={{
            transform: transformStyles[idx] ?? 'none',
            zIndex: idx
          }}
          onMouseEnter={() => pushSiblings(idx)}
          onMouseLeave={resetSiblings}
        >
          {card}
        </div>
      ))}
    </div>
  );
}
