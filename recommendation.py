import random
from typing import List

import bigbox
import util
from catalog import Catalog, Item


class UserData:
    """
    A class to represent user data for gift recommendations.

    Attributes:
    -----------
    age_range : str
        The age range of the user.
    price_range : str
        The price_range for the gift.
    relationship : str
        The relationship of the user to the gift recipient.
    interested : str
        The interests of the user or the gift recipient.
    """
    def __init__(self, age_range: str = "", price_range: str = "", relationship: str = "", interests: str = "", event_type: str = ""):
        """
        Constructs all the necessary attributes for the UserData object.

        Parameters:
        -----------
        age_range : int
            The age range of the user.
        price_range : int
            The budget for the gift.
        relationship : str
            The relationship of the user to the gift recipient.
        interested : str
            The interests of the user or the gift recipient.
        event_type : str
            The event_type of the user or the gift recipient.
        """
        self.age_range = age_range
        self.price_range = price_range
        self.relationship = relationship
        self.interests = interests
        self.event_type = event_type


class RecommendationService(metaclass=util.SingletonMeta):
    """
    A singleton class to represent the recommendation service.

    Methods:
    --------
    recommend(user_data: UserData):
        Recommends a gift based on the user's age range and budget.
    """

    def __init__(self, catalog: Catalog):
        """
        Constructs all the necessary attributes for the RecommendationService object.

        Parameters:
        -----------
        catalog : Catalog
            The catalog of items to recommend.
        """
        self.catalog = catalog

    def recommend(self, user_data: UserData) -> List[bigbox.Box]:
        """
        Recommends a gift based on the user's age range and budget.

        Parameters:
        -----------
        user_data : UserData
            The user data containing age range, budget, relationship, and interests.
        """

        recommended_items: List[Item] = []
        for item in self.catalog.items:
            if (item.age_range == user_data.age_range and
                    item.price_range == user_data.price_range and
                    item.relationship == user_data.relationship and
                    item.interests == user_data.interests and
                    item.event_type == user_data.event_type):
                recommended_items.append(item)

        if not recommended_items:
            recommended_items.append(random.choice(self.catalog.items))

        boxes: List[bigbox.Box] = []
        for item in recommended_items:
            slug = item.url.rstrip('/').split('/')[-1]

            if "experiencias" in item.url:
                box = bigbox.fetch_activity(item.url)
                boxes.append(box)

            if "regalos" in item.url:
                box: bigbox.Box = bigbox.fetch_box(slug)
                boxes.append(box)

        return boxes
