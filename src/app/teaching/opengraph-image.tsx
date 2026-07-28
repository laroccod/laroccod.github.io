import { NAME } from "@/data/content";
import { OG_SIZE, ogCard } from "@/lib/og";

export const alt = `Teaching experience of ${NAME}`;
export const size = OG_SIZE;
export const contentType = "image/png";

export default function Image() {
  return ogCard({
    kicker: ">> Section 03 // instruction",
    title: "Teaching",
    subtitle: NAME,
  });
}

export const dynamic = "force-static";
