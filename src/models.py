from datetime import datetime
from src.database import db
from sqlalchemy import or_

class Candidate(db.Model):
    """Model to store CV analysis results."""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    candidate_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    github = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    education_history = db.Column(db.JSON, nullable=True)  
    work_experience = db.Column(db.JSON, nullable=True)  
    skills = db.Column(db.JSON, nullable=True)            
    projects = db.Column(db.JSON, nullable=True)
    certifications = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CVAnalysisResult {self.candidate_name}>"
    
    @classmethod
    def find_by_field(cls, field, keywords):
        filters = [field.contains(keyword) for keyword in keywords]
        results = Candidate.query.filter(or_(*filters)).all()
        return [cls._serialize_candidate(c) for c in results]
    
    @classmethod
    def match_job_requirements(cls, details):
        required_skills = details.get("skills", [])
        required_experience = details.get("experience", [])

        query = Candidate.query
        if required_skills:
            filters = [Candidate.skills.contains(keyword) for keyword in required_skills]
            query = query.filter(or_(*filters))
        if required_experience:
            filters = [Candidate.work_experience.contains(keyword) for keyword in required_experience]
            query = query.filter(or_(*filters))

        results = query.all()
        return [cls._serialize_candidate(c) for c in results]

    @classmethod
    def _serialize_candidate(cls, candidate):
        return {
            "name": candidate.candidate_name,
            "email": candidate.email,
            "phone": candidate.phone,
            "skills": candidate.skills,
            "experience": candidate.work_experience,
            "education": candidate.education_history,
            "certifications": candidate.certifications,
            "projects": candidate.projects
        }