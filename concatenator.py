import os
import glob

def concatenate_posts(input_dir="posts_clean", output_file="pg_knowledge_base.md"):
    """
    Concatenates all .md files from an input directory into a single output file.
    
    Args:
        input_dir (str): The directory containing the cleaned markdown files.
        output_file (str): The path for the final concatenated markdown file.
    """
    print(f"Starting concatenation from '{input_dir}'...")

    try:
        # Use glob to find all .md files. The list is sorted to ensure a
        # consistent and predictable order of articles in the final file.
        files_to_process = sorted(glob.glob(os.path.join(input_dir, '*.md')))
        
        if not files_to_process:
            print(f"Warning: No '.md' files found in '{input_dir}'.")
            return
            
        print(f"Found {len(files_to_process)} files to concatenate.")

        # Open the output file in write mode. This will create it if it doesn't
        # exist or overwrite it if it does.
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for filepath in files_to_process:
                filename = os.path.basename(filepath)
                print(f"  - Appending '{filename}'...")
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        # Read the content of the current file
                        content = infile.read()
                        # Write the content to the output file
                        outfile.write(content)
                        # Optionally, add a newline between files for cleaner separation,
                        # though the '---' already handles this.
                        outfile.write("\n")
                except Exception as e:
                    print(f"    -  Error reading {filename}: {e}")

        print(f"\nConcatenation complete. All articles saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: The input directory '{input_dir}' was not found.")
        print("Please make sure the 'posts_clean' directory exists and contains your files.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # This makes the script runnable from the command line.
    # It will look for your 'posts_clean' directory and create the final file.
    concatenate_posts()
