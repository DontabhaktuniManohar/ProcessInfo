Feature: Sample API Test

  Scenario: Validate GET Request
    Given url 'https://jsonplaceholder.typicode.com/posts/1'
    When method GET
    Then status 200
    And match response.id == 1
