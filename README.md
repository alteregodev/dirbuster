# dirbuster

Simple directory checking tool

## Installing (make sure you have git and python installed)

### Step 1

`git clone https://github.com/alteregodev/diruster` - Clone the repo

`cd dirbuster` (Cd into the directory with readme.md and license)

### Step 2

`pip install -r requirements.txt` - Install dependencies

### Step 3

`python dirbuster.py --your-flags` - Run the script

## Flags

- `-u --url` - Set the target's url
- `-w --wordlist` - Specify the wordlist to use
- `-x --extenions` - Add custom extensions to check divided by a comma, ex. php,html,txt
- `-t --timeout` - Set custom timeout
