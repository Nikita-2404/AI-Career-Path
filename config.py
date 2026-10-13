import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "ai-career-path-secret-key"

DATABASE = os.path.join(BASE_DIR, "career.db")

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "career_model.pkl"
)