import { Chip } from "@/components/ui/Chip";
import { FigureStrip } from "@/components/ui/FigureStrip";
import { LinkButton } from "@/components/ui/LinkButton";
import { StatusChip } from "@/components/ui/StatusChip";
import { TerminalCard } from "@/components/ui/TerminalCard";
import type { Project } from "@/data/types";

export function ProjectCard({ project }: { project: Project }) {
  const hasLinks =
    project.githubUrl || project.pypiUrl || project.demoUrl || project.docsUrl;
  return (
    <TerminalCard label={project.name.toUpperCase()}>
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <h3 className="text-[17px] font-bold">{project.name}</h3>
        {project.role && <span className="kicker">{project.role}</span>}
      </div>
      <p className="mt-1 text-[13px] italic text-secondary">
        {project.tagline}
      </p>
      <p className="mt-3 text-[13px] leading-relaxed">{project.description}</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {project.tech.map((tech) => (
          <Chip key={tech}>{tech}</Chip>
        ))}
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {project.githubUrl && (
          <LinkButton href={project.githubUrl}>GitHub</LinkButton>
        )}
        {project.pypiUrl && <LinkButton href={project.pypiUrl}>PyPI</LinkButton>}
        {project.demoUrl && (
          <LinkButton href={project.demoUrl} variant="primary">
            Launch live demo
          </LinkButton>
        )}
        {project.docsUrl && <LinkButton href={project.docsUrl}>Docs</LinkButton>}
        {!hasLinks && (
          <StatusChip tone="secondary">Public release pending</StatusChip>
        )}
      </div>
      {project.screenshots && project.screenshots.length > 0 && (
        <FigureStrip
          figures={project.screenshots.map((src, i) => ({
            src,
            caption: `${project.name} screenshot ${i + 1}`,
          }))}
          caption="Screenshots. Click one to enlarge."
          matted={false}
        />
      )}
    </TerminalCard>
  );
}
