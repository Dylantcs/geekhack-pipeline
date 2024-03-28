"""Define a single post in the topic forum"""
from typing import List

from bs4.element import Tag


class TopicPost(object):
    """An object class to represent a singular topic post"""

    def __init__(self, user_post: Tag):
        """Initialise the topicPost from a BeautifulSoup element Tag object"""
        self.tag = user_post
        self.id = user_post["id"].split("_")[-1]
        self.text: str = user_post.text
        self.parent_post_id: List[int] = None
        self.previous_post_target_text: List[str] = None
        self.replies: List[str] = None
        self.find_replies()

    def find_replies(self):
        """Looks through Tag to see whether the current post is a reply
        of another post.
        If there is a reply/ies, then the current post's parent(s) is the post(s)
        it replies to"""
        # TODO: handle self.text when post has reply?
        if not self.parent_post_id:
            parent_post_id: List[int] = []
            reply_target_text: List[str] = []
            prev_post_reply: List[str] = []
            replies_from_tag: List[Tag] = self.tag.find_all("div", class_="quoteheader")

            if replies_from_tag:
                for prev_post in replies_from_tag:
                    # get previous post message id
                    prev_post_url: str = prev_post.find("a").get("href")
                    prev_post_id: int = prev_post_url.split("msg")[-1]
                    parent_post_id.append(prev_post_id)

                    # get text part of post that user is replying to
                    prev_post_target_text = prev_post.next_sibling.text
                    reply_target_text.append(prev_post_target_text)
                    # get text of reply
                    reply_text = (
                        prev_post.next_sibling.next_sibling.next_sibling.next_sibling
                    )
                    prev_post_reply.append(reply_text)

            self.parent_post_id = parent_post_id
            self.reply_target_text = reply_target_text
            self.replies = prev_post_reply
