import { Composition } from "remotion";
import { SonTinhThuyTinh } from "./Composition";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="SonTinhThuyTinh"
    component={SonTinhThuyTinh}
    durationInFrames={3900}
    fps={30}
    width={1920}
    height={1080}
  />
);
