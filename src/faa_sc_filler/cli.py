import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Tuple, Optional, Dict, List
from .processor import DocumentProcessor
from .validator import DocumentValidator
from .config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="FAA Special Conditions Template Filler")
    parser.add_argument("--template", required=True, help="Path to template DOCX")
    parser.add_argument("--worksheet", required=True, help="Path to worksheet DOCX")
    parser.add_argument("--output", help="Output path (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without saving")
    parser.add_argument("--need-token", default=DEFAULT_CONFIG["need_token"],
                      help="Token for missing fields")
    parser.add_argument("--log-level", choices=["DEBUG","INFO","WARNING","ERROR"],
                      default="INFO", help="Logging level")
    
    # Add version argument
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    return parser.parse_args(args)

def main() -> int:
    """Main CLI entry point."""
    args = parse_args()
    # ... implementation ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
