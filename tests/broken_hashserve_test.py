import requests
import json
import sys
import pytest
import pytest_check as check
from clients.modules.hashing_clients import HashingClient

client = HashingClient()
print = sys.stdout


def test_start_hashserver():
    server = client.starting_server()
    check.is_not_none(server)
    print.write(server)


def test_verify_correctly_formatted_post_request():
    pass_w, status_code, job_id = client.create_hash_password(
        endpoint="hash", body=None
    )
    assert status_code == requests.codes.ok
    assert job_id is not None
    print.write(
        f"Post request success: status_code:{status_code}, job_id:{job_id}, test_string:{pass_w}"
    )


def test_verify_invalid_hash_post_fails():
    pass_w, status_code, job_id = client.create_hash_password(
        endpoint="hash", body={"username": "xassword"}
    )
    check.equal(status_code, requests.codes.bad_request)
    assert job_id is None
    print.write(
        f"Post request success: status_code:{status_code}, job_id:None, test_string:{pass_w}"
    )


def test_verify_post_request_to_stats_fails():
    pass_w, status_code, job_id = client.create_hash_password(
        endpoint="stats", body=None
    )
    check.equal(status_code, requests.codes.not_allowed)
    assert job_id is None
    print.write(
        f"Post request success: status_code:{status_code}, job_id:None, test_string:{pass_w}"
    )


def test_verify_multiple_simultaneous_post():
    number_of_runs = 10
    response_list = client.simultaneous_post(number_of_runs)
    for response in response_list:
        check.equal(response.status_code, requests.codes.ok)
        check.is_not_none(response.text)
    assert len(response_list) == number_of_runs
    print.write(
        f"Post request success: status_code:200, total runs:{len(response_list)}"
    )


def test_verify_get_hash_returns_hash():
    pass_w, status_code, job_id = client.create_hash_password(
        endpoint="hash", body=None
    )
    check.equal(status_code, requests.codes.ok)
    check.is_not_none(job_id)
    print.write(
        f"Post request success: status_code:{status_code}, job_id:{job_id}, test_string:{pass_w}"
    )

    hash_response = client.get_hash_by_id(job_id=job_id)
    hash_validator = client.hash_validator(pass_w)
    check.equal(hash_response.status_code, requests.codes.ok)
    assert hash_response.text == hash_validator
    print.write(
        f"Get request success: status_code:{hash_response.status_code}, job_id:{job_id}, test_string:{pass_w}, hashed:{hash_response.text}"
    )


def test_verify_invalid_hash_get_request_job_id():
    hash_response = client.get_hash_by_id(job_id="12345678")
    check.equal(hash_response.status_code, requests.codes.bad_request)
    assert "Hash not found" in hash_response.text
    print.write(
        f"Get request success: status_code:{hash_response.status_code}, job_id:12345678"
    )


def test_verify_stats_get_request():
    stats_response = client.get_hash_server_stats()
    res = stats_response.text
    res = json.loads(res)
    res_list = list(res.keys())
    check.is_in("TotalRequests", res_list)
    check.is_in("AverageTime", res_list)
    assert stats_response.status_code == requests.codes.ok
    print.write(
        f"Get request success: status_code:{stats_response.status_code}, test_string:{res}"
    )


def test_verify_stats_post_request_fails():
    stats_post_response = client.post_request()
    assert stats_post_response.status_code == requests.codes.not_allowed


def test_verify_graceful_shutdown_during():
    number_of_runs = 500
    response_list = client.simultaneous_post(number_of_runs)
    shutdown_response = client.graceful_shutdown(endpoint="hash")
    check.equal(shutdown_response.status_code, requests.codes.ok)
    assert len(response_list) == number_of_runs
    print.write(
        f"Graceful shutdown: status_code:{shutdown_response.status_code},number_0f_runs{number_of_runs}"
    )


def test_verify_no_connection_after_shutdown():
    try:
        client.post_request()
    except Exception as e:
        print.write("no connection:success")
