"""Codacy coverage reporter for Python"""

import argparse
import json
import logging
import os
from xml.dom import minidom

import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

CODACY_PROJECT_TOKEN = os.getenv('CODACY_PROJECT_TOKEN')
CODACY_BASE_API_URL = os.getenv('CODACY_BASE_API_URL', 'https://api.codacy.com')
URL = CODACY_BASE_API_URL + '/2.0/coverage/{commit}/python'
DEFAULT_REPORT_FILE = 'coverage.xml'


def get_git_revision_hash():
    import subprocess

    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()


def parse_report_file(report_file):
    # Convert decimal string to floored int percent value
    percent = lambda s: int(float(s) * 100)

    # Parse the XML into the format expected by the API
    report_xml = minidom.parse(report_file)

    report = {
        'language': "python",
        'total': percent(report_xml.getElementsByTagName('coverage')[0].attributes['line-rate'].value),
        'fileReports': [],
    }

    classes = report_xml.getElementsByTagName('class')
    for cls in classes:
        file_report = {
            'filename': cls.attributes['filename'].value,
            'total': percent(cls.attributes['line-rate'].value),
            'coverage': {},
        }
        lines = cls.getElementsByTagName('line')
        for line in lines:
            hits = int(line.attributes['hits'].value)
            if hits >= 1:
                # The API assumes 0 if a line is missing
                file_report['coverage'][line.attributes['number'].value] = hits
        report['fileReports'] += [file_report]

    return report


def upload_report(report, token, commit):
    # Try to send the data, raise an exception if we fail
    url = URL.format(commit=commit)
    data = json.dumps(report)
    headers = {
        "project_token": token,
        "Content-Type": "application/json"
    }

    logging.debug(data)

    r = requests.post(url, data=data, headers=headers, allow_redirects=True)

    logging.debug(r.content)
    r.raise_for_status()

    message = json.loads(r.content)['success']
    logging.info(message)


def main(report_file, token, commit):
    """Parse XML file and POST it to the Codacy API"""

    logging.info("Parsing report file...")
    report = parse_report_file(report_file)

    logging.info("Uploading report...")
    upload_report(report, token, commit)


def run():
    parser = argparse.ArgumentParser(description='Codacy coverage reporter for Python.')
    parser.add_argument("-r", "--report", type=str, help="coverage report file", default=DEFAULT_REPORT_FILE)
    parser.add_argument("-c", "--commit", type=str, help="coverage report file")
    parser.add_argument("-v", "--verbose", help="coverage report file", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.Logger.setLevel(logging.getLogger(), logging.DEBUG)

    if not CODACY_PROJECT_TOKEN:
        logging.error("environment variable CODACY_PROJECT_TOKEN is not defined.")
        exit(1)

    if not args.commit:
        args.commit = get_git_revision_hash()

    main(args.report, CODACY_PROJECT_TOKEN, args.commit)
