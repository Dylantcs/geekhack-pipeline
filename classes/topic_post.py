"""Define a single post in the topic forum"""
from typing import List

from bs4.element import Tag


class topicPost(object):
    """An object class to represent a singular topic post"""

    def __init__(self, userPost: Tag):
        """Initialise the topicPost from a BeautifulSoup element Tag object"""
        self.text = userPost.text
        self.parent_id: List[str] = None
