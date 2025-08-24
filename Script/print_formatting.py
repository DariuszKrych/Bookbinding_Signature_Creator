import pypdf
import reportlab
from reportlab.pdfgen.canvas import Canvas as RL_Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import copy
import math

print(f"\n\npypdf library version: {pypdf.__version__}\n"
      f"reportlab library version: {reportlab.__version__}\n")

pdfmetrics.registerFont(TTFont('Baskervville', 'Script/Baskervville-Regular.ttf'))
# https://fonts.google.com/specimen/Baskervville


def stamp_book(book_file_1, numbered_pdf_output):
    with open(book_file_1, 'rb') as book_file:
        reader = pypdf.PdfReader(book_file)
        # writer = pypdf.PdfWriter()

        first_page = reader.pages[0]
        page_width = first_page.mediabox.width
        page_height = first_page.mediabox.height
        page_count = len(reader.pages)
        print(f"Width coords: {page_width}")
        print(f"Height coords: {page_height}")
        print(f"Page Count: {page_count}")
        # Width coords: 841.92      # Height coords: 595.32     # Page Count: 209
        # 72 coordinate unit points per inch of physical length.

    x_1 = (.5 + 4.95129 - .125)*72
    x_2 = (.5 + (4.95129*2) + (2/2.54) - .125)*72
    page_num = 1
    page_doubling_adjust = 0
    while page_num < page_count+1:
        file_path = os.path.join("Script/page_num_stamps", str(page_num)+".pdf")
        canvas = RL_Canvas(file_path, pagesize=(page_width, page_height))
        canvas.setFont("Baskervville", 10)

        canvas.drawRightString(x_1, 24, str(page_num+page_doubling_adjust))
        canvas.drawRightString(x_2, 24, str(page_num+1+page_doubling_adjust))
        canvas.save()

        page_doubling_adjust = page_doubling_adjust + 1
        page_num = page_num + 1



    with open(book_file_1, 'rb') as book_file:
        writer = pypdf.PdfWriter(clone_from = book_file)
            
        # Loop through all pages of the source PDF
        for i, page in enumerate(writer.pages):
            page_number = i + 1
            stamp_file_path = os.path.join("Script/page_num_stamps", f"{page_number}.pdf")

            # Read the corresponding stamp PDF
            stamp_reader = pypdf.PdfReader(stamp_file_path)
            stamp_page = stamp_reader.pages[0]

            # Merge the stamp over the target page
            page.merge_page(stamp_page, over=True)
            print(f"Stamped page {page_number}...")

        # Write the final, merged PDF to a new file
        with open(numbered_pdf_output, "wb") as f_out:
            writer.write(f_out)



def split_to_signatures(book_file, signature_pages, signature_save_folder):

    reader = pypdf.PdfReader(book_file)
    first_page = reader.pages[0]
    page_width = first_page.mediabox.width
    page_height = first_page.mediabox.height
    half_width = page_width/2
    page_doubling_adjust = 0

    page_halves = {}
    for i, page in enumerate(reader.pages):
        page_num = i + 1

        # --- Create Left Half ---
        left_half = copy.deepcopy(reader.pages[i])
        # Crop the left half out & save to object.
        left_half.cropbox.upper_right = (half_width, page_height)
        left_half.mediabox.upper_right = (half_width, page_height)
        page_halves[page_num+page_doubling_adjust] = left_half

        # --- Create Right Half ---
        right_half = copy.deepcopy(reader.pages[i])
        # Crop the right half out & save to object.
        transformation = pypdf.Transformation().translate(tx=-half_width, ty=0)
        right_half.add_transformation(transformation)
        right_half.cropbox.upper_right = (half_width, page_height)
        right_half.mediabox.upper_right = (half_width, page_height)
        page_halves[page_num+1+page_doubling_adjust] = right_half

        page_doubling_adjust = page_doubling_adjust + 1

        print(f"Splitting up page {page_num} into pages {page_num+page_doubling_adjust} & {page_num+1+page_doubling_adjust}.")

    page_num = 1
    signature_num = 1
    pages_in_sig = 1
    sig_jump_up_adjust = 0
    signature_pages_x2 = signature_pages*2
    signature_pdf_writer = pypdf.PdfWriter()

    total_page_num = len(page_halves)/2
    full_sig_count = math.floor(total_page_num/(signature_pages_x2))
    extra_sig_size = total_page_num % (signature_pages_x2)
    small_sig_save_adjust = 0

    while True:
        if signature_num > full_sig_count+1:
            break

        if signature_num == full_sig_count+1:
            small_sig_save_adjust = signature_pages_x2 - extra_sig_size

        left_side_num = page_num+sig_jump_up_adjust
        right_side_num = (signature_pages*4*signature_num)-page_num+1+sig_jump_up_adjust-(small_sig_save_adjust*2)
        full_page = pypdf.PageObject.create_blank_page(width=page_width, height=page_height)
        full_page.merge_page(page_halves[left_side_num])
        full_page.merge_translated_page(page_halves[right_side_num], half_width, 0)
        print(f"Page halves {left_side_num} and {right_side_num} have been merged.")

        signature_pdf_writer.add_page(full_page)
        print(f"Created signature "+str(signature_num)+" part "+str(pages_in_sig))

        pages_in_sig = pages_in_sig + 1
        page_num = page_num + 1
        if pages_in_sig == (signature_pages_x2)+1-small_sig_save_adjust:

            output_file_path = os.path.join(signature_save_folder, "signature_"+str(signature_num)+".pdf")
            with open(output_file_path, "wb") as output_stream:
                signature_pdf_writer.write(output_stream)
            print(f"Saved complete signature "+str(signature_num)+".\n")
            signature_pdf_writer = pypdf.PdfWriter()

            pages_in_sig = 1
            signature_num = signature_num + 1
            sig_jump_up_adjust = sig_jump_up_adjust + (signature_pages_x2)


book_file_name = 'EDIT_THIS_PUT_YOUR_COOL_BOOK_PDF_NAME_HERE'
book_input_location = 'Input/'+str(book_file_name)+'.pdf'
book_output_location = 'Output/'+str(book_file_name)

numbered_pdf_book_file = book_output_location+'/numbered_book.pdf'
signature_split_pdfs = book_output_location+'/book_signatures'
signature_page_count = 5 # EDIT THIS TO CHANGE THE PAGE COUNT PER SIGNATURE

if not os.path.exists(signature_split_pdfs):
    os.makedirs(signature_split_pdfs)

# Input: pdf_book_file                                    Output: numbered_pdf_book_file
stamp_book(book_input_location, numbered_pdf_book_file)
# Input: numbered_pdf_book_file & signature_page_count    Output: signature_split_pdfs
split_to_signatures(numbered_pdf_book_file, signature_page_count, signature_split_pdfs)