#!/usr/bin/env python3

# Import modules needed
import sys
import os


# Function to get terminal width and create a separator line
def dynamic_separator():
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80  # Default to 80 columns if terminal size is unavailable
    return '-' * terminal_width


# Check for required packages
required_packages = ['requests']


def check_dependencies():
    import importlib
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print("\n" + dynamic_separator())
            print(f"* Error * '{package}' is not installed. To install and use this tool - 'pip install {package}'")
            print(dynamic_separator() + "\n")
            sys.exit(1)

# Check dependencies before importing other modules
check_dependencies()

# Import rest of themodules needed
import requests
from urllib.parse import urljoin


def fetch_with_fallback(url, timeout=10):
    """Try HEAD request using curl UA, fallback to Safari UA if 403."""

    # First attempt — curl-like headers
    primary_headers = {
        "User-Agent": "curl",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
    }

    try:
        response = requests.head(url, allow_redirects=False, timeout=timeout, headers=primary_headers)

        # If WAF/Sucuri blocks curl → retry with Safari UA
        if response.status_code == 403:
            print("    ⚠ 403 received — retrying with Safari User-Agent…")

            fallback_headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
                ),
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br",
            }

            response = requests.head(url, allow_redirects=False, timeout=timeout, headers=fallback_headers)

        return response

    except requests.RequestException as e:
        raise e


def check_redirects(base_url, paths):
    # Create a session to maintain state (like cookies)
    session = requests.Session()

    # Set headers similar to curl's default headers
    # headers = {
    #     #'User-Agent': 'curl',
    #     "User-Agent": (
    #         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    #         "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    #     ),
    #     'Accept': '*/*',
    #     'Referer': base_url,
    #     'Connection': 'keep-alive',
    #     'Accept-Encoding': 'gzip, deflate, br',
    # }
    # session.headers.update(headers)
    print("\n" + dynamic_separator())
    # Loop through each path
    for path in paths:
        # Combine the base URL with the relative path
        url = urljoin(base_url, path)
        #print(dynamic_separator())
        #print("")
        #print(f"Processing URL: {url}\n")

        try:
            # Send a HEAD request to match curl -IL behavior
            response = session.head(url, allow_redirects=True, timeout=10)
            
            # If we got a 403, retry once with Safari User-Agent
            if response.status_code == 403:
                session.headers["User-Agent"] = (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
                )
                response = session.head(url, allow_redirects=True, timeout=10)
                # Restore curl UA for next iteration
                session.headers["User-Agent"] = "curl"

            # Get the final URL and status code after all redirects
            final_url = response.url
            final_status_code = response.status_code

            # Check if there was a redirect
            if response.history:
                status_chain = [resp.status_code for resp in response.history] + [final_status_code]
                url_chain = [resp.url for resp in response.history] + [final_url]
                
                print(f"♡ Redirect detected ♡\n")

                # Print the redirect chain in a more readable format
                print("    Full redirect chain")
                print(f"        Original URL : {url_chain[0]}")
                for i, u in enumerate(url_chain[1:-1], start=1):
                    print(f"        -> Redirect {i}: {u}")
                print(f"        -> Final URL : {url_chain[-1]}")

                # Print the status code chain
                print(f"    Status code chain:  {' -> '.join(map(str, status_chain))}")           
                print(f"\n♡ Final status & URL: ({final_status_code}) {final_url} ♡")
            else:
                print(f"♡ No redirects found ♡")
                print(f"    Complete URL: {url}")
                print(f"    Status code : {final_status_code}")
            print(dynamic_separator())

        # Error messages
        except requests.Timeout:
            print(f"* This request has timed out, try again *\n")
            print(f"    {url}")
            print(dynamic_separator())
        except requests.RequestException as e:
            print(f"* Error While Processing {url} *\n")
            print(f"    {e}")
            print(dynamic_separator())
    print()


# Main function that handles argument parsing and calls the check_redirects function
def main():
    if len(sys.argv) < 3:
        print("\n" + dynamic_separator())
        print("* Incorrect Usage * Try `python <path to file>/check_redirects.py <base_url> <path1>`")
        print(dynamic_separator() + "\n")
        sys.exit(1)

    base_url = sys.argv[1]
    paths = sys.argv[2:]
    check_redirects(base_url, paths)


if __name__ == "__main__":
    main()
