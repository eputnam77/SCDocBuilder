import gradio as gr
from typing import Tuple, Optional, Dict
from .processor import DocumentProcessor

def create_ui() -> gr.Blocks:
    """Create the Gradio web interface."""
    with gr.Blocks(title="FAA Special Conditions Template Filler") as demo:
        template_file = gr.File(label="SC Template (.docx)", file_types=['.docx'])
        worksheet_file = gr.File(label="Worksheet (.docx)", file_types=['.docx'])
        dry_run = gr.Checkbox(label="Dry-run (preview JSON diff)")
        output_view = gr.File(label="Generated Document")
        diff_view = gr.JSON()

        def generate(template, worksheet, dry_run) -> Tuple[Optional[str], Optional[Dict]]:
            processor = DocumentProcessor()
            path, diff = processor.process_document(template, worksheet, dry_run=dry_run)
            return (None if dry_run else path), (diff or None)

        gr.Button("Generate").click(
            generate,
            inputs=[template_file, worksheet_file, dry_run],
            outputs=[output_view, diff_view]
        )
    return demo

def main():
    demo = create_ui()
    demo.launch()

if __name__ == "__main__":
    main()
