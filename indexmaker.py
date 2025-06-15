import os
import re
import requests
import json
import time
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables directly.")

# --- Configuration ---
# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required. Please add it to your .env file.")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

INPUT_FILE = "pg_knowledge_base.md"
OUTPUT_FILE = "KNOWLEDGE_INDEX.md"
MAX_RETRIES = 3 # Number of times to retry a failed API call

def get_essay_title(essay_text):
    """Extracts the title from an essay's text."""
    match = re.search(r'ESSAY_TITLE:\s*(.*)', essay_text)
    return match.group(1).strip() if match else "Untitled"

def load_processed_titles(filepath):
    """Reads the output file and returns a set of titles already processed."""
    processed_titles = set()
    if not os.path.exists(filepath):
        return processed_titles

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title_matches = re.findall(r'^\* \*\*Title:\*\*\s*(.*?)$', content, re.MULTILINE)
    for title in title_matches:
        processed_titles.add(title.strip())

    print(f"Found {len(processed_titles)} already processed articles in '{filepath}'.")
    return processed_titles

def generate_index_for_article(essay_content):
    """
    Calls the Gemini API to analyze a single essay and return a structured index.
    Includes a retry mechanism for network errors.
    """
    meta_prompt = """
You are an AI imbued with the worldview, heuristics, and principles of Paul Graham. Your task is to analyze an essay written by him and distill its essence into a structured format. Your analysis should reflect a deep understanding of his core ideas, such as counter-intuitive thinking, the importance of user needs, organic growth, and first-principles reasoning.

For the following essay content, provide:
1.  A "summary" which is a single, concise sentence articulating the central argument of the essay.
2.  A list called "principles" containing 3-5 of the most durable, actionable principles or mental models presented. These should be the core "heuristics for parsing reality" that a reader could apply themselves.
3.  A list called "themes" containing 2-4 thematic tags that capture the subject matter. Use a consistent vocabulary from this list where possible: `startups`, `technology`, `thinking`, `writing`, `life`, `work`, `investing`, `economics`, `society`, `YC`, `history`.

Your output must be only a single, valid JSON object with the keys "summary", "principles", and "themes", without any preamble or explanation.
"""
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"text": meta_prompt + "\n\n---\n\n" + essay_content}],
        "generationConfig": {"responseMimeType": "application/json"}
    }

    response = None
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data), timeout=90)
            response.raise_for_status()

            response_text = response.json()['candidates'][0]['content']['parts'][0]['text']
            cleaned_json_text = re.sub(r'^```json\s*|```\s*$', '', response_text).strip()

            return json.loads(cleaned_json_text)
        except requests.exceptions.RequestException as e:
            print(f"    -  API request failed (Attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                sleep_time = 2 ** (attempt + 1) # Exponential backoff: 2s, 4s, 8s
                print(f"    -  Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print("    -  Max retries reached. Failing this article.")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"    -  Error parsing API response: {e}")
            if response is not None:
                print(f"    -  Raw response: {response.text}")
            return None # Don't retry on parsing errors

    return None

def split_into_articles(file_content):
    """Splits content from a single file into multiple articles."""
    articles = re.split(r'\n---\n', file_content)
    return [article.strip() for article in articles if article.strip()]

def main():
    """
    Main function to orchestrate reading, processing, and writing the index.
    """
    if API_KEY and "YOUR_GEMINI_API_KEY" in API_KEY:
        print("Error: Please replace 'YOUR_GEMINI_API_KEY' with your actual Gemini API key in the script.")
        return

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        print("Please make sure your concatenated knowledge base is in the same directory.")
        return

    articles = split_into_articles(raw_content)
    total_articles = len(articles)
    processed_titles = load_processed_titles(OUTPUT_FILE)

    print(f"\nFound {total_articles} total articles. Will skip {len(processed_titles)} already processed.")

    # Open the output file in append mode ('a') to resume progress
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as outfile:
        for i, article_text in enumerate(articles):
            title = get_essay_title(article_text)

            if title in processed_titles:
                print(f"  - Skipping article {i+1}/{total_articles}: '{title}' (already processed).")
                continue

            print(f"  - Processing article {i+1}/{total_articles}: '{title}'...")

            content_match = re.search(r'CONTENT:\n(.*)', article_text, re.DOTALL)
            if not content_match:
                print("    -  Could not find CONTENT section. Skipping.")
                continue

            content_for_api = content_match.group(1).strip()

            index_data = generate_index_for_article(content_for_api)

            if index_data:
                outfile.write(f"* **Title:** {title}\n")
                outfile.write(f"    * **Summary:** {index_data.get('summary', 'N/A')}\n")
                outfile.write("    * **Key Principles:**\n")
                for principle in index_data.get('principles', []):
                    outfile.write(f"        * {principle}\n")

                themes_str = ", ".join(f"`{theme}`" for theme in index_data.get('themes', []))
                outfile.write(f"    * **Themes:** {themes_str}\n")
                outfile.write("---\n")
                print("    -  Successfully generated and wrote index entry.")
            else:
                print("    -  Failed to generate index for this article after retries.")

            time.sleep(1) # A short delay to avoid hitting rate limits

    print(f"\nProcessing complete. Knowledge index saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()


# import os
# import re
# import requests
# import json
# import time
# import glob

# # --- Configuration ---
# # IMPORTANT: API key is now loaded from environment variables via .env file

# INPUT_FILE = "pg_knowledge_base.md"
# OUTPUT_FILE = "KNOWLEDGE_INDEX.md"

# def get_essay_title(essay_text):
#     """Extracts the title from an essay's text."""
#     match = re.search(r'ESSAY_TITLE:\s*(.*)', essay_text)
#     return match.group(1).strip() if match else "Untitled"

# def generate_index_for_article(essay_content):
#     """
#     Calls the Gemini API to analyze a single essay and return a structured index.
#     """
#     # This is the "meta-prompt" that instructs the AI on how to analyze the text.
#     # It's designed to make the AI adopt PG's way of thinking.
#     meta_prompt = """
# You are an AI imbued with the worldview, heuristics, and principles of Paul Graham. Your task is to analyze an essay written by him and distill its essence into a structured format. Your analysis should reflect a deep understanding of his core ideas, such as counter-intuitive thinking, the importance of user needs, organic growth, and first-principles reasoning.

# For the following essay content, provide:
# 1.  A "summary" which is a single, concise sentence articulating the central argument of the essay.
# 2.  A list called "principles" containing 3-5 of the most durable, actionable principles or mental models presented. These should be the core "heuristics for parsing reality" that a reader could apply themselves.
# 3.  A list called "themes" containing 2-4 thematic tags that capture the subject matter. Use a consistent vocabulary from this list where possible: `startups`, `technology`, `thinking`, `writing`, `life`, `work`, `investing`, `economics`, `society`, `YC`, `history`.

# Your output must be only a single, valid JSON object with the keys "summary", "principles", and "themes", without any preamble or explanation.
# """

#     headers = {'Content-Type': 'application/json'}
#     data = {
#         "contents": [{
#             "parts": [{"text": meta_prompt + "\n\n---\n\n" + essay_content}]
#         }],
#         "generationConfig": {
#             "responseMimeType": "application/json",
#         }
#     }

#     try:
#         response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data), timeout=60)
#         response.raise_for_status()  # Raise an exception for bad status codes

#         # The Gemini API may wrap the JSON in markdown backticks. Clean it up.
#         response_text = response.json()['candidates'][0]['content']['parts'][0]['text']
#         cleaned_json_text = re.sub(r'^```json\s*|```\s*$', '', response_text).strip()

#         return json.loads(cleaned_json_text)
#     except requests.exceptions.RequestException as e:
#         print(f"    -  API request failed: {e}")
#     except (KeyError, IndexError, json.JSONDecodeError) as e:
#         print(f"    -  Error parsing API response: {e}")
#         print(f"    -  Raw response: {response.text}")
#     return None

# def split_into_articles(file_content):
#     """Splits content from a single file into multiple articles."""
#     articles = re.split(r'\n---\n', file_content)
#     return [article.strip() for article in articles if article.strip()]

# def main():
#     """
#     Main function to orchestrate reading, processing, and writing the index.
#     """
#     if API_KEY == "YOUR_GEMINI_API_KEY":
#         print("Error: Please replace 'YOUR_GEMINI_API_KEY' with your actual Gemini API key in the script.")
#         return

#     try:
#         with open(INPUT_FILE, 'r', encoding='utf-8') as f:
#             raw_content = f.read()
#     except FileNotFoundError:
#         print(f"Error: Input file '{INPUT_FILE}' not found.")
#         print("Please make sure your concatenated knowledge base is in the same directory.")
#         return

#     articles = split_into_articles(raw_content)
#     total_articles = len(articles)
#     print(f"Found {total_articles} articles to process in '{INPUT_FILE}'.")

#     with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
#         for i, article_text in enumerate(articles):
#             title = get_essay_title(article_text)
#             print(f"  - Processing article {i+1}/{total_articles}: '{title}'...")

#             # Extract just the content for API analysis
#             content_match = re.search(r'CONTENT:\n(.*)', article_text, re.DOTALL)
#             if not content_match:
#                 print("    -  Could not find CONTENT section. Skipping.")
#                 continue

#             content_for_api = content_match.group(1).strip()

#             # Call the API
#             index_data = generate_index_for_article(content_for_api)

#             if index_data:
#                 # Write formatted output to the index file
#                 outfile.write(f"* **Title:** {title}\n")
#                 outfile.write(f"    * **Summary:** {index_data.get('summary', 'N/A')}\n")
#                 outfile.write(f"    * **Key Principles:**\n")
#                 for principle in index_data.get('principles', []):
#                     outfile.write(f"        * {principle}\n")

#                 themes_str = ", ".join(f"`{theme}`" for theme in index_data.get('themes', []))
#                 outfile.write(f"    * **Themes:** {themes_str}\n")
#                 outfile.write("---\n")
#                 print("    -  Successfully generated and wrote index entry.")
#             else:
#                 print("    -  Failed to generate index for this article.")

#             # Respect API rate limits
#             time.sleep(1.5) # A short delay to avoid hitting rate limits

#     print(f"\nProcessing complete. Knowledge index saved to '{OUTPUT_FILE}'.")

# if __name__ == "__main__":
#     main()
