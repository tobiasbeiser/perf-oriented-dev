import json
import sys
import os

def generate_markdown_row(data):
    command_params = data["command"].split()[1:]
    mean = data["mean"]
    variance = data["variance"]
    
    row = "|"
    for param in command_params:
        row += f"{param}|"
    for key in ["real", "user", "sys", "max_mem"]:
        row += f"{mean[key]:.3f} &plusmn; {variance[key]:.3f}|"
    
    return row

def process_files(pattern):
    markdown_rows = []

    for filename in sorted(os.listdir()):
        if filename.startswith(pattern) and filename.endswith('.json'):
            try:
                with open(filename, "r") as file:
                    json_data = json.load(file)
                    markdown_row = generate_markdown_row(json_data)
                    markdown_rows.append(markdown_row)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error processing file '{filename}': {e}")
                continue

    return markdown_rows

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <pattern>")
        sys.exit(1)

    pattern = sys.argv[1]

    markdown_rows = process_files(pattern)
    for row in markdown_rows:
        print(row)

if __name__ == "__main__":
    main()
