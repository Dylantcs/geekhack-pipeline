"""Helpers for scraping a geekhack page"""
import requests
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


def all_topic_posts(topic_id: int):
    """Loops all pages of a given topic to obtain
    all user posts in html block format"""

    topic_fp_url = f"https://geekhack.org/index.php?topic={topic_id}"
    topic_fp = requests.get(topic_fp_url)
    topic_fp_soup = BeautifulSoup(topic_fp.content, "html.parser")

    topic_page_no = topic_pages(topic_fp_soup)
    topic_posts = topic_posts_by_page(topic_fp_soup)

    # gb url has page number as gb_fp_url.00 for page 1
    # followed by gb_fp_url.50 for page 2

    for i in range(1, topic_page_no):
        page_counter = i * 0.5
        topic_page_id = topic_id + page_counter
        topic_page_url = f"https://geekhack.org/index.php?topic={topic_page_id}0"
        topic_page = requests.get(topic_page_url)
        topic_page_soup = BeautifulSoup(topic_page.content, "html.parser")

        topic_page_posts = topic_posts_by_page(topic_page_soup)
        topic_posts.extend(topic_page_posts)

    return topic_posts
