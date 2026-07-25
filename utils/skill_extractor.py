import json
import re


def load_skill_database(json_path='data/skills_database.json'):
    with open(json_path, 'r') as file:
        skill_data = json.load(file)

    all_skills = []
    for category, skills in skill_data.items():
        all_skills.extend(skills)

    return all_skills


def extract_skills(cleaned_text, skill_list):
    found_skills = []

    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, cleaned_text):
            found_skills.append(skill)

    return found_skills


def get_candidate_skills(cleaned_text, json_path='data/skills_database.json'):
    skill_list = load_skill_database(json_path)
    matched_skills = extract_skills(cleaned_text, skill_list)
    return matched_skills

DISPLAY_NAMES = {
    'cplusplus': 'C++',
    'csharp': 'C#',
    'nodejs': 'Node.js',
    'reactjs': 'React.js',
    'vuejs': 'Vue.js',
    'aspnet': 'ASP.NET',
    'dotnet': '.NET',
    'cicd': 'CI/CD',
}

def get_display_name(skill):
    return DISPLAY_NAMES.get(skill, skill)