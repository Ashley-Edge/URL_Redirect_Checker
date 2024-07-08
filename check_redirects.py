#!/usr/bin/env python3

# Imports needed
import sys
import requests
from urllib.parse import urljoin


def check_redirects(base_url, paths):
    # Loop through each path
    for path in paths:
        # Combine the base URL with the relative path
        url = urljoin(base_url, path)
        print(f"Processing URL: {url}")

        try:
            # Send a GET request and allow redirects
            response = requests.get(url, allow_redirects=True, timeout=10)

            # Get the final URL and status code after all redirects
            final_url = response.url
            final_status_code = response.status_code
            print(f"Status code: {final_status_code}")

            # Check if there was a redirect
            if response.history:
                print(f"Final URL Location: {final_url}\n")
            else:
                print("No Redirect\n")

        # Error messages
        except requests.Timeout:
            print(f"Request to {url} timed has out.\n")
        except requests.RequestException as e:
            print(f"Error While Processing: {e} for {url}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_redirects.py <base_url> <path1> <path2> ...")
        sys.exit(1)

    base_url = sys.argv[1]
    paths = sys.argv[2:]
    check_redirects(base_url, paths)
