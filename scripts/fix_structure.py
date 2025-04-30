import os
import shutil

def fix_directory_structure():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create input directory if it doesn't exist
    input_dir = os.path.join(base_dir, 'input')
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created directory: {input_dir}")
    
    # Move worksheet file
    worksheet_src = os.path.join(base_dir, 'worksheet', 'SC_worksheet.docx')
    worksheet_dst = os.path.join(input_dir, 'SC_worksheet.docx')
    if os.path.exists(worksheet_src):
        shutil.move(worksheet_src, worksheet_dst)
        print(f"Moved worksheet file to: {worksheet_dst}")
        # Remove empty worksheet directory
        os.rmdir(os.path.join(base_dir, 'worksheet'))
        print("Removed empty worksheet directory")
    
    # Rename template file
    template_dir = os.path.join(base_dir, 'templates')
    old_template = os.path.join(template_dir, 'SC - Notice of Proposed SC TEMPLATE - Placeholders.docx')
    new_template = os.path.join(template_dir, 'SC_Notice_Template.docx')
    if os.path.exists(old_template):
        os.rename(old_template, new_template)
        print(f"Renamed template file to: {new_template}")

if __name__ == "__main__":
    fix_directory_structure()
