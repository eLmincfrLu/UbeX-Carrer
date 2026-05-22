from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


def skill_level_label(score: float) -> str:
    if score >= 85:
        return "Expert"
    if score >= 70:
        return "Advanced"
    if score >= 50:
        return "Intermediate"
    return "Developing"