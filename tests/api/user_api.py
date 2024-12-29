import requests

TIMEOUT = 3 # sec

class UsersApi:
    """API Requests for CRUD User Service"""

    @staticmethod
    def create_user(url, data):
        """Create User with API Request"""
        return requests.post(url + 'api/v1.0/users', json=data, timeout=TIMEOUT)

    @staticmethod
    def get_user(url, user_id):
        """Get User Data with API Request"""
        return requests.get(url + 'api/v1.0/users/' + str(user_id), timeout=TIMEOUT)

    @staticmethod
    def update_user(url, user_id, data):
        """Update User Data with API Request"""
        return requests.put(url + 'api/v1.0/users/' + str(user_id), json=data, timeout=TIMEOUT)

    @staticmethod
    def delete_user(url, user_id):
        """Delete User with API Request"""
        return requests.delete(url + 'api/v1.0/users/' + str(user_id), timeout=TIMEOUT)
