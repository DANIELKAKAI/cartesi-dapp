from os import environ
import logging
import requests

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

import json


def dict_to_hex(dictionary):
    json_str = json.dumps(dictionary)
    bytes_data = json_str.encode('utf-8')
    hex_str = '0x' + bytes_data.hex()
    return hex_str


def hex_to_str(hex_str):
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]
    bytes_data = bytes.fromhex(hex_str)
    original_str = bytes_data.decode('utf-8')
    return original_str


tx_counter = {}


def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    status = "accept"

    sender = data["metadata"]["msg_sender"]

    if sender in tx_counter:
        tx_counter[sender] += 1
    else:
        tx_counter[sender] = 1

    response = requests.post(
        rollup_server + "/notice", json={"payload": dict_to_hex(tx_counter)}
    )
    logger.info(
        f"Received notice status {response.status_code} body {response.content}"
    )
    return status


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")

    status = "accept"

    inputPayload = data["payload"]
    route = hex_to_str(inputPayload)  # for inpsect its a path /inspect/<payload>
    logger.info(f"Route is {route}")
    if route == "tx_counter":
        inputPayload = dict_to_hex(tx_counter)
    response = requests.post(
        rollup_server + "/report", json={"payload": inputPayload}
    )
    logger.info(
        f"Received notice status {response.status_code} body {response.content}"
    )

    return status


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
