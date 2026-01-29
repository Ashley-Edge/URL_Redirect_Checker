# URL Redirect Checker

This script checks a list of URLs and returns their redirect location and status code. I have based this on how `curl -IL` works. I wanted something to show me wether the redirect is in place and with what status. I do plan on adding features as and when I need them in my day to day use of this script

## Requirements

- Python 3 minimum 
- `requests` library - this script will detact if this isn't installed and prompt the user to install it.

## Usage
#### <u>Option 1</u>
```bash
python <path to file>/check_redirects.py <base_url> <path1> <path2> ...
```
#### <u>Option 2</U>
You can set aan alis for a quicker command call
`vim ~/.bashrc` and paste the below into your file

`alias redirect_checker='python3 /path/to/your/redirect_checker.py'`

To appy the changes `source ~/.bashrc` now you can use this script by 
```bash
check_redirects <base_url> <path1> <path2> ...
```

## Output Examples
For a base URL of 'https://www.example.com' and the paths '/women/shoes' and '/men/shirts':
```bash
check_redirects https://www.example.com /women/shoes /men/shirts
```
#### <u>Redirects</u>
```bash
-------------------------------------------------------------------------------------
♡ Redirect detected ♡
    Full redirect chain
        Original URL : https://www.example.com/dogs
        -> Final URL : https://www.example.com/cute-dogs
    Status code chain:  301 -> 200

♡ Final status & URL: (200) https://www.example.com/cute-dogs ♡
-------------------------------------------------------------------------------------
```
#### <u>No Redirect</u>
```bash
-------------------------------------------------------------------------------------
♡ No redirects found ♡
    Complete URL: https://www.example.com/cute-dogs
    Status code : 200
-------------------------------------------------------------------------------------
```
#### <u>Output with more than one in the chain</u>
```bash
-------------------------------------------------------------------------------------
♡ Redirect detected ♡
    Full redirect chain
        Original URL : https://www.example.com/dogs
        -> Final URL : https://www.example.com/cute-dogs
    Status code chain:  301 -> 200

Final status & URL: (200) https://www.example.com/cute-dogs
-------------------------------------------------------------------------------------
```
#### <u>Requests isn't installed</u>
```bash
-------------------------------------------------------------------------------------
* Error * 'requests' is not installed. Please install it using 'pip install requests'
-------------------------------------------------------------------------------------
```
#### <u>Error While Processing</u>
```bash
-------------------------------------------------------------------------------------
* Error While Processing https://www.example.com/cute-dogs *
        404 Client Error: XYZ
-------------------------------------------------------------------------------------
```
#### <u>Timed out</u>
```bash
-------------------------------------------------------------------------------------
* This request has timed out *
        https://www.example.com/cute-dogs
-------------------------------------------------------------------------------------
```
## <u>Updates</u>
1. Monday 8<sup>th</sup> of July 2024 ~ `edit_outputs` Tidying up the output and adding in a timeout after 10 seconds with an error message.
2. Monday 8<sup>th</sup> of July 2024 ~ `Headers` Adding common browser User-Agents, this acts more like curl (used my script IRL and the output compared to curl differed)
3. Wednesday 7<sup>th</sup> of August 2024 ~ Made the outputs pretty.
4. Thursday 8<sup>th</sup> of August 2024 ~ Added more `Headers`, switched from `GET` to `HEAD`to mimic `curl -IL` closer. Added a `requests.Session` to maintain headers and cookies across requests 
5. Wednesday 14<sup>th</sup> of August 2024 ~ Added `check_dependencies` for the `requests` library, it will prompt the user to install `requirements.txt` if it is not installed.
6. Thursday 22<sup>nd</sup> of August 2024 ~ created a dynamic line separator function that bases the number of `-` on the width of the terminal.
7. Tuseday 12<sup>th</sup> of November 2024 ~ Tightended up the output, to much space earlier

End of File
End of File test 2
