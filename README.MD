# TikTok Username Availability Checker

This script checks the availability of TikTok usernames by parsing the HTML response from TikTok profile pages. It uses concurrent threads to speed up the checking process.

## Requirements

Ensure you have the following Python libraries installed:

- `requests`
- `beautifulsoup4`

You can install these libraries using pip:

```bash
pip install -r requirements.txt
```

# Usage

- Place your list of usernames in a file named usernames.txt in the same directory as the script.

Run the script:

```sh
<python path variable> main.py
```

# Notice

- Since TikTok doesn't expose data in regards to ban status, a username may appear available using this application if it was banned.
