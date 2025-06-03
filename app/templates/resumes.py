from app.models.resume import EducationEntry, JobEntry, Resume


originalResume = Resume(
    full_name="Jesse Raffield",
    email="jhraffield@gmail.com",
    phone="850-227-8585",
    linkedin="https://www.linkedin.com/in/jesse-raffield",
    location="Wilson, NC",
    headline="Senior Software Engineer",
    summary="Senior software engineer with 7 years of experience delivering scalable, production-grade systems using .NET Core, C#, Python, and cloud-native technologies. Skilled in architecting microservices, optimizing performance, and building resilient APIs for real-world applications.",
    technical_skills=["C#", ".NET Core", "Python", "C++", "SQL", "AWS", "Typescript", "Kafka", "Langchain", "NLP", "Docker", "scikit-learn", "gRPC", "REST", "Agile", "TDD"],
    core_competencies=["Microservices Architecture", "API Development", "Cloud Infrastructure", "AI/ML Integration", "Agile Methodologies"],
    work_experience=[
        JobEntry(
            title="Senior Software Engineer",
            company="Chegg",
            location="Santa Clara, CA",
            dates="Mar 2024 – May 2025",
            description=[
                "Developed and maintained distributed services in C# and Python, ensuring high availability and fault tolerance.",
                "Owned architecture and delivery of core backend services supporting Chegg's flagship AI Q&A platform.",
                "Led design and deployment of Kafka-based pipelines and AWS-hosted infrastructure to handle millions of users.",
                "Scoped, prototyped, and transitioned agentic LLM-based features from R&D into production."
            ]
        ),
        JobEntry(
            title="Software Engineer II",
            company="Chegg",
            location="Santa Clara, CA",
            dates="Jun 2020 – Mar 2024",
            description=[
                "Drove backend development for Chegg's first LLM-enabled product, coordinating across C# and TensorFlow services.",
                "Took ownership of user-facing feature delivery pipelines, including routing logic and personalization systems.",
                "Played a critical role in the technical integration of Mathway's codebase and infrastructure.",
                "Led performance tuning and observability improvements that improved system reliability and response times."
            ]
        ),
        JobEntry(
            title="R&D Software Engineer",
            company="Mathway",
            location="Bethlehem, PA",
            dates="Oct 2018 – Jun 2020",
            description=[
                "Designed and delivered backend APIs and internal tooling used across Mathway's mobile and web platforms.",
                "Led integration of ML models into Mathway's C# service stack to improve solution accuracy and ranking.",
                "Maintained and implemented C# microservices that are accessed by millions of real-time users.",
                "Contributed to both backend resilience and customer-facing improvements through cross-platform collaboration."
            ]
        ),
    ],
    education=[
        EducationEntry(degree="Masters of Science Physics", school="Lehigh University"),
        EducationEntry(degree="Bachelors of Science Physics", school="Florida State University")
    ]
)