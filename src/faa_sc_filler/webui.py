import logging
import gradio as gr
from typing import Tuple, Optional, Dict
from pathlib import Path
from docx import Document
from .processor import DocumentProcessor

logger = logging.getLogger(__name__)

def generate(template: gr.File, worksheet: gr.File, dry_run: bool = False) -> Tuple[Optional[str], Optional[dict]]:
    """Process document through web interface."""
    try:
        logger.info("Starting document generation")
        logger.debug(f"Template file: {template}")
        logger.debug(f"Worksheet file: {worksheet}")
        
        processor = DocumentProcessor()
        
        # Load documents from Gradio file objects
        template_doc = Document(template.name)
        worksheet_doc = Document(worksheet.name)
        
        # Extract data first
        worksheet_data = processor.extractor.extract_data(worksheet_doc)
        logger.debug(f"Extracted data: {worksheet_data}")
        
        # Process document with temporary output path
        output_path = "output/processed_SC.docx" if not dry_run else None
        path, diff = processor.process_document(
            template=template_doc,
            replacements=worksheet_data,
            output_path=output_path,
            dry_run=dry_run
        )
        
        logger.info("Document processing complete")
        return path, diff if dry_run else None
        
    except Exception as e:
        logger.exception("Error in document generation")
        return None, {"error": str(e)}

def create_ui() -> gr.Blocks:
    """Create the Gradio web interface."""
    with gr.Blocks(title="FAA Special Conditions Template Filler") as demo:
        template_file = gr.File(label="SC Template (.docx)", file_types=['.docx'])
        worksheet_file = gr.File(label="Worksheet (.docx)", file_types=['.docx'])
        dry_run = gr.Checkbox(label="Dry-run (preview JSON diff)")
        output_view = gr.File(label="Generated Document")
        diff_view = gr.JSON()

        gr.Button("Generate").click(
            generate,
            inputs=[template_file, worksheet_file, dry_run],
            outputs=[output_view, diff_view]
        )
        
        gr.Markdown("""
        ## Instructions
        1. Upload template DOCX file
        2. Upload worksheet DOCX file
        3. Optional: Check dry-run to preview changes
        4. Click Generate
        """)
    return demo

def main():
    demo = create_ui()
    demo.launch()

if __name__ == "__main__":
    main()
