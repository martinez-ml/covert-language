import os

def align_and_combine_sentences(base_dir, output_dir, max_lines=1000):
    """
    Read, align, and combine sentences from language pair files.
    Filter out empty or dash-only English sentences.
    
    Args:
        base_dir (str): Base directory containing language pair folders
        output_dir (str): Directory to write output files
        max_lines (int): Maximum number of lines to process
    """
    language_folders = [
        'ar-en.txt',
        'en-es.txt',
        'en-fr.txt',
        'en-he.txt',
        'en-ja.txt',
        'en-zh.txt'
    ]
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each language pair
    for folder in language_folders:
        lang_pair = folder.replace('.txt', '')  # e.g., 'ar-en'
        parts = lang_pair.split('-')
        
        # Determine language code and file paths
        if parts[0] == 'en':
            lang_code = parts[1]  # For folders like en-es.txt, the code is 'es'
            foreign_file = f'OpenSubtitles.{lang_pair}.{lang_code}'
            english_file = f'OpenSubtitles.{lang_pair}.en'
        else:
            lang_code = parts[0]  # For folders like ar-en.txt, the code is 'ar'
            foreign_file = f'OpenSubtitles.{lang_pair}.{lang_code}'
            english_file = f'OpenSubtitles.{lang_pair}.en'
        
        foreign_file_path = os.path.join(base_dir, folder, foreign_file)
        english_file_path = os.path.join(base_dir, folder, english_file)
        
        # Read both files
        try:
            with open(foreign_file_path, 'r', encoding='utf-8') as f_file, \
                 open(english_file_path, 'r', encoding='utf-8') as e_file:
                
                foreign_lines = f_file.readlines()
                english_lines = e_file.readlines()
                
                # Check if files have the same number of lines
                if len(foreign_lines) != len(english_lines):
                    print(f"Warning: Line count mismatch in {folder}. Foreign: {len(foreign_lines)}, English: {len(english_lines)}")
                
                # Create aligned pairs, filtering out empty or dash-only English sentences
                aligned_pairs = []
                min_lines = min(len(foreign_lines), len(english_lines))
                
                count = 0
                i = 0
                
                while count < max_lines and i < min_lines:
                    foreign = foreign_lines[i].strip()
                    english = english_lines[i].strip()
                    
                    # Skip if English sentence is empty, just a dash, or only whitespace
                    if english and english != "-" and not english.isspace():
                        aligned_pairs.append((foreign, english))
                        count += 1
                    
                    i += 1
                    
                    # Break if we've gone through all lines but haven't found enough valid pairs
                    if i >= min_lines and count < max_lines:
                        print(f"Warning: Could only find {count} valid sentence pairs in {folder}")
                        break
                
                # Write aligned pairs to output file
                output_file_path = os.path.join(output_dir, f"en-{lang_code}_combined.txt")
                with open(output_file_path, 'w', encoding='utf-8') as out_file:
                    for foreign, english in aligned_pairs:
                        out_file.write(f"{foreign}\t{english}\n")
                
                print(f"Created combined file for {lang_code}: {output_file_path} with {len(aligned_pairs)} aligned pairs")
                
        except FileNotFoundError as e:
            print(f"Warning: File not found - {e}")
        except Exception as e:
            print(f"Error processing {folder}: {e}")

# Main execution
base_directory = "."  # Current directory, change if needed
output_directory = "combined_output"
max_lines = 1000

align_and_combine_sentences(base_directory, output_directory, max_lines)
print("Processing complete.")