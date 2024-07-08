# URL Redirect Checker

* This script checks a list of URLs and returns their redirect location and status code.
* The `check_redirects` function takes `base_url` and `paths` as arguments.
* The script combines the base URL with each relative path using `urljoin`.
* The script sends a GET request to each combined URL and prints the HTTP status code and final URL after any redirects, or indicates if there were no redirects.
* The __main__ block checks for enough command-line arguments and calls `check_redirects` with the base URL and relative paths.

## Requirements

- Python 3 minimum 
- `requests` library

## Usage

```bash
python <path to file>/check_redirects.py <base_url> <path1> <path2> ...
```
For a base URL of 'https://www.example.com' and the paths '/women/shoes' and '/men/shirts':

### Output Examples
For a base URL of 'https://www.example.com' and the paths '/women/shoes' and '/men/shirts':
```bash
python Ashley_Code/URL_Redirect_Checker/check_redirects.py https://www.example.com /women/shoes /men/shirts
```
#### Redirects
```bash
Processing URL: https://www.example.com/women/shoes
Status code: 301
Final URL Location: https://www.example.com/women/new-shoes
```
#### No Redirect
```bash
Processing URL: https://www.example.com/women/shoes
Status code: 200
No Redirect
```
#### Output with more than one path called
```bash
Processing URL: https://www.example.com/women/shoes
Status code: 301
Final URL Location: https://www.example.com/women/new-shoes

Processing URL: https://www.example.com/men/shirts
Status code: 200
No Redirect
```
#### Error While Processing
```bash
Processing URL: https://www.example.com/women/shoes
Error While Processing: 404 Client Error: Not Found for https://www.example.com/women/shoes
```
#### Timed out
```bash
Processing URL: https://www.example.com/women/shoes
Request to https://www.example.com/women/shoes has timed out.
```
## Updates
1. Monday 8<sup>th</sup> of July 2024 ~ `edit_outputs` Tidying up the output and adding in a timeout after 10 seconds with an error message.