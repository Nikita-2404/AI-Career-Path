# ============================================================
# AI CAREER PATH - HYBRID CAREER RECOMMENDATION MODEL
# ============================================================

import re


# ============================================================
# CAREER DATABASE
# ============================================================

CAREER_PROFILES = {

    "Data Scientist": {
        "domain": "Data Science & Analytics",
        "keywords": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "machine learning",
            "statistics",
            "data science",
            "data analysis",
            "matplotlib",
            "scikit learn"
        ]
    },

    "Data Analyst": {
        "domain": "Data Science & Analytics",
        "keywords": [
            "sql",
            "excel",
            "power bi",
            "tableau",
            "python",
            "data analysis",
            "statistics",
            "reporting",
            "dashboard",
            "analytics"
        ]
    },

    "Machine Learning Engineer": {
        "domain": "Artificial Intelligence & Machine Learning",
        "keywords": [
            "python",
            "machine learning",
            "tensorflow",
            "pytorch",
            "scikit learn",
            "numpy",
            "pandas",
            "deep learning",
            "artificial intelligence",
            "ml"
        ]
    },

    "AI Researcher": {
        "domain": "Artificial Intelligence & Machine Learning",
        "keywords": [
            "python",
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "mathematics",
            "statistics",
            "research",
            "neural networks"
        ]
    },

    "Generative AI Engineer": {
        "domain": "Artificial Intelligence & Machine Learning",
        "keywords": [
            "python",
            "generative ai",
            "llm",
            "langchain",
            "rag",
            "openai",
            "prompt engineering",
            "machine learning",
            "artificial intelligence"
        ]
    },

    "Software Developer": {
        "domain": "Software Development",
        "keywords": [
            "python",
            "java",
            "c++",
            "c",
            "javascript",
            "git",
            "oop",
            "software development",
            "programming",
            "data structures"
        ]
    },

    "Web Developer": {
        "domain": "Web Development",
        "keywords": [
            "html",
            "css",
            "javascript",
            "react",
            "angular",
            "node",
            "flask",
            "django",
            "web development",
            "frontend",
            "backend"
        ]
    },

    "Mobile App Developer": {
        "domain": "Software Development",
        "keywords": [
            "android",
            "kotlin",
            "java",
            "flutter",
            "dart",
            "react native",
            "mobile development",
            "ios"
        ]
    },

    "Cloud Engineer": {
        "domain": "Cloud & DevOps",
        "keywords": [
            "aws",
            "azure",
            "gcp",
            "cloud",
            "docker",
            "kubernetes",
            "linux",
            "terraform",
            "cloud computing"
        ]
    },

    "DevOps Engineer": {
        "domain": "Cloud & DevOps",
        "keywords": [
            "docker",
            "kubernetes",
            "jenkins",
            "git",
            "linux",
            "aws",
            "azure",
            "ci cd",
            "devops",
            "terraform"
        ]
    },

    "Cybersecurity Analyst": {
        "domain": "Cybersecurity",
        "keywords": [
            "cybersecurity",
            "network security",
            "ethical hacking",
            "linux",
            "networking",
            "security",
            "penetration testing",
            "cryptography",
            "soc"
        ]
    },

    "Network Engineer": {
        "domain": "Networking",
        "keywords": [
            "networking",
            "cisco",
            "routing",
            "switching",
            "tcp ip",
            "linux",
            "network security",
            "firewall",
            "ccna"
        ]
    },

    "Database Administrator": {
        "domain": "Database & Data Management",
        "keywords": [
            "sql",
            "mysql",
            "postgresql",
            "oracle",
            "database",
            "database administration",
            "mongodb",
            "backup",
            "query optimization"
        ]
    },

    "Business Analyst": {
        "domain": "Business & Management",
        "keywords": [
            "business analysis",
            "requirements",
            "business intelligence",
            "excel",
            "power bi",
            "communication",
            "stakeholder management",
            "process analysis"
        ]
    },

    "Product Manager": {
        "domain": "Business & Management",
        "keywords": [
            "product management",
            "product strategy",
            "business",
            "market research",
            "communication",
            "leadership",
            "agile",
            "scrum"
        ]
    },

    "UI/UX Designer": {
        "domain": "Design",
        "keywords": [
            "ui",
            "ux",
            "figma",
            "adobe xd",
            "user experience",
            "user interface",
            "wireframe",
            "prototype",
            "design"
        ]
    },

    "QA/Test Engineer": {
        "domain": "Software Testing",
        "keywords": [
            "testing",
            "manual testing",
            "automation testing",
            "selenium",
            "pytest",
            "java",
            "quality assurance",
            "test cases"
        ]
    },

    "Digital Marketing Specialist": {
        "domain": "Digital Marketing",
        "keywords": [
            "digital marketing",
            "seo",
            "sem",
            "social media",
            "content marketing",
            "google analytics",
            "advertising",
            "marketing"
        ]
    },

    "Technical Support Engineer": {
        "domain": "IT Support",
        "keywords": [
            "technical support",
            "troubleshooting",
            "windows",
            "linux",
            "networking",
            "hardware",
            "customer support",
            "it support"
        ]
    }
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize(text):

    if text is None:
        return ""

    text = str(text).lower().strip()

    text = text.replace("-", " ")
    text = text.replace("/", " ")
    text = text.replace(",", " ")
    text = text.replace("_", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# SPLIT SKILLS
# ============================================================

def make_skill_list(skills):

    if not skills:
        return []

    skills = str(skills)

    skills = skills.replace(";", ",")
    skills = skills.replace("|", ",")

    result = []

    for item in skills.split(","):

        item = normalize(item)

        if item and item not in result:
            result.append(item)

    return result


# ============================================================
# CHECK KEYWORD
# ============================================================

def keyword_exists(keyword, text):

    keyword = normalize(keyword)
    text = normalize(text)

    if not keyword or not text:
        return False

    if keyword in text:
        return True

    return False


# ============================================================
# DOMAIN NORMALIZATION
# ============================================================

def normalize_domain(domain):

    domain = normalize(domain)

    domain_map = {

        "data science":
            "data science analytics",

        "data analytics":
            "data science analytics",

        "analytics":
            "data science analytics",

        "artificial intelligence":
            "artificial intelligence machine learning",

        "ai":
            "artificial intelligence machine learning",

        "machine learning":
            "artificial intelligence machine learning",

        "software development":
            "software development",

        "web development":
            "web development",

        "cyber security":
            "cybersecurity",

        "cybersecurity":
            "cybersecurity",

        "cloud computing":
            "cloud devops",

        "cloud":
            "cloud devops",

        "devops":
            "cloud devops",

        "database":
            "database data management",

        "database management":
            "database data management",

        "testing":
            "software testing",

        "software testing":
            "software testing",

        "it support":
            "it support",

        "networking":
            "networking",

        "design":
            "design",

        "digital marketing":
            "digital marketing",

        "business":
            "business management"
    }

    return domain_map.get(domain, domain)


# ============================================================
# RECOMMEND CAREERS
# ============================================================

def recommend_careers(
    skills,
    education,
    interests,
    experience,
    career_domain=""
):

    # --------------------------------------------------------
    # NORMALIZE INPUT
    # --------------------------------------------------------

    skills_text = normalize(skills)
    education_text = normalize(education)
    interests_text = normalize(interests)
    experience_text = normalize(experience)
    domain_text = normalize_domain(career_domain)

    selected_skills = make_skill_list(skills)

    # --------------------------------------------------------
    # COMBINE ALL INPUT
    # --------------------------------------------------------

    all_text = (
        skills_text
        + " "
        + education_text
        + " "
        + interests_text
        + " "
        + experience_text
        + " "
        + domain_text
    )

    all_text = normalize(all_text)

    results = []

    # ========================================================
    # LOOP THROUGH CAREERS
    # ========================================================

    for career, profile in CAREER_PROFILES.items():

        keywords = profile["keywords"]

        score = 0

        matched = []

        # ----------------------------------------------------
        # DOMAIN MATCH
        # ----------------------------------------------------

        profile_domain = normalize_domain(
            profile["domain"]
        )

        if domain_text:

            if domain_text == profile_domain:

                score += 30

            elif (
                domain_text in profile_domain
                or profile_domain in domain_text
            ):

                score += 20

        # ----------------------------------------------------
        # SKILL MATCH
        # ----------------------------------------------------

        for keyword in keywords:

            keyword_normalized = normalize(
                keyword
            )

            found = False

            # Complete text match
            if keyword_normalized in all_text:

                found = True

            # Individual skill match
            if not found:

                for skill in selected_skills:

                    skill_normalized = normalize(
                        skill
                    )

                    if (
                        keyword_normalized
                        == skill_normalized
                    ):

                        found = True
                        break

                    if (
                        keyword_normalized
                        in skill_normalized
                    ):

                        found = True
                        break

                    if (
                        skill_normalized
                        in keyword_normalized
                    ):

                        found = True
                        break

            if found:

                score += 8

                if keyword not in matched:

                    matched.append(keyword)

        # ----------------------------------------------------
        # INTEREST MATCH
        # ----------------------------------------------------

        interest_rules = {

            "data science": [
                "Data Scientist",
                "Data Analyst"
            ],

            "data": [
                "Data Scientist",
                "Data Analyst",
                "Database Administrator"
            ],

            "analytics": [
                "Data Analyst",
                "Data Scientist",
                "Business Analyst"
            ],

            "artificial intelligence": [
                "AI Researcher",
                "Machine Learning Engineer",
                "Generative AI Engineer"
            ],

            "ai": [
                "AI Researcher",
                "Machine Learning Engineer",
                "Generative AI Engineer"
            ],

            "machine learning": [
                "Machine Learning Engineer",
                "Data Scientist",
                "AI Researcher"
            ],

            "programming": [
                "Software Developer",
                "Web Developer",
                "Mobile App Developer"
            ],

            "web": [
                "Web Developer"
            ],

            "software development": [
                "Software Developer",
                "QA/Test Engineer"
            ],

            "security": [
                "Cybersecurity Analyst"
            ],

            "cybersecurity": [
                "Cybersecurity Analyst"
            ],

            "cloud": [
                "Cloud Engineer",
                "DevOps Engineer"
            ],

            "cloud computing": [
                "Cloud Engineer",
                "DevOps Engineer"
            ],

            "database": [
                "Database Administrator",
                "Data Analyst"
            ],

            "design": [
                "UI/UX Designer"
            ],

            "testing": [
                "QA/Test Engineer"
            ],

            "devops": [
                "DevOps Engineer"
            ]
        }

        for interest, careers in interest_rules.items():

            if interest in interests_text:

                if career in careers:

                    score += 12

        # ----------------------------------------------------
        # EDUCATION MATCH
        # ----------------------------------------------------

        if "bsc it" in education_text:

            if career in [
                "Data Scientist",
                "Data Analyst",
                "Machine Learning Engineer",
                "Software Developer",
                "Web Developer",
                "Database Administrator",
                "Cybersecurity Analyst",
                "Cloud Engineer"
            ]:

                score += 6

        elif "bca" in education_text:

            if career in [
                "Software Developer",
                "Web Developer",
                "Data Analyst",
                "QA/Test Engineer"
            ]:

                score += 6

        elif "btech" in education_text:

            if career in [
                "Software Developer",
                "Machine Learning Engineer",
                "Cloud Engineer",
                "DevOps Engineer",
                "Cybersecurity Analyst"
            ]:

                score += 6

        elif "mca" in education_text:

            if career in [
                "Software Developer",
                "Data Scientist",
                "Machine Learning Engineer",
                "AI Researcher",
                "Cloud Engineer"
            ]:

                score += 7

        elif "mtech" in education_text:

            if career in [
                "AI Researcher",
                "Machine Learning Engineer",
                "Data Scientist",
                "Cloud Engineer"
            ]:

                score += 8

        # ----------------------------------------------------
        # EXPERIENCE MATCH
        # ----------------------------------------------------

        if "fresher" in experience_text:

            if career in [
                "Data Analyst",
                "Software Developer",
                "Web Developer",
                "QA/Test Engineer",
                "Technical Support Engineer"
            ]:

                score += 5

        elif (
            "0 1 years" in experience_text
            or "0 1 year" in experience_text
        ):

            if career in [
                "Data Analyst",
                "Software Developer",
                "Web Developer",
                "QA/Test Engineer"
            ]:

                score += 4

        elif (
            "1 3 years" in experience_text
            or "1 3 year" in experience_text
        ):

            score += 5

        elif "3 years" in experience_text:

            score += 6

        # ====================================================
        # STRONG COMBINATION RULES
        # ====================================================

        # ----------------------------------------------------
        # PYTHON + SQL + MACHINE LEARNING
        # ----------------------------------------------------

        if (
            "python" in all_text
            and "sql" in all_text
            and (
                "machine learning" in all_text
                or "ml" in all_text
                or "data science" in all_text
            )
        ):

            if career == "Data Scientist":

                score += 25

            elif career == "Machine Learning Engineer":

                score += 22

            elif career == "Data Analyst":

                score += 12

        # ----------------------------------------------------
        # PYTHON + SQL + DATA
        # ----------------------------------------------------

        if (
            "python" in all_text
            and "sql" in all_text
            and (
                "data" in all_text
                or "analytics" in all_text
            )
        ):

            if career == "Data Analyst":

                score += 15

            elif career == "Data Scientist":

                score += 18

        # ----------------------------------------------------
        # PYTHON + MACHINE LEARNING
        # ----------------------------------------------------

        if (
            "python" in all_text
            and "machine learning" in all_text
        ):

            if career == "Machine Learning Engineer":

                score += 18

            elif career == "Data Scientist":

                score += 15

        # ----------------------------------------------------
        # PYTHON + AI
        # ----------------------------------------------------

        if (
            "python" in all_text
            and (
                "artificial intelligence" in all_text
                or " ai " in " " + all_text + " "
            )
        ):

            if career == "AI Researcher":

                score += 15

            elif career == "Machine Learning Engineer":

                score += 15

            elif career == "Generative AI Engineer":

                score += 10

        # ----------------------------------------------------
        # GENERATIVE AI
        # ----------------------------------------------------

        if (
            "generative ai" in all_text
            or "llm" in all_text
            or "langchain" in all_text
            or "rag" in all_text
        ):

            if career == "Generative AI Engineer":

                score += 30

        # ----------------------------------------------------
        # SQL + POWER BI / TABLEAU
        # ----------------------------------------------------

        if (
            "sql" in all_text
            and (
                "power bi" in all_text
                or "tableau" in all_text
                or "excel" in all_text
            )
        ):

            if career == "Data Analyst":

                score += 22

        # ----------------------------------------------------
        # HTML + CSS + JAVASCRIPT
        # ----------------------------------------------------

        if (
            "html" in all_text
            and "css" in all_text
            and "javascript" in all_text
        ):

            if career == "Web Developer":

                score += 30

        # ----------------------------------------------------
        # JAVA + PROGRAMMING
        # ----------------------------------------------------

        if (
            "java" in all_text
            and (
                "programming" in all_text
                or "software development" in all_text
            )
        ):

            if career == "Software Developer":

                score += 25

        # ----------------------------------------------------
        # AWS / AZURE / GCP
        # ----------------------------------------------------

        if (
            "aws" in all_text
            or "azure" in all_text
            or "gcp" in all_text
        ):

            if career == "Cloud Engineer":

                score += 25

            elif career == "DevOps Engineer":

                score += 15

        # ----------------------------------------------------
        # DOCKER / KUBERNETES
        # ----------------------------------------------------

        if (
            "docker" in all_text
            or "kubernetes" in all_text
        ):

            if career == "DevOps Engineer":

                score += 25

            elif career == "Cloud Engineer":

                score += 12

        # ----------------------------------------------------
        # CYBERSECURITY
        # ----------------------------------------------------

        if (
            "cybersecurity" in all_text
            or "ethical hacking" in all_text
            or "penetration testing" in all_text
        ):

            if career == "Cybersecurity Analyst":

                score += 30

        # ----------------------------------------------------
        # NETWORKING
        # ----------------------------------------------------

        if (
            "networking" in all_text
            or "cisco" in all_text
            or "ccna" in all_text
        ):

            if career == "Network Engineer":

                score += 30

        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        if (
            "mysql" in all_text
            or "postgresql" in all_text
            or "oracle" in all_text
            or "database" in all_text
        ):

            if career == "Database Administrator":

                score += 25

        # ----------------------------------------------------
        # UI / UX
        # ----------------------------------------------------

        if (
            "figma" in all_text
            or "ui ux" in all_text
            or "user experience" in all_text
        ):

            if career == "UI/UX Designer":

                score += 30

        # ----------------------------------------------------
        # TESTING
        # ----------------------------------------------------

        if (
            "testing" in all_text
            or "selenium" in all_text
            or "pytest" in all_text
        ):

            if career == "QA/Test Engineer":

                score += 25

        # ----------------------------------------------------
        # DIGITAL MARKETING
        # ----------------------------------------------------

        if (
            "digital marketing" in all_text
            or "seo" in all_text
            or "social media" in all_text
        ):

            if career == "Digital Marketing Specialist":

                score += 30

        # ----------------------------------------------------
        # SUPPORT
        # ----------------------------------------------------

        if (
            "technical support" in all_text
            or "troubleshooting" in all_text
            or "it support" in all_text
        ):

            if career == "Technical Support Engineer":

                score += 30

        # ----------------------------------------------------
        # MINIMUM SCORE
        # ----------------------------------------------------

        if score < 5:

            score = 5

        # ----------------------------------------------------
        # MAXIMUM SCORE
        # ----------------------------------------------------

        score = min(98, score)

        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        results.append({

            "career": career,

            "score": round(
                score,
                2
            ),

            "matched": len(
                matched
            ),

            "keywords": matched[:8],

            "domain": profile["domain"]

        })

    # ========================================================
    # SORT RESULTS
    # ========================================================

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # ========================================================
    # RETURN TOP 5
    # ========================================================

    return results[:5]


# ============================================================
# MAIN PREDICTION FUNCTION
# ============================================================

def predict_career(
    education,
    skills,
    interests,
    experience,
    career_domain=""
):
    """
    Main function used by Flask app.py.

    Returns:

        career, score

    Example:

        (
            "Data Scientist",
            86
        )
    """

    try:

        # ----------------------------------------------------
        # GET RECOMMENDATIONS
        # ----------------------------------------------------

        results = recommend_careers(

            skills=skills,

            education=education,

            interests=interests,

            experience=experience,

            career_domain=career_domain

        )

        # ----------------------------------------------------
        # SAFETY CHECK
        # ----------------------------------------------------

        if not results:

            return (
                "Data Analyst",
                50
            )

        # ----------------------------------------------------
        # BEST RESULT
        # ----------------------------------------------------

        best_result = results[0]

        career = best_result.get(
            "career",
            "Data Analyst"
        )

        score = best_result.get(
            "score",
            50
        )

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        return (
            career,
            score
        )

    except Exception as error:

        print(
            "MODEL PREDICTION ERROR:",
            error
        )

        return (
            "Data Analyst",
            50
        )


# ============================================================
# GET TOP CAREER RECOMMENDATIONS
# ============================================================

def get_top_careers(
    education,
    skills,
    interests,
    experience,
    career_domain=""
):

    return recommend_careers(

        skills=skills,

        education=education,

        interests=interests,

        experience=experience,

        career_domain=career_domain

    )


# ============================================================
# TEST MODEL
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("       AI CAREER PATH - MODEL TEST")
    print("==============================================")

    test_skills = (
        "Python, SQL, Machine Learning"
    )

    test_education = "BSc IT"

    test_interests = "Data"

    test_experience = "Fresher"

    test_domain = "Data Science"

    print()
    print("INPUT")
    print("----------------------------------------------")

    print(
        "Education:",
        test_education
    )

    print(
        "Skills:",
        test_skills
    )

    print(
        "Interest:",
        test_interests
    )

    print(
        "Experience:",
        test_experience
    )

    print(
        "Domain:",
        test_domain
    )

    print()
    print("MODEL RESULTS")
    print("----------------------------------------------")

    results = recommend_careers(

        skills=test_skills,

        education=test_education,

        interests=test_interests,

        experience=test_experience,

        career_domain=test_domain

    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print()

        print(
            index,
            ".",
            result["career"]
        )

        print(
            "Score:",
            result["score"],
            "%"
        )

        print(
            "Domain:",
            result["domain"]
        )

        print(
            "Matched:",
            result["matched"]
        )

        print(
            "Keywords:",
            result["keywords"]
        )

    print()
    print("==============================================")
    print("BEST CAREER")
    print("==============================================")

    career, score = predict_career(

        test_education,

        test_skills,

        test_interests,

        test_experience,

        test_domain

    )

    print(
        "Career:",
        career
    )

    print(
        "Score:",
        score,
        "%"
    )

    print("==============================================")