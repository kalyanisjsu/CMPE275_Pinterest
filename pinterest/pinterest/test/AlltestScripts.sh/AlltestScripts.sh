#!/bin/bash
password='pinterest'
boardname='thirdBoard22'

echo -e "******************************************************** Testing Registration ********************************************************\n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Content-Type: application/json" -H "Accept: application/json" -d \
'{"name":"testpintee","username":"testpinte","password":"'$password'"}' http://localhost:8080/v1/reg)
userJson=$(echo $arr | awk -F'STATUS' '{print $1}')
status=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status

echo $userJson
user_id=$(echo $userJson | python -c 'import sys, json; print json.load(sys.stdin)["user_id"]')
echo $user_id
username=$(echo $userJson | python -c 'import sys, json; print json.load(sys.stdin)["username"]')
echo $username


echo -e "\n******************************************************** Testing Login ********************************************************\n"

arr=$(curl -s -w 'STATUS%{http_code}' -H "Accept: application/json" -H "Content-Type: application/json" -d \
'{"username":"testpinte","password":"'$password'"}'  http://localhost:8080/v1/login)
userJson=$(echo $arr | awk -F'STATUS' '{print $1}')
status1=$(echo $arr | awk -F'STATUS' '{print $2}')
user_id=$(echo $userJson | python -c 'import sys, json; print json.load(sys.stdin)["user_id"]')
echo " User id logged in: "
echo $user_id
echo 'Status Code is' $status1

echo -e "\n******************************************************** Creating Board ********************************************************\n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Accept: application/json" -H "Content-Type: application/json" -d \
'{"boardname":"'$boardname'"}'  http://localhost:8080/v1/user/$user_id/board)
boardid=$(echo $arr | awk -F'STATUS' '{print $1}')
status2=$(echo $arr | awk -F'STATUS' '{print $2}')
echo $boardid
board_id=$(echo $boardid | python -c 'import sys, json; print json.load(sys.stdin)["board_id"]')
echo " Board id created is: "
echo $board_id
echo 'Status Code is' $status2

echo -e "\n******************************************************** Getting All Board ******************************************************** \n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Accept: application/json" http://localhost:8080/v1/boards)
echo $arr | awk -F'STATUS' '{print $1}' | jq '.'
status3=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status3

echo -e "\n******************************************************** Get User Boards ********************************************************\n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Accept: application/json" http://localhost:8080/v1/user/$user_id)
echo $arr | awk -F'STATUS' '{print $1}' | jq '.'
status4=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status4

echo -e "\n******************************************************** Upload Pin ********************************************************\n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Content-Type: multipart/related" \
 --form "content=@image1.jpg;type=image/jpeg" http://localhost:8080/v1/user/$user_id/pin/upload)
echo "Pin id created is: "
pin_id=$(echo $arr | awk -F'STATUS' '{print $1}' | jq '.pin_id')
echo $pin_id
status5=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status5

echo -e "\n******************************************************** Add Comments to created Pin *************************************************** \n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Accept: application/json" -H "Content-Type: application/json" \
 -d '{"comment":"testcomments"}' http://localhost:8080/v1/user/$user_id/pin/$pin_id)
echo $arr | awk -F'STATUS' '{print $1}'
status6=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status6

echo -e "\n******************************************************** Get a Single Pin Uploaded now********************************************************\n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Accept: application/json" http://localhost:8080/v1/pin/$pin_id)
echo $arr | awk -F'STATUS' '{print $1}' | jq '.'
status7=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status7

echo -e "\n******************************************************** Getting All Pins ********************************************************\n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Accept: application/json" http://localhost:8080/v1/pins)
echo $arr | awk -F'STATUS' '{print $1}' | jq '.'
status8=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status8

echo -e "\n********************************************************Attach Pin to Board Created********************************************************\n"
arr=$(curl -s -w 'STATUS%{http_code}' -X PUT -H "Accept: application/json" -H "Content-Type: application/json" -d '{"pin_id":"'$pin_id'"}'  http://localhost:8080/v1/user/$user_id/board/$board_id)
echo $arr | awk -F'STATUS' '{print $1}'
status9=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status9

echo -e "\n********************************************************Get a Single Board created now ********************************************************\n"
arr=$(curl -s -w 'STATUS%{http_code}' -H "Accept: application/json" http://localhost:8080/v1/boards/$board_id)
echo $arr | awk -F'STATUS' '{print $1}' | jq '.'
status10=$(echo $arr | awk -F'STATUS' '{print $2}')
echo 'Status Code is' $status10

