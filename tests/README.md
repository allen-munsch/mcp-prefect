
Run tests

```
uv pip install -e ".[dev]"
docker compose up
pytest -svvl tests/


.... some time later ...

    "updated": "2025-11-11 08:47:01.653328+00:00",
      "name": "te...
02:51:08.267 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_variables.py::test_get_variables_with_offset[trio] 02:51:08.304 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.304 | INFO    | mcp.client.streamable_http - Received session ID: bc9a030918584c2d970ed436242f9f1c
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: bc9a030918584c2d970ed436242f9f1c
02:51:08.305 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:08.306 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:08.309 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:08.310 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.314 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.325 | INFO    | prefect-mcp-test - Testing get_variables with offset...
INFO     prefect-mcp-test:test_variables.py:51 Testing get_variables with offset...
02:51:08.329 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.351 | INFO    | prefect-mcp-test - Offset variables result: {
  "variables": [
    {
      "id": "3684b874-109c-42a5-baa2-72620830de1c",
      "created": "2025-11-11 08:47:03.303427+00:00",
      "updated": "2025-11-11 08:47:03.303445+00:00",
      "name": "te...
INFO     prefect-mcp-test:test_variables.py:62 Offset variables result: {
  "variables": [
    {
      "id": "3684b874-109c-42a5-baa2-72620830de1c",
      "created": "2025-11-11 08:47:03.303427+00:00",
      "updated": "2025-11-11 08:47:03.303445+00:00",
      "name": "te...
02:51:08.357 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_variables.py::test_get_variable[trio] 02:51:08.395 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.396 | INFO    | mcp.client.streamable_http - Received session ID: 1c188e10dea349baaaca5703a2e551c1
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 1c188e10dea349baaaca5703a2e551c1
02:51:08.397 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:08.398 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:08.404 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.405 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:08.410 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.434 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.464 | INFO    | prefect-mcp-test - Testing get_variable with name: test_get_15ba92b7...
INFO     prefect-mcp-test:test_variables.py:80 Testing get_variable with name: test_get_15ba92b7...
02:51:08.469 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.488 | INFO    | prefect-mcp-test - Get variable result: {
  "id": "9afbbca0-3537-4cf4-ace2-61f648511df4",
  "created": "2025-11-11 08:51:08.458952+00:00",
  "updated": "2025-11-11 08:51:08.458967+00:00",
  "name": "test_get_15ba92b7",
  "value": {
    "tes...
INFO     prefect-mcp-test:test_variables.py:88 Get variable result: {
  "id": "9afbbca0-3537-4cf4-ace2-61f648511df4",
  "created": "2025-11-11 08:51:08.458952+00:00",
  "updated": "2025-11-11 08:51:08.458967+00:00",
  "name": "test_get_15ba92b7",
  "value": {
    "tes...
02:51:08.492 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.516 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_variables.py::test_get_nonexistent_variable[trio] 02:51:08.551 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.552 | INFO    | mcp.client.streamable_http - Received session ID: 43c701fbf87947f38b3273791f770ea4
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 43c701fbf87947f38b3273791f770ea4
02:51:08.553 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:08.555 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:08.560 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:08.562 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.567 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.584 | INFO    | prefect-mcp-test - Testing get_variable with nonexistent name: nonexistent_75236beb...
INFO     prefect-mcp-test:test_variables.py:100 Testing get_variable with nonexistent name: nonexistent_75236beb...
02:51:08.589 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.612 | INFO    | prefect-mcp-test - Get nonexistent variable result: {
  "error": "Variable 'nonexistent_75236beb' not found"
}
INFO     prefect-mcp-test:test_variables.py:108 Get nonexistent variable result: {
  "error": "Variable 'nonexistent_75236beb' not found"
}
02:51:08.617 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_variables.py::test_create_and_delete_variable[trio] 02:51:08.656 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.657 | INFO    | mcp.client.streamable_http - Received session ID: 6c10c02ff7714997a155ebfda2637f55
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 6c10c02ff7714997a155ebfda2637f55
02:51:08.657 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:08.658 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:08.662 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:08.662 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.666 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.680 | INFO    | prefect-mcp-test - Testing create_variable with name: test_var_e211535a...
INFO     prefect-mcp-test:test_variables.py:118 Testing create_variable with name: test_var_e211535a...
02:51:08.684 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.711 | INFO    | prefect-mcp-test - Create variable result: {
  "variable": {
    "id": "ce39b932-26d5-4473-a681-aee352ae40b3",
    "created": "2025-11-11 08:51:08.705977+00:00",
    "updated": "2025-11-11 08:51:08.705994+00:00",
    "name": "test_var_e211535a...
INFO     prefect-mcp-test:test_variables.py:132 Create variable result: {
  "variable": {
    "id": "ce39b932-26d5-4473-a681-aee352ae40b3",
    "created": "2025-11-11 08:51:08.705977+00:00",
    "updated": "2025-11-11 08:51:08.705994+00:00",
    "name": "test_var_e211535a...
02:51:08.712 | INFO    | prefect-mcp-test - Testing delete_variable for name: test_var_e211535a...
INFO     prefect-mcp-test:test_variables.py:141 Testing delete_variable for name: test_var_e211535a...
02:51:08.718 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.749 | INFO    | prefect-mcp-test - Delete variable result: {
  "message": "Variable 'test_var_e211535a' deleted successfully"
}
INFO     prefect-mcp-test:test_variables.py:149 Delete variable result: {
  "message": "Variable 'test_var_e211535a' deleted successfully"
}
02:51:08.754 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_variables.py::test_create_variable_with_different_value_types[trio] 02:51:08.793 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.793 | INFO    | mcp.client.streamable_http - Received session ID: b6c397af3bbd44879b9808e9de45dd50
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: b6c397af3bbd44879b9808e9de45dd50
02:51:08.794 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:08.795 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:08.798 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.800 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:08.805 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.818 | INFO    | prefect-mcp-test - Testing string value with variable: test_string_ddd4c474
INFO     prefect-mcp-test:test_variables.py:172 Testing string value with variable: test_string_ddd4c474
02:51:08.823 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.858 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.893 | INFO    | prefect-mcp-test - Testing number value with variable: test_number_6c2b1ef2
INFO     prefect-mcp-test:test_variables.py:172 Testing number value with variable: test_number_6c2b1ef2
02:51:08.898 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.931 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.962 | INFO    | prefect-mcp-test - Testing float value with variable: test_float_b126e9cf
INFO     prefect-mcp-test:test_variables.py:172 Testing float value with variable: test_float_b126e9cf
02:51:08.968 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:08.994 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.023 | INFO    | prefect-mcp-test - Testing boolean value with variable: test_boolean_95d63ded
INFO     prefect-mcp-test:test_variables.py:172 Testing boolean value with variable: test_boolean_95d63ded
02:51:09.029 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.054 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.080 | INFO    | prefect-mcp-test - Testing list value with variable: test_list_cc4a7f23
INFO     prefect-mcp-test:test_variables.py:172 Testing list value with variable: test_list_cc4a7f23
02:51:09.083 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.106 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.129 | INFO    | prefect-mcp-test - Testing dict value with variable: test_dict_47eb2285
INFO     prefect-mcp-test:test_variables.py:172 Testing dict value with variable: test_dict_47eb2285
02:51:09.133 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.176 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.200 | INFO    | prefect-mcp-test - Testing null value with variable: test_null_a81e4b24
INFO     prefect-mcp-test:test_variables.py:172 Testing null value with variable: test_null_a81e4b24
02:51:09.204 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.227 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.250 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_variables.py::test_update_variable[trio] 02:51:09.292 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.293 | INFO    | mcp.client.streamable_http - Received session ID: fe9be5d3575a4d4097b4b9423c4e82cc
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: fe9be5d3575a4d4097b4b9423c4e82cc
02:51:09.294 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:09.295 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:09.300 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:09.302 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.307 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.326 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.344 | INFO    | prefect-mcp-test - Testing update_variable with name: test_update_5b2ae3c5...
INFO     prefect-mcp-test:test_variables.py:204 Testing update_variable with name: test_update_5b2ae3c5...
02:51:09.348 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.388 | INFO    | prefect-mcp-test - Update variable result: {
  "message": "Variable 'test_update_5b2ae3c5' updated successfully",
  "variable": {
    "id": "a741e1cc-7c40-4a8d-b986-3034fa6a93e2",
    "created": "2025-11-11 08:51:09.341178+00:00",
    "updated...
INFO     prefect-mcp-test:test_variables.py:216 Update variable result: {
  "message": "Variable 'test_update_5b2ae3c5' updated successfully",
  "variable": {
    "id": "a741e1cc-7c40-4a8d-b986-3034fa6a93e2",
    "created": "2025-11-11 08:51:09.341178+00:00",
    "updated...
02:51:09.393 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.422 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_variables.py::test_update_nonexistent_variable[trio] 02:51:09.458 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.458 | INFO    | mcp.client.streamable_http - Received session ID: 6e391c8760234c52a8245154844c8e8c
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 6e391c8760234c52a8245154844c8e8c
02:51:09.459 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:09.460 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:09.464 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.464 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:09.468 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.485 | INFO    | prefect-mcp-test - Testing update_variable with nonexistent name: nonexistent_update_ba443fb8...
INFO     prefect-mcp-test:test_variables.py:230 Testing update_variable with nonexistent name: nonexistent_update_ba443fb8...
02:51:09.490 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.508 | INFO    | prefect-mcp-test - Update nonexistent variable result: {
  "error": "Variable 'nonexistent_update_ba443fb8' not found"
}
INFO     prefect-mcp-test:test_variables.py:241 Update nonexistent variable result: {
  "error": "Variable 'nonexistent_update_ba443fb8' not found"
}
02:51:09.513 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_variables.py::test_delete_nonexistent_variable[trio] 02:51:09.551 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.551 | INFO    | mcp.client.streamable_http - Received session ID: 1109ad5e822e43ffab9cff4169c47024
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 1109ad5e822e43ffab9cff4169c47024
02:51:09.552 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:09.553 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:09.563 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.564 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:09.568 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.578 | INFO    | prefect-mcp-test - Testing delete_variable with nonexistent name: nonexistent_delete_4185906d...
INFO     prefect-mcp-test:test_variables.py:250 Testing delete_variable with nonexistent name: nonexistent_delete_4185906d...
02:51:09.581 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.601 | INFO    | prefect-mcp-test - Delete nonexistent variable result: {
  "error": "Variable 'nonexistent_delete_4185906d' not found"
}
INFO     prefect-mcp-test:test_variables.py:258 Delete nonexistent variable result: {
  "error": "Variable 'nonexistent_delete_4185906d' not found"
}
02:51:09.606 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workqueues.py::test_get_work_queues[asyncio] 02:51:09.648 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.649 | INFO    | mcp.client.streamable_http - Received session ID: a305cb22f63449b2ada05dc9f56ae813
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: a305cb22f63449b2ada05dc9f56ae813
02:51:09.650 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:09.651 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:09.654 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:09.655 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.659 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.666 | INFO    | prefect-mcp-test - Testing get_work_queues tool...
INFO     prefect-mcp-test:test_workqueues.py:15 Testing get_work_queues tool...
02:51:09.672 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.709 | INFO    | prefect-mcp-test - Work queues result: {'work_queues': [{'id': UUID('3b8d4014-7d20-4327-a8ef-84b647c21a4b'), 'created': datetime.datetime(2025, 11, 11, 7, 33, 59, 985557, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 7, 33,...
INFO     prefect-mcp-test:test_workqueues.py:23 Work queues result: {'work_queues': [{'id': UUID('3b8d4014-7d20-4327-a8ef-84b647c21a4b'), 'created': datetime.datetime(2025, 11, 11, 7, 33, 59, 985557, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 7, 33,...
02:51:09.714 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workqueues.py::test_get_work_queues_with_filter[asyncio] 02:51:09.751 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.752 | INFO    | mcp.client.streamable_http - Received session ID: 845ddd0b768c4c9ea8f5a45e7f1dc62d
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 845ddd0b768c4c9ea8f5a45e7f1dc62d
02:51:09.752 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:09.753 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:09.757 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:09.757 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.761 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.775 | INFO    | prefect-mcp-test - Testing get_work_queues with filter...
INFO     prefect-mcp-test:test_workqueues.py:29 Testing get_work_queues with filter...
02:51:09.780 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.812 | INFO    | prefect-mcp-test - Filtered work queues result: {'work_queues': [{'id': UUID('3b8d4014-7d20-4327-a8ef-84b647c21a4b'), 'created': datetime.datetime(2025, 11, 11, 7, 33, 59, 985557, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 7, 33,...
INFO     prefect-mcp-test:test_workqueues.py:40 Filtered work queues result: {'work_queues': [{'id': UUID('3b8d4014-7d20-4327-a8ef-84b647c21a4b'), 'created': datetime.datetime(2025, 11, 11, 7, 33, 59, 985557, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 7, 33,...
02:51:09.817 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workqueues.py::test_create_and_delete_work_queue[asyncio] 02:51:09.856 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.856 | INFO    | mcp.client.streamable_http - Received session ID: 227582e28e0845e8a89ee78272937509
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 227582e28e0845e8a89ee78272937509
02:51:09.857 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:09.858 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:09.862 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:09.863 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.868 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.882 | INFO    | prefect-mcp-test - Testing create_work_queue with name: test_queue_1f0ffacc...
INFO     prefect-mcp-test:test_workqueues.py:48 Testing create_work_queue with name: test_queue_1f0ffacc...
02:51:09.888 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.928 | INFO    | prefect-mcp-test - Create work queue result: {'id': UUID('16f73f8a-12fd-472c-8056-a9b0f13b28c1'), 'created': datetime.datetime(2025, 11, 11, 8, 51, 9, 920069, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 8, 51, 9, 920083, tzinfo...
INFO     prefect-mcp-test:test_workqueues.py:61 Create work queue result: {'id': UUID('16f73f8a-12fd-472c-8056-a9b0f13b28c1'), 'created': datetime.datetime(2025, 11, 11, 8, 51, 9, 920069, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 8, 51, 9, 920083, tzinfo...
02:51:09.928 | INFO    | prefect-mcp-test - Testing get_work_queue for ID: 16f73f8a-12fd-472c-8056-a9b0f13b28c1...
INFO     prefect-mcp-test:test_workqueues.py:69 Testing get_work_queue for ID: 16f73f8a-12fd-472c-8056-a9b0f13b28c1...
02:51:09.934 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.965 | INFO    | prefect-mcp-test - Get work queue result: {'id': UUID('16f73f8a-12fd-472c-8056-a9b0f13b28c1'), 'created': datetime.datetime(2025, 11, 11, 8, 51, 9, 920069, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 8, 51, 9, 920083, tzinfo...
INFO     prefect-mcp-test:test_workqueues.py:77 Get work queue result: {'id': UUID('16f73f8a-12fd-472c-8056-a9b0f13b28c1'), 'created': datetime.datetime(2025, 11, 11, 8, 51, 9, 920069, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 8, 51, 9, 920083, tzinfo...
02:51:09.966 | INFO    | prefect-mcp-test - Testing delete_work_queue for ID: 16f73f8a-12fd-472c-8056-a9b0f13b28c1...
INFO     prefect-mcp-test:test_workqueues.py:82 Testing delete_work_queue for ID: 16f73f8a-12fd-472c-8056-a9b0f13b28c1...
02:51:09.973 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:09.995 | INFO    | prefect-mcp-test - Delete work queue result: Work queue '16f73f8a-12fd-472c-8056-a9b0f13b28c1' deleted successfully.
INFO     prefect-mcp-test:test_workqueues.py:89 Delete work queue result: Work queue '16f73f8a-12fd-472c-8056-a9b0f13b28c1' deleted successfully.
02:51:10.001 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workqueues.py::test_get_work_queues[trio] 02:51:10.042 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.042 | INFO    | mcp.client.streamable_http - Received session ID: 341f29dfae094444b03f9951f2c22bc2
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 341f29dfae094444b03f9951f2c22bc2
02:51:10.043 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:10.044 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:10.049 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:10.050 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.054 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.070 | INFO    | prefect-mcp-test - Testing get_work_queues tool...
INFO     prefect-mcp-test:test_workqueues.py:15 Testing get_work_queues tool...
02:51:10.074 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.099 | INFO    | prefect-mcp-test - Work queues result: {'work_queues': [{'id': UUID('3b8d4014-7d20-4327-a8ef-84b647c21a4b'), 'created': datetime.datetime(2025, 11, 11, 7, 33, 59, 985557, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 7, 33,...
INFO     prefect-mcp-test:test_workqueues.py:23 Work queues result: {'work_queues': [{'id': UUID('3b8d4014-7d20-4327-a8ef-84b647c21a4b'), 'created': datetime.datetime(2025, 11, 11, 7, 33, 59, 985557, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 7, 33,...
02:51:10.103 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workqueues.py::test_get_work_queues_with_filter[trio] 02:51:10.137 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.137 | INFO    | mcp.client.streamable_http - Received session ID: 592c3bf950704767b3b8834cc0abfa47
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 592c3bf950704767b3b8834cc0abfa47
02:51:10.138 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:10.139 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:10.142 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:10.143 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.146 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.156 | INFO    | prefect-mcp-test - Testing get_work_queues with filter...
INFO     prefect-mcp-test:test_workqueues.py:29 Testing get_work_queues with filter...
02:51:10.161 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.187 | INFO    | prefect-mcp-test - Filtered work queues result: {'work_queues': [{'id': UUID('3b8d4014-7d20-4327-a8ef-84b647c21a4b'), 'created': datetime.datetime(2025, 11, 11, 7, 33, 59, 985557, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 7, 33,...
INFO     prefect-mcp-test:test_workqueues.py:40 Filtered work queues result: {'work_queues': [{'id': UUID('3b8d4014-7d20-4327-a8ef-84b647c21a4b'), 'created': datetime.datetime(2025, 11, 11, 7, 33, 59, 985557, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 7, 33,...
02:51:10.190 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workqueues.py::test_create_and_delete_work_queue[trio] 02:51:10.224 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.225 | INFO    | mcp.client.streamable_http - Received session ID: f4d84bfd3570408a87ab6709db96582a
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: f4d84bfd3570408a87ab6709db96582a
02:51:10.225 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:10.227 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:10.237 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:10.238 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.241 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.251 | INFO    | prefect-mcp-test - Testing create_work_queue with name: test_queue_8f0fe4cc...
INFO     prefect-mcp-test:test_workqueues.py:48 Testing create_work_queue with name: test_queue_8f0fe4cc...
02:51:10.256 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.277 | INFO    | prefect-mcp-test - Create work queue result: {'id': UUID('150d4246-49ab-4815-8adf-9441c6404f81'), 'created': datetime.datetime(2025, 11, 11, 8, 51, 10, 272995, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 8, 51, 10, 273003, tzin...
INFO     prefect-mcp-test:test_workqueues.py:61 Create work queue result: {'id': UUID('150d4246-49ab-4815-8adf-9441c6404f81'), 'created': datetime.datetime(2025, 11, 11, 8, 51, 10, 272995, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 8, 51, 10, 273003, tzin...
02:51:10.278 | INFO    | prefect-mcp-test - Testing get_work_queue for ID: 150d4246-49ab-4815-8adf-9441c6404f81...
INFO     prefect-mcp-test:test_workqueues.py:69 Testing get_work_queue for ID: 150d4246-49ab-4815-8adf-9441c6404f81...
02:51:10.282 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.303 | INFO    | prefect-mcp-test - Get work queue result: {'id': UUID('150d4246-49ab-4815-8adf-9441c6404f81'), 'created': datetime.datetime(2025, 11, 11, 8, 51, 10, 272995, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 8, 51, 10, 273003, tzin...
INFO     prefect-mcp-test:test_workqueues.py:77 Get work queue result: {'id': UUID('150d4246-49ab-4815-8adf-9441c6404f81'), 'created': datetime.datetime(2025, 11, 11, 8, 51, 10, 272995, tzinfo=TzInfo(0)), 'updated': datetime.datetime(2025, 11, 11, 8, 51, 10, 273003, tzin...
02:51:10.303 | INFO    | prefect-mcp-test - Testing delete_work_queue for ID: 150d4246-49ab-4815-8adf-9441c6404f81...
INFO     prefect-mcp-test:test_workqueues.py:82 Testing delete_work_queue for ID: 150d4246-49ab-4815-8adf-9441c6404f81...
02:51:10.309 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.336 | INFO    | prefect-mcp-test - Delete work queue result: Work queue '150d4246-49ab-4815-8adf-9441c6404f81' deleted successfully.
INFO     prefect-mcp-test:test_workqueues.py:89 Delete work queue result: Work queue '150d4246-49ab-4815-8adf-9441c6404f81' deleted successfully.
02:51:10.340 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workspaces.py::test_get_workspaces[asyncio] 02:51:10.383 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.384 | INFO    | mcp.client.streamable_http - Received session ID: afd3f9e089f9445db37452e3568f6f10
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: afd3f9e089f9445db37452e3568f6f10
02:51:10.385 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:10.386 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:10.391 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.392 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:10.395 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.407 | INFO    | prefect-mcp-test - Testing get_workspaces tool (expect message about Cloud-only)...
INFO     prefect-mcp-test:test_workspaces.py:13 Testing get_workspaces tool (expect message about Cloud-only)...
02:51:10.412 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.426 | INFO    | prefect-mcp-test - Workspaces response: Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance.
INFO     prefect-mcp-test:test_workspaces.py:21 Workspaces response: Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance.
02:51:10.430 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workspaces.py::test_get_workspaces_with_filter[asyncio] 02:51:10.466 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.467 | INFO    | mcp.client.streamable_http - Received session ID: 20248540624243eb8fe98c02458c9b82
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 20248540624243eb8fe98c02458c9b82
02:51:10.467 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:10.468 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:10.471 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:10.473 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.475 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.484 | INFO    | prefect-mcp-test - Testing get_workspaces with filter (expect message about Cloud-only)...
INFO     prefect-mcp-test:test_workspaces.py:28 Testing get_workspaces with filter (expect message about Cloud-only)...
02:51:10.490 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.502 | INFO    | prefect-mcp-test - Filtered workspaces response: Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance.
INFO     prefect-mcp-test:test_workspaces.py:39 Filtered workspaces response: Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance.
02:51:10.504 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workspaces.py::test_get_workspaces[trio] 02:51:10.536 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.537 | INFO    | mcp.client.streamable_http - Received session ID: e9bedb6564404509bd2da9b295a75140
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: e9bedb6564404509bd2da9b295a75140
02:51:10.538 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:10.539 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:10.545 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:10.547 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.551 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.558 | INFO    | prefect-mcp-test - Testing get_workspaces tool (expect message about Cloud-only)...
INFO     prefect-mcp-test:test_workspaces.py:13 Testing get_workspaces tool (expect message about Cloud-only)...
02:51:10.561 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.573 | INFO    | prefect-mcp-test - Workspaces response: Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance.
INFO     prefect-mcp-test:test_workspaces.py:21 Workspaces response: Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance.
02:51:10.577 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED
tests/test_workspaces.py::test_get_workspaces_with_filter[trio] 02:51:10.619 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"

--------------------------------------------------------------------------------------- live log call ----------------------------------------------------------------------------------------
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.620 | INFO    | mcp.client.streamable_http - Received session ID: 6f270b4a83784fd38d5c5a686d25e984
INFO     mcp.client.streamable_http:streamable_http.py:134 Received session ID: 6f270b4a83784fd38d5c5a686d25e984
02:51:10.621 | INFO    | mcp.client.streamable_http - Negotiated protocol version: 2025-06-18
INFO     mcp.client.streamable_http:streamable_http.py:146 Negotiated protocol version: 2025-06-18
02:51:10.623 | INFO    | prefect-mcp-test - Connected to MCP server at http://localhost:8000/mcp
INFO     prefect-mcp-test:conftest.py:41 Connected to MCP server at http://localhost:8000/mcp
02:51:10.628 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 202 Accepted"
02:51:10.629 | INFO    | httpx - HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: GET http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.634 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.647 | INFO    | prefect-mcp-test - Testing get_workspaces with filter (expect message about Cloud-only)...
INFO     prefect-mcp-test:test_workspaces.py:28 Testing get_workspaces with filter (expect message about Cloud-only)...
02:51:10.653 | INFO    | httpx - HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: POST http://localhost:8000/mcp "HTTP/1.1 200 OK"
02:51:10.668 | INFO    | prefect-mcp-test - Filtered workspaces response: Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance.
INFO     prefect-mcp-test:test_workspaces.py:39 Filtered workspaces response: Workspaces are only available in Prefect Cloud. This appears to be a local Prefect instance.
02:51:10.671 | INFO    | httpx - HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
INFO     httpx:_client.py:1740 HTTP Request: DELETE http://localhost:8000/mcp "HTTP/1.1 200 OK"
PASSED

===================================================================================== 48 passed in 6.15s =====================================================================================

```
