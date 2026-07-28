import { NAME } from "@/data/content";
import { OG_SIZE, ogCard } from "@/lib/og";

export const alt = `Contact ${NAME}`;
export const size = OG_SIZE;
export const contentType = "image/png";

export default function Image() {
  return ogCard({
    kicker: ">> Section 05 // transmission",
    title: "Contact",
    subtitle: NAME,
  });
}

export const dynamic = "force-static";
