from flask import Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
api = Api(app)


class User(Resource):
    """ Service that allows to create, update, delete a user and get user data"""

    __users = []

    def post(self):
        """User Creation"""

        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("name")
        parser.add_argument("surname")
        params = parser.parse_args()
        user_id = params["id"]
        try:
            if user_id is None or not user_id.isdigit():
                raise ValidationException("Id must be integer")
            for user in self.__users:
                if int(user_id) == user["id"]:
                    raise ValidationException(f"User with id {user_id} already exists")
            self.__validate_params(params)
        except ValidationException as ex:
            return str(ex), 400
        user = {
            "id": int(user_id),
            "name": params["name"].strip(),
            "surname": params["surname"].strip()
        }

        self.__users.append(user)
        return user, 201

    def get(self, user_id):
        """Get User Data"""

        for user in self.__users:
            if user["id"] == int(user_id):
                return user, 200
        return "User not found", 404

    def put(self, user_id):
        """Update User Data"""

        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        params = parser.parse_args()
        try:
            self.__validate_params(params)
        except ValidationException as ex:
            return str(ex), 400
        for user in self.__users:
            if int(user_id) == user["id"]:
                user["name"] = params["name"]
                user["surname"] = params["surname"]
                return user, 200

        user = {
            "id": int(user_id),
            "name": params["name"].strip(),
            "surname": params["surname"].strip()
        }

        self.__users.append(user)
        return user, 201

    def delete(self, user_id):
        """Remove User Data"""

        for user in self.__users:
            if user["id"] == int(user_id):
                self.__users.remove(user)
                result = {
                    "ok": True
                }
                return result, 200
        return "User not found", 404

    def __validate_params(self, params):
        """Method to Validate User Data"""

        name = params["name"]
        surname = params["surname"]
        if name is None or surname is None:
            raise ValidationException('Please specify name and surname fields')
        name = name.strip()
        surname = surname.strip()
        if name == '' or surname == '':
            raise ValidationException("Name and Surname should contain 1 char at least")
        if not name.isalpha() or not surname.isalpha():
            raise ValidationException("Name and surname must be a string")


class ValidationException(BaseException):
    """Custom Validation Error"""

    def __init__(self, message=None):
        super().__init__(message)


api.add_resource(User, "/api/v1.0/users/<int:user_id>", "/api/v1.0/users")
if __name__ == '__main__':
    app.run(debug=True)
