"""Single source of truth for all site text, transcribed from the private
resume in content/ (which is gitignored — never import from or copy it here
verbatim; in particular the phone number stays OFF this public site)."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Link:
    label: str
    url: str
    icon: str = ""  # ft.Icons name, resolved by components


NAME = "Daniel La Rocco"
TITLE = "Physics Ph.D. · Scientific Software Developer"
LOCATION = "Orange County, CA"
EMAIL = "laroccod@uci.edu"
GITHUB = "https://github.com/laroccod"

TAGLINE = (
    "I build open-source simulation and modeling tools for particle physics — "
    "Monte Carlo frameworks, statistical inference, and the software that makes "
    "them usable."
)

SUMMARY = (
    "Physics PhD (UC Irvine, 2026) specializing in large-scale scientific "
    "simulation, statistical inference, and open-source scientific software. "
    "I build and maintain Python Monte Carlo and modeling tools used by research "
    "collaborations, with a track record of performance optimization, validated "
    "numerical methods, and clear technical communication across publications "
    "and invited talks."
)

THESIS_TITLE = (
    "GeV-Scale Heavy Neutral Leptons: Modeling, Discovery and Characterization "
    "in Colliders and Fixed Target Experiments"
)
THESIS_URL = "https://escholarship.org/uc/item/25v386s5"
THESIS_BLURB = (
    "My doctoral thesis develops the modeling, simulation, and statistical "
    "machinery to discover and characterize heavy neutral leptons at the LHC "
    "and fixed-target experiments."
)


@dataclass(frozen=True)
class SkillGroup:
    name: str
    items: tuple[str, ...]


SKILLS: tuple[SkillGroup, ...] = (
    SkillGroup("Languages", (
        "Python (NumPy, SciPy, pandas, Matplotlib, Scikit-HEP)", "Bash", "LaTeX",
    )),
    SkillGroup("Scientific computing & modeling", (
        "Monte Carlo simulation", "Likelihood-based statistical inference",
        "Hypothesis testing", "Numerical integration",
        "Performance optimization & vectorization", "Numba JIT compilation",
        "Parallel computing", "Ab-initio DFT", "Hartree-Fock methods",
    )),
    SkillGroup("Software engineering", (
        "Open-source package design & maintenance", "Automated testing (pytest)",
        "Reproducible computational pipelines", "Git / GitHub",
        "Technical documentation",
    )),
    SkillGroup("Computing environments", (
        "Unix/Linux", "HPC clusters (Slurm)", "SSH-based remote workflows",
    )),
    SkillGroup("Domain knowledge", (
        "Accelerator-based experiments (LHC, FASER, fixed-target beams)",
        "Detector acceptance modeling", "BSM phenomenology",
        "Solid-state / condensed-matter physics",
    )),
)


@dataclass(frozen=True)
class Experience:
    role: str
    org: str
    dates: str
    advisor: str
    bullets: tuple[str, ...]


EXPERIENCE: tuple[Experience, ...] = (
    Experience(
        role="Graduate Researcher",
        org="UC Irvine, Department of Physics & Astronomy",
        dates="Aug 2021 – Jun 2026",
        advisor="Advisor: Jonathan L. Feng",
        bullets=(
            "Designed and maintain HNLCalc, an open-source Python package "
            "(100+ decay and 150+ production channels) for modeling new-physics "
            "particle phenomenology across the MeV–GeV mass range; validated "
            "channel-by-channel against published results, adopted by an "
            "external group for cosmology studies, and selected as a tool for "
            "the LLP2026 workshop's reinterpretation hackathon (University of "
            "Cambridge).",
            "As a member of the FORESEE development team — an open-source "
            "Python Monte Carlo framework for projecting particle-physics "
            "experiment sensitivity — re-engineered core components for the v2 "
            "release: vectorized numerical kernels with Numba JIT compilation, "
            "compressed multi-GB simulation spectra ~40× (15 GB → 400 MB), "
            "built a unified model library, and extended the framework to a "
            "new class of experiments. Contributing author on the v2 release "
            "paper.",
            "Ran large-scale Monte Carlo simulation campaigns projecting the "
            "discovery reach of the FASER and FASER2 experiments at the LHC, "
            "producing the first sensitivity results for previously unstudied "
            "multi-parameter scenarios.",
            "Performed likelihood-based statistical analyses on simulated "
            "datasets to estimate physical parameters and discriminate "
            "competing theoretical hypotheses from multidimensional kinematic "
            "distributions.",
            "Communicated results through two Physical Review D publications "
            "and six international conference presentations and invited "
            "seminars in 2024–2026.",
        ),
    ),
    Experience(
        role="Undergraduate Researcher",
        org="Lawrence Berkeley National Laboratory",
        dates="Sep 2020 – May 2021",
        advisor="Advisor: Sinéad Griffin",
        bullets=(
            "Ran ab-initio density functional theory calculations (VASP, "
            "Quantum Espresso) on HPC clusters, computing phonon-induced "
            "decoherence in candidate solid-state qubit materials to evaluate "
            "their feasibility as quantum-computing platforms.",
        ),
    ),
    Experience(
        role="Undergraduate Researcher",
        org="UC Irvine, Department of Physics & Astronomy",
        dates="Apr 2020 – May 2021",
        advisor="Advisor: Jin Yu",
        bullets=(
            "Developed Hartree-Fock-based procedures for generating molecular "
            "force fields for nucleotide analogs on HPC clusters, applied to "
            "studies of remdesivir's interaction with the SARS-CoV-2 "
            "RNA-dependent RNA polymerase.",
        ),
    ),
)


@dataclass(frozen=True)
class Education:
    school: str
    degree: str
    dates: str
    details: tuple[str, ...] = ()


EDUCATION: tuple[Education, ...] = (
    Education(
        school="University of California, Irvine",
        degree="Ph.D. in Physics (Jun 2026) · M.S. in Physics (Jun 2023)",
        dates="Aug 2021 – Jun 2026",
        details=(
            "Advisor: Jonathan L. Feng",
            "Thesis: " + THESIS_TITLE,
            "Coursework: Quantum Field Theory, Advanced QFT, Elementary "
            "Particle Physics, Quantum Chromodynamics, Solid State Physics, "
            "General Relativity, Early Universe Cosmology, Machine Learning "
            "and Statistics",
        ),
    ),
    Education(
        school="University of California, Berkeley",
        degree="B.A. in Physics",
        dates="May 2019 – Jun 2021",
        details=(
            "Coursework: Quantum Information Science and Technology, Solid "
            "State Physics, Introduction to Quantum Field Theory, "
            "Differentiable Manifolds (Graduate), Abstract Algebra",
        ),
    ),
    Education(
        school="Orange Coast College, Costa Mesa CA",
        degree="A.S. in Physics, Mathematics, and Natural Science with Honors",
        dates="Aug 2016 – May 2019",
        details=(
            "Dean's List · Peter Christian Hernandez Memorial Scholarship",
        ),
    ),
)


@dataclass(frozen=True)
class Publication:
    authors: str
    title: str
    venue: str
    year: str
    url: str


PUBLICATIONS: tuple[Publication, ...] = (
    Publication(
        authors="Feng J. L., Hewitt A., La Rocco D., Whiteson D.",
        title="Characterizing Heavy Neutral Leptons: Measuring Parameters, "
              "Discriminating Majorana versus Dirac, and Using FASER2 as a "
              "Trigger for ATLAS",
        venue="Physical Review D 113, 035006 · arXiv:2510.16107",
        year="2026",
        url="https://inspirehep.net/literature/3071130",
    ),
    Publication(
        authors="Feng J. L., Hewitt A., Kling F., La Rocco D.",
        title="Simulating heavy neutral leptons with general couplings at "
              "collider and fixed target experiments",
        venue="Physical Review D 110, 035029 · arXiv:2405.07330",
        year="2024",
        url="https://inspirehep.net/literature/2786389",
    ),
    Publication(
        authors="Romero M. E., Long C., La Rocco D., Keerthi A. M., Xu D., Yu J.",
        title="Probing remdesivir nucleotide analogue insertion to SARS-CoV-2 "
              "RNA-dependent RNA polymerase in viral replication",
        venue="Molecular Systems Design & Engineering 6, 888–902",
        year="2021",
        url="https://doi.org/10.1039/d1me00088h",
    ),
    Publication(
        authors="Long C., Romero M. E., La Rocco D., Yu J.",
        title="Dissecting nucleotide selectivity in viral RNA polymerases",
        venue="Computational and Structural Biotechnology Journal 19, "
              "3339–3348",
        year="2021",
        url="https://doi.org/10.1016/j.csbj.2021.06.005",
    ),
)


@dataclass(frozen=True)
class Presentation:
    date: str
    kind: str
    event: str
    where: str
    title: str
    url: str = ""


PRESENTATIONS: tuple[Presentation, ...] = (
    Presentation(
        date="Mar 2026", kind="Contributed talk",
        event="9th Forward Physics Facility Meeting", where="CERN",
        title="Characterizing Heavy Neutral Leptons: Measuring Parameters, "
              "Discriminating Majorana versus Dirac, and Using FASER2 as a "
              "Trigger for ATLAS",
        url="https://indico.cern.ch/event/1609755/contributions/6902878/",
    ),
    Presentation(
        date="Nov 2025", kind="Invited seminar",
        event="HET Lunch Seminar", where="Brookhaven National Laboratory",
        title="Simulating and Characterizing Heavy Neutral Leptons at Forward "
              "Physics Experiments",
        url="https://indico.bnl.gov/event/30171/",
    ),
    Presentation(
        date="Nov 2025", kind="Invited seminar",
        event="C.N. Yang Institute for Theoretical Physics",
        where="Stony Brook University",
        title="Simulating and Characterizing Heavy Neutral Leptons at Forward "
              "Physics Experiments",
    ),
    Presentation(
        date="Aug 2025", kind="Contributed talk",
        event="SUSY 2025 (32nd International Conference on Supersymmetry)",
        where="Santa Cruz, CA",
        title="Simulating Heavy Neutral Leptons with General Couplings at "
              "Collider and Fixed Target Experiments",
        url="https://indico.cern.ch/event/1446820/contributions/6588109/",
    ),
    Presentation(
        date="Mar 2025", kind="Contributed talk",
        event="APS Global Physics Summit", where="Anaheim, CA",
        title="Characterizing long-lived particles at forward-physics "
              "experiments in the presence of a signal excess",
        url="https://schedule.aps.org/smt/2025/events/APR-S09/2",
    ),
    Presentation(
        date="Jun 2024", kind="Contributed talk",
        event="FLASY 2024 (10th Workshop on Flavor Symmetries)",
        where="UC Irvine",
        title="Simulating Heavy Neutral Leptons with General Couplings at "
              "Collider and Fixed Target Experiments",
        url="https://indico.global/event/688/contributions/17445/",
    ),
)


TEACHING: tuple[str, ...] = (
    "Teaching Assistant, UC Irvine Physics & Astronomy — 11 courses across "
    "upper- and lower-division lecture and laboratory sections (2021–2026).",
    "UAEC delegate, Annual High-Energy Physics Advocacy Trip, Washington DC "
    "(Fermilab, 2025).",
    "Tutor, CAL-BRIDGE program, UC Irvine (2024).",
    "Group Tutor, upper-division Quantum Mechanics, UC Berkeley (2021).",
    "Honors Mathematics Tutor, Orange Coast College Student Success Center "
    "(2018–2019).",
)


CONTACT_LINKS: tuple[Link, ...] = (
    Link("Email", f"mailto:{EMAIL}", "EMAIL"),
    Link("GitHub", GITHUB, "CODE"),
    Link("Ph.D. Thesis", THESIS_URL, "SCHOOL"),
    # Add when available:
    # Link("LinkedIn", "https://www.linkedin.com/in/...", "WORK"),
    # Link("ORCID", "https://orcid.org/...", "BADGE"),
)
