Feature: LLM interface tests


  Background:
    Given The service is started locally
      And REST API service hostname is localhost
      And REST API service port is 8080
      And REST API service prefix is /v1


  Scenario: Check if LLM responds to sent question
    Given the system is in default state
     When I ask question "Say hello"
     Then The status code of the response is 200
      And The response should have proper LLM response format
      And The response should contain following fragments
          | Fragments in LLM response |
          | Hello                     |
