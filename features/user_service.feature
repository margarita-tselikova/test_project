Feature: User API CRUD

Background:
  Given I set sample REST API url

Scenario: Create unique user via post request
  Given I generate user data
  When I save new user
  Then I receive HTTP status code "201"
  Then I receive valid response

Scenario: Get existing user info
  Given I have existing user
  When I get user
  Then I receive HTTP status code "200"
  Then I receive valid response

Scenario: Create non-unique user via post request
  Given I have existing user
  Given I generate user data with existing id
  When I save new user
  Then I receive HTTP status code "400"

Scenario: Change user info via PUT request
  Given I have existing user
  Given I generate user data with existing id
  When I update user
  Then I receive HTTP status code "200"
  Then I receive valid response

Scenario: Get non-existing user info
  Given I generate user data
  When I get user
  Then I receive HTTP status code "404"

Scenario: Create user through PUT request
  Given I generate user data
  When I update user
  Then I receive HTTP status code "201"
  Then I receive valid response

Scenario: Delete existing user via DELETE request
  Given I have existing user
  When I delete user
  Then I receive HTTP status code "200"
  Then I receive valid delete response
