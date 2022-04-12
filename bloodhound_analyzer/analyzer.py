import csv
import json
import logging
import os
import shutil
import subprocess  # nosec
from datetime import datetime
from pathlib import Path

from .config import config

OUTPUT_DIR = config["bloodhound-analyzer"]["output_dir"]
TMP_DIR = config["bloodhound-analyzer"]["tmp_dir"]
QUERIES_DEFINITION = config["bloodhound-analyzer"]["query_file"]
NEO4J_ADDR = config["neo4j"]["address"]
NEO4J_USERNAME = config["neo4j"]["username"]
NEO4J_PASSWORD = config["neo4j"]["password"]


def neo4j_json_to_csv(prefix, path):
    results_array = []
    json_file = open(path, "r")
    _, file_name_ext = os.path.split(path)
    file_name = os.path.splitext(file_name_ext)[0]

    for line in json_file.readlines():
        json_result = json.loads(line)
        keys = list(json_result.keys())
        results_array.append(json_result[keys[0]])

    with open(
        os.path.join(
            "{0}/{1}".format(TMP_DIR, prefix), "{0}.csv".format(file_name)
        ),
        "w",
    ) as csv_file:
        writer = csv.writer(csv_file)

        columns = list(
            {column for row in results_array for column in row.keys()}
        )

        writer.writerow(columns)
        for row in results_array:
            writer.writerow(
                [
                    None if column not in row else row[column]
                    for column in columns
                ]
            )


def run():
    if not Path(TMP_DIR).exists():
        Path(TMP_DIR).mkdir()
    else:
        for directory, _, files in os.walk(TMP_DIR):
            for file in files:
                # Clean files from TMP_DIR
                os.unlink(os.path.join(directory, file))

    subprocess.run(  # nosec
        [
            "/usr/bin/cypher-shell",
            "-a",
            NEO4J_ADDR,
            "-u",
            NEO4J_USERNAME,
            "-p",
            NEO4J_PASSWORD,
            "-f",
            QUERIES_DEFINITION,
        ],
        shell=False,
    )

    prefix = datetime.now().strftime("%Y%m%d%H%M")
    os.makedirs(os.path.join(TMP_DIR, prefix))
    for directory, _, files in os.walk(TMP_DIR):
        for file in files:
            # For each exported json, construct the appropriate csv
            logging.info("Parsed {0}".format(os.path.join(directory, file)))
            path = os.path.join(directory, file)
            neo4j_json_to_csv(prefix, path)
        break
    shutil.make_archive(
        os.path.join(OUTPUT_DIR, prefix), "zip", os.path.join(TMP_DIR, prefix)
    )
