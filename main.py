import subprocess
import os
import argparse

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using pdftotext."""
    try:
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running pdftotext: {e}")
        return ""

def write_to_txt(txt_path, text):
    """Write extracted text into a .txt file."""
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

def aiconversion(txt_path):
    """Read extracted text and process it with Ollama AI."""
    with open(txt_path, "r", encoding="utf-8") as f:
        textdata = f.read()
    
    print(textdata)  # Print only the first 500 characters

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1"],  # Assuming `pdf` is the model name
            input=textdata,  # Pass text as stdin
            capture_output=True,
            text=True,
            check=True
        )
        print("AI Response:\n", result.stdout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running Ollama: {e}")
        return ""





def main():
    parser = argparse.ArgumentParser(description="Convert a PDF to a text file using pdftotext.")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    txt_path = os.path.splitext(pdf_path)[0] + ".txt"

    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        return

    extracted_text = extract_text_from_pdf(pdf_path)

    if not extracted_text:
        print("Error: No text extracted from the PDF.")
        return
    
    write_to_txt(txt_path, extracted_text)

    aiconversion(txt_path)

if __name__ == "__main__":
    main()

