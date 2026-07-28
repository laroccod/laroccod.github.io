import type { Metadata } from "next";
import { Roboto_Mono, Space_Mono } from "next/font/google";
import { ThemeProvider } from "next-themes";
import { ViewTransition } from "react";
import { CommandPalette } from "@/components/layout/CommandPalette";
import { Footer } from "@/components/layout/Footer";
import { Navbar } from "@/components/layout/Navbar";
import { ScrollReveal } from "@/components/ui/ScrollReveal";
import { NAME, SUMMARY, TITLE } from "@/data/content";
import { SITE_URL } from "@/lib/site";
import "./globals.css";

const spaceMono = Space_Mono({
  weight: ["400", "700"],
  subsets: ["latin"],
  variable: "--font-space-mono",
});

// Greek coverage for the physics-glyph rain (Space Mono has none).
const robotoMono = Roboto_Mono({
  subsets: ["latin", "greek"],
  variable: "--font-roboto-mono",
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${NAME} · ${TITLE}`,
    template: `%s · ${NAME}`,
  },
  description: SUMMARY,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${spaceMono.variable} ${robotoMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col font-mono">
        <ThemeProvider
          attribute="class"
          defaultTheme="matrix"
          themes={["dark", "light", "matrix"]}
          enableSystem={false}
          disableTransitionOnChange
        >
          <Navbar />
          <main className="flex-1 w-full max-w-5xl mx-auto px-5 sm:px-8">
            <ViewTransition default="page-fade">
              <div>{children}</div>
            </ViewTransition>
          </main>
          <Footer />
          <ScrollReveal />
          <CommandPalette />
        </ThemeProvider>
      </body>
    </html>
  );
}
