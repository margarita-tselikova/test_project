# pylint: disable=too-few-public-methods

from random import randint
from faker import Faker

fake = Faker()


class UserFactory:
    """Class to create a Test User"""

    def __init__(self):
        self.id = randint(1, 999999)
        self.name = fake.first_name()
        self.surname = fake.last_name()
