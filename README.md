# AI Rewriting Assistant

A desktop application built with PySide6 that helps you practice rewriting text excerpts and get AI-powered feedback on your rewrites.
![video](https://github.com/juangrukat/Rewrites/blob/main/Rewrite.gif)
## Features

- Import excerpts from CSV files
- SQLite database for storing excerpts, analysis, and rewrites
- OpenAI API integration for analyzing rewrites
- Random excerpt selection for practice
- Customizable prompt templates
- Secure API key storage with password masking
- Model selection (gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4o)
- Custom font settings (family and size)
- Load prompt templates from files

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python mainwindow.py
```

## Usage

### Setting up OpenAI API

1. Go to the "Settings" tab
2. Enter your OpenAI API key in the text field
3. Click "Save API" to store your API key securely

### Importing Excerpts

1. Go to the "Settings" tab
2. Click "Import CSV" and select your CSV file
3. The CSV file must have the following columns:
   - Excerpt: The original text
   - Analysis: Optional analysis of the excerpt
   - Rewrite: Optional existing rewrite

### Practicing Rewrites

1. Go to the "Work Area" tab
2. Click "Get Random" to load a random excerpt
3. Read the original excerpt and write your rewrite in the "Rewrite" text area
4. Click "Send to AI" to get feedback on your rewrite

### Using Prompt Templates

The application comes with several default prompt templates for different types of analysis:

- Basic Analysis: Simple feedback on clarity, conciseness, and meaning preservation
- Detailed Critique: In-depth analysis of meaning, clarity, grammar, and suggestions
- Academic Style: Analysis focused on academic writing standards

You can select a prompt template from the dropdown menu in the Settings tab.

## CSV Format

Your CSV file should have the following format:

```
Excerpt,Analysis,Rewrite
"This is the first excerpt.","This is a simple sentence.","This is a rewrite of the first excerpt."
"This is the second excerpt.","This is another simple sentence.","This is a rewrite of the second excerpt."
```

The "Analysis" and "Rewrite" columns are optional and can be left empty.

## Prompt Templates

Prompt templates use placeholders to insert the excerpt and rewrite:

- `{excerpt}`: Will be replaced with the original excerpt
- `{rewrite}`: Will be replaced with your rewrite

For example:

```
Please analyze my rewrite of the following excerpt:

Original: {excerpt}

Rewrite: {rewrite}

Provide feedback on clarity, conciseness, and how well I've maintained the original meaning.
```