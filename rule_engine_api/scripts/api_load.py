import requests
import time
import random
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Define the rules
rules = [
    {
        "description": "Amount less than 1,500,000",
        "rule": "transaction['amount'] < 1500000",
        "id": 1,
    },
    {
        "description": "Email address ends with .ci",
        "rule": "transaction['email_address'].endswith('.ci')",
        "id": 2,
    },
    {
        "description": "Minimum amount of transaction greater than 500",
        "rule": "transaction['amount'] > 500",
        "id": 3,
    },
]


# Function to generate a transaction payload
def generate_transaction(approved=False):
    transaction_data = {
        "transaction_id": str(random.randint(1000, 9999)),
        "transaction_amount": str(random.randint(100, 2000000)),  # Varying amounts
        "merchant_id": str(random.randint(100, 999)),
        "client_id": str(random.randint(100, 999)),
        "phone_number": str(random.randint(1000000000, 9999999999)),
        "ip_address": "127.0.0.1",
        "email_address": (
            "test@example.ci" if approved else "test@example.com"
        ),  # .ci for approved, .com for rejected
        "amount": (
            random.randint(501, 1250000)
            if approved
            else random.randint(2000001, 10250000)
        ),  # Varying amounts
    }
    return transaction_data


# Function to apply rules to a transaction
def apply_rules(transaction, rules):
    return all(eval(rule["rule"], {"transaction": transaction}) for rule in rules)


# Function to send a request
def send_request(url, data):
    start_time = time.time()
    response = requests.post(url, json=data)
    end_time = time.time()
    return response.json()["status_code"], end_time - start_time


# Function to send multiple requests in parallel
def send_requests_parallel(endpoint, payloads):
    results = []
    times = []
    with ThreadPoolExecutor() as executor, tqdm(total=len(payloads)) as pbar:
        for result, time_taken in executor.map(
            send_request, [endpoint] * len(payloads), payloads
        ):
            results.append(result)
            times.append(time_taken)
            pbar.update(1)
    return results, times


def main(endpoint, num_requests=100):

    # Generate payloads
    approved_payloads = [
        generate_transaction(approved=True) for _ in range(num_requests // 2)
    ]
    rejected_payloads = [
        generate_transaction(approved=False) for _ in range(num_requests // 2)
    ]
    payloads = approved_payloads + rejected_payloads

    # Send requests in parallel
    results, times = send_requests_parallel(endpoint, payloads)

    # Calculate and print execution time
    execution_time = sum(times)
    print(
        f"Total time taken to send {num_requests} requests: {execution_time:.2f} seconds"
    )

    # Count successful and failed requests
    success_count = results.count(200)
    failure_count = len(results) - success_count
    print(f"Successful requests: {success_count}, Failed requests: {failure_count}")

    # Calculate and print average, min, and max request times
    if times:
        min_time = min(times)
        max_time = max(times)
        avg_time = sum(times) / len(times)
        print(f"Min request time: {min_time:.2f} seconds")
        print(f"Max request time: {max_time:.2f} seconds")
        print(f"Average request time: {avg_time:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send multiple requests to an endpoint."
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        default="http://localhost:8000/v0/transactions/check-transaction",
        help="The endpoint to send requests to.",
    )
    parser.add_argument(
        "--num_requests",
        type=int,
        default=100,
        help="The number of requests to send.",
    )
    args = parser.parse_args()

    main(args.endpoint, args.num_requests)
