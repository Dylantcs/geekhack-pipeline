"""Define a single topic forum, that contains multiple user posts"""

from typing import List

from classes.topic_post import TopicPost
from helpers.web_scraping import all_topic_posts


class Topic(object):
    """An object to represent a whole GB topic"""

    def __init__(self, topic_no: int):
        """Initialise the Topic from the topic number"""
        self.topic_no = topic_no
        self.raw_user_posts = all_topic_posts(topic_no)
        self._user_posts = None
        self.main_post = self.user_posts[0]

    def __repr__(self) -> str:
        return f"Topic {self.topic_no}"

    @property
    def user_posts(self) -> List[TopicPost]:
        """Convert user posts in TopicPost object format"""
        if not self._user_posts:
            self._user_posts = [
                TopicPost(user_post) for user_post in self.raw_user_posts
            ]
        return self._user_posts
