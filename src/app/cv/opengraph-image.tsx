import { NAME } from "@/data/content";
import { OG_SIZE, ogCard } from "@/lib/og";

export const alt = `Curriculum vitae of ${NAME}`;
export const size = OG_SIZE;
export const contentType = "image/png";

export default function Image() {
  return ogCard({
    kicker: ">> Section 01 // curriculum vitae",
    title: "CV",
    subtitle: NAME,
  });
}

export const dynamic = "force-static";
