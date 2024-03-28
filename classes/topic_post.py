"""Define a single post in the topic forum"""
from typing import List

from bs4.element import Tag


class TopicPost(object):
    """An object class to represent a singular topic post"""

    def __init__(self, user_post: Tag):
        """Initialise the topicPost from a BeautifulSoup element Tag object"""
        self.tag = user_post
        self.text: str = user_post.text
        self._parent_post_id: List[int] = None

    @property
    def parent_post_id(self):
        """Looks through Tag to see whether the current post is a reply
        of another post.
        If there is a reply/ies, then the current post's parent(s) is the post(s)
        it replies to"""
        if not self._parent_post_id:
            parent_post_id: List[int] = []
            replies_from_tag: List[Tag] = self.tag.find_all("div", class_="quoteheader")

            if replies_from_tag:
                for prev_post in replies_from_tag:
                    prev_post_url: str = prev_post.find("a").get("href")
                    prev_post_id: int = prev_post_url.split("msg")[-1]
                    parent_post_id.append(prev_post_id)
            self._parent_post_id = parent_post_id

        return self._parent_post_id
