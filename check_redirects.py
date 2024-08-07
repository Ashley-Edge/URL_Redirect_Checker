#!/usr/bin/env python3

# Imports needed
import sys
import requests
from urllib.parse import urljoin


def check_redirects(base_url, paths):
    # Adding common browser User-Agents - to act more like curl
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': base_url,  # Adding a referer header
    }
    # Loop through each path
    for path in paths:
        # Combine the base URL with the relative path
        url = urljoin(base_url, path)
        print("____________________________________________________________\n")
        print(f"Processing URL: {url}\n")

        try:
            # Send a GET request and allow redirects
            response = requests.get(url, allow_redirects=True, timeout=10)

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
            print(f"    * Error While Processing * {e} for {url}\n")
    print("____________________________________________________________\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("____________________________________________________________\n")
        print("Usage: python check_redirects.py <base_url> <path1> <path2> ...")
        print("____________________________________________________________\n")
        sys.exit(1)

    base_url = sys.argv[1]
    paths = sys.argv[2:]
    check_redirects(base_url, paths)
