#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Victor V. R. Matos (@vvrmatos)
# Description: This script creates a directory structure for books of the Bible,
# fetches chapter content from the ACF Bible website, and saves verses as text files.
# License: CC0 1.0 Universal


import os
import re
import sys

from pathlib import Path
from collections import namedtuple
from acf_online_scraper import SessionManager, VerseExtractor


file_path = Path(__file__)
root_path = file_path.parent.parent


Book = namedtuple("Book", ["name", "chapters", "code"])


books_data = [
    ("Gênesis", 50, "gn"), ("Êxodo", 40, "ex"), ("Levítico", 27, "lv"), ("Números", 36, "nm"),
    ("Deuteronômio", 34, "dt"), ("Josué", 24, "js"), ("Juízes", 21, "jz"), ("Rute", 4, "rt"),
    ("I Samuel", 31, "1sm"), ("II Samuel", 24, "2sm"), ("I Reis", 22, "1rs"), ("II Reis", 25, "2rs"),
    ("I Crônicas", 29, "1cr"), ("II Crônicas", 36, "2cr"), ("Esdras", 10, "ed"), ("Neemias", 13, "ne"),
    ("Ester", 10, "et"), ("Jó", 42, "jó"), ("Salmos", 150, "sl"), ("Provérbios", 31, "pv"),
    ("Eclesiastes", 12, "ec"), ("Cânticos", 8, "ct"), ("Isaías", 66, "is"), ("Jeremias", 52, "jr"),
    ("Lamentações", 5, "lm"), ("Ezequiel", 48, "ez"), ("Daniel", 12, "dn"), ("Oséias", 14, "os"),
    ("Joel", 3, "jl"), ("Amós", 9, "am"), ("Obadias", 1, "ob"), ("Jonas", 4, "jn"), ("Miquéias", 7, "mq"),
    ("Naum", 3, "na"), ("Habacuque", 3, "hc"), ("Sofonias", 3, "sf"), ("Ageu", 2, "ag"),
    ("Zacarias", 14, "zc"), ("Malaquias", 4, "ml"), ("Mateus", 28, "mt"), ("Marcos", 16, "mc"),
    ("Lucas", 24, "lc"), ("João", 21, "jo"), ("Atos", 28, "atos"), ("Romanos", 16, "rm"),
    ("I Coríntios", 16, "1co"), ("II Coríntios", 13, "2co"), ("Gálatas", 6, "gl"),
    ("Efésios", 6, "ef"), ("Filipenses", 4, "fp"), ("Colossenses", 4, "cl"),
    ("I Tessalonicenses", 5, "1ts"), ("II Tessalonicenses", 3, "2ts"), ("I Timóteo", 6, "1tm"),
    ("II Timóteo", 4, "2tm"), ("Tito", 3, "tt"), ("Filemom", 1, "fm"), ("Hebreus", 13, "hb"),
    ("Tiago", 5, "tg"), ("I Pedro", 5, "1pe"), ("II Pedro", 3, "2pe"), ("I João", 5, "1jo"),
    ("II João", 1, "2jo"), ("III João", 1, "3jo"), ("Judas", 1, "jd"), ("Apocalipse", 22, "ap")
]


books = [Book(name, chapters, code) for name, chapters, code in books_data]


def create_book_dir(books: Book):
    for book in books:
        book_number = books.index(book) + 1
        book_number = str(book_number) if book_number >= 10 else "0" + str(book_number)        
        book_dir_name = f"{book_number}-{book.code}"
        os.makedirs(root_path / book_dir_name, exist_ok=True)


def main():    
    base_url = "https://www.bibliaonline.com.br"
    session_manager = SessionManager(base_url)

    create_book_dir(books)

    for book in books:

        book_number = books.index(book) + 1
        book_number = f"0{book_number}" if book_number < 10 else str(book_number)
        book_dir_name = f"{book_number}-{book.code}"
        print(book_dir_name)

        for chapter in range(1, book.chapters + 1):
            chapter_number = f"0{chapter}" if chapter < 10 else str(chapter)
            file_name = f"{book.code}-{chapter_number}.txt"
            print(file_name)
    
            page_path = f"/acf/{book.code}/{chapter}"
            
            page_content = session_manager.fetch_page(page_path)

            # Extract verses
            extractor = VerseExtractor(page_content)
            container = extractor.get_text_container()

            
            if container:
                verses = []

                    
                verses.extend(extractor.extract_all_verses(container))

                # Process the verses (e.g., save to file, print, etc.)
                print(f"Book: {book.name}, Chapter: {chapter}")
                file_path = root_path / book_dir_name / file_name
                if not file_path.exists() or file_path.stat().st_size == 0:
                    for verse in verses:
                        cleaned_verse = re.sub(r"^\d+\s*", "", verse)
                        print(cleaned_verse)

                        with open(file_path, "a") as file:
                            if verse == verses[-1]:
                                file.write(cleaned_verse)
                            else:
                                file.write(cleaned_verse + "\n")
                else:
                    print(f"File {file_name} is not empty. Skipping.")
            else:
                print(f"No verses found for {book.name} Chapter {chapter}!")


if __name__ == "__main__":
    main()
