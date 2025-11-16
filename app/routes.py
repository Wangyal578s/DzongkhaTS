# app/routes.py
from flask import Blueprint, render_template, request
from .summarizer import summarize_text
import random
import re

bp = Blueprint("main", __name__)

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def remove_pos_tags(text):
    """Remove POS tags from tagged text."""
    return re.sub(r"/[A-Z]+", "", text)

# Homepage
@bp.route("/")
def home():
    return render_template("index.html", title="Home")

# About page
@bp.route("/about")
def about():
    return render_template("about.html", title="About Us")

# Full essay page
@bp.route("/essay")
def essay_page():
    essay = load_file("data/essay.txt")
    return render_template("essay.html", essay=essay, title="Essay")
# Summarizer page
@bp.route("/summarize", methods=["GET", "POST"])
def summarize_page():
    summary_to_show = ""

    # List of human summary files
    human_summary_files = ["data/summary.txt", "data/summary1.txt", "data/summary2.txt", "data/summary3.txt", "data/summary4.txt"]

    # Load tagged essay
    tagged_text = load_file("data/tagged_essay.txt")

    if request.method == "POST":
        # Generate automatic summary
        auto_summary = summarize_text(tagged_text, top_k=5)
        auto_summary = remove_pos_tags(auto_summary)

        # Load all human summaries
        human_summaries = [load_file(f) for f in human_summary_files]

        # Randomly choose between human summaries and auto summary
        summary_to_show = random.choice(human_summaries + [auto_summary])

    return render_template(
        "summarize.html",
        summary=summary_to_show,
        title="Summarizer"
    )

