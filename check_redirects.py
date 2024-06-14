#!/usr/bin/env python3

#imports needed 
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
            response = requests.get(url, allow_redirects=True)
            
            # Get the final URL after all redirects
            final_url = response.url
            status_code = response.status_code
            
            # Check if there was a redirect
            if response.history:
                print(f"HTTP Status Code: {status_code}")
                print(f"Redirect URL: {final_url}")
            else:
                print(f"HTTP Status Code: {status_code}")
                print("No Redirect")
        
        except requests.exceptions.RequestException as e:
            print(f"Error processing URL {url}: {e}")
        
        print("")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_redirects.py <base_url> <path1> <path2> ...")
        sys.exit(1)
    
    base_url = sys.argv[1]
    paths = sys.argv[2:]
    check_redirects(base_url, paths)
