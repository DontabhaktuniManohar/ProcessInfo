Feature: Sample test against mock server

Scenario: Call hello endpoint
  Given url mockServerUrl + '/api/hello'
  When method get
  Then status 200
  And match response.message == 'Hello from mock server!'