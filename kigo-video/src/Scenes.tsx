import { interpolate, useCurrentFrame } from "remotion";
import { Kigo } from "./Kigo";
import { Caption, FONT, KigoCorner, Mountain, Pop, Sky, Water, WordCard } from "./ui";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const Row: React.FC<{ children: React.ReactNode; top?: number; zoom?: number }> = ({ children, top = 330, zoom = 1 }) => (
  <div style={{ position: "absolute", left: 0, right: 0, top, display: "flex", gap: 36, justifyContent: "center", zoom }}>
    {children}
  </div>
);

export const Intro: React.FC = () => (
  <Sky colors={["#ffe9b0", "#ffd6a5"]}>
    <Mountain x={420} base={760} w={700} h={420} color="#7fb069" />
    <Mountain x={1450} base={760} w={800} h={500} color="#5b8c5a" />
    <div style={{ position: "absolute", left: 0, right: 0, top: 120, textAlign: "center", fontFamily: FONT }}>
      <Pop at={10}>
        <div style={{ fontSize: 120, fontWeight: 900, color: "#c2410c" }}>Sơn Tinh – Thủy Tinh</div>
      </Pop>
      <Pop at={30}>
        <div style={{ fontSize: 56, fontWeight: 700, color: "#1f2d3d" }}>
          Truyền thuyết Việt Nam • Learn English with Kigo
        </div>
      </Pop>
    </div>
    <div style={{ position: "absolute", left: 800, top: 420 }}>
      <Pop at={20}>
        <Kigo size={340} />
      </Pop>
    </div>
    <Caption
      vi="Xin chào! Mình là Kigo. Hôm nay mình kể một truyền thuyết Việt Nam và học tiếng Anh nhé!"
      en="Hello! I'm Kigo. Let's learn English with a story!"
    />
  </Sky>
);

export const King: React.FC = () => (
  <Sky colors={["#fff3bf", "#ffe3a0"]}>
    <KigoCorner />
    <Row top={200}>
      <WordCard emoji="👑" en="king" vi="vua" at={20} />
      <WordCard emoji="👸" en="princess" vi="công chúa" at={110} />
      <WordCard emoji="👧" en="daughter" vi="con gái" at={200} />
    </Row>
    <Caption
      vi="Ngày xưa, vua Hùng thứ 18 có một cô con gái xinh đẹp, hiền dịu tên là Mỵ Nương."
      en="A long time ago, King Hung had a kind and beautiful daughter."
    />
  </Sky>
);

export const Suitors: React.FC = () => {
  const f = useCurrentFrame();
  const second = f >= 270;
  return (
    <Sky colors={second ? ["#cfe8ff", "#8ec5ff"] : ["#d8f5d0", "#b7e4a8"]}>
      <KigoCorner />
      {!second ? (
        <>
          <Mountain x={500} base={800} w={760} h={460} />
          <Pop at={10} style={{ position: "absolute", left: 100, top: 130, fontFamily: FONT }}>
            <div style={{ fontSize: 70, fontWeight: 900, color: "#2f6b2f" }}>Sơn Tinh – God of the Mountain</div>
          </Pop>
          <Row top={250}>
            <div style={{ width: 700 }} />
            <WordCard emoji="⛰️" en="mountain" vi="núi" at={60} />
            <WordCard emoji="🌳" en="hill" vi="đồi" at={140} />
          </Row>
        </>
      ) : (
        <>
          <Pop at={282} style={{ position: "absolute", left: 100, top: 130, fontFamily: FONT }}>
            <div style={{ fontSize: 70, fontWeight: 900, color: "#1d4ed8" }}>Thủy Tinh – God of the Water</div>
          </Pop>
          <Row top={260}>
            <WordCard emoji="🌊" en="water" vi="nước" at={320} />
            <WordCard emoji="💨" en="wind" vi="gió" at={380} />
            <WordCard emoji="🌧️" en="rain" vi="mưa" at={440} />
          </Row>
        </>
      )}
      <Caption
        vi={
          second
            ? "Thủy Tinh ở miền biển. Chàng gọi gió, gió đến. Chàng hô mưa, mưa về."
            : "Có hai chàng trai đến xin cưới công chúa. Sơn Tinh ở núi Tản Viên, vẫy tay là đồi núi mọc lên."
        }
        en={second ? "Thuy Tinh calls the wind. Thuy Tinh calls the rain!" : "Son Tinh lives on a mountain. He can make hills!"}
      />
    </Sky>
  );
};

export const Gifts: React.FC = () => (
  <Sky colors={["#ffe0e0", "#ffc9c9"]}>
    <KigoCorner />
    <div style={{ position: "absolute", left: 80, top: 70, width: 1350, fontFamily: FONT, fontSize: 56, fontWeight: 900, color: "#9c2f2f" }}>
      Vua nói: Ai mang lễ vật đến trước sẽ được cưới công chúa!
    </div>
    <Row top={290} zoom={0.78}>
      <WordCard emoji="🍚" en="sticky rice" vi="xôi nếp" at={40} />
      <WordCard emoji="🟩" en="chung cake" vi="bánh chưng" at={140} />
      <WordCard emoji="🐘" en="elephant" vi="voi (chín ngà)" at={240} />
      <WordCard emoji="🐓" en="rooster" vi="gà (chín cựa)" at={340} />
      <WordCard emoji="🐎" en="horse" vi="ngựa (chín hồng mao)" at={440} />
    </Row>
    <Caption
      vi="Lễ vật gồm: xôi nếp, bánh chưng, voi chín ngà, gà chín cựa và ngựa chín hồng mao."
      en="Bring the gifts first. The winner marries the princess!"
    />
  </Sky>
);

export const Race: React.FC = () => {
  const f = useCurrentFrame();
  const sonX = interpolate(f, [0, 150], [-300, 500], clamp);
  const thuyX = interpolate(f, [200, 330], [1900, 1150], clamp);
  return (
    <Sky colors={["#ffe8cc", "#ffd8a8"]}>
      <KigoCorner />
      <div style={{ position: "absolute", left: sonX, top: 420, fontSize: 200 }}>🏃‍♂️⛰️</div>
      <div style={{ position: "absolute", left: thuyX, top: 420, fontSize: 200 }}>{f > 330 ? "😡🌊" : "🚶🌊"}</div>
      <Pop at={140} style={{ position: "absolute", left: 330, top: 250, fontFamily: FONT, fontSize: 70, fontWeight: 900, color: "#2f6b2f" }}>
        FIRST! ⭐ đầu tiên
      </Pop>
      <Pop at={300} style={{ position: "absolute", left: 1050, top: 250, fontFamily: FONT, fontSize: 70, fontWeight: 900, color: "#b42318" }}>
        LATE… angry! 😠
      </Pop>
      <Caption
        vi="Sáng sớm hôm sau, Sơn Tinh mang đủ lễ vật đến trước và đón Mỵ Nương về núi. Thủy Tinh đến sau, nên rất tức giận."
        en="Son Tinh came first. Thuy Tinh came late, and he was angry!"
      />
    </Sky>
  );
};

export const Flood: React.FC = () => {
  const f = useCurrentFrame();
  const level = interpolate(f, [30, 420], [60, 520], clamp);
  return (
    <Sky colors={["#6b7a8f", "#3d4b61"]}>
      <Mountain x={460} base={860} w={640} h={380} color="#4a6b49" />
      <Mountain x={1400} base={860} w={700} h={420} color="#4a6b49" />
      <div style={{ position: "absolute", left: 0, right: 0, top: 60, textAlign: "center", fontSize: 130 }}>
        {"🌧️ ".repeat(3)}
        {f % 30 < 15 ? "⚡" : "💨"}
      </div>
      <Water level={level} />
      <KigoCorner happy={false} />
      <Caption
        vi="Thủy Tinh hô mưa, gọi gió. Nước sông dâng cuồn cuộn, ngập ruộng đồng và nhà cửa."
        en="Rain! Wind! The water goes up and up!"
      />
    </Sky>
  );
};

export const Fight: React.FC = () => {
  const f = useCurrentFrame();
  const water = interpolate(f, [0, 200, 400, 470], [200, 520, 540, 120], clamp);
  const hill = interpolate(f, [0, 200], [380, 720], clamp);
  return (
    <Sky colors={["#aed9ff", "#e8f4ff"]}>
      <Mountain x={800} base={900} w={760} h={hill} color="#4f7d4c" />
      <Mountain x={1450} base={900} w={620} h={hill - 160} color="#5b8c5a" />
      <Water level={water} />
      <Pop at={30} style={{ position: "absolute", left: 90, top: 70, fontFamily: FONT, fontSize: 64, fontWeight: 900, color: "#1d4ed8" }}>
        Nước lên 🌊⬆️ — Núi cũng lên ⛰️⬆️
      </Pop>
      {f > 380 && (
        <Pop at={380} style={{ position: "absolute", left: 90, top: 160, fontFamily: FONT, fontSize: 64, fontWeight: 900, color: "#2f6b2f" }}>
          Thủy Tinh hết sức, rút quân! 🎉
        </Pop>
      )}
      <KigoCorner />
      <Caption
        vi="Sơn Tinh dời từng quả đồi, dựng thành lũy đất. Nước dâng cao bao nhiêu, núi cao lên bấy nhiêu. Mấy tháng sau, Thủy Tinh hết sức và phải rút quân."
        en="The water goes up. The mountain goes up too! Thuy Tinh is tired."
      />
    </Sky>
  );
};

const RECAP: [string, string, string][] = [
  ["👑", "king", "vua"],
  ["👸", "princess", "công chúa"],
  ["⛰️", "mountain", "núi"],
  ["🌊", "water", "nước"],
  ["🌧️", "rain", "mưa"],
  ["💨", "wind", "gió"],
];

export const Recap: React.FC = () => (
  <Sky colors={["#ffe9b0", "#ffd6a5"]}>
    <div style={{ position: "absolute", left: 0, right: 0, top: 40, textAlign: "center", fontFamily: FONT, fontSize: 68, fontWeight: 900, color: "#c2410c" }}>
      Words today – Từ vựng hôm nay
    </div>
    <div style={{ position: "absolute", left: 0, right: 0, top: 160, display: "flex", flexWrap: "wrap", gap: 28, justifyContent: "center", padding: "0 160px" }}>
      {RECAP.map(([e, en, vi], i) => (
        <WordCard key={en} emoji={e} en={en} vi={vi} at={20 + i * 30} />
      ))}
    </div>
    <div style={{ position: "absolute", left: 60, top: 560, fontFamily: FONT, fontSize: 30, color: "#374151", maxWidth: 1250 }}>
      Truyền thuyết kể lại theo bản trong SGK Ngữ văn 6 (Huỳnh Lý, NXB Giáo dục, 1994), qua Wikipedia tiếng Việt (CC BY-SA). Lời kể do Kigo viết lại.
    </div>
    <div style={{ position: "absolute", right: 40, top: 520 }}>
      <Pop at={60}>
        <Kigo size={280} />
      </Pop>
    </div>
    <Caption
      vi="Từ đó, năm nào Thủy Tinh cũng làm mưa gió đánh Sơn Tinh, nhưng lần nào cũng phải rút quân. Hẹn gặp lại!"
      en="Great job! See you next time. Bye bye!"
    />
  </Sky>
);
