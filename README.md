# AI Resume Shortlisting System

An AI-powered recruitment application that helps HR teams screen resumes, identify candidate skills, predict job categories, and rank applicants against job descriptions.

Built using Python, Flask, Natural Language Processing (NLP), Machine Learning, and SQLite, this project demonstrates an end-to-end workflow from resume upload to recruiter-friendly candidate analytics.

## Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [System Architecture](#system-architecture)
* [Technology Stack](#technology-stack)
* [How It Works](#how-it-works)
* [Installation and Setup](#installation-and-setup)
* [How to Use](#how-to-use)
* [Machine Learning Model](#machine-learning-model)
* [Database Design](#database-design)
* [Important Design Decisions](#important-design-decisions)
* [Limitations](#limitations)
* [Future Improvements](#future-improvements)
* [Learning Outcomes](#learning-outcomes)
* [Author](#author)

## Overview

Recruiters often receive a large number of resumes for a single job opening. Manually reviewing every application can be time-consuming.

The AI Resume Shortlisting System simplifies the initial screening process by extracting information from PDF resumes, identifying relevant skills, predicting candidate job categories, and comparing candidates with job requirements.

The application provides a web-based interface where candidates can upload resumes and recruiters can create job descriptions, review ranked applicants, and explore recruitment analytics.

**The system uses two separate matching metrics:**

* **Skill Match:** Measures the percentage of required job skills identified in a candidate's resume.
* **Content Relevance:** Measures textual similarity between the resume and job description using TF-IDF and cosine similarity.

Skill Match is the primary ranking metric, while Content Relevance is used to break ties.

## Key Features

### Candidate Features

* Upload resumes in PDF format.
* Extract resume text automatically.
* Identify skills using a predefined skill database.
* Predict a likely job category using a trained machine learning model.
* View detected skills and the predicted category after processing.

### Recruiter Features

* Create and save job descriptions.
* Automatically extract required skills from job descriptions.
* Select a job from a dropdown menu.
* View candidates ranked by skill match.
* Compare skill match and content relevance scores.
* Filter candidates by predicted job category.
* Explore candidate category and skill distribution charts.
* Export candidate, job, and scoring data to Excel.

### Technical Features

* PDF text extraction using PyMuPDF.
* Text preprocessing using NLTK and regular expressions.
* Skill identification using word-boundary matching.
* Text vectorization and similarity calculation using TF-IDF and cosine similarity.
* Supervised job-category classification using scikit-learn.
* Persistent storage using SQLite.
* Asynchronous-feeling form interactions using the JavaScript Fetch API without full-page reloads for supported submissions.

## System Architecture

The following diagram shows how information flows through the application, from resume upload and job description entry to candidate ranking and dashboard visualization.
## System Architecture

```text
                 AI RESUME SHORTLISTING SYSTEM
                              |
                 +------------+------------+
                 |                         |
          Resume Upload              Job Description
                 |                         |
                 +------------+------------+
                              |
                              v
                     Flask Backend
                              |
                              v
                      Text Extraction
                     (PyMuPDF for PDF)
                              |
                              v
                      NLP Preprocessing
                  (NLTK and Regular Expressions)
                              |
                  +-----------+-----------+
                  |                       |
                  v                       v
            Skill Extraction       TF-IDF Vectorization
                  |                       |
                  v                       v
          Detected Candidate       ML Job Category
                Skills               Prediction
                  |                       |
                  +-----------+-----------+
                              |
                              v
                       SQLite Database
                  (Candidates, Jobs, Scores)
                              |
                              v
                      Matching Engine
                              |
                  +-----------+-----------+
                  |                       |
                  v                       v
             Skill Match             Content Relevance
             Percentage              (Cosine Similarity)
                  |                       |
                  +-----------+-----------+
                              |
                              v
                    Candidate Ranking
                              |
                              v
                    Recruiter Dashboard
                              |
                 +------------+------------+
                 |            |            |
                 v            v            v
             Ranked       Charts and    Excel Export
            Candidates     Filters
```

The architecture separates the main responsibilities of the application:

* **Flask Backend:** Handles user requests, resume uploads, job submissions, and application workflows.
* **NLP Pipeline:** Cleans text and extracts relevant skills.
* **Machine Learning Model:** Predicts a likely job category from resume text.
* **Matching Engine:** Calculates skill coverage and content similarity.
* **SQLite Database:** Stores candidate information, job descriptions, and matching scores.
* **Recruiter Dashboard:** Displays ranked candidates and recruitment analytics.

## Technology Stack

| Component                   | Technologies                                 |
| --------------------------- | -------------------------------------------- |
| Programming Language        | Python                                       |
| Backend Framework           | Flask                                        |
| PDF Processing              | PyMuPDF                                      |
| Natural Language Processing | NLTK, Regular Expressions                    |
| Machine Learning            | scikit-learn                                 |
| Text Representation         | TF-IDF                                       |
| Similarity Calculation      | Cosine Similarity                            |
| Classification Algorithms   | Multinomial Naive Bayes, Logistic Regression |
| Database                    | SQLite                                       |
| Frontend                    | HTML, CSS, JavaScript                        |
| UI Framework                | Bootstrap 5                                  |
| Data Visualization          | Chart.js                                     |
| Excel Export                | pandas, openpyxl                             |

## How It Works

### 1. Resume Upload and Text Extraction

A candidate uploads a PDF resume through the web interface. PyMuPDF extracts text from the document so it can be processed by the application.

### 2. Text Preprocessing

The extracted text is cleaned and prepared for analysis using NLTK and regular expressions.

The preprocessing pipeline includes lowercasing, tokenization, stopword removal, and lemmatization. Special handling protects technology names such as `C++`, `Node.js`, and `.NET` from being corrupted during cleaning.

### 3. Skill Extraction

The system identifies candidate skills by matching the processed resume against a predefined skill taxonomy containing more than 150 terms across 14 categories.

Word-boundary matching helps prevent incorrect matches, such as detecting `Java` inside `JavaScript`.

### 4. Job Category Prediction

The cleaned resume text is converted into TF-IDF features and passed to a trained classification model.

The model predicts a likely category, such as Data Analyst, Data Scientist, Software Engineer, or HR, based on the categories available in the training dataset.

### 5. Job Description Processing

Recruiters enter a job title and description through the web interface.

The system processes the description using the same text-cleaning and skill-extraction pipeline used for resumes, helping maintain consistency during comparison.

### 6. Candidate Matching and Ranking

When a recruiter opens a dashboard for a selected job, the application evaluates candidates using two metrics.

**Skill Match**

Measures how many required skills are present in the candidate's detected skill set.

$$
\text{Skill Match (\%)} =
\frac{\text{Matched Required Skills}}
{\text{Total Required Skills}} \times 100
$$

For example, if a job requires 8 skills and a candidate has 6 of them, the skill match is 75%.

**Content Relevance**

Uses TF-IDF vectors and cosine similarity to measure textual similarity between the resume and job description.

The two scores are displayed separately. Candidates are ranked primarily by Skill Match, with Content Relevance used to break ties.

### 7. Recruiter Dashboard

The dashboard presents the matching results in a recruiter-friendly format, including:

* Ranked candidate lists.
* Skill match and content relevance percentages.
* Predicted job categories.
* Candidate category distribution charts.
* Skill distribution charts.
* Client-side filtering by category.

## Installation and Setup

### Prerequisites

Install the following before running the application:

* Python
* Git
* pip, the Python package installer

### Step 1: Clone the Repository

Replace the repository URL below with your actual GitHub repository URL.

```bash
git clone <your-repository-url>
cd resume_shortlisting_system
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download NLTK Resources

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

If your installed NLTK version requires `punkt_tab`, download that resource as well.

### Step 4: Initialize the Database

```bash
python -c "from utils.db_manager import initialize_database; initialize_database()"
```

Run this command if your project uses the `utils.db_manager.initialize_database` function shown above.

### Step 5: Train the Machine Learning Model

```bash
python train_model.py
```

This step trains the classifier using the project's labeled training dataset. Run it whenever the model needs to be regenerated.

### Step 6: Start the Application

```bash
python app.py
```

Open the following URL in your browser:

http://127.0.0.1:5000/

Make sure the file paths and commands match your actual repository structure.

## How to Use

**For candidates**

1. Open the application home page.
2. Upload a PDF resume.
3. Review the detected skills and predicted job category.

**For recruiters**

1. Open the Post a Job section.
2. Enter a job title and description.
3. Save the job.
4. Navigate to the View Dashboard section.
5. Select the job from the dropdown.
6. Review the ranked candidates, scores, charts, and category filters.

### Exporting Data

To export candidate, job, and matching data into an Excel workbook, run:

```bash
python export_to_excel.py
```

The script generates an Excel file containing separate worksheets for Candidates, Jobs, and Scores, provided the export functionality is configured as described.

## Machine Learning Model

The application uses supervised machine learning to predict candidate job categories from resume text.

### Algorithms

* Multinomial Naive Bayes
* Logistic Regression

### Training Pipeline

1. Load the labeled resume dataset.
2. Preprocess resume text.
3. Split the dataset into training and testing subsets using stratified sampling.
4. Fit the TF-IDF vectorizer on the training data.
5. Train and evaluate the classification models.
6. Compare evaluation metrics and inspect the classification report and confusion matrix.

### Reported Results

The current experimental dataset contains 48 labeled examples across four categories, with 12 examples per category. Both models achieved 100% test accuracy on the described split.

**Important:** This result reflects performance on a small, clearly separated dataset. It does not establish that the models will achieve the same accuracy on real-world resumes, where job categories and technical skills often overlap.

A reliable production evaluation would require a larger, more diverse dataset and additional validation.

### Matching Is Separate from Classification

The machine learning classifier predicts a job category. The matching engine separately calculates Skill Match and Content Relevance for a selected job.

This separation makes the results easier to interpret and prevents a category prediction from being confused with a candidate's suitability for a specific role.

## Database Design

The application uses SQLite to persist candidate records, job descriptions, and matching scores.

### Main Tables

**Candidates**

Stores candidate details, resume file paths, processed text, predicted categories, and detected skills.

**Jobs**

Stores job titles, processed job descriptions, and required skills.

**Scores**

Stores the calculated matching results associated with each candidate and job.

### Simplified Schema

```sql
candidates (
    id,
    name,
    resume_path,
    cleaned_text,
    predicted_category,
    detected_skills
);

jobs (
    id,
    title,
    cleaned_text,
    required_skills
);

scores (
    id,
    candidate_id,
    job_id,
    match_score,
    content_score
);
```

Candidate and job references connect each score to the corresponding records.

The application uses parameterized SQL queries to reduce SQL injection risks. Skill lists are stored as JSON-encoded strings and converted back into Python lists when retrieved.

## Important Design Decisions

### Separate Skill Match from Content Relevance

Skill coverage is a direct measure of how many listed job requirements a candidate appears to satisfy. Overall textual similarity is useful but can be affected by resume wording and document length.

Reporting these metrics separately makes candidate comparisons more transparent.

### Protect Technology Names During Text Cleaning

Standard punctuation removal can corrupt terms such as `C++`, `Node.js`, and `.NET`. The preprocessing pipeline protects these terms before applying general text-cleaning operations.

### Use Consistent Preprocessing

Resumes and job descriptions pass through the same cleaning and skill-extraction logic. This reduces inconsistencies when comparing their contents.

### Calculate Scores on Demand

Candidates can upload resumes before a recruiter creates a job. The system calculates scores when a dashboard is opened and can reuse previously stored scores for the same candidate-job pairs.

This avoids unnecessary recalculation on repeat visits.

## Limitations

* Skill extraction depends on a predefined taxonomy and may miss synonyms or skills that are implied rather than explicitly mentioned.
* Short skill names can create false positives in some contexts.
* The machine learning dataset is small and may not represent real-world resume diversity.
* The application does not include authentication or role-based access control in the described implementation.
* SQLite is appropriate for local development and small demonstrations but may not suit high-concurrency production workloads.
* Client-side filtering may become inefficient with very large candidate datasets.
* TF-IDF similarity depends on the text and vocabulary of the documents being compared.
* The system supports initial screening and should not be treated as an autonomous hiring decision-maker.

## Future Improvements

* Introduce semantic skill matching to recognize synonyms and related technical terms.
* Expand and diversify the training dataset.
* Use cross-validation and more robust model evaluation.
* Add candidate and recruiter authentication with role-based access control.
* Migrate to PostgreSQL for applications requiring greater concurrency.
* Distinguish mandatory skills from preferred skills.
* Improve resume parsing for different document layouts and formats.
* Add pagination and server-side filtering for larger datasets.
* Provide clearer explanations of why a candidate matched a job.
* Add human-review workflows and fairness monitoring.

## Learning Outcomes

Developing this project provided practical experience in:

* Building a complete Python web application using Flask.
* Extracting text from PDF documents.
* Applying NLP techniques to unstructured text.
* Designing rule-based skill extraction with regular expressions.
* Training and evaluating supervised classification models.
* Using TF-IDF and cosine similarity for document comparison.
* Designing relational database tables and SQL queries.
* Integrating frontend forms with backend APIs using the Fetch API.
* Visualizing recruitment analytics with Chart.js.
* Identifying data leakage risks and understanding the limitations of small datasets.
* Making engineering decisions based on observed application behavior.

## Author

**Gowtham G**

Generative AI Engineer | Python Developer | Machine Learning

* GitHub: [Gowtham-Tech0419](https://github.com/Gowtham-Tech0419)
* LinkedIn: [Gowtham G](https://www.linkedin.com/in/here-gowtham-g/)
* Portfolio: [gowthamgopalakrishnan.vercel.app](https://gowthamgopalakrishnan.vercel.app/)

---

This project is intended for educational and portfolio purposes. Candidate rankings are based on extracted information and automated matching metrics and should support, not replace, human review.

