import re

def split_file(input_file, max_size):
    start_pattern = r'^@[^@{]*\{'
    # Open the input file for reading
    with open(input_file, 'r', encoding='utf-8') as infile:
        # Initialize variables
        part_num = 1
        current_size = 0
        part_content = []
        entry = []
        open_curly = 0
        close_curly = 0

        # Iterate through each line in the input file
        for line in infile:

            if open_curly == close_curly and entry:
                line_sizes = sum([len(line.encode('utf-8')) for line in entry])

                # If adding the current line exceeds the max size, write the current content to a new file
                if current_size + line_sizes > max_size:
                    write_part(part_content, input_file, part_num)
                    part_num += 1
                    part_content = []
                    current_size = 0

                part_content.extend(entry)
                current_size += line_sizes
                open_curly = 0
                close_curly = 0
                entry = []
            
            # If line is start pattern
            if re.findall(start_pattern, line):
                # If entry exists, save old one, start new one
                if entry:
                    part_content.append(entry)
                    entry = []
                    open_curly = 0
                    close_curly = 0
                # If no entry exists, start new one
                else:
                    entry.append(line)
                    open_curly += line.count("{")
                    close_curly += line.count("}")
            # If line is no start pattern
            else:
                # If entry exists
                if entry:
                    entry.append(line)
                    open_curly += line.count("{")
                    close_curly += line.count("}")
                # Ignore comments and blanks
                else:
                    continue
        
        # Write the last part
        if part_content:
            write_part(part_content, input_file, part_num)

def write_part(content, input_file, part_num):
    # Define the output file name
    file_name, extension = input_file.split(".")
    output_file = "{}_{}.{}".format(file_name, part_num, extension)

    # Write the content to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in content:
            outfile.write(line)

if __name__ == "__main__":
    # Define the maximum size for each split file (in bytes)
    max_size = 50 * 1000 * 1000  # 50 MB

    # Input file path
    input_file = "anthology.bib"

    # Split the file
    split_file(input_file, max_size)