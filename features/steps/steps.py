from behave import given, when, then, step
import requests
from faker import Faker
from random import randint

faker = Faker()

existing_user = None
new_user = None
expected_user = None
response = None
api_url = 'http://127.0.0.1:5000'

@given('I set sample REST API url')
def step_impl(context):
    global api_url
    api_url = 'http://127.0.0.1:5000'

@given('I generate user data')
def impl_step(context):
    global new_user
    global expected_user
    new_user = {'id': randint(1, 9999), 'name': faker.first_name(), 'surname': faker.last_name()}
    expected_user = new_user #

@when('I save new user')
def step_impl(context):
    global response
    global expected_user
    response = requests.post(api_url + '/api/v1.0/users', data=new_user)
#    expected_user = new_user

@then('I receive HTTP status code "{status_code}"')
def step_impl(context, status_code):
    print(response.status_code)
    print(status_code)
    assert response.status_code == int(status_code)

@then('I receive valid response')
def step_impl(context):
    resp = response.json()
    print(resp)
    print(expected_user)
    assert len(resp) == 3
    assert resp['id'] == expected_user['id']
    assert resp['name'] == expected_user['name']
    assert resp['surname'] == expected_user['surname']

@given('I have existing user')
def step_impl(context):
    global existing_user
    global expected_user
    existing_user = new_user
    expected_user = existing_user #

@given('I generate user data with existing id')
def step_impl(context):
    global expected_user
    new_user['id'] = existing_user['id']
    new_user['name'] = faker.first_name()
    new_user['surname'] = faker.last_name()
    expected_user = new_user #


@when('I get user')
def step_impl(context):
    global response
    global expected_user
    #expected_user = existing_user
    #user_id = existing_user['id']
    response = requests.get(api_url + '/api/v1.0/users/' + str(expected_user['id']))

@when('I update user')
def step_impl(context):
    global new_user
    global response
    response = requests.put(api_url + '/api/v1.0/users/' + str(new_user['id']), data=new_user)

@when('I delete user')
def step_impl(context):
    global response
    global expected_user
    response = requests.delete(api_url + '/api/v1.0/users/' + str(expected_user['id']))

@then('I receive valid delete response')
def step_impl(context):
    global response
    resp = response.json()
    assert resp['ok'] is True