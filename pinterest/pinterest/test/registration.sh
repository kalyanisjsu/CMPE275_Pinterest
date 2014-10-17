#!/bin/bash
#
# test client access to our service

echo -e "\n"
curl -i -H "Accept: application/json" --data "name='Pooja'&username='pooja'&password='poo'"  http://localhost:8080/v1/reg
echo -e "\n"
