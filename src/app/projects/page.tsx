import type { Metadata } from "next";
import { ProjectCard } from "@/components/cards/ProjectCard";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { PROJECTS } from "@/data/projects";

export const metadata: Metadata = {
  title: "Projects",
  description:
    "Open-source scientific software: labforge, FORESEE Lab, HNLCalc, and " +
    "the FORESEE Monte Carlo framework.",
};

export default function ProjectsPage() {
  const featured = PROJECTS.filter((p) => p.featured);
  const research = PROJECTS.filter((p) => !p.featured);

  return (
    <div className="pt-12">
      <SectionHeader index={4} kicker="SOFTWARE" title="Projects" />

      <p className="max-w-2xl text-[13px] leading-relaxed text-muted">
        Open-source tools I author and maintain, from application frameworks
        to the Monte Carlo software behind published physics results.
      </p>

      <div className="mt-6 space-y-6">
        {featured.map((project) => (
          <ProjectCard key={project.slug} project={project} />
        ))}
      </div>

      <h3 className="kicker !text-accent mt-12 mb-4">▸ Research software</h3>
      <div className="grid gap-6 md:grid-cols-2">
        {research.map((project) => (
          <ProjectCard key={project.slug} project={project} />
        ))}
      </div>
    </div>
  );
}
