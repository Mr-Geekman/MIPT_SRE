#!/bin/bash

# Delete all users
curl -X DELETE http://localhost:8080/api/v0/users/s.petrov
curl -X DELETE http://localhost:8080/api/v0/users/v.ivanov
curl -X DELETE http://localhost:8080/api/v0/users/n.fedorov
curl -X DELETE http://localhost:8080/api/v0/users/a.alexeev

# Create Sergey Petrov
curl -0 -v -X POST http://localhost:8080/api/v0/users \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"name": "s.petrov"
}
EOF

curl -0 -v -X PUT http://localhost:8080/api/v0/users/s.petrov \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"contacts": {
		"call": "+7 111-111-1111",
		"email": "s.petrov@student.com",
		"slack": "s.petrov",
		"sms": "+7 111-111-1111"
	},
	"full_name": "Sergey Petrov",
	"photo_url": null,
	"time_zone": "Europe/Moscow",
	"active": 1
}
EOF

# Create Vasilyi Ivanov
curl -0 -v -X POST http://localhost:8080/api/v0/users \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"name": "v.ivanov"
}
EOF

curl -0 -v -X PUT http://localhost:8080/api/v0/users/v.ivanov \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"contacts": {
		"call": "+7 222-222-2222",
		"email": "v.ivanov@student.com",
		"slack": "v.ivanov",
		"sms": "+7 222-222-2222"
	},
	"full_name": "Vasilyi Ivanov",
	"photo_url": null,
	"time_zone": "Europe/Moscow",
	"active": 1
}
EOF

# Create Nikolay Fedorov
curl -0 -v -X POST http://localhost:8080/api/v0/users \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"name": "n.fedorov"
}
EOF

curl -0 -v -X PUT http://localhost:8080/api/v0/users/n.fedorov \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"contacts": {
		"call": "+7 333-333-3333",
		"email": "n.fedorov@student.com",
		"slack": "n.fedorov",
		"sms": "+7 333-333-3333"
	},
	"full_name": "Nikolay Fedorov",
	"photo_url": null,
	"time_zone": "Europe/Moscow",
	"active": 1
}
EOF

# Create Andrey Alexeev
curl -0 -v -X POST http://localhost:8080/api/v0/users \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"name": "a.alexeev"
}
EOF

curl -0 -v -X PUT http://localhost:8080/api/v0/users/a.alexeev \
	-H "Expect:" \
	-H 'Content-Type: application/json; charset=utf-8' \
	--data-binary @- << EOF
{
	"contacts": {
		"call": "+7 444-444-4444",
		"email": "a.alexeev@student.com",
		"slack": "a.alexeev",
		"sms": "+7 444-444-4444"
	},
	"full_name": "Andrey Alexeev",
	"photo_url": null,
	"time_zone": "Europe/Moscow",
	"active": 1
}
EOF
