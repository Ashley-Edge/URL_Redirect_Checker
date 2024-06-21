# URL Redirect Checker

* This script checks a list of URLs and returns their redirect location and status code.
* The `check_redirects` function takes `base_url` and `paths` as arguments.
* The script combines the base URL with each relative path using `urljoin`.
* The script sends a GET request to each combined URL and prints the HTTP status code and final URL after any redirects, or indicates if there were no redirects.
* The __main__ block checks for enough command-line arguments and calls `check_redirects` with the base URL and relative paths.

## Requirements

- Python 3 minimum 
- `requests` library

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Ashley-Edge/URL_Redirect_Checker.git
    cd URL_Redirect_Checker
    ```

2. **Install dependencies**:

    ```bash
    pip install requests
    ```

## Usage

```bash
python <path to file>/check_redirects.py <base_url> <path1> <path2> ...
```
### Example
For a base URL of 'https://www.example.com' and paths '/home/women/shoes' and '/home/men/shirts':
#### Command
```bash
python Ashley_Code/URL_Redirect_Checker/check_redirects.py https://www.example.com /home/women/shoes /home/men/shirts
```
#### Output
```bash
Processing URL: https://www.example.com/home/women/shoes
HTTP Status Code: 301
Redirect URL: https://www.example.com/home/women/new-shoes

Processing URL: https://www.example.com/home/men/shirts
HTTP Status Code: 200
No Redirect
```
