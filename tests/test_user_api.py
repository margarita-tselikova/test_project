# pylint: disable=too-many-public-methods

import random
import string
from http import HTTPStatus
from random import randint

import pytest

from tests.api.user_api import UsersApi
from tests.test_data.testing_data import UserFactory
from tests.test_data.tests_assertions import UserTestAssertion

USER_NOT_STRING_ERROR = "Name and surname must be a string"
USER_ALREADY_EXISTS_ERROR = "User with id {id} already exists"
USER_DATA_NOT_SPECIFIED_ERROR = "Please specify name and surname fields"
USER_ID_IS_NOT_INT_ERROR = "Id must be integer"
USER_NOT_FOUND_ERROR = "User not found"
USER_DATA_EMPTY_STRING_ERROR = 'Name and Surname should contain 1 char at least'


class TestUserApi:
    """User API Service Tests"""

    @pytest.fixture
    def user_dict(self, base_url):
        """Generating Test User Data and Deleting User after a Test"""
        user = UserFactory().__dict__
        yield user
        UsersApi.delete_user(base_url, user_id=user["id"])

    def test_create_user(self, base_url, user_dict):
        """User Creation Test"""
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.CREATED
        UserTestAssertion.verify_user(user_dict, response.json())

    def test_create_duplicate(self, base_url, user_dict):
        """Bad Request: User already exists error check"""
        user = UsersApi.create_user(base_url, data=user_dict)
        assert user.status_code == HTTPStatus.CREATED
        duplicate = UsersApi.create_user(base_url, data=user_dict)
        assert duplicate.status_code == HTTPStatus.BAD_REQUEST
        assert duplicate.json() == USER_ALREADY_EXISTS_ERROR.format(id=user_dict["id"])

    def test_create_user_without_id(self, base_url, user_dict):
        """Bad Request: User ID is Undefined"""
        user_dict['id'] = None
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_ID_IS_NOT_INT_ERROR

    def test_create_user_without_name(self, base_url, user_dict):
        """Bad Request: User Name is Undefined"""
        user_dict['name'] = None
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_DATA_NOT_SPECIFIED_ERROR

    def test_create_user_with_empty_name(self, base_url, user_dict):
        """Bad Request: min. length verification - empty User Name"""
        user_dict['name'] = ''
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_DATA_EMPTY_STRING_ERROR

    def test_create_user_with_one_char_name(self, base_url, user_dict):
        """User Creation: min. length verification - 1 char User Name"""
        user_dict['name'] = random.choice(string.ascii_letters)
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.CREATED
        UserTestAssertion.verify_user(user_dict, response.json())

    def test_create_user_without_surname(self, base_url, user_dict):
        """Bad Request: User Surname is Undefined"""
        user_dict['surname'] = None
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_DATA_NOT_SPECIFIED_ERROR

    def test_create_user_with_empty_surname(self, base_url, user_dict):
        """Bad Request: min. length verification - empty User Surname"""
        user_dict['surname'] = ''
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_DATA_EMPTY_STRING_ERROR

    def test_create_user_with_one_char_surname(self, base_url, user_dict):
        """User Creation: min. length verification - 1 char User Surname"""
        user_dict['surname'] = random.choice(string.ascii_letters)
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.CREATED
        UserTestAssertion.verify_user(user_dict, response.json())

    def test_create_user_with_not_unique_name_and_surname(self, base_url, user_dict):
        """Namesake Users Creation"""
        first_user_creation_response = UsersApi.create_user(base_url, data=user_dict)
        assert first_user_creation_response.status_code == HTTPStatus.CREATED
        second_user_data = user_dict.copy()
        second_user_data['id'] = randint(1, 999999)
        second_user_creation_response = UsersApi.create_user(base_url, data=second_user_data)
        assert second_user_creation_response.status_code == HTTPStatus.CREATED
        UserTestAssertion.verify_user(second_user_data, second_user_creation_response.json())

    def test_create_user_with_string_id(self, base_url, user_dict):
        """Bad Request: Not Digital ID"""
        user_dict['id'] = 'test'
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_ID_IS_NOT_INT_ERROR

    def test_create_user_when_name_is_number(self, base_url, user_dict):
        """Bad Request: Non-Alphabetical User Name"""
        user_dict['name'] = randint(0, 123456)
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_NOT_STRING_ERROR

    def test_create_user_when_surname_is_number(self, base_url, user_dict):
        """Bad Request: Non-Alphabetical User Surname"""
        user_dict['surname'] = randint(0, 123456)
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_NOT_STRING_ERROR

    def test_create_user_with_leading_spaces(self, base_url, user_dict):
        """Leading Spaces Trimming Test"""
        test_data = user_dict.copy()
        test_data['name'] = ' ' + user_dict['name']
        test_data['surname'] = ' ' + user_dict['surname']
        response = UsersApi.create_user(base_url, data=test_data)
        assert response.status_code == HTTPStatus.CREATED
        UserTestAssertion.verify_user(user_dict, response.json())

    def test_create_user_with_trailing_spaces(self, base_url, user_dict):
        """Trailing Spaces Trimming Test"""
        test_data = user_dict.copy()
        test_data['name'] = user_dict['name'] + ' '
        test_data['surname'] = user_dict['surname'] + ' '
        response = UsersApi.create_user(base_url, data=test_data)
        assert response.status_code == HTTPStatus.CREATED
        UserTestAssertion.verify_user(user_dict, response.json())

    def test_create_user_with_spaces_in_name_only(self, base_url, user_dict):
        """Bad Request: Incorrect User Name (spaces only)"""
        user_dict['name'] = ' '
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_DATA_EMPTY_STRING_ERROR

    def test_create_user_with_only_spaces_in_surname(self, base_url, user_dict):
        """Bad Request: Incorrect User Surname (spaces only)"""
        user_dict['surname'] = '  '
        response = UsersApi.create_user(base_url, data=user_dict)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == USER_DATA_EMPTY_STRING_ERROR

    @pytest.mark.critical_test
    def test_get_user_by_id(self, base_url, user_dict):
        """Get Existing User Data"""
        creation_response = UsersApi.create_user(base_url, data=user_dict)
        assert creation_response.status_code == HTTPStatus.CREATED
        get_request = UsersApi.get_user(base_url, user_dict['id'])
        assert get_request.status_code == HTTPStatus.OK
        UserTestAssertion.verify_user(user_dict, get_request.json())

    def test_get_user_by_non_existing_id(self, base_url):
        """Get Non-Existing User"""
        non_existing_id = 0
        response = UsersApi.get_user(base_url, non_existing_id)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == USER_NOT_FOUND_ERROR

    @pytest.mark.critical_test
    def test_change_user_name(self, base_url, user_dict):
        """Update User: Change User Name"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        data_for_update = user_dict.copy()
        data_for_update['name'] += 'test'
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=data_for_update)
        assert update_user_result.status_code == HTTPStatus.OK
        UserTestAssertion.verify_user(data_for_update, update_user_result.json())
        get_updated_user = UsersApi.get_user(base_url, user_dict['id'])
        assert get_updated_user.status_code == HTTPStatus.OK
        assert get_updated_user.json()['name'] == data_for_update['name']

    @pytest.mark.critical_test
    def test_change_user_surname(self, base_url, user_dict):
        """Update User: Change User Surname"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['surname'] += 'test'
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.OK
        UserTestAssertion.verify_user(update_data, update_user_result.json())
        get_updated_user_result = UsersApi.get_user(base_url, user_dict['id'])
        assert get_updated_user_result.status_code == HTTPStatus.OK
        assert get_updated_user_result.json()['surname'] == update_data['surname']

    def test_create_user_through_update(self, base_url, user_dict):
        """Update User: User Creation through PUT Request"""
        response = UsersApi.update_user(base_url, user_dict['id'], data=user_dict)
        assert response.status_code == HTTPStatus.CREATED
        UserTestAssertion.verify_user(user_dict, response.json())

    def test_update_user_name_with_trailing_spaces(self, base_url, user_dict):
        """Update User: Trailing Spaces Trimming"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['name'] = user_dict['name'] + ' '
        update_data['surname'] = user_dict['surname'] + '  '
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.OK
        UserTestAssertion.verify_user(update_data,update_user_result.json())

    def test_update_user_name_with_leading_spaces(self, base_url, user_dict):
        """Update User: Leading Spaces Trimming"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['name'] = '  ' + user_dict['name']
        update_data['surname'] = ' ' + user_dict['surname']
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.OK
        UserTestAssertion.verify_user(update_data,update_user_result.json())

    def test_update_user_name_to_none(self, base_url, user_dict):
        """Update User: Change User Name to Undefined Value"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['name'] = None
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.BAD_REQUEST
        assert update_user_result.json() == USER_DATA_NOT_SPECIFIED_ERROR

    def test_update_user_name_to_empty_value(self, base_url, user_dict):
        """Update User: Change User Name to Empty Value"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['name'] = ''
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.BAD_REQUEST
        assert update_user_result.json() == USER_DATA_EMPTY_STRING_ERROR

    def test_update_user_name_to_one_char_value(self, base_url, user_dict):
        """Update User: Change User Name to 1 char Value"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['name'] = random.choice(string.ascii_letters)
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.OK
        UserTestAssertion.verify_user(update_data, update_user_result.json())

    def test_update_user_surname_to_none(self, base_url, user_dict):
        """Update User: Change User Surname to Undefined Value"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['name'] = None
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.BAD_REQUEST
        assert update_user_result.json() == USER_DATA_NOT_SPECIFIED_ERROR

    def test_update_user_surname_to_empty_value(self, base_url, user_dict):
        """Update User: Change User Surname to Empty Value"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['surname'] = ''
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.BAD_REQUEST
        assert update_user_result.json() == USER_DATA_EMPTY_STRING_ERROR

    def test_update_user_surname_to_one_char_value(self, base_url, user_dict):
        """Update User: Change User Surname to 1 char Value"""
        user_creation_response = UsersApi.create_user(base_url, user_dict)
        assert user_creation_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['surname'] = random.choice(string.ascii_letters)
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.OK
        UserTestAssertion.verify_user(update_data, update_user_result.json())

    def test_update_users_name_to_int(self, base_url, user_dict):
        """Update User: Change User Name to Digital Value"""
        creation_user_response = UsersApi.create_user(base_url, user_dict)
        assert creation_user_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['name'] = randint(1, 999999)
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.BAD_REQUEST
        assert update_user_result.json() == USER_NOT_STRING_ERROR

    def test_update_users_surname_to_int(self, base_url, user_dict):
        """Update User: Change User Surname to Digital Value"""
        creation_user_response = UsersApi.create_user(base_url, user_dict)
        assert creation_user_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['surname'] = randint(1, 999999)
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.BAD_REQUEST
        assert update_user_result.json() == USER_NOT_STRING_ERROR

    def test_update_user_name_to_spaces(self, base_url, user_dict):
        """Update User: User Name Consists of Spaces Only"""
        creation_user_response = UsersApi.create_user(base_url, user_dict)
        assert creation_user_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['name'] = '  '
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.BAD_REQUEST
        assert update_user_result.json() == USER_DATA_EMPTY_STRING_ERROR

    def test_update_user_surname_to_spaces(self, base_url, user_dict):
        """Update User: User Surname Consists of Spaces Only"""
        creation_user_response = UsersApi.create_user(base_url, user_dict)
        assert creation_user_response.status_code == HTTPStatus.CREATED
        update_data = user_dict.copy()
        update_data['surname'] = ' '
        update_user_result = UsersApi.update_user(base_url, user_dict['id'], data=update_data)
        assert update_user_result.status_code == HTTPStatus.BAD_REQUEST
        assert update_user_result.json() == USER_DATA_EMPTY_STRING_ERROR

    @pytest.mark.critical_test
    def test_delete_existing_user(self, base_url, user_dict):
        """Delete User Test"""
        create_user_response = UsersApi.create_user(base_url, user_dict)
        assert create_user_response.status_code == HTTPStatus.CREATED
        delete_user_response = UsersApi.delete_user(base_url, user_dict['id'])
        assert delete_user_response.status_code == HTTPStatus.OK
        assert delete_user_response.json()['ok'] is True
        get_deleted_user_response = UsersApi.get_user(base_url, user_dict['id'])
        assert get_deleted_user_response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_non_existing_user(self, base_url, user_dict):
        """Delete Non-Existing User"""
        delete_user_response = UsersApi.delete_user(base_url, user_dict['id'])
        assert delete_user_response.status_code == HTTPStatus.NOT_FOUND
        assert delete_user_response.json() == USER_NOT_FOUND_ERROR
