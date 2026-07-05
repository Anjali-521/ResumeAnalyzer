from flask import Flask, render_template, request, jsonify
import PyPDF2
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "../frontend"),
    static_folder=os.path.join(os.path.dirname(__file__), "../frontend")
)


def analyze_resume(text):
    text_lower = text.lower()

    skills = []

    skill_map = {
        "Python": ["python"],
        "Java": ["java"],
        "SQL": ["sql"],
        "C++/C#": ["c++", "c#"],
        "HTML": ["html"],
        "CSS": ["css"],
        "JavaScript": ["javascript", "js"],
        "React": ["react"],
        "Node.js": ["node", "nodejs"],
        "Machine Learning": ["machine learning"],
        "Deep Learning": ["deep learning"],
        "AWS": ["aws"],
        "Docker": ["docker"],
        "Git": ["git"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "TensorFlow": ["tensorflow"],
        "REST API": ["api", "rest api"],
        "Linux": ["linux"],
        "MongoDB": ["mongodb"],
        "Data Visualization": ["power bi", "tableau"]
    }

    for skill, keywords in skill_map.items():
        if any(word in text_lower for word in keywords):
            skills.append(skill)

    skills = list(set(skills))

    roles = []

    if any(x in text_lower for x in ["python", "django", "flask"]):
        roles.append("Backend Developer")

    if any(x in text_lower for x in ["html", "css", "javascript", "react"]):
        roles.append("Frontend Developer")

    if any(x in text_lower for x in ["node", "express"]):
        roles.append("Full Stack Developer")

    if any(x in text_lower for x in ["machine learning", "deep learning"]):
        roles.append("Machine Learning Engineer")

    if any(x in text_lower for x in ["aws", "docker", "kubernetes"]):
        roles.append("DevOps Engineer")

    if any(x in text_lower for x in ["sql", "mongodb"]):
        roles.append("Database Administrator")

    if any(x in text_lower for x in ["power bi", "tableau"]):
        roles.append("Data Analyst")

    roles = list(set(roles))

    mistakes = []

    if "education" not in text_lower:
        mistakes.append("Education section missing")

    if "project" not in text_lower:
        mistakes.append("Projects section missing")

    if "experience" not in text_lower:
        mistakes.append("Work Experience section missing")

    # if "github.com" not in text_lower:
    #     mistakes.append("GitHub profile missing")

    # if "linkedin.com" not in text_lower:
    #     mistakes.append("LinkedIn profile missing")

    if "@" not in text_lower:
        mistakes.append("Email address missing")

    return {
        "skills": skills,
        "recommended_roles": roles,
        "mistakes": mistakes
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["file"]

    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    result = analyze_resume(text)

    return jsonify(result)


if __name__ == "__main__":
    print("Starting Flask Server...")
    app.run(debug=True)