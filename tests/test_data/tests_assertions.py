class UserTestAssertion:

    @staticmethod
    def verify_user(expected, actual):
        assert len(actual) == 3
        assert actual["id"] == expected["id"]
        assert actual["name"] == expected["name"]
        assert actual["surname"] == expected["surname"]
