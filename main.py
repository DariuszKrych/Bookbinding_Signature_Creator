from Script.print_formatting import stamp_book, split_to_signatures
import os
import glob
import shutil


book_file_names = []
book_file_paths = glob.glob('Input/*.pdf')
print(book_file_paths)
for book_file_path in book_file_paths:
    book_file_names.append(book_file_path[6:-4])
print(f"\nInput book file name(s):\n{book_file_names}")

for book_file_name in book_file_names:
    book_input_location = 'Input/'+str(book_file_name)+'.pdf'
    book_output_location = 'Output/'+str(book_file_name)

    numbered_pdf_book_file = book_output_location+'/numbered_book.pdf'
    signature_split_pdfs = book_output_location+'/book_signatures'
    signature_page_count = 5 # EDIT THIS TO CHANGE THE PAGE COUNT PER SIGNATURE

    if not os.path.exists(signature_split_pdfs):
        os.makedirs(signature_split_pdfs)

    # Input: pdf_book_file                                    Output: numbered_pdf_book_file
    page_margin_inch = 0.5
    column_gap_inch = 0.99
    column_width_inch = 4.85
    stamp_book(book_input_location, numbered_pdf_book_file, page_margin_inch, column_gap_inch, column_width_inch)

    # Input: numbered_pdf_book_file & signature_page_count    Output: signature_split_pdfs
    split_to_signatures(numbered_pdf_book_file, signature_page_count, signature_split_pdfs)

    shutil.move(book_input_location, book_output_location)