from app.models import Application, User, Vacancy
from app.utils.helpers import skill_level_label


class AnalyticsService:
    @staticmethod
    def student_dashboard(user: User) -> dict:
        skills = user.skills or []
        return {
            "skill_count": len(skills),
            "avg_skill": round(sum(s.get("score", 0) for s in skills) / len(skills), 1) if skills else 0,
            "applications": Application.query.filter_by(student_id=user.id).count(),
            "verified": user.verified,
            "skills": [
                {**s, "level": skill_level_label(s.get("score", 0))} for s in skills
            ],
        }

    @staticmethod
    def partner_dashboard(user: User) -> dict:
        vacancies = Vacancy.query.filter_by(partner_id=user.id).all()
        apps = (
            Application.query.join(Vacancy)
            .filter(Vacancy.partner_id == user.id)
            .all()
        )
        return {
            "vacancy_count": len(vacancies),
            "application_count": len(apps),
            "active_vacancies": sum(1 for v in vacancies if v.is_active),
            "top_matches": sorted(apps, key=lambda a: a.match_score, reverse=True)[:5],
        }

    @staticmethod
    def university_dashboard() -> dict:
        students = User.query.filter_by(role="student").count()
        teachers = User.query.filter_by(role="teacher").count()
        partners = User.query.filter_by(role="partner").count()
        vacancies = Vacancy.query.filter_by(is_active=True).count()
        return {
            "students": students,
            "teachers": teachers,
            "partners": partners,
            "active_vacancies": vacancies,
        }

    @staticmethod
    def chart_payload(user: User | None = None, role: str | None = None) -> dict:
        if role == "student" and user:
            skills = user.skills or []
            return {
                "labels": [s.get("name", "Skill") for s in skills],
                "scores": [s.get("score", 0) for s in skills],
            }
        if role == "partner" and user:
            vacancies = Vacancy.query.filter_by(partner_id=user.id).all()
            return {
                "labels": [v.title[:24] for v in vacancies] or ["No vacancies"],
                "scores": [Application.query.filter_by(vacancy_id=v.id).count() for v in vacancies] or [0],
            }
        return {
            "labels": ["Students", "Teachers", "Partners", "Vacancies"],
            "scores": [
                User.query.filter_by(role="student").count(),
                User.query.filter_by(role="teacher").count(),
                User.query.filter_by(role="partner").count(),
                Vacancy.query.count(),
            ],
        }