import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
from datetime import datetime

def get_weather(api_key, location):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return None

def get_forecast(api_key, location):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching forecast data: {e}")
        return None

def display_weather(data):
    if data:
        city = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()
        icon_code = data["weather"][0]["icon"]
        wind_speed = data["wind"]["speed"]
        sunrise_timestamp = data["sys"]["sunrise"]
        sunset_timestamp = data["sys"]["sunset"]

        # Update labels
        city_label.config(text=f"City: {city}")
        temp_label.config(text=f"Temperature: {temp}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        description_label.config(text=f"Weather: {description}")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")

        # Fetch and display weather icon
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            icon_response = requests.get(icon_url)
            icon_response.raise_for_status()
            icon_data = icon_response.content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo  # Keep a reference to prevent garbage collection
        except requests.exceptions.RequestException as e:
            print("Error fetching icon:", e)
            icon_label.config(image="")
            icon_label.image = None

        # Format sunrise and sunset times
        sunrise_time = datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M')
        sunset_time = datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M')
        sunrise_label.config(text=f"Sunrise: {sunrise_time}")
        sunset_label.config(text=f"Sunset: {sunset_time}")
    else:
        city_label.config(text="")
        temp_label.config(text="")
        humidity_label.config(text="")
        description_label.config(text="")
        wind_label.config(text="")
        sunrise_label.config(text="")
        sunset_label.config(text="")
        icon_label.config(image="")
        icon_label.image = None

def fetch_weather():
    location = location_entry.get()
    weather_data = get_weather(api_key, location)
    display_weather(weather_data)

def fetch_forecast():
    location = location_entry.get()
    forecast_data = get_forecast(api_key, location)
    if forecast_data:
        # Display forecast for the next 5 days (assuming the API provides data in 3-hour intervals)
        forecast_text = "5-Day Forecast:\n"
        for i in range(0, 5):
            timestamp = forecast_data["list"][i * 8]["dt"]
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            temp_min = forecast_data["list"][i * 8]["main"]["temp_min"]
            temp_max = forecast_data["list"][i * 8]["main"]["temp_max"]
            description = forecast_data["list"][i * 8]["weather"][0]["description"].capitalize()
            forecast_text += f"{date}: {description}, Min: {temp_min}°C, Max: {temp_max}°C\n"
        messagebox.showinfo("5-Day Forecast", forecast_text)
    else:
        messagebox.showwarning("Forecast", "No forecast data available.")

# Initialize Tkinter window
app = tk.Tk()
app.title("Weather App")

# API Key (Replace with your OpenWeatherMap API key)
api_key = "6969e586ab8a37d6cd71dea980c2f25d"

# GUI Elements
location_label = tk.Label(app, text="Enter city name or ZIP code:")
location_label.pack()

location_entry = tk.Entry(app)
location_entry.pack()

fetch_weather_button = tk.Button(app, text="Get Current Weather", command=fetch_weather)
fetch_weather_button.pack()

fetch_forecast_button = tk.Button(app, text="Get 5-Day Forecast", command=fetch_forecast)
fetch_forecast_button.pack()

city_label = tk.Label(app, text="")
city_label.pack()

temp_label = tk.Label(app, text="")
temp_label.pack()

humidity_label = tk.Label(app, text="")
humidity_label.pack()

description_label = tk.Label(app, text="")
description_label.pack()

wind_label = tk.Label(app, text="")
wind_label.pack()

sunrise_label = tk.Label(app, text="")
sunrise_label.pack()

sunset_label = tk.Label(app, text="")
sunset_label.pack()

icon_label = tk.Label(app)
icon_label.pack()

app.mainloop()
