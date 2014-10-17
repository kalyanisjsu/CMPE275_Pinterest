#!/bin/bash
#
# test client access to our service

echo -e "\n"
curl -i -H "Accept: application/json" --data "name='Robert'&username='rob'&password='rob'"  http://localhost:8080/v1/login
echo -e "\n"
