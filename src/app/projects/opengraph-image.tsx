import { NAME } from "@/data/content";
import { OG_SIZE, ogCard } from "@/lib/og";

export const alt = `Open-source projects by ${NAME}`;
export const size = OG_SIZE;
export const contentType = "image/png";

export default function Image() {
  return ogCard({
    kicker: ">> Section 04 // software",
    title: "Projects",
    subtitle: NAME,
  });
}

export const dynamic = "force-static";
