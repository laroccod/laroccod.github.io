import { OG_CARDS } from "@/lib/og-cards";
import { ogCard } from "@/lib/og";

export const dynamic = "force-static";

export function GET() {
  return ogCard(OG_CARDS.home);
}
