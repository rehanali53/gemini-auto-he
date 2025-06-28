import json
import requests

# Load and parse the JSON file to get URLs
def load_urls_from_json():
    file_path = 'autobot fiverr.postman_collection.json' # user your Postman Json file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    urls = []
    for item in data['item']:
        url_raw = item['request']['url']['raw']
        urls.append(url_raw)
    return urls

# Make HTTP requests to the URLs and extract car data
def extract_car_data(urls):
    all_cars_data = []  # A list to store data for all cars from all URLs

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                response_data = response.json()
                cars_data = response_data.get('content', {}).get('messages', [])
                all_cars_data.extend(cars_data)  # Add the cars data to the all_cars_data list
            except json.JSONDecodeError:
                print(f"Error decoding JSON from response of {url}")
        else:
            print(f"Failed to retrieve data from {url}")
    
    return all_cars_data

# Function to search for a car by name and return its action_url and image_url
def search_car_by_name(car_name, car_data):
    for car in car_data:
        if car['type'] == 'cards':
            for element in car['elements']:
                if element['title'] == car_name:
                    return element['action_url'], element['image_url']
    return None, None
def extract_car_titles(car_data):
    car_titles = []
    for car in car_data:
        if car['type'] == 'cards':
            for element in car['elements']:
                car_titles.append(element['title'])
    return car_titles


urls = load_urls_from_json()
car_data = extract_car_data(urls)
#print(car_data)

# Search for a specific car by name
#car_name = 'מאזדה-CX-5 2015'
#action_url, image_url = search_car_by_name(car_name, car_data)

# Print the action_url and image_url of the car
#print(f'Action URL: {action_url}')
#print(f'Image URL: {image_url}')
