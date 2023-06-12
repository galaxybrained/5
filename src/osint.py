import requests
import geonamescache
from bs4 import BeautifulSoup

# Function to check username on social media
def check_username_on_social_media(username):
    # Platforms dictionary with URLs
    platforms = {
        'Twitter': f"https://twitter.com/{username}",
        'Instagram': f"https://www.instagram.com/{username}",
        'Facebook': f"https://www.facebook.com/{username}",
        'LinkedIn': f"https://www.linkedin.com/in/{username}",
    }

    # Iterate over platforms and check if the user exists
    for platform, url in platforms.items():
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{username} is found on {platform} - {url}")
        else:
            print(f"{username} is not found on {platform}")

# Function to search numbers on social media
def search_numbers_on_social_media(phone_number, twitter_api_key, twitter_api_secret_key, twitter_access_token, twitter_access_token_secret):
    # Twitter API search
    twitter_url = f"https://api.twitter.com/2/users/by/phone/phone_number:{phone_number}"
    response = requests.get(
        twitter_url,
        auth=(twitter_api_key, twitter_api_secret_key),
        headers={"Authorization": f"Bearer {twitter_access_token}"},
    )
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            username = data['data'][0]['username']
            check_username_on_social_media(username)
        else:
            print(f"No user found on Twitter associated with phone number {phone_number}")

# Function to search address on social media
def search_address_on_social_media(address):
    # GeonamesCache to retrieve location information
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries_by_names()
    states = gc.get_us_states_by_names()
    cities = gc.get_cities_by_name(address)

    if cities:
        city = list(cities.values())[0]
        state = states.get(city['admin1code'])
        country = countries.get(city['countrycode'])
        location = {
            'name': city['name'],
            'countryname': country['name'],
            'admin1name': state['name'] if state else '',
            'admin2name': city['admin2name'],
            'latitude': city['latitude'],
            'longitude': city['longitude']
        }
        print_data(location)
    else:
        print("No data found.")

# Function to print location data
def print_data(location):
    if location is None:
        print("No data found.")
        return

    print("Address: ", location['name'])
    print("Country: ", location['countryname'])
    print("State: ", location['admin1name'])
    print("City: ", location['admin2name'])
    print("Latitude: ", location['latitude'])
    print("Longitude: ", location['longitude'])

# Function to handle OSINT analysis by username
def osint_analysis(target_username, twitter_api_key, twitter_api_secret_key, twitter_access_token, twitter_access_token_secret):
    check_username_on_social_media(target_username)

# Function for the OSINT analysis menu
def osint_menu():
    print("OSINT Analysis Menu:")
    print("1. Search by username")
    print("2. Search by phone number")
    print("3. Search by address")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        target_username = input("Enter the target username: ")
        osint_analysis(target_username)
    elif choice == '2':
        phone_number = input("Enter the phone number: ")
        twitter_api_key = 'SK8qNeiK8gCrizAyCReTxnlj6'
        twitter_api_secret_key = '7tVWrMJDiiLaLMISJNdWuCNkDfejjYH5sH9VM1YXCVeLAvye3X'
        twitter_access_token = '1568815643503247360-kg9lQqbJtPDip8K3FHrO6RyJmdqahm'
        twitter_access_token_secret = 'mpsKOxumhjjr6O7Z2R3oIRSjpTJB3KKMMBjPBMOGxAqsd'
        search_numbers_on_social_media(phone_number, twitter_api_key, twitter_api_secret_key, twitter_access_token, twitter_access_token_secret)
    elif choice == '3':
        address = input("Enter the address: ")
        search_address_on_social_media(address)
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please try again.")

    print("\n" + "=" * 40 + "\n")
    osint_menu()

# Example usage
osint_menu()
