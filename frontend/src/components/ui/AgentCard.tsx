interface AgentCardProps {
  badge: string;
  badgeColor: string;
  title: string;
  description: string;
  emoji: string;
  bgColor: string;
  textColor?: string;
}

export default function AgentCard({
  badge,
  badgeColor,
  title,
  description,
  emoji,
  bgColor,
  textColor = 'text-charcoal'
}: AgentCardProps) {
  return (
    <div
      className={`${bgColor} ${textColor} border-3 border-charcoal rounded-[24px] p-xl shadow-brutalist relative overflow-hidden w-full h-full flex flex-col`}
    >
      {/* Emoji Background */}
      <div className="absolute -right-6 -top-6 text-[140px] opacity-10 pointer-events-none">
        {emoji}
      </div>

      {/* Badge */}
      <span
        className={`inline-block self-start px-4 py-3 ${badgeColor} text-white font-mono text-sm font-bold border-3 border-charcoal rounded-lg mb-md z-10`}
      >
        {badge}
      </span>

      {/* Title */}
      <h3 className="font-heading text-3xl font-extrabold mb-sm tracking-tight z-10">
        {title}
      </h3>

      {/* Description */}
      <p className={`leading-relaxed text-lg flex-1 z-10 ${textColor === 'text-white' ? 'text-white/90' : 'opacity-90'}`}>
        {description}
      </p>

      {/* Decorative corner accent */}
      <div className={`absolute bottom-0 right-0 w-16 h-16 ${badgeColor} opacity-20 rounded-tl-full`}></div>
    </div>
  );
}
