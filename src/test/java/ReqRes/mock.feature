Feature: Sample mock API Test

  Scenario: Validate mock GET Request
    Given url 'https://jsonplaceholder.typicode.com/posts/12'
    When method GET
    Then status 200
    And match response.id == 12
