#proper working
"""
$env:GEMINI_API_KEY="AIzaSyCu7N_Ym8LSWznaPEYgqApgzQPZadH52f8"
python scaffolderCLI.py -t template1.json --readme
"""
#Step 1: Generating of the project folder structure

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

    #Create root folder
    os.makedirs(root, exist_ok=True)
    print(f"Created root folder: {root}")

    #Iterate and create subfolders
    for folder, files in structure.items():
        folder_path = os.path.join(root, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")
        for file in files:
            open(os.path.join(folder_path, file), "w").close()
            print(f"  Created file: {file}")

    print(f"\nProject '{root}' created successfully!")
    return root, structure

#Step 2: Generation of readME with Gemini API

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

    model_name = "gemini-3-flash-preview" 

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    readme_text = response.text

    readme_path = os.path.join(project_name, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_text)

    print(f"README.md generated in {readme_path}")


#Step 2.2: Given a topic from user, generate a template.json file
def suggest_template(description, api_key):
    """
    Generates a template.json file using Gemini AI based on project description.
    """
    client = genai.Client(api_key=api_key)
    prompt = f"""
Generate a JSON template for a project based on this description:
'{description}'

Requirements:
- project_name: short, lowercase, hyphenated
- structure: folders as keys, each with a list of markdown files
- output ONLY valid JSON, no extra text
"""
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    template_text = response.text.strip()

    import re
    safe_desc = re.sub(r'[^a-z0-9]+', '_', description.lower()).strip('_') #to create a template file with name as description of the suggestion
    filename = f"template_{safe_desc}.json"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(template_text)

    print(f"Suggested template saved as {filename}")
    print("Here is the generated template:\n")
    print(template_text)





#COMMAND-LINE INTERFACE

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Scaffolder CLI")

    #Make -t and -suggest mutually exclusive
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--template", help="Path to template.json")
    group.add_argument("-suggest", type=str, help="Ask AI to suggest a template.json for this description")

    parser.add_argument("--readme", action="store_true", help="Generate README.md using Gemini")
    parser.add_argument("--api_key", type=str, help="Your Gemini API key (required for -suggest)")

    args = parser.parse_args()

    #Handle -suggest
    if args.suggest:
        if not args.api_key:
            print("ERROR: --api_key is required for -suggest")
            exit(1)
        suggest_template(args.suggest, args.api_key)
        exit(0)

    #Handle -t
    if args.template:
        try:
            root, structure = create_structure(args.template)
        except ValueError as e:
            print(e)
            exit(1)

        if args.readme:
            generate_readme_gemini(root, structure)
