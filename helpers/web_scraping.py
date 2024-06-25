"""Helpers for scraping a geekhack page"""
from datetime import datetime
from typing import Dict, List

import bs4
import requests


def topic_pages(page_soup: bs4.BeautifulSoup) -> int:
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


def topic_posts_by_page(page_soup: bs4.BeautifulSoup) -> List[bs4.element.Tag]:
    """Obtain user posts in html block format for a particular page"""
    subposts = page_soup.find_all("div", class_="inner")
    # return [subpost.text for subpost in subposts]
    return subposts


def all_topic_posts(topic_id: int) -> List[bs4.element.Tag]:
    """Loops all pages of a given topic to obtain
    all user posts in html block format"""

    topic_fp_url = f"https://geekhack.org/index.php?topic={topic_id}"
    topic_fp = requests.get(topic_fp_url)
    topic_fp_soup = bs4.BeautifulSoup(topic_fp.content, "html.parser")

    topic_page_no = topic_pages(topic_fp_soup)
    topic_posts = topic_posts_by_page(topic_fp_soup)

    # gb url has page number as gb_fp_url.00 for page 1
    # followed by gb_fp_url.50 or gb_fp_url.050 for page 2

    for pg in range(1, topic_page_no):
        page_counter = pg * 0.05
        topic_page_id = topic_id + page_counter
        if (pg + 1) % 2 == 0:
            topic_page_url = f"https://geekhack.org/index.php?topic={topic_page_id}0"
        else:
            topic_page_url = f"https://geekhack.org/index.php?topic={topic_page_id}00"
        topic_page = requests.get(topic_page_url)
        topic_page_soup = bs4.BeautifulSoup(topic_page.content, "html.parser")

        topic_page_posts = topic_posts_by_page(topic_page_soup)
        topic_posts.extend(topic_page_posts)

    return topic_posts


def get_gb_pages(first_gb_page_bs: bs4.BeautifulSoup) -> int:
    """Find page navigation bar and get total gb pages"""
    gb_page_nav_bar = first_gb_page_bs.find("div", class_ = "pagelinks floatleft")
    gb_pages = gb_page_nav_bar.find_all("a", class_ = "navPages")
    gb_page_text_list = [
        navPage.text for navPage in gb_pages if "»" not in navPage.text
    ]
    page_num_list = [int(text) for text in gb_page_text_list]
    return max(page_num_list)


def get_gb_listings() -> Dict[str, Dict[str, bs4.Tag]]:
    """Searches through group buy listings and obtains subject block and last post block for each
    listing in a dictionary"""
    gb_first_page_url = "https://geekhack.org/index.php?board=70"
    listed_gb_blocks = {}
    gb_first_page_req = requests.get(gb_first_page_url)
    gb_first_page_bs = bs4.BeautifulSoup(gb_first_page_req.content, "html.parser")
    gb_pages = get_gb_pages(gb_first_page_bs)
    # TODO: change page range to all gb pages gb_pages attribute
    for gb_page in range(5):
        print(f"--Looking at page {gb_page + 1}--")
        gb_url_tag = str(round(0.05 * gb_page, 2))[1:]
        if (gb_page + 1) % 2 == 0:
            gb_page_url = gb_first_page_url + f"{gb_url_tag}0"
        else:
            gb_page_url = gb_first_page_url + f"{gb_url_tag}00"
        gb_page_req = requests.get(gb_page_url)
        gb_page_bs = bs4.BeautifulSoup(gb_page_req.content, "html.parser")
        listed_gbs_main_block = gb_page_bs.find_all(
            "span", id=lambda txt: txt is not None and "msg" in txt
        )

        for gb_subject_block in listed_gbs_main_block:
            gb_id = gb_subject_block.get("id")
            last_post_block = (
                gb_subject_block.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling
            )
            gb_content_blocks = {
                "main_block": gb_subject_block,
                "last_post_block": last_post_block,
            }
            listed_gb_blocks[gb_id] = gb_content_blocks

    return listed_gb_blocks


def get_subject_details(subject_block: bs4.Tag) -> List[str]:
    """Takes in a subject block and looks at its contents to retrieve
    the following as a list:
        - subject title
        - author's username
        - total number of pages
        - sub-forum url
    """
    subject_title = subject_block.text
    sub_forum_url = subject_block.find("a").get("href")
    author_block = subject_block.next_sibling.next_sibling
    author_username = author_block.find("a").text

    pages_block = author_block.find("small")
    navPages_block = pages_block.find_all("a", class_="navPages")
    if navPages_block:
        subject_pages = int(navPages_block[-1].text)
    else:
        subject_pages = 1

    return [subject_title, author_username, subject_pages, sub_forum_url]


def get_last_post_details(last_post_block: bs4.Tag) -> List[str]:
    """Takes in a last post block and return the following in a list:
    - last post date
    - author of last post"""
    details = last_post_block.text
    cleaned_details = details.replace("\t", "").replace("\n", "")
    split_details = cleaned_details.split("by")

    last_post_date = split_details[0]
    last_post_date_no_day = "".join(last_post_date.split(",")[1:]).strip()
    last_post_datetime = datetime.strptime(last_post_date_no_day, "%d %B %Y %H:%M:%S")
    last_post_author = split_details[1].strip()

    return [str(last_post_datetime), last_post_author]


def get_listed_gb_details() -> List[List[str]]:
    """
    Finds the gb listing blocks on first page and collates them into a List of List of details
    Returns the following details for each listing in order:
        - GB message number (part of html data)
        - GB author
        - total number of pages of the GB
        - GB url (Used later to access post in sub-forum)
        - date of last post in GB sub-forum
        - author of last post in GB sub-forum
    """
    # TODO: Extend search to all GB listing pages
    gb_listings = get_gb_listings()
    gb_listings_details = []

    for msg_no, detail_blocks in gb_listings.items():
        print(msg_no)
        subject_details = get_subject_details(detail_blocks["main_block"])
        last_post_details = get_last_post_details(detail_blocks["last_post_block"])

        listing_details = []
        listing_details.append(msg_no)
        listing_details.extend(subject_details)
        listing_details.extend(last_post_details)
        print("Done")
        gb_listings_details.append(listing_details)
    return gb_listings_details
