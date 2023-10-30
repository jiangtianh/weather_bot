from apicaller import *
from telegram_api import *


ADDRESS = #Your address

geo_data = get_coordinates(ADDRESS)


weather_data = get_weather_data(geo_data)


image_path = generate_plot(weather_data)

message = generate_message(geo_data, weather_data)

send_message(message)
send_photo(image_path)

