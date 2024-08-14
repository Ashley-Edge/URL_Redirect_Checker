#!/usr/bin/env python3

# Import modules needed
import sys

# Check for required packages
required_packages = ['requests']

def check_dependencies():
    import importlib
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"\n    * Error * '{package}' is not installed. Please install it using 'pip install -r requirements.txt'")
            print("--------------------------------------------------------------------------------------------------------\n")
            sys.exit(1)

# Check dependencies before importing other modules
check_dependencies()

# Import rest of themodules needed
import requests
from urllib.parse import urljoin


def check_redirects(base_url, paths):
    # Create a session to maintain state (like cookies)
    session = requests.Session()

    # Set headers similar to curl's default headers
    headers = {
        'User-Agent': 'curl/7.64.1',
        'Accept': '*/*',
        'Referer': base_url,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    session.headers.update(headers)

    # Loop through each path
    for path in paths:
        # Combine the base URL with the relative path
        url = urljoin(base_url, path)
        print("------------------------------------------------------------------------------\n")
        print(f"Processing URL: {url}\n")

        try:
            # Send a HEAD request to match curl -IL behavior
            response = session.head(url, allow_redirects=True, timeout=10)

            # Get the final URL and status code after all redirects
            final_url = response.url
            final_status_code = response.status_code

            # Check if there was a redirect
            if response.history:
                status_chain = [resp.status_code for resp in response.history] + [final_status_code]
                print(f"    Status code chain: {' -> '.join(map(str, status_chain))}")
                print(f"    Final URL Location: {final_url}\n")
            else:
                print(f"* No redirect applied * Status code: {final_status_code}\n")

        # Error messages
        except requests.Timeout:
            print(f"    * This request has timed out *\n")
        except requests.RequestException as e:
            print(f"    * Error While Processing * {e} for {url}")
    print("------------------------------------------------------------------------------\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("------------------------------------------------------------------------------")
        print("Incorrect Usage: python check_redirects.py <base_url> <path1> <path2> ...")
        print("------------------------------------------------------------------------------\n")
        sys.exit(1)

    base_url = sys.argv[1]
    paths = sys.argv[2:]
    check_redirects(base_url, paths)
