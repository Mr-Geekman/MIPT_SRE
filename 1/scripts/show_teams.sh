#!/bin/bash

curl http://localhost:8080/api/v0/teams | json_pp
curl http://localhost:8080/api/v0/teams/team-1 | json_pp
curl http://localhost:8080/api/v0/teams/team-2 | json_pp
