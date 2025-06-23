import os


def print_directory_structure(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = "  " * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = "  " * (level + 1)
        for f in files:
            print(f"{subindent}{f}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("Current directory structure:")
    print_directory_structure(base_dir)

    # Check for required directories and files
    required_dirs = ["templates", "input", "output"]
    required_files = {
        "templates/SC_Notice_Template.docx": "Template file",
        "input/SC_worksheet.docx": "Worksheet file",
    }

    missing_dirs = []
    missing_files = []

    # Check directories
    for dir_name in required_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_name)

    # Check files
    for file_path, file_desc in required_files.items():
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append((file_path, file_desc))

    # Print results
    if missing_dirs or missing_files:
        if missing_dirs:
            print("\nMissing required directories:")
            for dir_name in missing_dirs:
                print(f"- {dir_name}")

        if missing_files:
            print("\nMissing required files:")
            for file_path, file_desc in missing_files:
                print(f"- {file_desc}: {file_path}")
    else:
        print("\nAll required directories and files exist!")
