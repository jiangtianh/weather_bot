import requests
import plotly.graph_objects as go
from datetime import datetime, timezone
from timezonefinder import TimezoneFinder
import pytz

WEATHER_API_KEY = #Your API Key

'''
Return the geolocation with the adderss passed in. Return the lat and lon in a list. 
PreCondition: The address must be valid, otherwise program would exit.
'''


def get_coordinates(address):
    base_url = f"https://geocode.maps.co/search"

    params = {
        "q": address
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if len(data) == 0:
        print("Geo API Error!")
        exit()

    lat = data[0]['lat']
    lon = data[0]['lon']
    address = data[0]["display_name"]

    current_time_zone = get_time_zone(lat, lon)

    return [lat, lon, current_time_zone, address]


''' 
Returns the weather data. Using openweathermap.org's api call. 
PreCondition: geo_data is a list with the first element being the lat, second being lon
'''


def get_weather_data(geo_data):
    base_url = f"https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": geo_data[0],
        "lon": geo_data[1],
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if not data:
        print("Weather API Error")
        exit()

    data = data["list"][:8]

    current_time_zone = geo_data[2]
    # Default Openweather api returns the time zone in UTC. Converting it to the timezone from the address passed in
    for forecast in data:
        utc_timestamp = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
        local_timestamp = utc_timestamp.replace(tzinfo=timezone.utc).astimezone(current_time_zone)
        forecast["local_time"] = local_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return data


def get_time_zone(lat, lon):
    tf = TimezoneFinder()
    current_time_zone = tf.timezone_at(lat=float(lat), lng=float(lon))
    time_zone = pytz.timezone(current_time_zone)

    return time_zone


def generate_plot(weather_data):
    timestamps = []
    temperature = []
    weather_conditions = []
    humidity = []

    for data in weather_data:
        timestamps.append(datetime.strptime(data["local_time"], "%Y-%m-%d %H:%M:%S"))
        temperature.append(data["main"]["temp"])
        weather_conditions.append(data["weather"][0]["description"])
        humidity.append(data["main"]["humidity"])

    fig = go.Figure()

    # Add temperature as a curved line
    fig.add_trace(go.Scatter(x=timestamps, y=temperature, mode='lines', line_shape='spline', name='Temperature'))

    # Add weather conditions as annotations at the bottom
    for i in range(len(timestamps)):
        fig.add_annotation(
            x=timestamps[i],
            y=min(temperature) - 1,
            text=weather_conditions[i],
            showarrow=False,
            font=dict(size=10)
        )

    # Add humidity as annotations at the bottom
    for i in range(len(timestamps)):
        fig.add_annotation(
            x=timestamps[i],
            y=min(temperature) - 2,
            text=f'Humidity: {humidity[i]}%',
            showarrow=False,
            font=dict(size=10)
        )

    fig.update_layout(
        title='Hourly Temperature Forecast',
        xaxis=dict(title='Time', side='top'),
        yaxis=dict(title='Temperature (°C)'),
        showlegend=False
    )

    width = 1200
    height = 800
    image_path = "forecast_plot.png"
    fig.write_image(image_path, width=width, height=height)
    return image_path


def generate_message(geo_data, weather_data):
    message = f"Hey there, It's The Weather Dude!!!\n\nHere is the weather forcasst for the next 24 hour of: {geo_data[3]}"
    print(weather_data)
    d = {}
    for data in weather_data:
        condition = data["weather"][0]["description"]
        if condition not in d:
            d[condition] = 1
        else:
            d[condition] += 1

    most = 0
    most_condition = ""
    for key in d:
        if d[key] > most:
            most = d[key]
            most_condition = key

    message += f"\n\n The weather condition through out the day is mostly going to be: {most_condition}"

    return message
