Feature: Mock API server for testing

Background:
  * configure headers = { 'Content-Type': 'application/json' }

Scenario: pathMatches('/api/hello') && methodIs('get')
  * def response = { message: 'Hello from mock server!' }
  * status 200

Scenario: pathMatches('/api/user') && methodIs('post')
  * def user = request
  * def response = { id: 101, name: user.name, email: user.email }
  * status 201

Scenario: pathMatches('/api/order') && methodIs('post')
  * def response = { orderId: 999, status: 'RECEIVED' }
  * status 200