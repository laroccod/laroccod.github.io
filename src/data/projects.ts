/** Project registry, ported from the old site's src/data/projects.py.
 * Buttons for GitHub / PyPI / live demo / docs render only when the
 * corresponding URL is non-empty, so filling in demoUrl later is a
 * one-line edit. */

import type { Project } from "./types";

export const PROJECTS: Project[] = [
  {
    slug: "labforge",
    name: "labforge",
    tagline: "Wrap plain Python functions into a small scientific app.",
    description:
      "A Python framework I designed and published that turns plain " +
      "functions (a simulation worker, matplotlib visualizations, " +
      "analysis routines, and LaTeX theory notes) into a polished " +
      "4-page scientific app (Theory → Simulation → Visualization → " +
      "Analysis) with auto-generated parameter controls, a parameter-" +
      "scan engine, and 8 built-in themes.",
    tech: ["Python", "Flet", "Matplotlib", "PyPI package"],
    role: "Author & maintainer",
    githubUrl: "https://github.com/laroccod/labforge",
    pypiUrl: "https://pypi.org/project/labforge/",
    demoUrl: "", // Fly.io deployment planned
    // Mirrors of the labforge README's assets/ images, so the strip tracks
    // upstream: re-fetch from raw.githubusercontent.com/laroccod/labforge/
    // main/assets/<name>.png when the README screenshots change.
    screenshots: [
      "/projects/labforge/screenshot.png",
      "/projects/labforge/multi_worker.png",
      "/projects/labforge/theme_instrument.png",
      "/projects/labforge/theme_lavender.png",
    ],
    featured: true,
  },
  {
    slug: "foresee-lab",
    name: "FORESEE Lab",
    tagline:
      "Interactive exploration of BSM physics at the LHC's forward " +
      "experiments.",
    description:
      "A labforge app wrapping the FORESEE Monte Carlo framework: pick " +
      "a beyond-Standard-Model particle model on the theory page, then " +
      "cache production spectra, generate signal events, and scan the " +
      "discovery reach of forward LHC experiments, with live plots of " +
      "hadron spectra, production rates, energy distributions, and " +
      "sensitivity reach.",
    tech: ["Python", "labforge", "SciPy", "Numba", "Monte Carlo"],
    role: "Author",
    githubUrl: "", // repo not yet public
    demoUrl: "", // deployment follows the public release
    // Screenshots pulled while the app is still in progress; restore the
    // /projects/foresee-lab/*.png strip once the pages settle.
    featured: true,
  },
  {
    slug: "hnlcalc",
    name: "HNLCalc",
    tagline: "Fast, flexible heavy-neutral-lepton phenomenology.",
    description:
      "Open-source Python package computing 100+ decay and 150+ " +
      "production channels for heavy neutral leptons with arbitrary " +
      "couplings across the MeV–GeV range. Validated channel-by-channel " +
      "against published results, adopted by an external cosmology " +
      "group, and selected for the LLP2026 workshop's reinterpretation " +
      "hackathon.",
    tech: ["Python", "NumPy", "Particle physics"],
    role: "Co-principal author",
    githubUrl: "https://github.com/laroccod/HNLCalc",
  },
  {
    slug: "foresee",
    name: "FORESEE",
    tagline: "Sensitivity projections for the LHC's forward experiments.",
    description:
      "The FORward Experiment SEnsitivity Estimator: the community " +
      "Monte Carlo framework for projecting new-physics reach at " +
      "forward LHC and fixed-target experiments. For the v2 release I " +
      "re-engineered core numerical kernels (vectorization + Numba " +
      "JIT), compressed simulation spectra ~40×, and built the unified " +
      "model library.",
    tech: ["Python", "NumPy", "Numba", "Monte Carlo"],
    role: "Core contributor",
    githubUrl: "https://github.com/KlingFelix/FORESEE",
  },
];
