import pdfplumber
import re

# Step 1: Extract text from PDF
def extract_text(pdf_path):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return "\n".join(all_text)

# Step 2: Clean headers, footers, and artifacts
def clean_text(raw_text):
    # Remove known headers/footers
    patterns = [
        r"STUCOR APP", r"DOWNLOADED FROM STUCOR APP", r"RMKCET - CSE DEPT",
        r"Page No-\s*\d+", r"OCE552 - GEOGRAPHIC INFORMATION SYSTEM"
    ]
    for p in patterns:
        raw_text = re.sub(p, "", raw_text)
    # Remove extra whitespace
    return re.sub(r"\n{2,}", "\n", raw_text).strip()

# Step 3: Chunk into manageable sections
def chunk_text(text, max_words=300):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        chunks.append(chunk)
    return chunks

# Step 4: Save to plain text file
def save_chunks(chunks, filename="gis_dataset.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n\n")  # double newline between chunks

# Run the pipeline
pdf_path = r"C:\Users\DQ5029\Default\Downloads\UNIT 4-GIS.pdf"
raw_text = extract_text(pdf_path)
cleaned_text = clean_text(raw_text)
chunks = chunk_text(cleaned_text, max_words=300)
save_chunks(chunks)

print(f"✅ Saved {len(chunks)} chunks to gis_dataset.txt")
