#!/usr/bin/env python3

# for more information about this script see: https://akoova.atlassian.net/wiki/x/EoDUv

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


def check_redirects(base_url, paths):
    # Create a session to maintain state (like cookies)
    session = requests.Session()

    # Set headers similar to curl's default headers
    headers = {
        'User-Agent': 'curl',
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
        print(dynamic_separator())
        #print(f"Processing URL: {url}\n")

        try:
            # Send a HEAD request to match curl -IL behavior
            response = session.head(url, allow_redirects=True, timeout=10)

            # Get the final URL and status code after all redirects
            final_url = response.url
            final_status_code = response.status_code

            # Check if there was a redirect
            if response.history:
                status_chain = [resp.status_code for resp in response.history] + [final_status_code]
                url_chain = [resp.url for resp in response.history] + [final_url]
                
                print(f"\n♡ Redirect detected ♡\n")

                # Print the redirect chain in a more readable format
                print("    Full redirect chain")
                print(f"        Original URL : {url_chain[0]}")
                for i, u in enumerate(url_chain[1:-1], start=1):
                    print(f"        -> Redirect {i}: {u}")
                print(f"        -> Final URL : {url_chain[-1]}")

                # Print the status code chain
                print(f"\n    Status code chain:  {' -> '.join(map(str, status_chain))}")           
                print(f"\n♡ Final status & URL: ({final_status_code}) {final_url} ♡\n")
            else:
                print(f"\n♡ No redirects found ♡\n")
                print(f"    Complete URL: {url}")
                print(f"    Status code : {final_status_code}\n")

        # Error messages
        except requests.Timeout:
            print(f"* This request has timed out, try again *\n")
            print(f"    {url}\n")
        except requests.RequestException as e:
            print(f"* Error While Processing {url} *\n")
            print(f"    {e}\n")
    print(dynamic_separator() + "\n")


# Main function that handles argument parsing and calls the check_redirects function
def main():
    if len(sys.argv) < 3:
        print("\n" + dynamic_separator() + "\n")
        print("* Incorrect Usage * Try `python <path to file>/redirect_checker.py <base_url> <path1>`")
        print("\n" + dynamic_separator() + "\n")
        sys.exit(1)

    base_url = sys.argv[1]
    paths = sys.argv[2:]
    check_redirects(base_url, paths)


if __name__ == "__main__":
    main()
