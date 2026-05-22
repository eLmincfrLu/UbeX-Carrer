import json
import os

from app.utils.security import parse_skills


class GeminiService:
    """AI layer for syllabus mining and semantic matching (MVP + optional Gemini API)."""

    @staticmethod
    def extract_skills_from_syllabus(text: str) -> list[str]:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                return GeminiService._extract_with_gemini(text, api_key)
            except Exception:
                pass
        return GeminiService._extract_heuristic(text)

    @staticmethod
    def _extract_heuristic(text: str) -> list[str]:
        keywords = [
            "Python",
            "Java",
            "JavaScript",
            "Data Analysis",
            "Machine Learning",
            "SQL",
            "Marketing Analytics",
            "Project Management",
            "UI/UX",
            "Cloud",
            "DevOps",
            "Statistics",
        ]
        lower = (text or "").lower()
        found = [k for k in keywords if k.lower() in lower]
        return found or ["Python", "Data Analysis"]

    @staticmethod
    def _extract_with_gemini(text: str, api_key: str) -> list[str]:
        import urllib.error
        import urllib.request

        prompt = (
            "Extract market-relevant technical skills from this university syllabus. "
            "Return JSON array of skill strings only.\n\n" + text[:4000]
        )
        body = json.dumps(
            {
                "contents": [{"parts": [{"text": prompt}]}],
            }
        ).encode()
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={api_key}"
        )
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        raw = data["candidates"][0]["content"]["parts"][0]["text"]
        start, end = raw.find("["), raw.rfind("]") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
        return parse_skills(raw)

    @staticmethod
    def match_score(student_skills: list[dict], required: str, gpa: float, min_gpa: float) -> float:
        required_list = [s.lower() for s in parse_skills(required)]
        if not required_list:
            return 50.0
        student_map = {s.get("name", "").lower(): float(s.get("score", 0)) for s in student_skills}
        hits = 0.0
        for skill in required_list:
            for name, score in student_map.items():
                if skill in name or name in skill:
                    hits += score
                    break
        skill_part = min(100.0, (hits / len(required_list)))
        gpa_part = 100.0 if gpa >= min_gpa else max(0, (gpa / max(min_gpa, 0.01)) * 100)
        return round(0.75 * skill_part + 0.25 * gpa_part, 1)