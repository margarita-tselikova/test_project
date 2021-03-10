import requests


class UsersApi:

    @staticmethod
    def create_user(url, data):
        return requests.post(url + 'api/v1.0/users', data=data)

    @staticmethod
    def get_user(url, user_id):
        return requests.get(url + 'api/v1.0/users/' + str(user_id))

    @staticmethod
    def update_user(url, user_id, data):
        return requests.put(url + 'api/v1.0/users/' + str(user_id), data=data)

    @staticmethod
    def delete_user(url, user_id):
        return requests.delete(url + 'api/v1.0/users/' + str(user_id))
