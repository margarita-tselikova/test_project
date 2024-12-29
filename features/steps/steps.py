# pylint: disable=no-name-in-module, disable=function-redefined

from random import randint
import requests

from behave import given, when, then
from faker import Faker

from tests.api.user_api import TIMEOUT

faker = Faker()

@given('I set sample REST API url')
def step_impl(context):
    """Define Testing REST API URL"""
    context.api_url = 'http://127.0.0.1:5000'

@given('I generate user data')
def impl_step(context):
    """Generate User Data before test"""
    context.new_user = {
        'id': randint(1, 9999),
        'name': faker.first_name(),
        'surname': faker.last_name()
    }
    context.expected_user = context.new_user

@when('I save new user')
def step_impl(context):
    """Send POST API Request to create User"""
    context.response = requests.post(url=context.api_url + '/api/v1.0/users',
                                     json=context.new_user,
                                     timeout=TIMEOUT)

@then('I receive HTTP status code "{status_code}"')
def step_impl(context, status_code):
    """Get Response status code"""
    assert context.response.status_code == int(status_code)

@then('I receive valid response')
def step_impl(context):
    """Get Response and validate User Data"""
    resp = context.response.json()
    assert len(resp) == 3
    assert resp['id'] == context.expected_user['id']
    assert resp['name'] == context.expected_user['name']
    assert resp['surname'] == context.expected_user['surname']

@given('I have existing user')
def step_impl(context):
    """Define Existing User"""
    context.new_user = {
        'id': randint(1, 9999),
        'name': faker.first_name(),
        'surname': faker.last_name()
    }
    requests.post(url=context.api_url + '/api/v1.0/users',
                  json=context.new_user,
                  timeout=TIMEOUT)
    context.existing_user = context.new_user
    context.expected_user = context.existing_user

@given('I generate user data with existing id')
def step_impl(context):
    """Generate New User Data with existing ID"""
    context.new_user['id'] = context.existing_user['id']
    context.new_user['name'] = faker.first_name()
    context.new_user['surname'] = faker.last_name()
    context.expected_user = context.new_user


@when('I get user')
def step_impl(context):
    """Get User Data"""
    context.response = requests.get(
        url=context.api_url + '/api/v1.0/users/' + str(context.expected_user['id']),
        timeout=TIMEOUT)

@when('I update user')
def step_impl(context):
    """Update User"""
    context.response = requests.put(
        url=context.api_url + '/api/v1.0/users/' + str(context.new_user['id']),
        json=context.new_user,
        timeout=TIMEOUT)

@when('I delete user')
def step_impl(context):
    """Delete User"""
    context.response = requests.delete(
        url=context.api_url + '/api/v1.0/users/' + str(context.expected_user['id']),
        timeout=TIMEOUT)

@then('I receive valid delete response')
def step_impl(context):
    """Check ok flag in Delete response"""
    resp = context.response.json()
    assert resp['ok'] is True
