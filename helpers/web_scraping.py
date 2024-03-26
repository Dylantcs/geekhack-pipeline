"""Helpers for scraping a geekhack page"""
from bs4 import BeautifulSoup


def topic_pages(page_soup: BeautifulSoup):
    """Obtain number of pages for a given topic"""
    page_navigation = list(set(page_soup.find_all("a", class_="navPages")))
    page_text_list = [
        navPage.text for navPage in page_navigation if "»" not in navPage.text
    ]
    page_num_list = [int(text) for text in page_text_list]
    return max(page_num_list)


def topic_posts(page_soup: BeautifulSoup):
    """Obtain user posts in html block format"""
    subposts = page_soup.find_all("div", class_="inner")
    # return [subpost.text for subpost in subposts]
    return subposts
