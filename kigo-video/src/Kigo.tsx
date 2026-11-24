import { interpolate, useCurrentFrame } from "remotion";

export const Kigo: React.FC<{ size?: number; happy?: boolean }> = ({
  size = 260,
  happy = true,
}) => {
  const frame = useCurrentFrame();
  const bob = Math.sin(frame / 8) * 6;
  const blink = frame % 90 > 84 ? 0.1 : 1;
  const tail = Math.sin(frame / 3) * 14;
  return (
    <svg width={size} height={size} viewBox="0 0 200 200" style={{ transform: `translateY(${bob}px)` }}>
      <g transform={`rotate(${tail} 160 150)`}>
        <ellipse cx="165" cy="140" rx="16" ry="9" fill="#E8A04A" />
      </g>
      <ellipse cx="100" cy="150" rx="55" ry="38" fill="#E8A04A" />
      <ellipse cx="100" cy="162" rx="30" ry="24" fill="#FFF4E0" />
      <polygon points="45,70 55,15 90,50" fill="#E8A04A" />
      <polygon points="155,70 145,15 110,50" fill="#E8A04A" />
      <polygon points="55,62 60,32 80,52" fill="#F7C9A0" />
      <polygon points="145,62 140,32 120,52" fill="#F7C9A0" />
      <circle cx="100" cy="85" r="58" fill="#E8A04A" />
      <ellipse cx="100" cy="102" rx="38" ry="32" fill="#FFF4E0" />
      <ellipse cx="78" cy="78" rx="8" ry={9 * blink} fill="#2b1d12" />
      <ellipse cx="122" cy="78" rx="8" ry={9 * blink} fill="#2b1d12" />
      <circle cx="80" cy="75" r="2.5" fill="#fff" />
      <circle cx="124" cy="75" r="2.5" fill="#fff" />
      <ellipse cx="100" cy="94" rx="9" ry="6.5" fill="#2b1d12" />
      {happy ? (
        <>
          <path d="M84 106 Q100 124 116 106" stroke="#2b1d12" strokeWidth="3" fill="none" />
          <path d="M94 113 Q100 128 106 113 Z" fill="#F0707A" />
        </>
      ) : (
        <path d="M86 112 Q100 104 114 112" stroke="#2b1d12" strokeWidth="3" fill="none" />
      )}
    </svg>
  );
};

export const useFadeIn = (start: number, dur = 15) =>
  interpolate(useCurrentFrame(), [start, start + dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
