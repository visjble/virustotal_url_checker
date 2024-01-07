import requests, json, argparse

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Send a POST request to a specified URL and process the response.")
    parser.add_argument("url_to_check", type=str, help="The URL to check (e.g., www.example.com).")
    return parser.parse_args()

def print_attributes(data):
    attributes = data['data']['attributes']
    for key, value in attributes.items():
        if key == 'results':
            for engine, engine_data in value.items():
                print(f"Engine: {engine}")
                for engine_key, engine_value in engine_data.items():
                    print(f"  {engine_key}: {engine_value}")
                print()  # Adding a blank line for better readability between engines
        else:
            print(f"{key}: {value}")

def read_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except IOError:
        print("Error: Unable to read the API key file.")
        return None
    
# Command-line argument parsing
args = parse_command_line_args()

# Read API key from an external file
api_key = read_api_key("api_key") # api_key.txt
if not api_key:
    exit(1)
# API URL and headers
api_url = "https://www.virustotal.com/api/v3/urls"
headers = {
    "accept": "application/json",
    "x-apikey": api_key,
    "content-type": "application/x-www-form-urlencoded"
}

# Format the payload
payload = {"url": args.url_to_check}

# POST request to get initial response
response = requests.post(api_url, data=payload, headers=headers)

if response.status_code == 200:
    api_response_dict = json.loads(response.text)
    link = api_response_dict['data']['links']['self']

    # Make a GET request to the link
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print_attributes(data)
    else:
        print("Failed to retrieve data from link. Status Code:", response.status_code)
else:
    print("Failed to retrieve initial API response. Status Code:", response.status_code)
