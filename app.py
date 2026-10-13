# ============================================================
# AI CAREER PATH
# Flask Application
# MySQL + Career Recommendation System
# ============================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

import os
from functools import wraps

from db import (
    fetch_one,
    fetch_all,
    execute_query
)

from ml_model import predict_career


# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "ai-career-path-secret-key-2026"
)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# PROFILE UPLOAD CONFIGURATION
# ============================================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads",
    "profile_photos"
)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = (
    5 * 1024 * 1024
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# LOGIN REQUIRED
# ============================================================

def login_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login first.",
                "warning"
            )

            return redirect(
                url_for("user_login")
            )

        return function(*args, **kwargs)

    return decorated_function


# ============================================================
# ADMIN REQUIRED
# ============================================================

def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "admin_id" not in session:

            flash(
                "Please login as administrator.",
                "warning"
            )

            return redirect(
                url_for("admin_login")
            )

        return function(*args, **kwargs)

    return decorated_function


# ============================================================
# ALLOWED FILE
# ============================================================

def allowed_file(filename):

    if not filename:
        return False

    return (
        "."
        in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# USER REGISTRATION
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        education = request.form.get(
            "education",
            ""
        ).strip()

        if not name:

            flash(
                "Please enter your name.",
                "warning"
            )

            return redirect(
                url_for("register")
            )

        if not email:

            flash(
                "Please enter your email.",
                "warning"
            )

            return redirect(
                url_for("register")
            )

        if not password:

            flash(
                "Please enter a password.",
                "warning"
            )

            return redirect(
                url_for("register")
            )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        existing_user = fetch_one(
            """
            SELECT id
            FROM users
            WHERE LOWER(TRIM(email))
                  = LOWER(TRIM(%s))
            LIMIT 1
            """,
            (email,)
        )

        if existing_user:

            flash(
                "Email is already registered.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        hashed_password = generate_password_hash(
            password
        )

        try:

            execute_query(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password,
                    education,
                    skills,
                    interests,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    name,
                    email,
                    hashed_password,
                    education,
                    "",
                    "",
                    "Active"
                )
            )

        except Exception as error:

            print(
                "REGISTRATION ERROR:",
                error
            )

            flash(
                "Registration failed. Please check the terminal.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("user_login")
        )

    return render_template(
        "register.html"
    )


# ============================================================
# USER LOGIN
# ============================================================

@app.route(
    "/user/login",
    methods=["GET", "POST"]
)
def user_login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not email or not password:

            flash(
                "Please enter email and password.",
                "warning"
            )

            return redirect(
                url_for("user_login")
            )

        user = fetch_one(
            """
            SELECT *
            FROM users
            WHERE LOWER(TRIM(email))
                  = LOWER(TRIM(%s))
            LIMIT 1
            """,
            (email,)
        )

        if not user:

            flash(
                "Invalid email or password.",
                "danger"
            )

            return redirect(
                url_for("user_login")
            )

        stored_password = str(
            user.get("password") or ""
        ).strip()

        password_valid = False

        if stored_password:

            try:

                password_valid = check_password_hash(
                    stored_password,
                    password
                )

            except Exception:

                password_valid = False

        if not password_valid:

            if stored_password == password:

                password_valid = True

                try:

                    new_hashed_password = (
                        generate_password_hash(
                            password
                        )
                    )

                    execute_query(
                        """
                        UPDATE users
                        SET password = %s
                        WHERE id = %s
                        """,
                        (
                            new_hashed_password,
                            user["id"]
                        )
                    )

                except Exception as error:

                    print(
                        "PASSWORD HASH UPDATE ERROR:",
                        error
                    )

        if not password_valid:

            flash(
                "Invalid email or password.",
                "danger"
            )

            return redirect(
                url_for("user_login")
            )

        user_status = str(
            user.get("status") or "Active"
        ).strip().lower()

        if user_status == "inactive":

            flash(
                "Your account has been deactivated.",
                "danger"
            )

            return redirect(
                url_for("user_login")
            )

        session.clear()

        session["user_id"] = user["id"]

        session["user_name"] = user["name"]

        session["user_email"] = user["email"]

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "user_login.html"
    )


# ============================================================
# USER LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("user_login")
    )


# ============================================================
# USER DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    user_id = session["user_id"]

    user = fetch_one(
        """
        SELECT *
        FROM users
        WHERE id = %s
        LIMIT 1
        """,
        (user_id,)
    )

    if not user:

        session.clear()

        return redirect(
            url_for("user_login")
        )

    # ========================================================
    # PROFILE COMPLETION
    # ========================================================

    profile_fields = [
        user.get("name"),
        user.get("email"),
        user.get("education"),
        user.get("skills"),
        user.get("interests"),
        user.get("phone"),
        user.get("location"),
        user.get("experience"),
        user.get("about"),
        user.get("linkedin"),
        user.get("github")
    ]

    completed_fields = 0

    for value in profile_fields:

        if (
            value is not None
            and str(value).strip() != ""
            and str(value).strip().lower()
            not in ["none", "null"]
        ):

            completed_fields += 1

    profile_completion = round(
        (
            completed_fields /
            len(profile_fields)
        ) * 100
    )

    profile_completion = max(
        0,
        min(
            100,
            profile_completion
        )
    )

    total_result = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM predictions
        WHERE user_id = %s
        """,
        (user_id,)
    )

    total_predictions = (
        total_result["total"]
        if total_result
        else 0
    )

    average_result = fetch_one(
        """
        SELECT AVG(score) AS average_score
        FROM predictions
        WHERE user_id = %s
        """,
        (user_id,)
    )

    average_score = 0

    if average_result:

        average_score = (
            average_result["average_score"]
            or 0
        )

    latest_prediction = fetch_one(
        """
        SELECT *
        FROM predictions
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    career_distribution = fetch_all(
        """
        SELECT
            TRIM(career) AS career,
            COUNT(*) AS total
        FROM predictions
        WHERE user_id = %s
        AND career IS NOT NULL
        AND TRIM(career) != ''
        GROUP BY TRIM(career)
        ORDER BY total DESC
        """,
        (user_id,)
    )

    recent_predictions = fetch_all(
        """
        SELECT *
        FROM predictions
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 5
        """,
        (user_id,)
    )

    return render_template(
        "user/dashboard.html",
        user=user,
        total_predictions=total_predictions,
        average_score=round(
            float(average_score),
            2
        ),
        latest_prediction=latest_prediction,
        career_distribution=career_distribution,
        recent_predictions=recent_predictions,
        profile_completion=profile_completion,
        profile_percent=profile_completion
    )


# ============================================================
# ROADMAP
# ============================================================

@app.route("/roadmap")
@login_required
def roadmap():

    return render_template(
        "user/roadmap.html"
    )


# ============================================================
# USER PROFILE
# ============================================================

@app.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    user_id = session["user_id"]

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        education = request.form.get(
            "education",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        interests = request.form.get(
            "interests",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        experience = request.form.get(
            "experience",
            ""
        ).strip()

        about = request.form.get(
            "about",
            request.form.get(
                "bio",
                ""
            )
        ).strip()

        linkedin = request.form.get(
            "linkedin",
            ""
        ).strip()

        github = request.form.get(
            "github",
            ""
        ).strip()

        if not name:

            flash(
                "Name is required.",
                "warning"
            )

            return redirect(
                url_for(
                    "profile",
                    edit=1
                )
            )

        if not email:

            flash(
                "Email is required.",
                "warning"
            )

            return redirect(
                url_for(
                    "profile",
                    edit=1
                )
            )

        duplicate_user = fetch_one(
            """
            SELECT id
            FROM users
            WHERE LOWER(TRIM(email))
                  = LOWER(TRIM(%s))
            AND id != %s
            LIMIT 1
            """,
            (
                email,
                user_id
            )
        )

        if duplicate_user:

            flash(
                "This email is already used by another account.",
                "danger"
            )

            return redirect(
                url_for(
                    "profile",
                    edit=1
                )
            )

        try:

            execute_query(
                """
                UPDATE users
                SET
                    name = %s,
                    email = %s,
                    education = %s,
                    skills = %s,
                    interests = %s,
                    phone = %s,
                    location = %s,
                    experience = %s,
                    about = %s,
                    linkedin = %s,
                    github = %s
                WHERE id = %s
                """,
                (
                    name,
                    email,
                    education,
                    skills,
                    interests,
                    phone,
                    location,
                    experience,
                    about,
                    linkedin,
                    github,
                    user_id
                )
            )

        except Exception as error:

            print(
                "PROFILE UPDATE ERROR:",
                error
            )

            flash(
                "Unable to update profile. Check the terminal.",
                "danger"
            )

            return redirect(
                url_for(
                    "profile",
                    edit=1
                )
            )

        image = request.files.get(
            "profile_image"
        )

        if image and image.filename:

            if allowed_file(
                image.filename
            ):

                original_filename = secure_filename(
                    image.filename
                )

                extension = (
                    original_filename
                    .rsplit(
                        ".",
                        1
                    )[1]
                    .lower()
                )

                new_filename = (
                    f"user_{user_id}.{extension}"
                )

                image_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    new_filename
                )

                try:

                    image.save(
                        image_path
                    )

                    execute_query(
                        """
                        UPDATE users
                        SET profile_image = %s
                        WHERE id = %s
                        """,
                        (
                            new_filename,
                            user_id
                        )
                    )

                except Exception as error:

                    print(
                        "PROFILE IMAGE ERROR:",
                        error
                    )

                    flash(
                        "Profile saved, but image upload failed.",
                        "warning"
                    )

            else:

                flash(
                    "Invalid image format. Use JPG, JPEG, PNG or WEBP.",
                    "warning"
                )

        session["user_name"] = name

        session["user_email"] = email

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("profile")
        )

    user = fetch_one(
        """
        SELECT *
        FROM users
        WHERE id = %s
        LIMIT 1
        """,
        (user_id,)
    )

    return render_template(
        "user/profile.html",
        user=user
    )


# ============================================================
# PROFILE IMAGE
# ============================================================

@app.route(
    "/profile-image/<filename>"
)
@login_required
def profile_image(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ============================================================
# PREDICTION PAGE
# ============================================================

@app.route(
    "/prediction",
    methods=["GET", "POST"]
)
@login_required
def prediction():

    if request.method == "POST":

        return process_prediction()

    user = fetch_one(
        """
        SELECT *
        FROM users
        WHERE id = %s
        LIMIT 1
        """,
        (
            session["user_id"],
        )
    )

    return render_template(
        "user/prediction.html",
        user=user
    )


# ============================================================
# PROCESS CAREER PREDICTION
# ============================================================

def process_prediction():

    education = request.form.get(
        "education",
        ""
    ).strip()

    experience = request.form.get(
        "experience",
        ""
    ).strip()

    career_domain = request.form.get(
        "career_domain",
        ""
    ).strip()

    interests = request.form.get(
        "interests",
        ""
    ).strip()

    skill1 = request.form.get(
        "skill1",
        ""
    ).strip()

    skill2 = request.form.get(
        "skill2",
        ""
    ).strip()

    skill3 = request.form.get(
        "skill3",
        ""
    ).strip()

    old_skills = request.form.get(
        "skills",
        ""
    ).strip()

    skills_list = []

    if skill1:
        skills_list.append(skill1)

    if skill2:
        skills_list.append(skill2)

    if skill3:
        skills_list.append(skill3)

    if skills_list:

        skills = ", ".join(
            skills_list
        )

    else:

        skills = old_skills

    if not education:

        flash(
            "Please select your education.",
            "warning"
        )

        return redirect(
            url_for("prediction")
        )

    if not experience:

        flash(
            "Please select your experience.",
            "warning"
        )

        return redirect(
            url_for("prediction")
        )

    if not career_domain:

        flash(
            "Please select your career domain.",
            "warning"
        )

        return redirect(
            url_for("prediction")
        )

    if not interests:

        flash(
            "Please select your career interest.",
            "warning"
        )

        return redirect(
            url_for("prediction")
        )

    if not skills:

        flash(
            "Please select at least one skill.",
            "warning"
        )

        return redirect(
            url_for("prediction")
        )

    # ========================================================
    # CAREER PREDICTION
    # FIXED:
    # predict_career() is returning a tuple in the current
    # ml_model.py. This code now handles dictionary, tuple
    # and list results safely.
    # ========================================================

    try:

        prediction_result = predict_career(
            skills=skills,
            education=education,
            interests=interests,
            experience=experience
        )

        print(
            "MODEL PREDICTION RESULT:",
            prediction_result
        )

        if prediction_result is None:

            raise ValueError(
                "No career recommendations were returned."
            )

        careers = []

        # ----------------------------------------------------
        # CASE 1: MODEL RETURNS DICTIONARY
        # ----------------------------------------------------

        if isinstance(
            prediction_result,
            dict
        ):

            careers = prediction_result.get(
                "results",
                []
            )

            if not careers:

                career_value = prediction_result.get(
                    "career"
                )

                score_value = prediction_result.get(
                    "score",
                    0
                )

                if career_value:

                    careers = [
                        {
                            "career": career_value,
                            "score": score_value
                        }
                    ]

        # ----------------------------------------------------
        # CASE 2: MODEL RETURNS TUPLE
        # ----------------------------------------------------

        elif isinstance(
            prediction_result,
            tuple
        ):

            # Example:
            # ("Data Analyst", 85.5)

            if (
                len(prediction_result) >= 2
                and isinstance(
                    prediction_result[0],
                    str
                )
            ):

                career_value = (
                    prediction_result[0]
                )

                score_value = (
                    prediction_result[1]
                )

                careers = [
                    {
                        "career": career_value,
                        "score": score_value
                    }
                ]

            # Example:
            # ([{"career": "...", "score": 90}], ...)
            elif (
                len(prediction_result) >= 1
                and isinstance(
                    prediction_result[0],
                    list
                )
            ):

                careers = (
                    prediction_result[0]
                )

            # Example:
            # (career, score, results)
            elif len(prediction_result) >= 3:

                career_value = (
                    prediction_result[0]
                )

                score_value = (
                    prediction_result[1]
                )

                result_value = (
                    prediction_result[2]
                )

                if isinstance(
                    result_value,
                    list
                ):

                    careers = result_value

                elif career_value:

                    careers = [
                        {
                            "career": career_value,
                            "score": score_value
                        }
                    ]

        # ----------------------------------------------------
        # CASE 3: MODEL RETURNS LIST
        # ----------------------------------------------------

        elif isinstance(
            prediction_result,
            list
        ):

            careers = prediction_result

        # ----------------------------------------------------
        # VALIDATE RESULTS
        # ----------------------------------------------------

        if not careers:

            raise ValueError(
                "No career results were returned by the model."
            )

        # ----------------------------------------------------
        # CLEAN CAREER RESULTS
        # ----------------------------------------------------

        cleaned_careers = []

        for item in careers:

            if isinstance(
                item,
                dict
            ):

                career_name = item.get(
                    "career",
                    "Data Analyst"
                )

                career_score = item.get(
                    "score",
                    0
                )

                cleaned_careers.append(
                    {
                        "career": career_name,
                        "score": career_score
                    }
                )

            elif isinstance(
                item,
                tuple
            ):

                if len(item) >= 2:

                    cleaned_careers.append(
                        {
                            "career": item[0],
                            "score": item[1]
                        }
                    )

            elif isinstance(
                item,
                str
            ):

                cleaned_careers.append(
                    {
                        "career": item,
                        "score": 0
                    }
                )

        careers = cleaned_careers

        if not careers:

            raise ValueError(
                "Career results could not be processed."
            )

        # ----------------------------------------------------
        # BEST CAREER
        # ----------------------------------------------------

        best = careers[0]

        career = best.get(
            "career",
            "Data Analyst"
        )

        score = best.get(
            "score",
            0
        )

    except Exception as error:

        print(
            "CAREER PREDICTION ERROR:",
            error
        )

        flash(
            "Career prediction failed. Check the Flask terminal.",
            "danger"
        )

        return redirect(
            url_for("prediction")
        )

    # ========================================================
    # SCORE
    # ========================================================

    try:

        score = float(
            score
        )

    except Exception:

        score = 0

    score = max(
        0,
        min(
            100,
            score
        )
    )

    # ========================================================
    # SAVE PREDICTION
    # ========================================================

    try:

        execute_query(
            """
            INSERT INTO predictions
            (
                user_id,
                education,
                skills,
                interests,
                experience,
                career,
                score
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                session["user_id"],
                education,
                skills,
                interests,
                experience,
                career,
                score
            )
        )

    except Exception as error:

        print(
            "PREDICTION DATABASE ERROR:",
            error
        )

        flash(
            "Prediction generated but could not be saved.",
            "warning"
        )

    # ========================================================
    # UPDATE USER INFORMATION
    # ========================================================

    try:

        execute_query(
            """
            UPDATE users
            SET
                education = %s,
                skills = %s,
                interests = %s
            WHERE id = %s
            """,
            (
                education,
                skills,
                interests,
                session["user_id"]
            )
        )

    except Exception as error:

        print(
            "USER UPDATE ERROR:",
            error
        )

    # ========================================================
    # GET USER
    # ========================================================

    user = fetch_one(
        """
        SELECT *
        FROM users
        WHERE id = %s
        LIMIT 1
        """,
        (
            session["user_id"],
        )
    )

    # ========================================================
    # RESULT PAGE
    # ========================================================

    return render_template(
        "user/result.html",
        user=user,
        career=career,
        score=score,
        careers=careers,
        education=education,
        skills=skills,
        interests=interests,
        experience=experience,
        career_domain=career_domain
    )


# ============================================================
# PREDICT ALIAS
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
@login_required
def predict():

    return process_prediction()


# ============================================================
# HISTORY
# ============================================================

@app.route("/history")
@login_required
def history():

    predictions = fetch_all(
        """
        SELECT *
        FROM predictions
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (
            session["user_id"],
        )
    )

    return render_template(
        "user/history.html",
        predictions=predictions
    )


# ============================================================
# DELETE HISTORY
# ============================================================

@app.route(
    "/history/delete/<int:prediction_id>",
    methods=["POST"]
)
@login_required
def delete_prediction(
    prediction_id
):

    prediction = fetch_one(
        """
        SELECT id
        FROM predictions
        WHERE id = %s
        AND user_id = %s
        LIMIT 1
        """,
        (
            prediction_id,
            session["user_id"]
        )
    )

    if not prediction:

        flash(
            "Prediction not found.",
            "warning"
        )

        return redirect(
            url_for("history")
        )

    try:

        execute_query(
            """
            DELETE FROM predictions
            WHERE id = %s
            AND user_id = %s
            """,
            (
                prediction_id,
                session["user_id"]
            )
        )

        flash(
            "Prediction deleted successfully.",
            "success"
        )

    except Exception as error:

        print(
            "DELETE PREDICTION ERROR:",
            error
        )

        flash(
            "Unable to delete prediction.",
            "danger"
        )

    return redirect(
        url_for("history")
    )


# ============================================================
# USER JOBS
# ============================================================

@app.route("/jobs")
@login_required
def jobs():

    jobs_data = fetch_all(
        """
        SELECT *
        FROM jobs
        ORDER BY id DESC
        """
    )

    return render_template(
        "user/jobs.html",
        jobs=jobs_data
    )


# ============================================================
# USER JOB DETAIL
# ============================================================

@app.route(
    "/jobs/<int:job_id>",
    endpoint="job_detail"
)
@login_required
def job_detail(job_id):

    job = fetch_one(
        """
        SELECT *
        FROM jobs
        WHERE id = %s
        LIMIT 1
        """,
        (job_id,)
    )

    if not job:

        flash(
            "Job not found.",
            "warning"
        )

        return redirect(
            url_for("jobs")
        )

    application = fetch_one(
        """
        SELECT *
        FROM applications
        WHERE user_id = %s
        AND job_id = %s
        LIMIT 1
        """,
        (
            session["user_id"],
            job_id
        )
    )

    return render_template(
        "user/job_detail.html",
        job=job,
        application=application
    )


# ============================================================
# JOB DETAIL ALIAS
# ============================================================

@app.route(
    "/job/<int:job_id>"
)
@login_required
def job_detail_alias(job_id):

    return redirect(
        url_for(
            "job_detail",
            job_id=job_id
        )
    )


# ============================================================
# APPLY JOB
# ============================================================

@app.route(
    "/jobs/<int:job_id>/apply",
    methods=["GET", "POST"]
)
@login_required
def apply_job(job_id):

    job = fetch_one(
        """
        SELECT *
        FROM jobs
        WHERE id = %s
        LIMIT 1
        """,
        (job_id,)
    )

    if not job:

        flash(
            "Job not found.",
            "warning"
        )

        return redirect(
            url_for("jobs")
        )

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        education = request.form.get(
            "education",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        experience = request.form.get(
            "experience",
            ""
        ).strip()

        existing = fetch_one(
            """
            SELECT *
            FROM applications
            WHERE user_id = %s
            AND job_id = %s
            LIMIT 1
            """,
            (
                session["user_id"],
                job_id
            )
        )

        if existing:

            flash(
                "You have already applied for this job.",
                "warning"
            )

            return redirect(
                url_for(
                    "job_detail",
                    job_id=job_id
                )
            )

        if not full_name:

            flash(
                "Please enter your full name.",
                "warning"
            )

            return render_template(
                "user/apply_job.html",
                job=job
            )

        if not email:

            flash(
                "Please enter your email.",
                "warning"
            )

            return render_template(
                "user/apply_job.html",
                job=job
            )

        resume_filename = None

        resume = request.files.get(
            "resume"
        )

        if resume and resume.filename:

            resume_name = secure_filename(
                resume.filename
            )

            if "." not in resume_name:

                flash(
                    "Invalid resume file.",
                    "danger"
                )

                return render_template(
                    "user/apply_job.html",
                    job=job
                )

            extension = (
                resume_name
                .rsplit(
                    ".",
                    1
                )[-1]
                .lower()
            )

            allowed_resume_extensions = {
                "pdf",
                "doc",
                "docx"
            }

            if (
                extension
                not in allowed_resume_extensions
            ):

                flash(
                    "Invalid resume format. Use PDF, DOC or DOCX.",
                    "danger"
                )

                return render_template(
                    "user/apply_job.html",
                    job=job
                )

            resume_folder = os.path.join(
                BASE_DIR,
                "static",
                "uploads",
                "resumes"
            )

            os.makedirs(
                resume_folder,
                exist_ok=True
            )

            resume_filename = (
                f"user_{session['user_id']}"
                f"_job_{job_id}."
                f"{extension}"
            )

            resume_path = os.path.join(
                resume_folder,
                resume_filename
            )

            try:

                resume.save(
                    resume_path
                )

            except Exception as error:

                print(
                    "RESUME SAVE ERROR:",
                    error
                )

                flash(
                    "Unable to upload resume.",
                    "danger"
                )

                return render_template(
                    "user/apply_job.html",
                    job=job
                )

        try:

            execute_query(
                """
                INSERT INTO applications
                (
                    user_id,
                    job_id,
                    full_name,
                    email,
                    phone,
                    education,
                    skills,
                    experience,
                    resume,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    session["user_id"],
                    job_id,
                    full_name,
                    email,
                    phone,
                    education,
                    skills,
                    experience,
                    resume_filename,
                    "Applied"
                )
            )

        except Exception as error:

            print(
                "APPLICATION ERROR:",
                error
            )

            flash(
                "Unable to submit application.",
                "danger"
            )

            return redirect(
                url_for(
                    "job_detail",
                    job_id=job_id
                )
            )

        return render_template(
            "user/application_success.html",
            job=job
        )

    user = fetch_one(
        """
        SELECT *
        FROM users
        WHERE id = %s
        LIMIT 1
        """,
        (
            session["user_id"],
        )
    )

    return render_template(
        "user/apply_job.html",
        job=job,
        user=user
    )


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        print(
            "================================"
        )

        print(
            "ADMIN LOGIN ATTEMPT"
        )

        print(
            "USERNAME:",
            repr(username)
        )

        print(
            "PASSWORD LENGTH:",
            len(password)
        )

        print(
            "================================"
        )

        if (
            username.lower() == "admin"
            and
            password == "admin123"
        ):

            session.clear()

            session["admin_id"] = 1

            session["admin_username"] = "admin"

            flash(
                "Admin login successful.",
                "success"
            )

            return redirect(
                url_for("admin_dashboard")
            )

        flash(
            "Invalid admin username or password.",
            "danger"
        )

        return redirect(
            url_for("admin_login")
        )

    return render_template(
        "admin_login.html"
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    flash(
        "Admin logged out successfully.",
        "success"
    )

    return redirect(
        url_for("admin_login")
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():

    users_result = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM users
        """
    )

    total_users = (
        int(users_result["total"])
        if users_result
        else 0
    )

    predictions_result = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM predictions
        """
    )

    total_predictions = (
        int(predictions_result["total"])
        if predictions_result
        else 0
    )

    jobs_result = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM jobs
        """
    )

    total_jobs = (
        int(jobs_result["total"])
        if jobs_result
        else 0
    )

    applications_result = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM applications
        """
    )

    total_applications = (
        int(applications_result["total"])
        if applications_result
        else 0
    )

    recent_predictions = fetch_all(
        """
        SELECT
            p.*,
            u.name,
            u.email
        FROM predictions p
        LEFT JOIN users u
            ON p.user_id = u.id
        ORDER BY p.id DESC
        LIMIT 10
        """
    )

    prediction_career_rows = fetch_all(
        """
        SELECT career
        FROM predictions
        WHERE career IS NOT NULL
        """
    )

    career_counts = {}

    for row in prediction_career_rows:

        career_name = row.get(
            "career"
        )

        if career_name is None:
            continue

        career_name = str(
            career_name
        ).strip()

        if not career_name:
            continue

        if career_name in career_counts:

            career_counts[career_name] += 1

        else:

            career_counts[career_name] = 1

    sorted_careers = sorted(
        career_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    career_rows = []

    for career_name, total in sorted_careers:

        career_rows.append(
            {
                "career": career_name,
                "total": total
            }
        )

    career_chart_data = []

    for career_name, total in sorted_careers:

        career_chart_data.append(
            {
                "label": career_name,
                "value": total
            }
        )

    top_career = "No Data"

    if sorted_careers:

        top_career = sorted_careers[0][0]

    career_options = len(
        sorted_careers
    )

    prediction_count = total_predictions

    education_rows = fetch_all(
        """
        SELECT education
        FROM users
        WHERE education IS NOT NULL
        AND TRIM(education) != ''
        """
    )

    education_counts = {}

    for row in education_rows:

        education_name = row.get(
            "education"
        )

        if education_name is None:
            continue

        education_name = str(
            education_name
        ).strip()

        if not education_name:
            continue

        if education_name in education_counts:

            education_counts[
                education_name
            ] += 1

        else:

            education_counts[
                education_name
            ] = 1

    sorted_education = sorted(
        education_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    education_chart_data = []

    for education_name, total in sorted_education:

        education_chart_data.append(
            {
                "label": education_name,
                "value": total
            }
        )

    return render_template(
        "admin/dashboard.html",

        total_users=total_users,

        total_predictions=total_predictions,

        total_jobs=total_jobs,

        total_applications=total_applications,

        recent_predictions=recent_predictions,

        career_rows=career_rows,

        career_distribution=career_chart_data,

        career_chart_data=career_chart_data,

        top_career=top_career,

        career_options=career_options,

        prediction_count=prediction_count,

        education_chart_data=education_chart_data
    )


# ============================================================
# ADMIN USERS
# ============================================================

@app.route("/admin/users")
@admin_required
def admin_users():

    users = fetch_all(
        """
        SELECT *
        FROM users
        ORDER BY id DESC
        """
    )

    return render_template(
        "admin/users.html",
        users=users
    )


# ============================================================
# ADMIN USER DETAIL
# ============================================================

@app.route(
    "/admin/users/<int:user_id>"
)
@admin_required
def admin_user_detail(user_id):

    user = fetch_one(
        """
        SELECT *
        FROM users
        WHERE id = %s
        LIMIT 1
        """,
        (user_id,)
    )

    if not user:

        flash(
            "User not found.",
            "warning"
        )

        return redirect(
            url_for("admin_users")
        )

    predictions = fetch_all(
        """
        SELECT *
        FROM predictions
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (user_id,)
    )

    return render_template(
        "admin/user_detail.html",
        user=user,
        predictions=predictions
    )


# ============================================================
# ADMIN USER STATUS
# ============================================================

@app.route(
    "/admin/users/<int:user_id>/status",
    methods=["POST"]
)
@admin_required
def admin_user_status(user_id):

    status = request.form.get(
        "status",
        "Active"
    ).strip()

    if status not in {
        "Active",
        "Inactive"
    }:

        status = "Active"

    try:

        execute_query(
            """
            UPDATE users
            SET status = %s
            WHERE id = %s
            """,
            (
                status,
                user_id
            )
        )

        flash(
            "User status updated successfully.",
            "success"
        )

    except Exception as error:

        print(
            "USER STATUS ERROR:",
            error
        )

        flash(
            "Unable to update user status.",
            "danger"
        )

    return redirect(
        url_for("admin_users")
    )


# ============================================================
# ADMIN PREDICTIONS
# ============================================================

@app.route("/admin/predictions")
@admin_required
def admin_predictions():

    predictions = fetch_all(
        """
        SELECT
            p.*,
            u.name,
            u.email
        FROM predictions p
        LEFT JOIN users u
            ON p.user_id = u.id
        ORDER BY p.id DESC
        """
    )

    return render_template(
        "admin/predictions.html",
        predictions=predictions
    )


# ============================================================
# ADMIN ANALYTICS
# ============================================================

@app.route("/admin/analytics")
@admin_required
def admin_analytics():

    prediction_rows = fetch_all(
        """
        SELECT career
        FROM predictions
        WHERE career IS NOT NULL
        """
    )

    career_counts = {}

    for row in prediction_rows:

        career = row.get(
            "career"
        )

        if career is None:
            continue

        career = str(
            career
        ).strip()

        if not career:
            continue

        career_counts[career] = (
            career_counts.get(
                career,
                0
            ) + 1
        )

    sorted_careers = sorted(
        career_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rows = []

    for career, total in sorted_careers:

        rows.append(
            {
                "career": career,
                "total": total
            }
        )

    education_data = fetch_all(
        """
        SELECT education
        FROM users
        WHERE education IS NOT NULL
        AND TRIM(education) != ''
        """
    )

    education_counts = {}

    for row in education_data:

        education = row.get(
            "education"
        )

        if education is None:
            continue

        education = str(
            education
        ).strip()

        if not education:
            continue

        education_counts[education] = (
            education_counts.get(
                education,
                0
            ) + 1
        )

    sorted_education = sorted(
        education_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    education_rows = []

    for education, total in sorted_education:

        education_rows.append(
            {
                "education": education,
                "total": total
            }
        )

    return render_template(
        "admin/analytics.html",
        rows=rows,
        education_rows=education_rows
    )


# ============================================================
# ADMIN JOBS
# ============================================================

@app.route(
    "/admin/jobs",
    methods=["GET", "POST"]
)
@admin_required
def admin_jobs():

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        company = request.form.get(
            "company",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        experience = request.form.get(
            "experience",
            ""
        ).strip()

        education = request.form.get(
            "education",
            ""
        ).strip()

        deadline = request.form.get(
            "deadline",
            ""
        ).strip()

        responsibilities = request.form.get(
            "responsibilities",
            ""
        ).strip()

        benefits = request.form.get(
            "benefits",
            ""
        ).strip()

        job_type = request.form.get(
            "job_type",
            ""
        ).strip()

        salary = request.form.get(
            "salary",
            ""
        ).strip()

        logo = request.form.get(
            "logo",
            ""
        ).strip()

        if not title or not company:

            flash(
                "Job title and company are required.",
                "warning"
            )

            return redirect(
                url_for("admin_jobs")
            )

        try:

            execute_query(
                """
                INSERT INTO jobs
                (
                    title,
                    company,
                    location,
                    skills,
                    description,
                    experience,
                    education,
                    deadline,
                    responsibilities,
                    benefits,
                    job_type,
                    salary,
                    logo
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    title,
                    company,
                    location,
                    skills,
                    description,
                    experience,
                    education,
                    deadline,
                    responsibilities,
                    benefits,
                    job_type,
                    salary,
                    logo
                )
            )

            flash(
                "Job added successfully.",
                "success"
            )

        except Exception as error:

            print(
                "ADMIN JOB ERROR:",
                error
            )

            flash(
                "Unable to add job.",
                "danger"
            )

        return redirect(
            url_for("admin_jobs")
        )

    jobs_data = fetch_all(
        """
        SELECT *
        FROM jobs
        ORDER BY id DESC
        """
    )

    return render_template(
        "admin/jobs.html",
        jobs=jobs_data
    )


# ============================================================
# ADMIN DELETE JOB
# ============================================================

@app.route(
    "/admin/jobs/<int:job_id>/delete",
    methods=["POST"]
)
@admin_required
def admin_delete_job(job_id):

    try:

        execute_query(
            """
            DELETE FROM applications
            WHERE job_id = %s
            """,
            (job_id,)
        )

        execute_query(
            """
            DELETE FROM jobs
            WHERE id = %s
            """,
            (job_id,)
        )

        flash(
            "Job deleted successfully.",
            "success"
        )

    except Exception as error:

        print(
            "DELETE JOB ERROR:",
            error
        )

        flash(
            "Unable to delete job.",
            "danger"
        )

    return redirect(
        url_for("admin_jobs")
    )


# ============================================================
# ADMIN APPLICATIONS
# ============================================================

@app.route("/admin/applications")
@admin_required
def admin_applications():

    applications = fetch_all(
        """
        SELECT
            a.*,
            j.title AS job_title,
            j.company,
            u.name AS user_name
        FROM applications a
        LEFT JOIN jobs j
            ON a.job_id = j.id
        LEFT JOIN users u
            ON a.user_id = u.id
        ORDER BY a.id DESC
        """
    )

    return render_template(
        "admin/applications.html",
        applications=applications
    )


# ============================================================
# ADMIN APPLICATION STATUS
# ============================================================

@app.route(
    "/admin/applications/<int:application_id>/status",
    methods=["POST"]
)
@admin_required
def admin_application_status(
    application_id
):

    status = request.form.get(
        "status",
        "Applied"
    ).strip()

    allowed_statuses = {
        "Applied",
        "Reviewing",
        "Shortlisted",
        "Rejected",
        "Selected"
    }

    if status not in allowed_statuses:

        status = "Applied"

    try:

        execute_query(
            """
            UPDATE applications
            SET status = %s
            WHERE id = %s
            """,
            (
                status,
                application_id
            )
        )

        flash(
            "Application status updated.",
            "success"
        )

    except Exception as error:

        print(
            "APPLICATION STATUS ERROR:",
            error
        )

        flash(
            "Unable to update application status.",
            "danger"
        )

    return redirect(
        url_for("admin_applications")
    )


# ============================================================
# RESUME DOWNLOAD
# ============================================================

@app.route(
    "/resume/<filename>"
)
@admin_required
def download_resume(filename):

    resume_folder = os.path.join(
        BASE_DIR,
        "static",
        "uploads",
        "resumes"
    )

    return send_from_directory(
        resume_folder,
        filename,
        as_attachment=True
    )


# ============================================================
# 404 ERROR
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "index.html"
    ), 404


# ============================================================
# 500 ERROR
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):

    print(
        "INTERNAL SERVER ERROR:",
        error
    )

    return (
        "<h2>Internal Server Error</h2>"
        "<p>Please check the Flask terminal "
        "for the exact error.</p>"
    ), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )