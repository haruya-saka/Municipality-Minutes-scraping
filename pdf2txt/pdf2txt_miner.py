import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as f:
        outf = StringIO()
        rm = PDFResourceManager()
        lap = LAParams()
        dev = TextConverter(rm, outf, laparams=lap)
        iprtr = PDFPageInterpreter(rm, dev)

        for page in PDFPage.get_pages(f):
            iprtr.process_page(page)

        contents = outf.getvalue()

        dev.close()
        outf.close()

        return contents

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def convert_pdfs(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        print(filename)
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            text = pdf_to_text(pdf_path)

            # 各PDFに対応するtxtファイルを作成し、output_folderに保存
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".txt")
            save_text_to_file(text, output_path)

if __name__ == "__main__":
    # PDFファイルがあるフォルダと出力先フォルダを指定
    pdf_folder = "/Users/sakaguchi/Documents/地方会議録/Municipality-Minutes-scraping/pdf/toyoura"
    output_folder = "/Users/sakaguchi/Documents/地方会議録/Municipality-Minutes-scraping/txt/toyoura"

    convert_pdfs(pdf_folder, output_folder)

