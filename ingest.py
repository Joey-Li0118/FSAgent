"""
Standalone ingestion script.
Run this once to load all FSA handbooks before starting the app.

Usage:
    python ingest.py data/pdfs/1-ARCPLC.pdf data/pdfs/1-CRP.pdf
    python ingest.py USDA_PDFs/   # ingest entire folder
"""

import sys
import os
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from chatbot.rag import FSANavigator


def main():
    paths = []

    if not sys.argv[1:]:
        print("Usage: python ingestion/ingest.py <pdf_path_or_folder>")
        print("\nTip: Download FSA handbooks from:")
        print("  https://www.fsa.usda.gov/Internet/FSA_File/1-arcplc.pdf")
        print("  https://www.fsa.usda.gov/Internet/FSA_File/1-crp.pdf")
        sys.exit(1)

    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            paths.extend(glob.glob(os.path.join(arg, "*.pdf")))
        elif os.path.isfile(arg) and arg.endswith(".pdf"):
            paths.append(arg)
        else:
            print(f"Skipping: {arg} (not a PDF or directory)")

    if not paths:
        print("No PDF files found.")
        sys.exit(1)

    print(f"Found {len(paths)} PDF(s) to ingest:")
    for p in paths:
        print(f"  - {p}")

    navigator = FSANavigator()
    print("\nIngesting...")
    count = navigator.ingest_pdfs(paths)
    total = navigator.collection_size()

    print(f"\n✅ Done. Added {count} new chunks. Total in DB: {total}")


if __name__ == "__main__":
    main()
