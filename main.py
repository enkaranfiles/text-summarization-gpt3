import openai
import wget
import pathlib
import pdfplumber
import fpdf
import json

from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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


def show_summary_save_file(paperContent):
    tldr_tag = "\n tl;dr:"
    openai.api_key = "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"
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

@app.route('/gpt_summary', methods=['GET'])
def show_summary(paperContent):
    """
    -for api call
    :param paperContent:
    :return:
    """
    tldr_tag = "\n tl;dr:"
    openai.api_key = "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"
    summary = ""
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
            summary = text + "\n"
    return summary

@app.route('/summary', methods=['GET'])
def show_one_summary():
    original_file = request.args.get("original_file")
    file = open("./summary.txt", "r").read()
    item = {
        "file_name": original_file,
        "summary_text": file
    }
    return json.dumps(item)


if __name__ == '__main__':
    app.run()

#print(show_one_summary("rondom_text.pdf"))
