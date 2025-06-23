import logging
from pathlib import Path
from typing import Optional

import streamlit as st
from docx import Document

from .processor import DocumentProcessor
from .logging import setup_logging

logger = logging.getLogger(__name__)


def process_files(
    template_bytes: bytes,
    worksheet_bytes: bytes,
    cfr_part: Optional[str] = None,
    docket_no: Optional[str] = None,
    notice_no: Optional[str] = None,
) -> Optional[str]:
    """Process uploaded files and return output path."""
    try:
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        template_path = temp_dir / "template.docx"
        worksheet_path = temp_dir / "worksheet.docx"

        template_path.write_bytes(template_bytes)
        worksheet_path.write_bytes(worksheet_bytes)

        processor = DocumentProcessor()
        template_doc = Document(template_path)
        worksheet_doc = Document(worksheet_path)
        data = processor.extractor.extract_data(worksheet_doc)

        if cfr_part:
            data["{CFRPart}"] = cfr_part
        if docket_no:
            data["{DocketNo}"] = docket_no
        if notice_no:
            data["{NoticeNo}"] = notice_no

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "processed_SC.docx"

        path, _ = processor.process_document(
            template_doc,
            data,
            output_path=str(output_path),
        )
        return path
    except Exception:  # pragma: no cover - log and return None
        logger.exception("Failed to process files")
        return None


def main() -> None:
    """Run the Streamlit application."""
    setup_logging()
    st.title("FAA Special Conditions Template Filler")
    template_file = st.file_uploader("Template DOCX", type="docx")
    worksheet_file = st.file_uploader("Worksheet DOCX", type="docx")
    cfr_part = st.text_input("CFR Part(s)")
    docket_no = st.text_input("Docket No.")
    notice_no = st.text_input("Notice No.")

    if st.button("Generate"):
        if not template_file or not worksheet_file:
            st.error("Both files are required")
        else:
            output = process_files(
                template_file.read(),
                worksheet_file.read(),
                cfr_part or None,
                docket_no or None,
                notice_no or None,
            )
            if output and Path(output).exists():
                with open(output, "rb") as f:
                    st.download_button(
                        label="Download Result",
                        data=f,
                        file_name=Path(output).name,
                    )
                st.success("Document generated successfully")
            else:
                st.error("Failed to generate document")


if __name__ == "__main__":
    main()
