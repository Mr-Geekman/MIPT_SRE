#!/bin/python3

import datetime
import time
import itertools

import requests


HOST = "http://localhost:8080"
START_DATE = "2022-10-09"
TEAM_NAME = "team-2"
ROSTER_NAME = "on_demand"
HOUR = 8
NUM_DAYS_IN_SHIFT = 2
NUM_DAYS_TOTAL = 65


def make_unix_timestamp(datetime_value):
    return int(time.mktime(datetime_value.timetuple()))


def main():
    start_datetime = datetime.datetime.fromisoformat(START_DATE)
    end_datetime = start_datetime + datetime.timedelta(days=NUM_DAYS_TOTAL)
    start_unix_timestamp = make_unix_timestamp(start_datetime)

    # load existing events for given team since given timestamp
    primary_events = requests.get(
        f"{HOST}/api/v0/events",
        params={"team": "team-2", "start__ge": start_unix_timestamp, "role": "primary"},
    ).json()
    secondary_events = requests.get(
        f"{HOST}/api/v0/events",
        params={
            "team": "team-2",
            "start__ge": start_unix_timestamp,
            "role": "secondary",
        },
    ).json()

    # remove them
    for event in primary_events + secondary_events:
        requests.delete(f"{HOST}/api/v0/events/{event['id']}")

    # load team members
    rost_members = requests.get(f"{HOST}/api/v0/teams/{TEAM_NAME}").json()["rosters"][
        ROSTER_NAME
    ]["users"]
    rotate_members = [x for x in rost_members if x["in_rotation"]]

    # start creating schedule since given date
    shifts = itertools.cycle(rotate_members)
    cur_secondary_shift = next(shifts)
    cur_datetime = start_datetime.replace(hour=HOUR)
    while cur_datetime < end_datetime:
        cur_primary_shift = cur_secondary_shift
        cur_secondary_shift = next(shifts)

        cur_datetime_start = cur_datetime
        cur_datetime_end = cur_datetime + datetime.timedelta(days=NUM_DAYS_IN_SHIFT)
        start_unix_timestamp = make_unix_timestamp(cur_datetime_start)
        end_unix_timestamp = make_unix_timestamp(cur_datetime_end)

        requests.post(
            f"{HOST}/api/v0/events",
            json={
                "user": cur_primary_shift["name"],
                "team": TEAM_NAME,
                "role": "primary",
                "start": start_unix_timestamp,
                "end": end_unix_timestamp,
            },
        )
        requests.post(
            f"{HOST}/api/v0/events",
            json={
                "user": cur_secondary_shift["name"],
                "team": TEAM_NAME,
                "role": "secondary",
                "start": start_unix_timestamp,
                "end": end_unix_timestamp,
            },
        )

        cur_datetime = cur_datetime_end


if __name__ == "__main__":
    main()
