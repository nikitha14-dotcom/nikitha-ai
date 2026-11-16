from typing import List, Dict, Any, Optional

CURATED_JOB_DATABASE: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Senior AI/ML Engineer",
        "company": "Cognitive Scale Labs",
        "location": "Bengaluru, India (Hybrid)",
        "category": "AI/ML Engineer",
        "job_type": "Full-time",
        "salary_range": "₹28,00,000 - ₹42,00,000 PA",
        "experience_level": "3-5 years",
        "skills_required": ["Python", "PyTorch", "LLM Fine-tuning", "vLLM", "Docker", "FastAPI"],
        "match_score": 95.0,
        "description": "Lead the design and deployment of specialized LLM inference engines, multi-agent frameworks, and vector retrieval pipelines for enterprise scale.",
        "application_url": "https://cognitivescale.example.com/careers/ai-engineer"
    },
    {
        "id": 2,
        "title": "Machine Learning Engineer - Computer Vision & NLP",
        "company": "Apex Dynamics AI",
        "location": "Hyderabad, India (Remote)",
        "category": "AI/ML Engineer",
        "job_type": "Full-time",
        "salary_range": "₹22,00,000 - ₹35,00,000 PA",
        "experience_level": "2-4 years",
        "skills_required": ["Python", "TensorFlow", "HuggingFace", "FastAPI", "OpenCV", "Kubernetes"],
        "match_score": 90.0,
        "description": "Build high-throughput multimodal perception models and production REST microservices for automated visual reasoning.",
        "application_url": "https://apexdynamics.example.com/jobs/ml-cv"
    },
    {
        "id": 3,
        "title": "Full Stack Python AI Developer",
        "company": "NeuralStack Global",
        "location": "San Francisco, CA / Remote",
        "category": "Full Stack",
        "job_type": "Full-time",
        "salary_range": "$110,000 - $145,000 USD",
        "experience_level": "2-5 years",
        "skills_required": ["Python", "FastAPI", "Next.js", "TypeScript", "Tailwind CSS", "PostgreSQL"],
        "match_score": 94.0,
        "description": "Develop full-stack generative AI applications, real-time agent visualization dashboards, and resilient WebSocket microservices.",
        "application_url": "https://neuralstack.example.com/apply/fullstack"
    },
    {
        "id": 4,
        "title": "Python Backend & AI Services Engineer",
        "company": "QuantPulse FinTech",
        "location": "Mumbai / Pune, India",
        "category": "Python Developer",
        "job_type": "Full-time",
        "salary_range": "₹18,00,000 - ₹26,00,000 PA",
        "experience_level": "1-3 years",
        "skills_required": ["Python", "FastAPI", "SQLAlchemy", "Redis", "Celery", "PostgreSQL"],
        "match_score": 88.0,
        "description": "Architect high-concurrency financial event streams, async data scrapers, and secure user data services.",
        "application_url": "https://quantpulse.example.com/careers/python"
    },
    {
        "id": 5,
        "title": "GenAI & LLM Research Intern",
        "company": "Bhasha Intelligence",
        "location": "Bengaluru / Remote, India",
        "category": "Internship",
        "job_type": "Internship",
        "salary_range": "₹40,000 - ₹60,000 / month Stipend",
        "experience_level": "0-1 years (Students / Grads)",
        "skills_required": ["Python", "PyTorch", "Prompt Engineering", "Git", "Scikit-learn"],
        "match_score": 92.0,
        "description": "Conduct benchmarks on multilingual open-weights LLMs, build automated evaluation suites, and write synthetic dataset generation pipelines.",
        "application_url": "https://bhasha.example.com/internships/genai"
    },
    {
        "id": 6,
        "title": "Full Stack Engineer (Next.js & Python)",
        "company": "Vanguard Autonomous",
        "location": "Berlin, Germany / Remote",
        "category": "Full Stack",
        "job_type": "Full-time",
        "salary_range": "€75,000 - €95,000 EUR",
        "experience_level": "3+ years",
        "skills_required": ["Next.js", "React", "TypeScript", "Python", "GraphQL", "Docker"],
        "match_score": 86.0,
        "description": "Create next-generation autonomous flight mission telemetry portals and modern web-based operator tools.",
        "application_url": "https://vanguardauto.example.com/careers/fullstack"
    }
]

class JobSearchTool:
    @staticmethod
    def search_jobs(
        query: str = "",
        category: Optional[str] = None,
        location: Optional[str] = None,
        experience_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        results = CURATED_JOB_DATABASE
        q_lower = query.lower()

        if q_lower and q_lower not in ["all", "*"]:
            results = [
                j for j in results
                if q_lower in j["title"].lower()
                or q_lower in j["company"].lower()
                or q_lower in j["category"].lower()
                or any(q_lower in s.lower() for s in j["skills_required"])
            ]

        if category and category != "All":
            results = [j for j in results if category.lower() in j["category"].lower()]

        if location and location != "All":
            results = [j for j in results if location.lower() in j["location"].lower()]

        return results

    @staticmethod
    def analyze_ats_compatibility(resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
        resume_lower = set(s.lower() for s in resume_skills)
        matched = []
        missing = []

        for req in job_skills:
            if req.lower() in resume_lower:
                matched.append(req)
            else:
                missing.append(req)

        score = int((len(matched) / max(len(job_skills), 1)) * 100)
        return {
            "ats_score": min(score + 10, 98),  # normalized score
            "matched_skills": matched,
            "missing_skills": missing,
            "recommendations": [
                f"Add concrete project achievements mentioning {s}" for s in missing[:3]
            ]
        }
