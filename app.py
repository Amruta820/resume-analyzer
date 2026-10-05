from flask import Flask, render_template, request, send_from_directory
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import re

app = Flask(__name__)

# ---------------------------------------------------
# SKILLS
# ---------------------------------------------------

skills = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "TypeScript",
    "R",

    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Express",
    "Flask",
    "Django",

    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Redis",

    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Excel",
    "Power BI",
    "Tableau",

    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "Computer Vision",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",

    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",
    "Linux",

    "Git",
    "GitHub",
    "VS Code"
]


# ---------------------------------------------------
# SKILL ALIASES
# ---------------------------------------------------

skill_aliases = {
    "ML": "Machine Learning",
    "AI": "Artificial Intelligence",
    "NLP": "Natural Language Processing",
    "JS": "JavaScript",
    "TS": "TypeScript",
    "Postgres": "PostgreSQL",
    "Postgre": "PostgreSQL",
    "Mongo": "MongoDB",
    "Scikit Learn": "Scikit-learn",
    "Sklearn": "Scikit-learn",
    "PowerBI": "Power BI"
}


# ---------------------------------------------------
# JOB ROLES
# ---------------------------------------------------

job_roles = {
    "Python Developer": {
        "skills": [
            "Python",
            "Flask",
            "Django",
            "SQL",
            "Git"
        ],
        "description":
            "Develops applications and backend systems "
            "using Python and related technologies."
    },

    "Data Analyst": {
        "skills": [
            "Python",
            "SQL",
            "Pandas",
            "NumPy",
            "MySQL"
        ],
        "description":
            "Analyzes data, creates insights, and supports "
            "business decisions using data."
    },

    "Machine Learning Engineer": {
        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn"
        ],
        "description":
            "Builds and deploys machine learning models "
            "using data and AI techniques."
    },

    "Web Developer": {
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Flask",
            "Git"
        ],
        "description":
            "Creates and maintains websites and web applications."
    },

    "AI Engineer": {
        "skills": [
            "Python",
            "Artificial Intelligence",
            "Machine Learning",
            "Deep Learning",
            "NumPy"
        ],
        "description":
            "Develops AI-powered applications using "
            "machine learning and deep learning."
    }
}


# ---------------------------------------------------
# SKILL DETECTION
# ---------------------------------------------------

def skill_found(skill, text):

    text = text.lower()
    skill = skill.lower()

    if skill == "c":

        if re.search(
            r"(?<!\w)c(?![\w+])",
            text
        ):
            return True

    if skill == "c++":

        if re.search(
            r"(?<!\w)c\+\+(?!\w)",
            text
        ):
            return True

    if re.search(
        r"(?<!\w)" + re.escape(skill) + r"(?!\w)",
        text
    ):
        return True

    for alias, actual_skill in skill_aliases.items():

        if actual_skill.lower() == skill:

            if re.search(
                r"(?<!\w)"
                + re.escape(alias.lower())
                + r"(?!\w)",
                text
            ):
                return True

    return False


# ---------------------------------------------------
# TEXT NORMALIZATION
# ---------------------------------------------------

def normalize_text(text):

    text = text.lower()

    for alias, actual_skill in skill_aliases.items():

        pattern = (
            r"(?<!\w)"
            + re.escape(alias.lower())
            + r"(?!\w)"
        )

        text = re.sub(
            pattern,
            actual_skill.lower(),
            text
        )

    return text


# ---------------------------------------------------
# UPLOAD FOLDER
# ---------------------------------------------------

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# ---------------------------------------------------
# RESUME ANALYSIS
# ---------------------------------------------------

@app.route("/upload", methods=["POST"])
def upload_resume():

    # Check resume
    if "resume" not in request.files:

        return "No resume selected"

    resume = request.files["resume"]

    if resume.filename == "":

        return "No resume selected"

    # Get job description
    job_description = request.form.get(
        "job_description",
        ""
    )

    # Save resume
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(file_path)


    # ------------------------------------------------
    # PDF TEXT EXTRACTION
    # ------------------------------------------------

    reader = PdfReader(file_path)

    resume_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:

            resume_text += text + "\n"


    # ------------------------------------------------
    # RESUME SKILLS
    # ------------------------------------------------

    resume_skills = []

    for skill in skills:

        if skill_found(
            skill,
            resume_text
        ):

            resume_skills.append(skill)


    # ------------------------------------------------
    # JOB DESCRIPTION SKILLS
    # ------------------------------------------------

    job_skills = []

    for skill in skills:

        if skill_found(
            skill,
            job_description
        ):

            job_skills.append(skill)


    # ------------------------------------------------
    # MATCHING SKILLS
    # ------------------------------------------------

    matching_skills = []

    for skill in job_skills:

        if skill in resume_skills:

            matching_skills.append(skill)


    # ------------------------------------------------
    # MISSING SKILLS
    # ------------------------------------------------

    missing_skills = []

    for skill in job_skills:

        if skill not in resume_skills:

            missing_skills.append(skill)


    # ------------------------------------------------
    # SKILL GAP RECOMMENDATIONS
    # ------------------------------------------------

    skill_recommendations = {}

    for skill in missing_skills:

        if skill in [
            "Python",
            "Java",
            "C",
            "C++",
            "JavaScript",
            "TypeScript",
            "R"
        ]:

            skill_recommendations[skill] = (
                "Improve your programming fundamentals "
                "and practice coding problems."
            )

        elif skill in [
            "HTML",
            "CSS",
            "React",
            "Node.js",
            "Express",
            "Flask",
            "Django"
        ]:

            skill_recommendations[skill] = (
                "Build a small web development project "
                "to gain practical experience."
            )

        elif skill in [
            "SQL",
            "MySQL",
            "PostgreSQL",
            "MongoDB",
            "Redis"
        ]:

            skill_recommendations[skill] = (
                "Practice database queries and build a "
                "project using this database technology."
            )

        elif skill in [
            "Pandas",
            "NumPy",
            "Matplotlib",
            "Seaborn",
            "Excel",
            "Power BI",
            "Tableau"
        ]:

            skill_recommendations[skill] = (
                "Work on a data analysis project using "
                "real-world datasets."
            )

        elif skill in [
            "Machine Learning",
            "Deep Learning",
            "Artificial Intelligence",
            "Natural Language Processing",
            "Computer Vision",
            "Scikit-learn",
            "TensorFlow",
            "PyTorch"
        ]:

            skill_recommendations[skill] = (
                "Build an AI/ML project and practice "
                "implementing models with real datasets."
            )

        elif skill in [
            "AWS",
            "Azure",
            "Docker",
            "Kubernetes",
            "Linux"
        ]:

            skill_recommendations[skill] = (
                "Learn the fundamentals and deploy a "
                "small project using this technology."
            )

        else:

            skill_recommendations[skill] = (
                "Learn the fundamentals and practice "
                "this skill through a small project."
            )


    # ------------------------------------------------
    # MATCH PERCENTAGE
    # ------------------------------------------------

    if len(job_skills) > 0:

        match_percentage = (
            len(matching_skills)
            / len(job_skills)
        ) * 100

    else:

        match_percentage = 0


    # ------------------------------------------------
    # SEMANTIC NLP SIMILARITY
    # ------------------------------------------------

    normalized_resume_text = normalize_text(
        resume_text
    )

    normalized_job_description = normalize_text(
        job_description
    )

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    resume_embedding = model.encode(
        normalized_resume_text
    )

    job_embedding = model.encode(
        normalized_job_description
    )

    cosine_similarity_score = cosine_similarity(
        [resume_embedding],
        [job_embedding]
    )[0][0]

    similarity_percentage = round(
        cosine_similarity_score * 100,
        2
    )


    # ------------------------------------------------
    # OVERALL COMPATIBILITY SCORE
    # ------------------------------------------------

    overall_score = round(
        (match_percentage * 0.60)
        + (similarity_percentage * 0.40),
        2
    )


    # ------------------------------------------------
    # SMART JOB ROLE RECOMMENDATION
    # ------------------------------------------------

    role_scores = {}

    for role, role_data in job_roles.items():

        required_skills = role_data["skills"]
        role_description = role_data["description"]

        resume_matches = []
        job_matches = []

        # ---------------------------------------------
        # Resume skill matching
        # ---------------------------------------------

        for skill in required_skills:

            if skill in resume_skills:

                resume_matches.append(skill)

        # ---------------------------------------------
        # Job description matching
        # ---------------------------------------------

        for skill in required_skills:

            if skill in job_skills:

                job_matches.append(skill)

        # ---------------------------------------------
        # Resume skill score
        # ---------------------------------------------

        if len(required_skills) > 0:

            resume_score = (
                len(resume_matches)
                / len(required_skills)
            ) * 100

        else:

            resume_score = 0

        # ---------------------------------------------
        # Job relevance score
        # ---------------------------------------------

        if len(required_skills) > 0:

            job_score = (
                len(job_matches)
                / len(required_skills)
            ) * 100

        else:

            job_score = 0

        # ---------------------------------------------
        # Role-specific semantic similarity
        # ---------------------------------------------

        role_text = (
            role_description
            + " "
            + " ".join(required_skills)
        )

        normalized_role_text = normalize_text(
            role_text
        )

        role_embedding = model.encode(
            normalized_role_text
        )

        role_semantic_score = cosine_similarity(
            [resume_embedding],
            [role_embedding]
        )[0][0] * 100

        # ---------------------------------------------
        # Final role score
        # ---------------------------------------------

        role_score = (
            resume_score * 0.40
            + job_score * 0.20
            + role_semantic_score * 0.40
        )

        role_scores[role] = round(
            role_score,
            2
        )


        # ------------------------------------------------
    # SORT TOP ROLES
    # ------------------------------------------------

    sorted_roles = sorted(
        role_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_roles = sorted_roles[:3]


    # ------------------------------------------------
    # GENERATE PDF REPORT
    # ------------------------------------------------

    report_folder = "reports"

    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    report_path = os.path.join(
        report_folder,
        "resume_analysis_report.pdf"
    )

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        report_path,
        pagesize=A4
    )

    report_content = []

    report_content.append(
        Paragraph(
            "Resume Analysis Report",
            styles["Title"]
        )
    )

    report_content.append(
        Spacer(1, 20)
    )

    report_content.append(
        Paragraph(
            f"Overall Compatibility Score: {overall_score}%",
            styles["Heading2"]
        )
    )

    report_content.append(
        Paragraph(
            f"Skill Match: {match_percentage}%",
            styles["Normal"]
        )
    )

    report_content.append(
        Paragraph(
            f"NLP Similarity: {similarity_percentage}%",
            styles["Normal"]
        )
    )

    report_content.append(
        Spacer(1, 15)
    )

    report_content.append(
        Paragraph(
            "Top Recommended Job Roles",
            styles["Heading2"]
        )
    )

    for role, score in top_roles:

        report_content.append(
            Paragraph(
                f"{role}: {score}%",
                styles["Normal"]
            )
        )

    report_content.append(
        Spacer(1, 15)
    )

    report_content.append(
        Paragraph(
            "Matching Skills",
            styles["Heading2"]
        )
    )

    for skill in matching_skills:

        report_content.append(
            Paragraph(
                f"- {skill}",
                styles["Normal"]
            )
        )

    report_content.append(
        Spacer(1, 15)
    )

    report_content.append(
        Paragraph(
            "Missing Skills",
            styles["Heading2"]
        )
    )

    for skill in missing_skills:

        report_content.append(
            Paragraph(
                f"- {skill}",
                styles["Normal"]
            )
        )

    document.build(report_content)


    # ------------------------------------------------
    # SEND RESULTS TO HTML
    # ------------------------------------------------

    return render_template(
        "results.html",

        resume_skills=resume_skills,

        job_skills=job_skills,

        matching_skills=matching_skills,

        missing_skills=missing_skills,

        match_percentage=round(
            match_percentage,
            2
        ),

        similarity_percentage=similarity_percentage,

        overall_score=overall_score,

        top_roles=top_roles,

        role_scores=role_scores,

        skill_recommendations=skill_recommendations
    )


# ---------------------------------------------------
# DOWNLOAD PDF REPORT
# ---------------------------------------------------

@app.route("/download-report")
def download_report():

    return send_from_directory(
        "reports",
        "resume_analysis_report.pdf",
        as_attachment=True
    )


# ---------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)