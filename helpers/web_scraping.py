"""Helpers for scraping a geekhack page"""
from bs4 import BeautifulSoup


def topic_pages(page_soup: BeautifulSoup):
    """Obtain number of pages for a given topic from front page"""
    page_navigation = list(set(page_soup.find_all("a", class_="navPages")))
    page_text_list = [
        navPage.text for navPage in page_navigation if "»" not in navPage.text
    ]
    page_num_list = [int(text) for text in page_text_list]

    # We do the following checks because we do not find the navPages button 1
    if page_num_list:
        return max(page_num_list)
    else:
        return 1


def topic_posts_by_page(page_soup: BeautifulSoup):
    """Obtain user posts in html block format for a particulat page"""
    subposts = page_soup.find_all("div", class_="inner")
    # return [subpost.text for subpost in subposts]
    return subposts
