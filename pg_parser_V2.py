import os
import re
import glob

def sanitize_filename(title):
    """
    Takes a string and returns a version that is safe for use as a filename.
    """
    if not title:
        return "untitled-article"
    # Remove invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
    # Replace spaces with hyphens
    sanitized = sanitized.replace(' ', '-').lower()
    # Truncate if too long
    return sanitized[:100]

def inline_footnotes(content):
    """
    Finds footnotes in the text and embeds them inline.
    Handles two common formats.
    """
    footnotes = {}

    # Pattern 1: Finds notes like "[1] Footnote text..." at the end of the file.
    # It also handles multi-line footnote text.
    note_pattern_1 = re.compile(r'^\s*\[(\d+)\]\s*(.*?)(?=\n\s*\[\d+\]|\Z)', re.MULTILINE | re.DOTALL)

    # Pattern 2: Finds notes within a "**Notes**" section like "[ \n\n 1] Footnote text..."
    note_pattern_2 = re.compile(r'\[\s*\n\n\s*(\d+)\s*\]\s*(.*?)(?=\s*\[\s*\n\n\s*\d+|$)', re.DOTALL)

    # Find and remove the notes section to avoid replacing definitions later
    notes_section_match = re.search(r'\n\*\*Notes\*\*\n', content)
    main_text = content
    notes_text = ""
    if notes_section_match:
        notes_start_index = notes_section_match.start()
        main_text = content[:notes_start_index]
        notes_text = content[notes_start_index:]

        # Extract footnotes from the notes section
        for match in note_pattern_2.finditer(notes_text):
            num, text = match.groups()
            footnotes[num] = ' '.join(text.strip().split())

    # Extract footnotes from the main body (for the other style)
    for match in note_pattern_1.finditer(main_text):
        num, text = match.groups()
        footnotes[num] = ' '.join(text.strip().split())

    # Now that we have the footnotes, remove the note definitions from the text
    full_text_for_replacement = content
    full_text_for_replacement = note_pattern_1.sub('', full_text_for_replacement).strip()
    if notes_section_match:
         full_text_for_replacement = re.sub(r'\n\*\*Notes\*\*.*', '', full_text_for_replacement, flags=re.DOTALL).strip()


    # Replace footnote references in the text
    # Style A: [[1](...)]
    ref_pattern_a = re.compile(r'\[\[(\d+)\]\(.*?\)\]')
    full_text_for_replacement = ref_pattern_a.sub(lambda m: f" (Footnote: {footnotes.get(m.group(1), 'Note not found.')})", full_text_for_replacement)

    # Style B: [1]
    ref_pattern_b = re.compile(r'\[(\d+)\]')
    full_text_for_replacement = ref_pattern_b.sub(lambda m: f" (Footnote: {footnotes.get(m.group(1), 'Note not found.')})", full_text_for_replacement)

    return full_text_for_replacement

def clean_and_format_post(raw_content):
    """
    Parses the raw content of a post, cleans it, and formats it.

    Args:
        raw_content (str): The string content of the raw markdown file.

    Returns:
        tuple[str, str] or [None, None]: A tuple containing the sanitized filename
                                         and the cleaned content, or None if parsing fails.
    """
    try:
        # --- 1. Use regex to parse metadata robustly ---
        title_match = re.search(r'^Title:(.*)', raw_content, re.MULTILINE)
        url_match = re.search(r'^URL Source:(.*)', raw_content, re.MULTILINE)

        content_marker = "Markdown Content:"
        content_start_index = raw_content.find(content_marker)
        if content_start_index == -1:
            return None, None

        content = raw_content[content_start_index + len(content_marker):].strip()

        title = title_match.group(1).strip() if title_match else ""
        url = url_match.group(1).strip() if url_match else ""

        # --- 2. Clean Content and Extract Date ---

        # First, strip all image tags, as they can sometimes appear on the same
        # line as the date, which would prevent the date regex from matching.
        image_regex = r'\[!\[.*?\]\(.*?\)\]\(.*?\)|!\[.*?\]\(.*?\)'
        content = re.sub(image_regex, '', content).strip()

        date_str = ""
        # Regex to find dates like "March 2012" or "November 2004, corrected June 2006"
        # It's designed to match the date only if it's at the beginning of the content.
        date_regex = re.compile(r"^\s*\(?_?([A-Z][a-z]+ \d{4}(?:, (?:rev|corrected) [A-Z][a-z]+ \d{4})?)\)?_?\s*\n", re.IGNORECASE)
        date_match = date_regex.search(content)
        if date_match:
            date_str = date_match.group(1).strip()
            # Remove the date line from the main content
            content = date_regex.sub('', content, count=1).strip()

        # Now, with images and date line gone (if found), assign to cleaned_content
        cleaned_content = content

        # Process and embed footnotes
        cleaned_content = inline_footnotes(cleaned_content)

        # Remove common end-of-article noise
        noise_patterns = [
            r'\[Comment\]\(.*?\) on this essay\.',
            r'^\*\*Thanks\*\* to .*? for reading drafts of this\.$',
            r'^\*\*Note[s]?\b.*', # Matches "Note" or "Notes"
            r'^\*\*Related:\**',
            r'^\*\*More Info:\**'
        ]
        for pattern in noise_patterns:
            cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.MULTILINE | re.DOTALL).strip()

        # --- 3. Format the Final Output ---
        date_line = f"DATE: {date_str}\n" if date_str else ""
        formatted_post = (
            "---\n"
            f"ESSAY_TITLE: {title}\n"
            f"URL: {url}\n"
            f"{date_line}"  # Add date line only if found
            "CONTENT:\n"
            f"{cleaned_content}\n"
            "---\n"
        )

        return sanitize_filename(title), formatted_post

    except Exception as e:
        # Catch other unexpected errors during parsing.
        print(f"    -  Error parsing file. It might be malformed. Skipping. Error: {e}")
        return None, None

def split_into_articles(file_content):
    """Splits content from a single file into multiple articles."""
    # Split based on "Title:", which marks the beginning of a new article.
    # The regex uses a positive lookahead to keep the "Title:" delimiter.
    articles = re.split(r'(?=^Title:)', file_content, flags=re.MULTILINE)
    # Filter out any empty strings that might result from the split
    return [article.strip() for article in articles if article.strip()]


def process_all_posts(input_dir="posts", output_dir="posts_clean"):
    """
    Main function to loop through all markdown files in the input directory,
    clean them, and save them to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: '{output_dir}'")

    print(f"Starting processing from '{input_dir}'...")

    try:
        # Use glob to find all .md files, making it more flexible
        files_to_process = glob.glob(os.path.join(input_dir, '*.md'))
        if not files_to_process:
            print(f"Warning: No '.md' files found in '{input_dir}'.")
            return
    except FileNotFoundError:
        print(f"Error: The input directory '{input_dir}' was not found.")
        print("Please create it and place your markdown files inside.")
        return

    for filepath in files_to_process:
        filename = os.path.basename(filepath)
        print(f"\n  - Reading '{filename}'...")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_content = f.read()

            articles = split_into_articles(raw_content)
            print(f"    -  Found {len(articles)} article(s) in this file.")

            for i, article_text in enumerate(articles):
                sanitized_title, cleaned_content = clean_and_format_post(article_text)

                if cleaned_content and sanitized_title:
                    output_filename = f"{sanitized_title}.md"
                    output_file_path = os.path.join(output_dir, output_filename)
                    # To handle multiple articles from one file having same title
                    if len(articles) > 1:
                        base, ext = os.path.splitext(output_filename)
                        output_file_path = os.path.join(output_dir, f"{base}-{i+1}{ext}")

                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    print(f"    -  Successfully cleaned and saved '{os.path.basename(output_file_path)}'")

        except Exception as e:
            print(f"    -  An unexpected error occurred while processing {filename}: {e}")

    print("\nProcessing complete.")


if __name__ == "__main__":
    process_all_posts()
