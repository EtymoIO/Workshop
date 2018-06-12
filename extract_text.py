from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from io import StringIO
import os
import os.path

def extract_all_text():
    paper_ids = os.listdir('papers')
    for paper_id in paper_ids:
        try:
            stem = 'papers/' + str(paper_id) + '/fulltext'
            extract_text(stem + '.pdf', stem + '.txt')
            print("Done ", paper_id)
        except Exception as e:
            print("Failed for ", paper_id)
            print(e)

def extract_text(in_filename, out_filename):
    text_pdfminer = ''

    laparams = LAParams()
    laparams.all_texts = True
    rsrcmgr = PDFResourceManager()

    page_num = 0
    fp = open(in_filename,'rb')
    for page in PDFPage.get_pages(fp):
        page_num += 1
        retstr = StringIO()
        device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        interpreter.process_page(page)
        data = retstr.getvalue()
        retstr.close()

        text_pdfminer += data

    with open(out_filename, 'w') as f:
        print(text_pdfminer, file=f)

def isolate_broken_pdfs():
    paper_ids = os.listdir('papers')
    for paper_id in paper_ids:
        if not os.path.isfile('papers/' + str(paper_id) + '/fulltext.txt'):
            print(paper_id)
            os.rename('papers/' + str(paper_id), 'broken_papers/' + str(paper_id))
