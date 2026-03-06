import pypdf
import json
import re
import os

def extract_paper_content(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # Define sections to look for
    sections = ["ABSTRACT", "INTRODUCTION", "METHODOLOGY", "RESULTS", "CONCLUSION", "REFERENCES"]
    extracted_content = {"filename": os.path.basename(pdf_path)}
    
    # Extract Abstract specifically (Task 5)
    abstract_match = re.search(r'(?i)ABSTRACT(.*s?)(?=INTRODUCTION|1\. Introduction|Keywords)', full_text, re.DOTALL)
    extracted_content["abstract"] = abstract_match.group(1).strip() if abstract_match else "Abstract not found"

    # Extract Sections (Task 4)
    current_text = full_text
    for i in range(len(sections)-1):
        pattern = f"(?i){sections[i]}(.*)(?={sections[i+1]})"
        match = re.search(pattern, current_text, re.DOTALL)
        if match:
            extracted_content[sections[i].lower()] = match.group(1).strip()
            
    return extracted_content

def process_all_papers(paper_list):
    all_data = []
    for paper in paper_list:
        if os.path.exists(paper):
            print(f"Processing {paper}...")
            all_data.append(extract_paper_content(paper))
    
    with open("extracted_content.json", "w", encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)

# List of your files
files = ["Paper A.pdf", "Paper B.pdf", "Paper C.pdf", "Paper D.pdf", "Paper E.pdf", 
         "Paper F.pdf", "Paper G.pdf", "Paper H.pdf", "Paper I.pdf",]

process_all_papers(files)