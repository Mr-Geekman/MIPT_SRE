#!/bin/python3

import pathlib
import subprocess
import time

DIRECTORIES_TO_CHECK = [
    pathlib.Path("/var/log"),
    pathlib.Path("/var/cache/apt"),
    pathlib.Path("/var/lib/prometheus"),
]

SAVE_PATH = pathlib.Path(
    "/opt/prometheus_exporters/textfile/directory_sizes.prom"
)


def get_directory_size(path: pathlib.Path) -> int:
    result_str = subprocess.check_output(["du", "-sb", path]).split()[0].decode("utf-8")
    result_int = int(result_str)
    return result_int


def main():
    start_time = time.perf_counter()

    results = {}
    for directory in DIRECTORIES_TO_CHECK:
        key = f'node_directory_size_bytes{{directory="{directory}"}}'
        results[key] = get_directory_size(directory)

    end_time = time.perf_counter()
    time_elapsed = end_time - start_time
    results["get_directory_size_duration_seconds"] = f"{time_elapsed:.5f}"

    with open(SAVE_PATH, "w") as ouf:
        for key, value in results.items():
            ouf.write(f"{key} {value}\n")


if __name__ == "__main__":
    main()
