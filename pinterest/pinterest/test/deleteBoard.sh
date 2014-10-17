#!/bin/bash
#
# test client access to our service

echo -e "\n"
curl -i -H "Accept: application/json" -H "X-HTTP-Method-Override: DELETE" -X POST http://localhost:8080/v1/user/5434321/board/94
echo -e "\n"