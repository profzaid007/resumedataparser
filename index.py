import os
import csv
import json
import re
import subprocess
import docx2txt
import nltk
from pdfminer.high_level import extract_text


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

RESERVED_WORDS = [
    'school',
    'college',
    'univers',
    'academy',
    'faculty',
    'institute',
    'faculdades',
    'Schola',
    'schule',
    'lise',
    'lyceum',
    'lycee',
    'polytechnic',
    'kolej',
    'ünivers',
    'okul',
]

SKILLS_CSV_FILE = 'skills.csv'


PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')

def load_local_skills():
    with open(SKILLS_CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        skills = {row[0].lower(): int(row[1]) for row in reader}
    return skills

LOCAL_SKILLS_DB = load_local_skills()

def skill_exists(skill):
    return skill.lower() in LOCAL_SKILLS_DB

def extract_text_from_docx(docx_path):
    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace('\t', ' ')
    return None

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def doc_to_text_catdoc(file_path):
    try:
        process = subprocess.Popen(
            ['catdoc', '-w', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except (
        FileNotFoundError,
        ValueError,
        subprocess.TimeoutExpired,
        subprocess.SubprocessError,
    ) as err:
        return (None, str(err))
    else:
        stdout, stderr = process.communicate()
        return (stdout.strip(), stderr.strip())

def extract_names(txt):
    person_names = []
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                )
    return person_names

def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
    if phone:
        number = ''.join(phone[0])
        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

   
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    
    found_skills = set()

    
    for token in filtered_tokens:
        if skill_exists(token.lower()):
            found_skills.add(token)

    
    for ngram in bigrams_trigrams:
        if skill_exists(ngram.lower()):
            found_skills.add(ngram)

    return found_skills


def extract_education(input_text):
    organizations = []
    for sent in nltk.sent_tokenize(input_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                organizations.append(' '.join(c[0] for c in chunk.leaves()))

    education = set()
    for org in organizations:
        for word in RESERVED_WORDS:
            if org.lower().find(word) >= 0:
                education.add(org)

    return education

def process_resume(file_path):
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'pdf':
        resume_text = extract_text_from_pdf(file_path)
    elif file_extension == 'docx':
        resume_text = extract_text_from_docx(file_path)
    else:
        return None, None  

    if resume_text:
        skills = extract_skills(resume_text)
        education = extract_education(resume_text)
        return skills, education
    else:
        return None, None  

def save_to_csv(data, csv_file='output_data.csv'):
    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Skills', 'Education']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        
        if os.stat(csv_file).st_size == 0:
            writer.writeheader()

        
        writer.writerow(data)


resumes_folder = 'resumes'


for filename in os.listdir(resumes_folder):
    if filename.endswith('.pdf'):
        file_path = os.path.join(resumes_folder, filename)

       
        skills, education = process_resume(file_path)

        
        name = os.path.splitext(filename)[0].replace('_', ' ')

        
        data = {'Name': name, 'Skills': skills, 'Education': education}
        save_to_csv(data)

print("Processing completed. Data saved to output_data.csv.")
