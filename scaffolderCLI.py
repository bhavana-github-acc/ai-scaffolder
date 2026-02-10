import os
import json
import argparse
#create cli scirpt to generate project struction from json template

def create_structure(template_file):
    print("DEBUG: Trying to open:", template_file)
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        print("DEBUG: Content length:", len(content))
        if not content: #error if JSON file is empty
            raise ValueError(f"ERROR: The JSON file '{template_file}' is empty!")
        data = json.loads(content)
    #get root folder and structure from JSON
    root = data.get("project_name")
    structure = data.get("structure")

#create the root folder
    os.makedirs(root, exist_ok=True)
    print(f"Created root folder: {root}")

#iterating and creating the subfolders
    for folder, files in structure.items():
        folder_path = os.path.join(root, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")
        for file in files:
            open(os.path.join(folder_path, file), "w").close()
            print(f"  Created file: {file}")

    print(f"\nProject '{root}' created successfully!")

#command-line interface

if __name__ == "__main__":
    parser = argparse.ArgumentParser() #command-line parser
    parser.add_argument("-t", "--template", required=True, help="Path to template.json")
    args = parser.parse_args() #reads what the user typed in terminal
    
#catches special error of empty json file
    try:
        create_structure(args.template)
    except ValueError as e:
        print(e)

