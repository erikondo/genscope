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

def aiconversion(textdata, tex_path_full):
    """Process extracted text with Ollama AI and write to a .tex file."""
    try:
        result = subprocess.run(
            ["ollama", "run", "pdf"],  # Assuming `pdf` is the model name
            input=textdata,  # Pass text as stdin
            capture_output=True,
            text=True,
            check=True
        )
        # Input string with LaTeX code block
        text = result.stdout
        cleaned_text = text.replace("```latex", "").replace("```", "")
        os.makedirs("build", exist_ok=True)  # Ensure build directory exists
        with open(tex_path_full, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running Ollama: {e}")
        return ""

def pdflatex(tex_path):
    """Run pdflatex on a .tex file in the build directory."""
    output_dir = "build"
    # Ensure the build directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Change to the build directory
    os.chdir(output_dir)
    if not os.path.exists(tex_path):
        os.chdir("..")  # Return to parent directory before raising error
        raise FileNotFoundError(f"The file {tex_path} does not exist in {output_dir}!")

    # Run pdflatex
    try:
        result = subprocess.run(
            ["pdflatex", tex_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("pdflatex ran successfully!")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running pdflatex:")
        print("Return code:", e.returncode)
        print("Error output:", e.stderr)
    except FileNotFoundError:
        print("pdflatex not found. Ensure a LaTeX distribution (e.g., TeX Live or MiKTeX) is installed and added to PATH.")
    finally:
        # Always return to the parent directory
        os.chdir("..")

def main():
    parser = argparse.ArgumentParser(description="Convert a PDF to a LaTeX file using pdftotext and Ollama.")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    tex_path_full = "build/" + os.path.splitext(os.path.basename(pdf_path))[0] + "_SOW.tex"  # Use .tex extension
    tex_path = os.path.splitext(os.path.basename(pdf_path))[0] + "_SOW.tex"

    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        return

    # Extract text and keep it in memory
    extracted_text = extract_text_from_pdf(pdf_path)

    if not extracted_text:
        print("Error: No text extracted from the PDF.")
        return
    
    # Pass the extracted text directly to aiconversion
    aiconversion(extracted_text, tex_path_full)
    pdflatex(tex_path)

if __name__ == "__main__":
    main()
