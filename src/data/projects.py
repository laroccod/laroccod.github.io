"""Project registry. To wire in a new labforge app (or any project), add a
Project entry here — buttons for GitHub / PyPI / live demo / docs render only
when the corresponding URL is non-empty, so filling in `demo_url` later is a
one-line edit."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    slug: str
    name: str
    tagline: str
    description: str
    tech: tuple[str, ...]
    role: str = ""
    github_url: str = ""
    pypi_url: str = ""
    demo_url: str = ""   # when set, a "Launch live demo" button appears
    docs_url: str = ""
    screenshots: tuple[str, ...] = ()  # asset paths under src/assets/
    featured: bool = False


PROJECTS: tuple[Project, ...] = (
    Project(
        slug="labforge",
        name="labforge",
        tagline="Wrap plain Python functions into a small scientific app.",
        description=(
            "A Python framework I designed and published that turns plain "
            "functions (a simulation worker, matplotlib visualizations, "
            "analysis routines, and LaTeX theory notes) into a polished "
            "4-page scientific app (Theory → Simulation → Visualization → "
            "Analysis) with auto-generated parameter controls, a parameter-"
            "scan engine, and 8 built-in themes. This site uses labforge's "
            "'paper' design system."
        ),
        tech=("Python", "Flet", "Matplotlib", "PyPI package"),
        role="Author & maintainer",
        github_url="https://github.com/laroccod/labforge",
        pypi_url="https://pypi.org/project/labforge/",
        demo_url="",  # Fly.io deployment planned — see TASKLOG
        screenshots=(
            "/projects/labforge/screenshot.png",
            "/projects/labforge/multi_worker.png",
            "/projects/labforge/theme_instrument.png",
            "/projects/labforge/theme_lavender.png",
        ),
        featured=True,
    ),
    Project(
        slug="foresee-lab",
        name="FORESEE Lab",
        tagline="Interactive exploration of BSM physics at the LHC's forward "
                "experiments.",
        description=(
            "A labforge app wrapping the FORESEE Monte Carlo framework: pick "
            "a beyond-Standard-Model particle model on the theory page, then "
            "cache production spectra, generate signal events, and scan the "
            "discovery reach of forward LHC experiments, with live plots of "
            "hadron spectra, production rates, energy distributions, and "
            "sensitivity reach."
        ),
        tech=("Python", "labforge", "SciPy", "Numba", "Monte Carlo"),
        role="Author",
        github_url="",  # repo not yet public
        demo_url="",    # deployment follows the public release
        screenshots=(
            "/projects/foresee-lab/reach_plot.png",
            "/projects/foresee-lab/hadron_spectrum.png",
            "/projects/foresee-lab/production_rate.png",
            "/projects/foresee-lab/energy_histogram.png",
        ),
        featured=True,
    ),
    Project(
        slug="hnlcalc",
        name="HNLCalc",
        tagline="Fast, flexible heavy-neutral-lepton phenomenology.",
        description=(
            "Open-source Python package computing 100+ decay and 150+ "
            "production channels for heavy neutral leptons with arbitrary "
            "couplings across the MeV–GeV range. Validated channel-by-channel "
            "against published results, adopted by an external cosmology "
            "group, and selected for the LLP2026 workshop's reinterpretation "
            "hackathon."
        ),
        tech=("Python", "NumPy", "Particle physics"),
        role="Co-principal author",
        github_url="https://github.com/laroccod/HNLCalc",
    ),
    Project(
        slug="foresee",
        name="FORESEE",
        tagline="Sensitivity projections for the LHC's forward experiments.",
        description=(
            "The FORward Experiment SEnsitivity Estimator: the community "
            "Monte Carlo framework for projecting new-physics reach at "
            "forward LHC and fixed-target experiments. For the v2 release I "
            "re-engineered core numerical kernels (vectorization + Numba "
            "JIT), compressed simulation spectra ~40×, and built the unified "
            "model library."
        ),
        tech=("Python", "NumPy", "Numba", "Monte Carlo"),
        role="Core contributor",
        github_url="https://github.com/KlingFelix/FORESEE",
    ),
)
