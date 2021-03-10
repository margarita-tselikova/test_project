from flask import Flask
from flask_restful import Api, Resource, reqparse
app = Flask(__name__)
api = Api(app)

users_list = []


class User(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("name")
        parser.add_argument("surname")
        params = parser.parse_args()
        id = params["id"]
        try:
            if id is None or not id.isdigit():
                raise ValidationException("Id must be integer")
            for user in users_list:
                if (int(id) == user["id"]):
                    raise ValidationException(f"User with id {id} already exists")
            self.__validate_params(params)
        except ValidationException as ex:
            return str(ex), 400
        user = {
            "id": int(id),
            "name": params["name"].strip(),
            "surname": params["surname"].strip()
        }

        users_list.append(user)
        return user, 201

    def get(self, id):
        for user in users_list:
            if (user["id"] == int(id)):
                return user, 200
        return "User not found", 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        params = parser.parse_args()
        try:
            self.__validate_params(params)
        except ValidationException as ex:
            return str(ex), 400
        for user in users_list:
            if (int(id) == user["id"]):
                user["name"] = params["name"]
                user["surname"] = params["surname"]
                return user, 200

        user = {
            "id": int(id),
            "name": params["name"].strip(),
            "surname": params["surname"].strip()
        }

        users_list.append(user)
        return user, 201

    def delete(self, id):
        global users_list
        user_ids = []
        for user in users_list:
            user_ids.append(user["id"])
        if id not in user_ids:
            return "User not found", 404
        users_list = [user for user in users_list if user["id"] != int(id)]
        result = {
            "ok": True
        }
        return result, 200

    def __validate_params(self, params):
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
    pass


api.add_resource(User, "/api/v1.0/users/<int:id>", "/api/v1.0/users")
if __name__ == '__main__':
    app.run(debug=True)
