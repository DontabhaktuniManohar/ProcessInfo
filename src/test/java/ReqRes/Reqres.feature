Feature: Sample Reqres API Test

  Scenario: Validate Reqres GET Request
    Given url 'https://jsonplaceholder.typicode.com/posts/1'
    When method GET
    Then status 200
    And match response.id == 1
