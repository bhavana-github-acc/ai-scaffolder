### AI Scaffolder CLI

A Python CLI tool for generating project structures and leveraging AI for documentation and content transformation.

This tool is developed as part of a technical test for DeepDil.ai. It provides:

1) Automatic scaffolding of projects from a JSON template.
2) AI-powered README generation.
3) AI-assisted template suggestions.
4) Advanced “vibe” coding: AI-powered transformation of multiple input files according to instructions.
   
---------------------------------------------------------------------------------------------------------------------------
## Table of Contents

Installation

Setup

Usage

1. Generate Project Structure

2. Generate README

3. Suggest Template

4. Vibe Coding

with AI Prompts

README generation: Generates a structured professional README based on folder structure.
Template suggestion: Generates an ideal template.json from a project description.
Vibe coding: Consolidates and transforms input files using detailed instructions.

---------------------------------------------------------------------------------------------------------------------------


## Installation

Clone the repository:

git clone https://github.com/<your-username>/ai-scaffolder.git
cd ai-scaffolder


Install dependencies:
pip install -r requirements.txt

---------------------------------------------------------------------------------------------------------------------------

## Setup

I have chosen to use my own API key from Gemini. I used multiple in the case where I had reached my maximum usage of prompts; I have stored them in API_keys.txt (locally for security).

LLM API key (Gemini):
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"  # Windows PowerShell
---------------------------------------------------------------------------------------------------------------------------

## Usage

#Step 1. Generate Project Structure

Given a template.json:

{
  "project_name": "my-audit",
  "structure": {
    "methodology": ["scope-of-work.md", "maturity-grid.md"],
    "meetings": ["tech-session.md", "code-review.md"],
    "report": ["week-1.md"]
  }
}

Run:

python scaffolderCLI.py -template template1.json

This will create the root folder and all subfolders/files.


---------------------------------------------------------------------------------------------------------------------------
# Step 2.1) Generate README

To generate a professional README automatically using AI:

python scaffolderCLI.py -template template1.json --readme --api_key "YOUR_API_KEY_HERE"

This reads the folder structure and creates README.md in the project root.

---------------------------------------------------------------------------------------------------------------------------
# Step 2.2) Suggest Template

To get an AI-generated template based on a description:

python scaffolderCLI.py -suggest "a cybersecurity maturity audit" --api_key "YOUR_API_KEY_HERE"
This generates a new template_<description>.json file.

---------------------------------------------------------------------------------------------------------------------------
# Step 3) Vibe Coding (Transformation Pipeline)

Apply AI-powered transformations to multiple files according to instructions in instructions.md:

python scaffolderCLI.py -vibe instructions.md --in meeting1.md meeting2.md --out summary.md --api_key "YOUR_API_KEY_HERE"

Example instruction file (instructions.md):

Summarize all meetings in a professional style.
Highlight key decisions and next steps.

The tool reads all input files, applies the instructions via AI, and saves the result in summary.md.

---------------------------------------------------------------------------------------------------------------------------
# AI Prompts

All AI interactions are recorded in /ai-meta/prompts.txt. Main prompts used:

---------------------------------------------------------------------------------------------------------------------------




