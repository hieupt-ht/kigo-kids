import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Kigo } from "./Kigo";

export const FONT = '"Segoe UI", Arial, sans-serif';

export const Pop: React.FC<{ at: number; children: React.ReactNode; style?: React.CSSProperties }> = ({
  at,
  children,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - at, fps, config: { damping: 12 } });
  return <div style={{ transform: `scale(${s})`, opacity: Math.min(1, s * 2), ...style }}>{children}</div>;
};

export const WordCard: React.FC<{ emoji: string; en: string; vi: string; at: number }> = ({ emoji, en, vi, at }) => (
  <Pop at={at} style={{ background: "#fff", borderRadius: 36, padding: "20px 32px", textAlign: "center",
    boxShadow: "0 10px 0 rgba(0,0,0,.15)", minWidth: 230 }}>
    <div style={{ fontSize: 110, lineHeight: 1.1 }}>{emoji}</div>
    <div style={{ fontSize: 60, fontWeight: 800, color: "#d9480f", fontFamily: FONT }}>{en}</div>
    <div style={{ fontSize: 34, color: "#555", fontFamily: FONT }}>{vi}</div>
  </Pop>
);

export const Caption: React.FC<{ vi: string; en: string }> = ({ vi, en }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 60, right: 60, bottom: 40, background: "rgba(255,255,255,.93)",
      borderRadius: 32, padding: "24px 44px", opacity: o, fontFamily: FONT, boxShadow: "0 8px 0 rgba(0,0,0,.15)" }}>
      <div style={{ fontSize: 44, fontWeight: 700, color: "#1f2d3d", lineHeight: 1.3 }}>{vi}</div>
      <div style={{ fontSize: 40, fontWeight: 600, color: "#d9480f", marginTop: 6 }}>{en}</div>
    </div>
  );
};

export const KigoCorner: React.FC<{ happy?: boolean }> = ({ happy = true }) => (
  <div style={{ position: "absolute", right: 50, top: 30 }}>
    <Kigo size={230} happy={happy} />
  </div>
);

export const Sky: React.FC<{ colors: [string, string]; children?: React.ReactNode }> = ({ colors, children }) => (
  <div style={{ position: "absolute", inset: 0, background: `linear-gradient(${colors[0]}, ${colors[1]})`, overflow: "hidden" }}>
    {children}
  </div>
);

export const Mountain: React.FC<{ x: number; base: number; w: number; h: number; color?: string }> = ({
  x, base, w, h, color = "#5b8c5a",
}) => (
  <svg style={{ position: "absolute", left: x - w / 2, top: base - h }} width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
    <polygon points={`0,${h} ${w / 2},0 ${w},${h}`} fill={color} />
    <polygon points={`${w / 2},0 ${w / 2 - w * 0.12},${h * 0.25} ${w / 2 + w * 0.12},${h * 0.25}`} fill="#fff" />
  </svg>
);

export const Water: React.FC<{ level: number }> = ({ level }) => {
  const frame = useCurrentFrame();
  const wave = Math.sin(frame / 6) * 12;
  return (
    <div style={{ position: "absolute", left: -20, right: -20, bottom: 0, height: level, background: "#2f80ed",
      opacity: 0.85, transform: `translateY(${wave}px)`, borderTop: "10px solid #7fb5ff" }} />
  );
};
