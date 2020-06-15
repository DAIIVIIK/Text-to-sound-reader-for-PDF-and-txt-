import argparse
import os
import sys
import time

import textract
from docx import Document
from gtts import gTTS
from playsound import playsound
from PyPDF2 import PdfFileReader


def play_text(text: str):

    save_name = "sentence.mp3"

    text_to_speech = gTTS(text=text, lang="en")

    text_to_speech.save(save_name)

    playsound(save_name)

    os.unlink(save_name)


def read_text(filename: str):

    with open(filename, "r+") as f:
        reading = f.read()
        contents = reading.rstrip()
        words = contents.split()

    play_text(" ".join(words))


def read_pdf(filename: str):

    with open(filename, "rb") as f:
        reader = PdfFileReader(f)
        num_pages = reader.numPages

    print(f"Your PDF document, {filename}, has {num_pages} pages")
    print("Reading file contents")

    text = textract.process(filename)

    play_text(str(text, "utf-8"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "-t", "--txt", required=False, help="Path to a txt file.",
    )

    ap.add_argument(
        "-p", "--pdf", required=False, help="Path to a pdf file.",
    )

    args = vars(ap.parse_args())

    if args["txt"] is not None:
        read_text(args["txt"])

    if args["pdf"] is not None:
        read_pdf(args["pdf"])
    elif not any(args.values()):
        ap.error("No filenames provided.")

    print("Done!")
