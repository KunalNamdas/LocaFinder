import signal
from setup.sprint import sprint
from setup.colors import c, r, ran, lr, lc, lg, g, ly, y
from setup.banner import banner, banner2, clear
from geopy import Nominatim, distance
import requests
import logging
import sys
import folium

# Setup logging
logging.basicConfig(filename='geotool.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize geolocator with user agent
geolocator = Nominatim(user_agent="geo_tool")

# Clear screen and display banner
clear()
banner()

# Configuration for OpenWeatherMap API
OWM_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'

def get_location_details(place_name):
    try:
        location = geolocator.geocode(place_name, language="en")
        if location:
            print(lg + "\n\nLocation: " + c + place_name)
            print(lg + 'Details: ' + c, location.address)
            print(lg + 'Latitude: ' + c, location.latitude)
            print(lg + 'Longitude: ' + c, location.longitude)
            print(lg + 'Country: ' + c, location.address.split(',')[-1])
                
            return location
        else:
            sprint(lr + "Could not find information for " + c + place_name)
    except Exception as e:
        sprint(lr + f"Error: {str(e)}")

def get_zip_code_details(zip_code):
    try:
        location = geolocator.geocode(zip_code)
        if location:
            print(lg + f"\nDetails of Zip Code {zip_code}:")
            print(lg + 'City: ' + c, location.address.split(',')[-5])
            print(lg + 'State: ' + c, location.address.split(',')[-2])
            print(lg + 'Country: ' + c, location.address.split(',')[-1])
            print(lg + 'Latitude: ' + c, location.latitude)
            print(lg + 'Longitude: ' + c, location.longitude)
        
            return location
        else:
            sprint(lr + "Could not find information for the given zip code")
    except Exception as e:
        sprint(lr + f"Error: {str(e)}")

def main():
    place_name = input(c + "Enter name of place: " + lr)
    location = get_location_details(place_name)
    logging.info(f"Queried place: {place_name}")

def main_with_place_name(place_name):
    location = get_location_details(place_name)
    logging.info(f"Queried place: {place_name}")

def zipper():
    code = input(g + "Enter zip code: ")
    get_zip_code_details(code)
    logging.info(f"Queried zip code: {code}")

def zipper_with_code(zip_code):
    get_zip_code_details(zip_code)
    logging.info(f"Queried zip code: {zip_code}")

def alti_longi():
    try:
        alti = input(ly + "Type Latitude: " + lc)
        logi = input(ly + "Type Longitude: " + ran)
        location = geolocator.reverse((alti, logi), language="en")
        if location:
            print(lr + f"Location address of {alti}, {logi} :")
            print(ran + location.address)
        else:
            sprint(lr + "Could not find information for the given coordinates")
    except Exception as e:
        sprint(lr + f"Error: {str(e)}")
    logging.info(f"Queried coordinates: {alti}, {logi}")

def alti_longi_with_coords(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language="en")
        if location:
            print(lr + f"Location address of {lat}, {lon} :")
            print(ran + location.address)
        else:
            sprint(lr + "Could not find information for the given coordinates")
    except Exception as e:
        sprint(lr + f"Error: {str(e)}")
    logging.info(f"Queried coordinates: {lat}, {lon}")

def calculate_distance():
    try:
        place1 = input(c + "Enter name of first place: " + lr)
        place2 = input(c + "Enter name of second place: " + lr)
        loc1 = get_location_details(place1)
        loc2 = get_location_details(place2)
        if loc1 and loc2:
            dist = distance.distance((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).km
            print("                             ")
            print(lg + f"Distance between {place1} and {place2} is {dist:.2f} km")
        else:
            sprint(lr + "Could not calculate distance due to missing location data")
    except Exception as e:
        sprint(lr + f"Error: {str(e)}")
    logging.info(f"Calculated distance between {place1} and {place2}")

def batch_process():
    try:
        print(g + "Batch Processing")
        print(r + "[1]" + c + " Enter multiple place names")
        print(r + "[2]" + c + " Enter multiple coordinates")
        print(r + "[3]" + c + " Enter multiple zip codes")
        choice = input(ran + "\nroot@GeoTool~ ")
        if choice == "1":
            places = input(c + "Enter place names separated by commas: " + lr).split(',')
            for place in places:
                main_with_place_name(place.strip())
        elif choice == "2":
            coords = input(c + "Enter coordinates separated by commas (lat1,lon1;lat2,lon2;...): " + lr).split(';')
            for coord in coords:
                alti, logi = coord.split(',')
                alti_longi_with_coords(alti.strip(), logi.strip())
        elif choice == "3":
            zips = input(c + "Enter zip codes separated by commas: " + lr).split(',')
            for code in zips:
                zipper_with_code(code.strip())
    except Exception as e:
        sprint(lr + f"Error: {str(e)}")

def visualize_on_map():
    try:
        place = input(c + "Enter name of place to visualize on map: " + lr)
        location = get_location_details(place)
        if location:
            map_location = folium.Map(location=[location.latitude, location.longitude], zoom_start=13)
            folium.Marker([location.latitude, location.longitude], popup=place).add_to(map_location)
            map_location.save('location_map.html')
            print(lg + f"Map for {place} saved as 'location_map.html'")
    except Exception as e:
        sprint(lr + f"Error: {str(e)}")

def fetch_weather():
    try:
        place = input(c + "Enter name of place to fetch weather: " + lr)
        location = get_location_details(place)
        if location:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={OWM_API_KEY}&units=metric"
            response = requests.get(weather_url)
            weather_data = response.json()
            if weather_data['cod'] == 200:
                print(lg + f"Weather in {place}:")
                print(lc + f"Temperature: {weather_data['main']['temp']}°C")
                print(lc + f"Weather: {weather_data['weather'][0]['description']}")
            else:
                sprint(lr + "Could not fetch weather information")
    except Exception as e:
        sprint(lr + f"Error: {str(e)}")

def signal_handler(sig, frame):
    print(lg + "\nProgram terminated successfully")
    banner2()
    sys.exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

no = ["n", "no"]
yes = ["y", "yes"]
cont = ""

while cont not in no:
    print(r + "[1]" + c + " Get details of a place")
    print(r + "[2]" + c + " With Latitude / Longitude")
    print(r + "[3]" + c + " Find details of a Zip Code")
    print(r + "[4]" + c + " Calculate distance between two places")
    print(r + "[5]" + c + " Batch process multiple inputs")
    print(r + "[6]" + c + " Visualize location on map")
    print(r + "[7]" + c + " Fetch weather information")
    print(r + "[8]" + c + " EXIT" + ly + "!!!")
    choice = input(ran + "\nroot@GeoTool~ ")
    
    if choice == "1":
        main()
    elif choice == "2":
        alti_longi()
    elif choice == "3":
        zipper()
    elif choice == "4":
        calculate_distance()
    elif choice == "5":
        batch_process()
    elif choice == "6":
        visualize_on_map()
    elif choice == "7":
        fetch_weather()
    elif choice == "8":
        sprint(ran + "Exiting tool...")
        banner2()
        sys.exit()
    else:
        sprint(ran + "Invalid Option!")
        sprint(ran + "Exiting tool...")
        banner2()
        sys.exit()

    cont = input(ran + "Continue?" + lr + " [y/n] " + ly)
    if cont in no:
        banner2()
        
    else: 
        banner2()
        
