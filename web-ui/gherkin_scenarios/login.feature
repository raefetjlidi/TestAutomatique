Feature: User Registration
  Scenario: Register a new user
    Given I am on the registration page
    When I enter "JohnDoe" as the username
    And I enter "john.doe@example.com" as the email
    And I enter "Password123" as the password
    And I click the register button
    Then I should see a success message
    And I should be redirected to the login page