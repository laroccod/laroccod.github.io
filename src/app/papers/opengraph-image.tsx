import { NAME } from "@/data/content";
import { OG_SIZE, ogCard } from "@/lib/og";

export const alt = `Research by ${NAME}: papers and talks`;
export const size = OG_SIZE;
export const contentType = "image/png";

export default function Image() {
  return ogCard({
    kicker: ">> Section 02 // papers & talks",
    title: "Research",
    subtitle: NAME,
  });
}

export const dynamic = "force-static";
