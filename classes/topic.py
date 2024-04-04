"""Define a single topic forum, that contains multiple user posts"""
from helpers.web_scraping import all_topic_posts


class Topic(object):
    """An object to represent a whole GB topic"""

    def __init__(self, topic_no: int):
        """Initialise the Topic from the topic number"""
        self.user_posts = all_topic_posts(topic_no)
