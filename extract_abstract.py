import fitz
import os
import json
import re

# Use current folder (NO pdfs folder required)
pdf_folder = "."

output_file = "abstracts.json"

abstracts = []

for pdf_file in os.listdir(pdf_folder):
    if pdf_file.lower().endswith(".pdf"):
        print("Processing:", pdf_file)
        doc = fitz.open(pdf_file)
        text = ""

        for page in doc:
            text += page.get_text()

        # Try to extract abstract
        match = re.search(r"abstract(.*?)(introduction)", text, re.S | re.I)

        if match:
            abstract_text = match.group(1).strip()
        else:
            abstract_text = "Abstract not found"

        abstracts.append({
            "paper_name": pdf_file,
            "abstract": abstract_text
        })

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(abstracts, f, indent=4)

print("\n✅ Abstract extraction completed successfully")