import openai
import wget
import pathlib
import pdfplumber



def getPaper(paper_url, filename="random_paper.pdf"):
    downloadedPaper = wget.download(paper_url, filename)
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)
    return downloadedPaperFilePath

paperContent = pdfplumber.open("data/random_paper.pdf").pages

def displayPaperContent(paperContent, page_start=0, page_end=5):
    for page in paperContent[page_start:page_end]:
        print(page.extract_text())


def showPaperSummary(paperContent):
    tldr_tag = "\n tl;dr:"
    openai.api_key = "API-KEY"

    for page in paperContent:
        text = page.extract_text() + tldr_tag
        response = openai.Completion.create(engine="davinci", prompt=text, temperature=0.3,
                                            max_tokens=140,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                            stop=["\n"]
                                            )
        print(response["choices"][0]["text"])

showPaperSummary(paperContent)
