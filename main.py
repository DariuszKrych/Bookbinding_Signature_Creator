from Script.print_formatting import stamp_book, split_to_signatures
import os
import glob
import shutil
from pathlib import Path

# Anchor to the project root (same level as main.py)
ROOT_DIR = Path(__file__).resolve().parent


def main():
    book_file_names = []
    # Search for PDFs using the absolute path to the Input folder
    book_file_paths = glob.glob(str(ROOT_DIR / 'Input' / '*.pdf'))

    print(f"Input book file path(s):\n{book_file_paths}")
    for book_file_path in book_file_paths:
        # .stem extracts just the file name (e.g., "my_book") safely from the absolute path
        book_file_names.append(Path(book_file_path).stem)
    print(f"\nInput book file name(s):\n{book_file_names}")

    for book_file_name in book_file_names:
        # Build all paths using ROOT_DIR
        book_input_location = ROOT_DIR / 'Input' / f"{book_file_name}.pdf"
        book_output_location = ROOT_DIR / 'Output' / book_file_name

        numbered_pdf_book_file = book_output_location / 'numbered_book.pdf'
        signature_split_pdfs = book_output_location / 'book_signatures'
        signature_page_count = 5  # EDIT THIS TO CHANGE THE PAGE COUNT PER SIGNATURE

        if not os.path.exists(signature_split_pdfs):
            os.makedirs(signature_split_pdfs)

        # Input: pdf_book_file                                    Output: numbered_pdf_book_file
        page_margin_inch = 0.5
        column_gap_inch = 0.99
        column_width_inch = 4.85

        # Wrapping in str() safely handles the arguments for your formatting script
        stamp_book(str(book_input_location), str(numbered_pdf_book_file), page_margin_inch, column_gap_inch,
                   column_width_inch)

        # Input: numbered_pdf_book_file & signature_page_count    Output: signature_split_pdfs
        split_to_signatures(str(numbered_pdf_book_file), signature_page_count, str(signature_split_pdfs))

        shutil.move(str(book_input_location), str(book_output_location))


# if __name__ == "__main__":
#     main()