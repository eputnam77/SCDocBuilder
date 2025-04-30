# Standard library imports
import os
import logging

# Third-party imports
from src.faa_sc_filler.processor import DocumentProcessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to orchestrate document processing."""
    try:
        # Initialize the processor
        processor = DocumentProcessor()
        
        # Set paths using project structure
        project_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(project_dir, 'templates', 'SC_Notice_Template.docx')
        worksheet_path = os.path.join(project_dir, 'input', 'SC_worksheet.docx')
        output_path = os.path.join(project_dir, 'output', 'processed_SC.docx')
        
        # Process the document
        processor.process_document(
            template_path=template_path,
            worksheet_path=worksheet_path,
            output_path=output_path
        )
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        raise

if __name__ == "__main__":
    main()
