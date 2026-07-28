import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/site";

/** Trailing slashes match the exported URLs (next.config.ts trailingSlash). */
const PATHS = [
  "/",
  "/cv/",
  "/papers/",
  "/teaching/",
  "/projects/",
  "/presentations/",
  "/contact/",
];

export default function sitemap(): MetadataRoute.Sitemap {
  return PATHS.map((path) => ({
    url: `${SITE_URL}${path}`,
    changeFrequency: "monthly",
    priority: path === "/" ? 1 : 0.7,
  }));
}

export const dynamic = "force-static";
