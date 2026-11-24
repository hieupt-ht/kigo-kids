import { Series } from "remotion";
import { Fight, Flood, Gifts, Intro, King, Race, Recap, Suitors } from "./Scenes";

export const SCENES = [
  { name: "Intro", frames: 300, C: Intro },
  { name: "King", frames: 420, C: King },
  { name: "Suitors", frames: 540, C: Suitors },
  { name: "Gifts", frames: 600, C: Gifts },
  { name: "Race", frames: 420, C: Race },
  { name: "Flood", frames: 480, C: Flood },
  { name: "Fight", frames: 480, C: Fight },
  { name: "Recap", frames: 660, C: Recap },
] as const;

export const TOTAL = SCENES.reduce((n, s) => n + s.frames, 0);

export const SonTinhThuyTinh: React.FC = () => (
  <Series>
    {SCENES.map(({ name, frames, C }) => (
      <Series.Sequence key={name} name={name} durationInFrames={frames}>
        <C />
      </Series.Sequence>
    ))}
  </Series>
);
