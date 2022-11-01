curl -X DELETE http://localhost:8080/api/v0/users/e.examplov.1

curl -0 -v -X POST http://localhost:8080/api/v0/users \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"name": "e.examplov.1"
}
EOF

# make team in web-interface

curl -X DELETE "http://localhost:8080/api/v0/teams/demo-team"
