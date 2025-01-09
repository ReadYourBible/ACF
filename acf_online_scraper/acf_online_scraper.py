from bs4 import BeautifulSoup
import requests

class SessionManager:
    """Handles HTTP sessions and requests."""
    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url

    def fetch_page(self, path):
        response = self.session.get(f"{self.base_url}{path}")
        response.raise_for_status()
        return response.text


class VerseExtractor:
    """Extracts verses from the HTML content."""
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    def get_text_container(self):
        """Find the main container div for the verses."""
        return self.soup.find("div", class_="FragmentView_text__g6Uq2 FragmentView_verseByVerse__l1TB0")

    def extract_all_verses(self, container):
        """Extract all verses except the first."""
        verses = []
        for span in container.find_all("span", class_="t"):
            verse_text = span.get_text()
            verses.append(verse_text)
        return verses
