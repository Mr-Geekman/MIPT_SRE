import os
import time
import http

import requests

from loguru import logger
from prometheus_client import start_http_server
from prometheus_client import Counter, Gauge


class Config:
    oncall_url = os.getenv("ONCALL_EXPORTER_API_URL", "http://127.0.0.1:8080")
    scrape_interval = int(os.getenv("ONCALL_EXPORTER_SCRAPE_INTERVAL", 60))
    exporter_port = int(os.getenv("ONCALL_EXPORTER_METRICS_PORT", 9200))


class OnCallMetricsExporter:
    def __init__(self, config):
        self.url = config.oncall_url
        self.scrape_interval = config.scrape_interval
        self.frac_users_without_phone = Gauge(
            "oncall_frac_users_without_phone",
            "Gauge with fraction of users without phone number.",
        )
        self.primary_role_present = Counter(
            "oncall_primary_role_present",
            "Counter with outcome of checking the presence of person with primary role in each team.",
            labelnames=["type"],
        )

    def run_metrics_loop(self):
        while True:
            self.fetch()
            time.sleep(self.scrape_interval)

    def _get_frac_users_without_phone(self):
        cur_request = f"{self.url}/api/v0/users"
        try:
            response = requests.get(cur_request)
        except requests.ConnectionError:
            logger.info(f"Connection error during fetching the list of users: {cur_request}")
            return None

        if response.status_code != http.HTTPStatus.OK:
            logger.info(f"Not ok response during fetching the list of teams: {response.content}")
            return None

        users = response.json()
        failed_users = 0
        for user in users:
            if not user["contacts"]:
                logger.info(f"Can't find contacts for the user: {user['name']}")
                failed_users += 1
        return failed_users / len(users)

    def _get_primary_oncall_result(self):
        cur_request = f"{self.url}/api/v0/teams"
        try:
            response = requests.get(cur_request)
        except requests.ConnectionError:
            logger.info(f"Connection error during fetching the list of teams: {cur_request}")
            return 0

        if response.status_code != http.HTTPStatus.OK:
            logger.info(f"Not ok response during fetching the list of teams: {response.content}")
            return 0

        teams = response.json()
        for team in teams:
            cur_request = f"{self.url}/api/v0/teams/{team}/summary"
            try:
                response = requests.get(cur_request)
            except requests.ConnectionError:
                logger.info(f"Connection error during fetching the summary for team: {cur_request}")
                return 0

            if response.status_code != http.HTTPStatus.OK:
                logger.info(f"Not ok response during fetching the summary for team: {team}, {response.content}")
                return 0
            team_summary = response.json()
            if "primary" not in team_summary["current"]:
                logger.info(f"There is no current primary role in a team: {team}")
                return 0
        return 1

    def fetch(self):
        # update gauge for number of users without phone number
        value = self._get_frac_users_without_phone()
        if value is not None:
            self.frac_users_without_phone.set(value)
        else:
            logger.info("Can't update oncall_frac_users_without_phone")

        # update counter for checking primary role
        is_success = self._get_primary_oncall_result()
        self.primary_role_present.labels("positive").inc(is_success)
        self.primary_role_present.labels("total").inc(1)


if __name__ == "__main__":
    config = Config()
    exporter = OnCallMetricsExporter(config)
    start_http_server(config.exporter_port)
    exporter.run_metrics_loop()
