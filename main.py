import openai
import wget
import pathlib
import pdfplumber
import fpdf



#optional method
def get_paper(paper_url, filename="random_paper.pdf"):
    """
    - download paper according to its URL
    :param paper_url: str
    :param filename: str
    :return: str
    """
    downloadedPaper = wget.download(paper_url, filename)
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)
    return downloadedPaperFilePath

paperContent = pdfplumber.open("data/random_paper.pdf").pages #already downloaded :)

def display_content(paperContent, page_start=0, page_end=5):
    """
    -displays paper content

    :param paperContent:
    :param page_start:
    :param page_end:
    :return:
    """
    for page in paperContent[page_start:page_end]:
        print(page.extract_text())

def show_summary(paperContent):
    tldr_tag = "\n tl;dr:"
    openai.api_key = "API-KEY"
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)  # font and textsize
    with open('summary.txt', 'w') as the_file:
        for page in paperContent:
            text = page.extract_text() + tldr_tag
            response = openai.Completion.create(engine="davinci", prompt=text, temperature=0.3,
                                                max_tokens=140,
                                                top_p=1,
                                                frequency_penalty=0,
                                                presence_penalty=0,
                                                stop=["\n"]
                                                )
            text = response["choices"][0]["text"].encode('latin-1', 'replace').decode('latin-1')
            print(text)
            the_file.write(text+"\n")
            pdf.cell(50,5,txt=text,ln = 1, align="C")
    pdf.output("summary.pdf")

show_summary(paperContent)
