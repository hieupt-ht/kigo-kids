import { Audio, Sequence, Series, staticFile } from "remotion";
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

// [global start frame, file in public/voice] — Windows "Zira" voice, English only (demo)
const VOICE: [number, string][] = [
  [20, "intro"], [310, "king_s"], [480, "king"], [560, "princess"], [640, "daughter"],
  [730, "suitor_s"], [900, "mountain"], [950, "hill"],
];

export const SonTinhThuyTinh: React.FC = () => (
  <>
    {VOICE.map(([from, file]) => (
      <Sequence key={file} from={from} name={`voice-${file}`}>
        <Audio src={staticFile(`voice/${file}.wav`)} />
      </Sequence>
    ))}
    <Series>
    {SCENES.map(({ name, frames, C }) => (
      <Series.Sequence key={name} name={name} durationInFrames={frames}>
        <C />
      </Series.Sequence>
    ))}
    </Series>
  </>
);
