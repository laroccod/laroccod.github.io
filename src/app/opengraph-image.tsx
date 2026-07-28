import { NAME, TITLE } from "@/data/content";
import { OG_SIZE, ogCard } from "@/lib/og";

export const alt = `${NAME} - ${TITLE}`;
export const size = OG_SIZE;
export const contentType = "image/png";

export default function Image() {
  return ogCard({
    kicker: ">> Orange County, CA // online",
    title: NAME,
    subtitle: "Physics Ph.D. / Scientific Software Developer",
  });
}

export const dynamic = "force-static";
