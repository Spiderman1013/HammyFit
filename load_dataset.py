import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Add a newline after each page
    return text

def chunk_pdf_text(pdf_path, chunk_size=1000, chunk_overlap=200):
    # Extract text from PDF
    full_text = extract_text_from_pdf(pdf_path)

    # Initialize the RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(full_text)

    return chunks

# Usage
if __name__ == '__main__':
    pdf_path = 'exercisebook.pdf'
    chunks = chunk_pdf_text(pdf_path)

    # Output the list of chunks
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")
