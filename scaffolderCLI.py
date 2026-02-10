# ----------------- STEP 1: Create Project Structure -----------------
import os
import json
import argparse
from google import genai


def create_structure(template_file):
    print("DEBUG: Trying to open:", template_file)
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        print("DEBUG: Content length:", len(content))
        if not content:
            raise ValueError(f"ERROR: The JSON file '{template_file}' is empty!")
        data = json.loads(content)

    root = data.get("project_name")
    structure = data.get("structure")

    # Create root folder
    os.makedirs(root, exist_ok=True)
    print(f"Created root folder: {root}")

    # Create subfolders and files
    for folder, files in structure.items():
        folder_path = os.path.join(root, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")
        for file in files:
            open(os.path.join(folder_path, file), "w").close()
            print(f"  Created file: {file}")

    print(f"\nProject '{root}' created successfully!")
    return root, structure


# ----------------- STEP 2: Generate README using Gemini -----------------
def generate_readme_gemini(project_name, structure):
    """
    Generates a professional README.md using Google Gemini (new API style).
    The API key must be set in the environment variable GEMINI_API_KEY.
    """
    client = genai.Client()  # Reads GEMINI_API_KEY from env

    # Convert folder structure into readable text
    structure_text = ""
    for folder, files in structure.items():
        structure_text += f"{folder}:\n"
        for file in files:
            structure_text += f"  - {file}\n"

    prompt = f"""
Generate a professional README.md for a project named '{project_name}'
with this folder structure:

{structure_text}
"""

    # Use a model available on your account (example: free-tier compatible)
    model_name = "gemini-3-flash-preview"  # or check your console for available models

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    readme_text = response.text

    # Save README.md in project folder
    readme_path = os.path.join(project_name, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_text)

    print(f"README.md generated in {readme_path}")


# ----------------- COMMAND-LINE INTERFACE -----------------


# ----------------- COMMAND-LINE INTERFACE -----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--template", required=True, help="Path to template.json")
    parser.add_argument("--readme", action="store_true", help="Generate README.md using Gemini")
    args = parser.parse_args()

    # Step 1: Create folders/files
    try:
        root, structure = create_structure(args.template)
    except ValueError as e:
        print(e)
        exit(1)

    # Step 2: Generate README
    if args.readme:
        generate_readme_gemini(root, structure)
