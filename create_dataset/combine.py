def combine_text_files(foreign_file_path, english_file_path, output_file_path, lang_code, max_lines=1000):
    """
    Combine lines from two text files and write them in a specific format.
    
    Args:
        foreign_file_path (str): Path to the foreign language text file
        english_file_path (str): Path to the English text file
        output_file_path (str): Path to the output file
        lang_code (str): Language code for the foreign language
        max_lines (int): Maximum number of lines to process
    """
    try:
        with open(foreign_file_path, 'r', encoding='utf-8') as foreign_file, \
             open(english_file_path, 'r', encoding='utf-8') as english_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:
            
            line_count = 0
            
            for foreign_line, english_line in zip(foreign_file, english_file):
                if line_count >= max_lines:
                    break
                
                # Strip whitespace and newlines
                foreign_text = foreign_line.strip()
                english_text = english_line.strip()
                
                # Write in the specified format
                if lang_code == "ar":
                    output_file.write(f"{english_text}\t{foreign_text}\n")
                else:
                    output_file.write(f"{foreign_text}\t{english_text}\n")
                
                line_count += 1
            
        print(f"Successfully combined {line_count} lines from the text files.")
        print(f"Output saved to: {output_file_path}")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

#foreign_file = "ar-en.txt/OpenSubtitles.ar-en.ar"
#english_file = "ar-en.txt/OpenSubtitles.ar-en.en"
#output_file = "ar-en_combined.txt"
foreign_file = "en-zh.txt/OpenSubtitles.en-zh.en"
english_file = "en-zh.txt/OpenSubtitles.en-zh.zh"
output_file = "en-zh_combined.txt"
language_code = "he"

# Call the function to combine the files
combine_text_files(foreign_file, english_file, output_file, language_code, 1000)