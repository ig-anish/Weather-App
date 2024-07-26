import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

#Function to search weather for a city
def get_weather(city):
    API_key = "214ef7306e7521b819cdcf548893bad7"
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(URL)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")

    #phrase the response JSON to get weather info
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    #get the icon url and return all the weather info
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    #if city is found, unpack weather info
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city},{country}")

    #get weather icon image
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image = icon)
    icon_label.image = icon

    #update the temperature
    temperature_label.configure(text=f"Temperature: {temperature:.2f} C")
    description_label.configure(text=f"description: {description}")

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x420")

#Entry widget, to enter the city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

#Button widget, to search for weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

#To show the city name/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

#To show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

#To show the temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

#To show weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()