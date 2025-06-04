from app.models.resume import EducationEntry, JobEntry, Resume


originalResume = Resume(
    full_name="Quasar McCodewrangler",
    email="quantum.taco@spaceducks.io",
    phone="555-867-5309",
    linkedin="https://www.linkedin.com/in/quasar-mccodewrangler",
    location="Gadgetopolis, ZZ",
    headline="Intergalactic Software Sorcerer",
    summary=(
        "Veteran software conjurer with 7 light-years of experience building scalable, stardust-powered systems using "
        "Arcane.NET, MoonPython, and hyperspace-native technologies. Specializes in architecting distributed microplanets, "
        "taming chaos in quantum message queues, and brewing resilient APIs in the nebulae of production."
    ),
    technical_skills=[
        "Arcane.NET", "MoonPython", "C+++", "SQL (Space Query Language)", "AWS (Astro Web Services)",
        "TypeScripts of Fate", "Kafka the Log Wizard", "Langchain Lightning", "Nebular NLP",
        "DockRockets", "Scikit-Sorcery", "gRPC (Galactic Remote Procedure Calls)", "REST (Really Elegant Space Transfers)", 
        "Agile (like space cats)", "TDD (Test-Driven Dimension-hopping)"
    ],
    core_competencies=[
        "Microplanetary Architecture",
        "API Alchemy",
        "Cloud Conjuring",
        "AI/ML Mindmelds",
        "Agile Time-Warping"
    ],
    work_experience=[
        JobEntry(
            title="Senior Nebula Engineer",
            company="AstroEd, Inc.",
            location="Moonbase Lambda, Jupiter Orbit",
            dates="Mar 3024 – May 3025",
            description=[
                "Maintained distributed comet-tracking services in MoonPython and Arcane.NET, ensuring uptime across solar storms.",
                "Architected and deployed the core backend for AstroEd's AI knowledge replicator (codename: BrainCloud).",
                "Led Kafka-based signal relay networks to broadcast answers across 42 star systems.",
                "Transitioned experimental LLM sentience simulators from the R&D wormhole into stable multiverse production."
            ]
        ),
        JobEntry(
            title="Code Alchemist II",
            company="AstroEd, Inc.",
            location="Moonbase Lambda, Jupiter Orbit",
            dates="Jun 3019 – Mar 3024",
            description=[
                "Piloted backend warp-core upgrades for the galaxy’s first LLM-powered tutoring pod.",
                "Implemented personalized learning pathways for alien species across 3 dimensions.",
                "Merged two sentient codebases (Cheggitron and Mathdroid) during the Great Refactor War of 3020.",
                "Enhanced observability spells and removed gremlins from core services, reducing runtime wobbles."
            ]
        ),
        JobEntry(
            title="Trainee Code Wizard",
            company="Mathdroid Research Collective",
            location="Cactus Ring Station, Outer Rim",
            dates="Oct 3017 – Jun 3019",
            description=[
                "Crafted backend potions and data scrolls used by millions of interstellar students.",
                "Integrated machine learning familiars into legacy systems using crystal C# runes.",
                "Stabilized microservices responsible for asteroid-sized traffic loads.",
                "Collaborated with both frontend illusionists and backend witches for total spell harmony."
            ]
        ),
    ],
    education=[
        EducationEntry(degree="Master of Astrophysics and Spellcraft", school="Lehigh University"),
        EducationEntry(degree="Bachelor of Quantum Broom Mechanics", school="Florida State University")
    ]
)