# pylint: disable=too-few-public-methods

class UserTestAssertion:
    """Class with bulk checks of User Data"""

    @staticmethod
    def verify_user(expected, actual):
        """Method to check all User Data"""

        assert len(actual) == 3
        assert actual["id"] == expected["id"]
        assert actual["name"] == expected["name"]
        assert actual["surname"] == expected["surname"]
