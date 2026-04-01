from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "3f0a484d3c9ccbd81dc10f3225581b66")


def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return None

    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "desc": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "main": data["weather"][0]["main"].lower()
    }


def fetch_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != "200":
        return []

    forecast_list = []

    for i in range(0, 40, 8):
        item = data["list"][i]
        forecast_list.append({
            "date": item["dt_txt"].split(" ")[0],
            "temp": item["main"]["temp"],
            "desc": item["weather"][0]["description"],
            "main": item["weather"][0]["main"].lower()
        })

    return forecast_list


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = []

    if request.method == "POST":
        city = request.form.get("city")
        weather = fetch_weather(city)
        forecast = fetch_forecast(city)

    return render_template("index.html", weather=weather, forecast=forecast)


if __name__ == "__main__":
    app.run(debug=True)




