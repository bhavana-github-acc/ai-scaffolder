#AI-Scaffolder, DeepDil.ai

"""
This script implements the AI Scaffolder CLI with project scaffolding, AI README generation, template suggestion, and vibe coding.
"""
#Step 1: Generating the project folder structure from JSON file

import os
import json
import argparse
from google import genai


def create_structure(template_file):
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content: #raises error if JSON file is empty
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

#Step 2.1: Generation of readME with Gemini API

def generate_readme_gemini(project_name, structure):
    """
    Generates a professional README.md using Google Gemini.
    The API key must be set in the environment variable GEMINI_API_KEY.
    """
    client = genai.Client()  #reads GEMINI_API_KEY

    #Convert (dictionary) folder structure into readable text
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

    response = client.models.generate_content( #Send prompt to Gemini LLM and receive AI-generated content
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


#Step 3: vibe-coding with instructions and input files to follow instructions detailed

def vibe_transform(instructions_file, input_files, output_file, api_key=None):
    # 1) Read instructions
    with open(instructions_file, "r", encoding="utf-8") as f:
        instructions = f.read()



    # 2) Read input files

#combining all the input files separated by file path
    combined_text = ""
    for file_path in input_files:


        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            

            combined_text += f"\n--- File: {file_path} ---\n"
            combined_text += content



    # 3) Build prompt
    prompt = f"""
    You MUST follow the instructions below.

    === INSTRUCTIONS ===
    {instructions}

    === INPUT FILES ===
    {combined_text}

    Now apply the instructions to the files and produce the transformed output.
    """


    # 4) Send to AI
    print("\n========= DEBUG: FINAL PROMPT SENT TO GEMINI =========\n")
    print(prompt)
    print("\n========= END DEBUG PROMPT =========\n")

    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        client = genai.Client()  #environment variable


    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    )



    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Vibe output saved to {output_file}")


#COMMAND-LINE INTERFACE

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Scaffolder CLI")

    #mutually exclusive group for template operations (required=False)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-t", "--template", help="Path to template.json")
    group.add_argument("-suggest", type=str, help="Ask AI to suggest a template.json for this description")

    #readme CLI argument
    parser.add_argument("--readme", action="store_true", help="Generate README.md using Gemini")
    parser.add_argument("--api_key", type=str, help="Your Gemini API key (required for -suggest or -vibe)")

    #Vibe CLI arguments
    parser.add_argument("-vibe", type=str, help="Path to instructions.md for vibe transform")
    parser.add_argument("--in", nargs="+", dest="input_files", help="List of input files for vibe transform")
    parser.add_argument("--out", type=str, help="Output file for vibe transform")

    args = parser.parse_args()

    #1) Handle -vibe independently
    if args.vibe:
        if not args.input_files or not args.out:
            parser.error("ERROR: --in [files] and --out [output file] are required with -vibe")
        vibe_transform(
            instructions_file=args.vibe,
            input_files=args.input_files,
            output_file=args.out,
            api_key=args.api_key
        )
        exit(0)  
        
    #2) Enforce -t or -suggest only if -vibe not used
    if not (args.template or args.suggest):
        parser.error("one of -t/--template or -suggest is required if -vibe is not used")

    #3) Handle -suggest
    if args.suggest:
        if not args.api_key:
            parser.error("ERROR: --api_key is required for -suggest")
        suggest_template(args.suggest, args.api_key)
        exit(0)

    #4) Handle -t
    if args.template:
        try:
            root, structure = create_structure(args.template)
        except ValueError as e:
            print(e)
            exit(1)

        if args.readme:
            generate_readme_gemini(root, structure)


