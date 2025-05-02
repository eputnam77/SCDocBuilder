import logging
import gradio as gr
from typing import Tuple, Optional, Dict
import re
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

def validate_inputs(cfr_part: str, docket_no: str, notice_no: str) -> Dict[str, str]:
    """Validate user inputs and return error messages."""
    errors = {}
    valid_parts = {"23", "25", "27", "29", "31", "33", "35"}
    
    if cfr_part:
        parts = {p.strip() for p in cfr_part.split(",")}
        if not all(p in valid_parts for p in parts):
            errors["cfr_part"] = "Invalid CFR Part(s). Use comma-separated values from: 23,25,27,29,31,33,35"
            
    if docket_no and not re.match(r'^FAA-\d{4}-\d{4}$', docket_no):
        errors["docket_no"] = "Invalid format. Use FAA-YYYY-XXXX"
        
    if notice_no and not re.match(r'^\d{2}-\d{2}-\d{2}-SC$', notice_no):
        errors["notice_no"] = "Invalid format. Use XX-XX-XX-SC"
        
    return errors

def enhanced_generate(template_file, worksheet_file, cfr_part=None, docket_no=None, notice_no=None, dry_run=False):
    """Enhanced document generation with optional fields."""
    try:
        # Load documents first
        template_doc = Document(template_file.name)
        worksheet_doc = Document(worksheet_file.name)
        
        # Process document with optional fields
        processor = DocumentProcessor()
        worksheet_data = processor.extractor.extract_data(worksheet_doc)
        
        # Add optional fields if provided
        if cfr_part: worksheet_data["{CFRPart}"] = cfr_part
        if docket_no: worksheet_data["{DocketNo}"] = docket_no
        if notice_no: worksheet_data["{NoticeNo}"] = notice_no
        
        return processor.process_document(template_doc, worksheet_data, dry_run=dry_run)
        
    except Exception as e:
        logger.exception("Error in enhanced document generation")
        return None, {"error": str(e)}

def create_ui() -> gr.Blocks:
    """Create the Gradio web interface."""
    # Create output directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)
    
    with gr.Blocks(title="FAA Special Conditions Template Filler") as demo:
        template_file = gr.File(label="SC Template (.docx)", file_types=['.docx'])
        worksheet_file = gr.File(label="Worksheet (.docx)", file_types=['.docx'])
        
        gr.Markdown("### Optional Fields")
        with gr.Row():
            cfr_part = gr.Textbox(label="CFR Part(s) (comma-separated)", placeholder="25,27")
            docket_no = gr.Textbox(label="Docket No.", placeholder="FAA-2024-0001")
            notice_no = gr.Textbox(label="Notice No.", placeholder="24-01-01-SC")
            
        dry_run = gr.Checkbox(label="Dry-run (preview JSON diff)")
        
        with gr.Column():
            output_view = gr.File(label="Generated Document", interactive=True)
            download_button = gr.Button("Download Result", visible=False)
            diff_view = gr.JSON(label="Changes Preview")
            error_view = gr.Markdown()

        def handle_generation(*args):
            template, worksheet, cfr, docket, notice, dry_run = args
            try:
                # Load documents first
                template_doc = Document(template.name)
                worksheet_doc = Document(worksheet.name)
                
                # Process with optional fields
                processor = DocumentProcessor()
                worksheet_data = processor.extractor.extract_data(worksheet_doc)
                
                # Add optional fields if provided
                if cfr: worksheet_data["{CFRPart}"] = cfr
                if docket: worksheet_data["{DocketNo}"] = docket
                if notice: worksheet_data["{NoticeNo}"] = notice
                
                # Process document
                output_path = "output/processed_SC.docx" if not dry_run else None
                path, diff = processor.process_document(
                    template=template_doc,
                    replacements=worksheet_data,
                    output_path=output_path,
                    dry_run=dry_run
                )
                
                if path:
                    return path, diff, True
                return None, diff, False
                
            except Exception as e:
                logger.exception("Error in document generation")
                return None, {"error": str(e)}, False

        def trigger_download(file_path):
            """Handle file download."""
            if file_path:
                return file_path
            return None

        gr.Button("Generate").click(
            fn=handle_generation,
            inputs=[template_file, worksheet_file, cfr_part, docket_no, notice_no, dry_run],
            outputs=[output_view, diff_view, download_button]
        )

        # Update download button handler
        download_button.click(
            fn=trigger_download,
            inputs=[output_view],
            outputs=[gr.File()],
            api_name="download"
        )

        gr.Markdown("""
        ## Instructions
        1. Upload template DOCX file
        2. Upload worksheet DOCX file
        3. Optionally enter CFR Part, Docket No., and Notice No.
        4. Click Generate
        """)
    return demo

def main():
    demo = create_ui()
    demo.launch()

if __name__ == "__main__":
    main()
