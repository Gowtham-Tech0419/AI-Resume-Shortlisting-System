# AI Resume Shortlisting System

An end-to-end AI-powered recruitment assistant that parses resumes, extracts skills, matches candidates against job descriptions, predicts candidate categories using machine learning, and presents everything through a recruiter-facing dashboard.

Built from scratch to demonstrate a complete pipeline spanning **backend engineering, NLP, classical machine learning, relational database design, and full-stack web development** — not a single-notebook demo, but a working, testable application.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Live Feature Overview](#live-feature-overview)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works — Pipeline Walkthrough](#how-it-works--pipeline-walkthrough)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Machine Learning Component](#machine-learning-component)
- [Database Schema](#database-schema)
- [Design Decisions Worth Knowing](#design-decisions-worth-knowing)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [What I Learned](#what-i-learned)

---

## Problem Statement

Large companies receive thousands of resumes per job opening. HR teams cannot manually review every application. This system automates the early screening funnel:

1. Reads and understands resumes (PDF text extraction + NLP)
2. Extracts candidate skills against a curated skill taxonomy
3. Predicts a likely job category using a trained ML classifier
4. Matches candidates against job descriptions on **skill coverage**, with content similarity as a secondary relevance signal
5. Presents ranked, filterable results with visual analytics on a recruiter dashboard

---

## Live Feature Overview

**For Candidates**
- Upload a PDF resume through a simple web form
- Immediate feedback: predicted job category and detected skills

**For HR**
- Paste and save a job description; required skills are extracted automatically
- Select any posted job from a dropdown — no need to know internal IDs
- View a ranked candidate dashboard per job, with:
  - Skill-match percentage per candidate (primary ranking metric)
  - Content-relevance percentage (secondary tie-breaking signal)
  - Predicted category per candidate
  - Pie chart: predicted category distribution
  - Bar chart: skill distribution across all applicants
  - Live client-side filtering by category

All three workflows — candidate upload, job posting, dashboard access — live on a **single home page**, with no full-page reloads for form submissions (implemented via the Fetch API).

---

## System Architecture

┌─────────────────────┐
                │     Home Page (UI)   │
                │  Upload | Post JD |   │
                │  View Dashboard       │
                └──────────┬────────────┘
                           │ Fetch API (JSON)
                           ▼
                ┌─────────────────────┐
                │     Flask Routes      │
                └──────────┬────────────┘
                           │
    ┌──────────────────────┼───────────────────────┐
    ▼                      ▼                        ▼
    ┌───────────────┐ ┌───────────────────┐ ┌────────────────────┐
│ Resume Parser │ │ NLP Preprocessing │ │ Skill Extractor │
│ (PyMuPDF) │──▶│ (NLTK: clean, │──▶│ (Regex + JSON │
│ │ │ tokenize, lemmatize)│ │ skill database) │
└───────────────┘ └───────────────────┘ └──────────┬─────────┘
│
┌─────────────────────────────────────┘
▼
┌───────────────────────┐ ┌──────────────────────┐
│ TF-IDF Vectorization │ │ ML Classifier │
│ + Cosine Similarity │ │ (Naive Bayes / │
│ (content relevance) │ │ Logistic Regression) │
└───────────┬────────────┘ └──────────┬────────────┘
│ │
└───────────────┬──────────────┘
▼
┌───────────────────────┐
│ SQLite Database │
│ candidates | jobs | │
│ scores │
└───────────┬────────────┘
▼
┌───────────────────────┐
│ Recruiter Dashboard │
│ (Bootstrap + Chart.js) │
└───────────────────────┘
---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| PDF Parsing | PyMuPDF (fitz) |
| NLP | NLTK (tokenization, stopwords, lemmatization), Regex |
| Machine Learning | scikit-learn (TF-IDF, Naive Bayes, Logistic Regression) |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript (Fetch API), Bootstrap 5, Chart.js |
| Data Export | pandas, openpyxl |

---
---

## How It Works — Pipeline Walkthrough

**1. Resume Upload → Text Extraction**
A candidate uploads a PDF via the home page. PyMuPDF extracts raw text page by page.

**2. NLP Preprocessing**
Raw text is lowercased, symbol-bearing terms (`C++`, `Node.js`, `.NET`) are protected from corruption, punctuation is stripped, and the result is tokenized, stopword-filtered, and lemmatized.

**3. Skill Extraction**
Cleaned text is scanned against a 14-category, 150+ term skill taxonomy using word-boundary regex matching — preventing false positives like matching "java" inside "javascript."

**4. Category Prediction**
The cleaned text is vectorized and passed through a trained Naive Bayes / Logistic Regression classifier, predicting a likely job category (e.g., Data Scientist, Software Engineer, HR, Data Analyst).

**5. Job Description Processing**
HR pastes a job description through the same cleaning and skill-extraction pipeline, guaranteeing consistent preprocessing on both sides of any future comparison.

**6. Matching & Scoring**
When HR opens a dashboard for a job, every candidate without an existing score is evaluated using two independent signals:
- **Skill Match** (primary, headline score) — the proportion of required skills the candidate actually has
- **Content Relevance** (secondary, tie-breaking score) — TF-IDF cosine similarity between full resume text and job description text

**7. Dashboard Rendering**
Candidates are ranked by skill match (ties broken by content relevance), with category and skill distribution charts rendered via Chart.js, and live client-side filtering.

---

## Setup & Installation

```bash
git clone <your-repo-url>
cd resume_shortlisting_system

pip install -r requirements.txt

python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"

python -c "from utils.db_manager import initialize_database; initialize_database()"

python train_model.py

python app.py
```

Visit `http://127.0.0.1:5000/`

---

## Usage

1. **As a candidate**: open the home page, upload a PDF resume, view your predicted category and detected skills instantly.
2. **As HR**: switch to the "Post a Job" tab, paste a job description and title, save it.
3. **View results**: switch to the "View Dashboard" tab, select the job from the dropdown (auto-populated, including any job you just posted), click "View Dashboard" to see ranked candidates and analytics.

To export all data for offline review:
```bash
python export_to_excel.py
```
Produces a timestamped `.xlsx` file with Candidates, Jobs, and Scores as separate sheets.

---

## Machine Learning Component

This is the one genuinely trained, supervised ML piece of the system (everything else — skill extraction, TF-IDF, cosine similarity — is deterministic NLP/statistics, not machine learning).

- **Algorithms compared**: Multinomial Naive Bayes and Logistic Regression
- **Features**: TF-IDF vectors of cleaned resume text
- **Evaluation**: stratified train/test split, accuracy, confusion matrix, classification report
- **Data leakage prevention**: the vectorizer is fit exclusively on training data; test data is only ever `.transform()`-ed, never `.fit()`-ed

**Honest note on results**: with a training dataset using clearly separated, category-typical vocabulary across 48 labeled examples (12 per category), both models reach 100% test accuracy. This reflects the dataset's clean class separation rather than proof the model would generalize equally well to messier, real-world resumes with overlapping terminology (e.g., a Data Analyst resume mentioning "machine learning"). A production version would require a much larger, more ambiguous, real-world-sourced training set.

---

## Database Schema

```sql
candidates (id, name, resume_path, cleaned_text, predicted_category, detected_skills)
jobs (id, title, cleaned_text, required_skills)
scores (id, candidate_id [FK], job_id [FK], match_score, content_score)
```

- Foreign key constraints enforced via `PRAGMA foreign_keys = ON`
- All queries use parameterized statements (`?` placeholders) — no string-built SQL anywhere, preventing SQL injection
- `detected_skills` / `required_skills` are stored as JSON-encoded strings (SQLite has no native array type) and parsed back into Python lists on read

---

## Design Decisions Worth Knowing

**Why skill match, not a single blended score, drives ranking.**
An early version blended cosine similarity and skill overlap into one weighted average. Testing revealed this let weak textual similarity mask a perfect skill match — a candidate with 100% of required skills could still show well under 100% simply because their resume's overall prose didn't closely resemble a short, skill-only job description. Skill match and content relevance are now reported as two separate, clearly labeled metrics, with skill match as the primary sort key.

**Why symbol-bearing skills (C++, Node.js, .NET) get special handling.**
Naive punctuation stripping merges adjacent tokens (`"C++,Java"` → `"cjava"`), silently destroying valid skills. A `PROTECTED_TERMS` dictionary converts known symbol-bearing terms into safe placeholder tokens *before* general text cleaning runs, with a corresponding `DISPLAY_NAMES` mapping to show the correct formatted name back to the user.

**Why job descriptions reuse the exact same cleaning/skill-extraction functions as resumes.**
Consistent preprocessing is required for any valid comparison between two documents — if one side were cleaned differently, equivalent terms could fail to match.

**Why the database uses lazy, on-demand scoring rather than scoring at upload time.**
Candidates can upload resumes before a relevant job even exists. Scores are computed the first time HR views a dashboard for a given job, checking for and skipping any candidate/job pairs already scored, avoiding redundant computation on repeat visits.

---

## Known Limitations

- **Skill detection is exact-match only** — it cannot infer implied skills or recognize unlisted synonyms/abbreviations not already in the skill database.
- **Short/ambiguous skill names** (e.g., "Go," "R") risk false positives against common English words; the taxonomy favors more specific variants (`golang`, `rprogramming`) where possible, but this isn't a complete solution.
- **ML training data is small (48 examples)** and uses cleanly separated category vocabulary — real-world accuracy would likely be lower on ambiguous, overlapping resumes.
- **No authentication** — dashboard and job-posting routes are open to anyone with the URL.
- **SQLite is single-file, single-writer** — appropriate for a portfolio project, not for concurrent multi-user production traffic.
- **Client-side table filtering** doesn't scale gracefully to very large candidate counts.
- **A new TF-IDF vectorizer is fit per scoring batch** rather than reused from a large historical corpus, meaning IDF weights are relative only to the current comparison set.

---

## Future Improvements

- Replace exact-match skill extraction with embedding-based semantic matching for synonym/paraphrase detection
- Move to a normalized `candidate_skills` junction table for direct SQL-level skill analytics
- Add authentication and role-based access (candidate vs. HR)
- Migrate from SQLite to PostgreSQL for concurrent production use
- Expand training data significantly and adopt cross-validation over a single train/test split
- Add required-vs-preferred skill distinction in job description parsing

---

## What I Learned

Building this project end-to-end — rather than following a single tutorial — surfaced real engineering problems that don't appear in toy examples: a punctuation-stripping regex silently destroying skill names, a stratified split failing on too few samples per class, a naive scoring blend producing a "wrong" 100%-skill-match result, and the concrete difference between deterministic NLP/statistics and genuine trained machine learning. Each of these became a documented design decision rather than a hidden bug — which is, I think, the actual point of building a portfolio project instead of copying one.
