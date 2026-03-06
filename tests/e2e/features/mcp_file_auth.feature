@MCPFileAuth
Feature: MCP file-based authorization tests

  Regression tests for LCORE-1414: MCP authorization tokens configured via
  file-based authorization_headers must survive model_dump() serialization
  and reach the MCP server as a valid Bearer token.

  Background:
    Given The service is started locally
      And REST API service prefix is /v1

  @skip-in-library-mode
  Scenario: Query succeeds with file-based MCP authorization
    Given The system is in default state
    When I use "query" to ask question
    """
    {"query": "Use the mock_tool_e2e tool to send the message 'hello'", "model": "{MODEL}", "provider": "{PROVIDER}"}
    """
    Then The status code of the response is 200
    And The body of the response contains mock_tool_e2e
