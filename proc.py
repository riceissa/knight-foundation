#!/usr/bin/env python3

import pdb

import requests
from bs4 import BeautifulSoup

def main():
    url = "https://knightfoundation.org/grants?content_sources=grant&page=1"


def get_grant_info(grant_url):
    """Get info off a single grant page."""
    soup = BeautifulSoup(requests.get(grant_url).content, "lxml")

    aside = {"Date Awarded": "",
             "Period": "",
             "Amount": "",
             "Focus Area": "",
             "Challenge": ""}

    for li in soup.find("aside").find_all("li"):
        text = li.text
        for key in aside:
            if text.startswith(key + ":"):
                aside[key] = text[len(key + ":"):].strip()

    headings = {"Goal": "",
                "Project Team": ""}

    for h3 in soup.find_all("h3"):
        # pdb.set_trace()
        text = h3.text
        if text in headings:
            tag = h3.next_element
            while tag.name not in ["div", "p"]:
                tag = tag.next_element
            headings[text] = tag.text.strip()

    aside.update(headings)
    
    return aside


def grants_urls(url):
    """Find all specific grants page URLs on the given page."""
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    for path in filter(lambda x: str(x).startswith("/grants/"),
                       (a.get("href") for a in soup.find_all("a"))):
        yield "https://knightfoundation.org" + path


if __name__ == "__main__":
    main()
