#!/bin/bash
#
# test client access to our service

echo -e "\n"
curl -i -H "Accept: application/json" --data "name='Pooja'&username='pooja'&password='poo'"  http://192.168.0.94:8080/v1/login
echo -e "\n"
