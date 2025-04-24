import sys

def process_file(input_file, output_file, max_lines=3000):
    line_count = 0
    with open(input_file, 'r', encoding='utf-8') as infile:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # Process only up to max_lines
                if line_count >= max_lines:
                    break
                
                # Split the line by tabs
                parts = line.strip().split('\t')
                
                # If there are at least two parts, flip them
                if len(parts) >= 2:
                    # Swap the first and second elements
                    parts[0], parts[1] = parts[1], parts[0]
                    # Keep only the first two parts (which are now flipped)
                    new_line = '\t'.join(parts[:2])
                    outfile.write(new_line + '\n')
                elif len(parts) == 1:
                    # If there's only one part, keep it
                    outfile.write(parts[0] + '\n')
                # If the line is empty, skip it
                
                line_count += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_file(input_file, output_file, max_lines=3000)
    print(f"Processed {input_file} (first 1,000 lines) and saved results to {output_file}")