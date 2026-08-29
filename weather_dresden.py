import requests #for the api datas
import weather_functions_dresden as wf
from datetime import datetime, timedelta #we need dates like "Today the 15.08.2026"
from zoneinfo import ZoneInfo
import os

#we need the different dates to make exact forecasts
today_us = datetime.now(ZoneInfo("Europe/Vienna")).date()
today = today_us.strftime("%d.%m.%Y")
tomorrow_us = today_us + timedelta(days=1)
tomorrow = tomorrow_us.strftime("%d.%m.%Y")
da_tomorrow_us = today_us + timedelta(days=2)
day_after_tomorrow = da_tomorrow_us.strftime("%d.%m.%Y")
today_api = today_us.isoformat()
tomorrow_api = tomorrow_us.isoformat()
da_tomorrow_api = da_tomorrow_us.isoformat()

url = "https://api.open-meteo.com/v1/forecast"
#url2 = "https://dataset.api.hub.geosphere.at/v1/datasets" 

parameter = {
    "latitude": 51.031580, #Dresden
    "longitude": 13.701534, 

    "hourly": ",".join([ #hourly forecast
        "temperature_2m",
        "apparent_temperature",
        "precipitation_probability",
        "weather_code",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
    ]),

    "minutely_15": ",".join([ 
        "weather_code",
        "wind_gusts_10m",
        ]),

    "daily": ",".join([ #forecast for tomorrow
        "temperature_2m_min",
        "temperature_2m_max",
        "apparent_temperature_min",
        "apparent_temperature_max",
        "precipitation_probability_max",
        "weather_code",
        "wind_speed_10m_max",
        "wind_direction_10m_dominant",
        "wind_gusts_10m_max",
    ]),

    "wind_speed_unit": "kmh", 
    "timezone": "Europe/Vienna",
    "forecast_days": 3 #until incl. the day after tomorrow
}

result = requests.get(url, params=parameter) 

if not result.ok: #debugging
    print(result.json()) #what happens when we let us show "result"
    result.raise_for_status() #successful would be 200

data = result.json() #the json file with all the data

times = data["hourly"]["time"]
temps = data["hourly"]["temperature_2m"]
minutely_times = data["minutely_15"]["time"]
weather_codes = data["hourly"]["weather_code"]
w_codes_minutely = data["minutely_15"]["weather_code"]
temp_min0 = data["daily"]["temperature_2m_min"][0] 
temp_max0 = data["daily"]["temperature_2m_max"][0] 
temp_min1 = data["daily"]["temperature_2m_min"][1] 
temp_max1 = data["daily"]["temperature_2m_max"][1] 
temp_min2 = data["daily"]["temperature_2m_min"][2] 
temp_max2 = data["daily"]["temperature_2m_max"][2] 
today_direction = data["daily"]["wind_direction_10m_dominant"][0]
tomorrow_direction = data["daily"]["wind_direction_10m_dominant"][1]
dat_direction = data["daily"]["wind_direction_10m_dominant"][2]
today_winddirection = wf.direction_function(today_direction)
tomorrow_winddirection = wf.direction_function(tomorrow_direction)
da_tomorrow_winddirection = wf.direction_function(dat_direction)
speed_today = data["daily"]["wind_speed_10m_max"][0]
speed_tomorrow = data["daily"]["wind_speed_10m_max"][1]
speed_da_tomorrow = data["daily"]["wind_speed_10m_max"][2]
wind_speed_today = wf.speed_function(speed_today)
wind_speed_tomorrow = wf.speed_function(speed_tomorrow)
wind_speed_da_tomorrow = wf.speed_function(speed_da_tomorrow)
gusts = data["minutely_15"]["wind_gusts_10m"]
gusts_max_today = data["daily"]["wind_gusts_10m_max"][0]
gusts_max_tomorrow = data["daily"]["wind_gusts_10m_max"][1]
gusts_max_da_tomorrow = data["daily"]["wind_gusts_10m_max"][2]

#TEMPERATURE-PART------------------------------------------------------------

#today

wf_morning, wf_late_morning, wf_noon, wf_afternoon, wf_evening = wf.temperature_function(times, temps, today_api)

morning = wf.average_values(wf_morning)
late_morning = wf.average_values(wf_late_morning)
noon = wf.average_values(wf_noon)
afternoon = wf.average_values(wf_afternoon)
evening = wf.average_values(wf_evening)

#tomorrow

wf_morning_tom, wf_late_morning_tom, wf_noon_tom, wf_afternoon_tom, wf_evening_tom = wf.temperature_function(times, temps, tomorrow_api)

morning1 = wf.average_values(wf_morning_tom)
late_morning1 = wf.average_values(wf_late_morning_tom)
noon1 = wf.average_values(wf_noon_tom)
afternoon1 = wf.average_values(wf_afternoon_tom)
evening1 = wf.average_values(wf_evening_tom)

#day after tomorrow

wf_morning_da_tom, wf_late_morning_da_tom, wf_noon_da_tom, wf_afternoon_da_tom, wf_evening_da_tom = wf.temperature_function(times, temps, da_tomorrow_api)

morning2 = wf.average_values(wf_morning_da_tom)
late_morning2 = wf.average_values(wf_late_morning_da_tom)
noon2 = wf.average_values(wf_noon_da_tom)
afternoon2 = wf.average_values(wf_afternoon_da_tom)
evening2 = wf.average_values(wf_evening_da_tom)

#THUNDERSTORM PROBABILITY----------------------------------------------------

#Today

periods_raw = wf.thunderstorm_times(wf.thunderstorm_forecast(minutely_times,
                                               w_codes_minutely,
                                               today_api))

periods_formatted = []

for start, end in periods_raw:
    periods_formatted.append(f"von {start} bis {end} Uhr")

#Tomorrow

periods_raw1 = wf.thunderstorm_times(wf.thunderstorm_forecast(minutely_times,
                                               w_codes_minutely,
                                               tomorrow_api))

periods_formatted1 = []

for start, end in periods_raw1:
    periods_formatted1.append(f"von {start} bis {end} Uhr")

#Day after tomorrow

periods_raw2 = wf.thunderstorm_times(wf.thunderstorm_forecast(minutely_times,
                                               w_codes_minutely,
                                               da_tomorrow_api))

periods_formatted2 = []

for start, end in periods_raw2:
    periods_formatted2.append(f"von {start} bis {end} Uhr")

#RAIN and SNOW---------------------------------------------------------------

#Today

rain_periods_raw = wf.rainfall_times(wf.rainfall_forecast(minutely_times,
                                               w_codes_minutely,
                                               today_api))

rain_periods_formatted = []

for start, end, rainfall_type in rain_periods_raw:
    rain_periods_formatted.append(f" von {start} bis {end} Uhr")

#Tomorrow

rain_periods_raw1 = wf.rainfall_times(wf.rainfall_forecast(minutely_times,
                                               w_codes_minutely,
                                               tomorrow_api))

rain_periods_formatted1 = []

for start, end, rainfall_type in rain_periods_raw1:
    rain_periods_formatted1.append(f" von {start} bis {end} Uhr")

#Day after tomorrow

rain_periods_raw2 = wf.rainfall_times(wf.rainfall_forecast(minutely_times,
                                               w_codes_minutely,
                                               da_tomorrow_api))

rain_periods_formatted2 = []

for start, end, rainfall_type in rain_periods_raw2:
    rain_periods_formatted2.append(f" von {start} bis {end} Uhr")

#WIND GUSTS -----------------------------------------------------------------

#Today

gusts_periods_raw = wf.wind_gusts_times(wf.wind_gusts_function(minutely_times,
                                               gusts,
                                               today_api))

gusts_periods_formatted = []

for start, end in gusts_periods_raw:
    gusts_periods_formatted.append(f" von {start} bis {end} Uhr")

#Tomorrow

gusts_periods_raw1 = wf.wind_gusts_times(wf.wind_gusts_function(minutely_times,
                                               gusts,
                                               tomorrow_api))

gusts_periods_formatted1 = []

for start, end in gusts_periods_raw1:
    gusts_periods_formatted1.append(f" von {start} bis {end} Uhr")

#Day after Tomorrow

gusts_periods_raw2 = wf.wind_gusts_times(wf.wind_gusts_function(minutely_times,
                                               gusts,
                                               da_tomorrow_api))

gusts_periods_formatted2 = []

for start, end in gusts_periods_raw2:
    gusts_periods_formatted2.append(f" von {start} bis {end} Uhr")

#OUTPUT-----------------------------------------------------------------------

#not as a function, for readability

print("\nTemperaturen heute: ")
print(f"Es wird zwischen {temp_min0} und {temp_max0} Grad.")
print(f"Morgens: {morning} Grad, vormittags: "
      f"{late_morning} Grad, mittags: {noon} Grad, \nnachmittags: "
      f"{afternoon} Grad, abends: {evening} Grad")
print("\nGewittergefahr:")
if periods_formatted:
    thunderstorm_message = ("Gewittergefahr "+ " und".join(periods_formatted)+ ".")
else:
    thunderstorm_message = "Heute besteht keine Gewittergefahr."
print(thunderstorm_message)
print("\nVoraussichtlicher Niederschlag:")
if rain_periods_formatted:
    rain_message = (rainfall_type + " und".join(rain_periods_formatted) + ".")
else:
    rain_message = "Kein Niederschlag heute."
print(rain_message)
if wind_speed_today == "0":
    print("\nWind:\nEs ist windstill.")
else:
    print(f"\nWind:\n{wind_speed_today} {today_winddirection}.\n"
          f"Windböen bis zu {gusts_max_today} km/h, am stärksten" + 
          " und".join(gusts_periods_formatted) + ".")

#tomorrow

print("\nTemperaturen morgen: ")
print(f"Es wird zwischen {temp_min1} und {temp_max1} Grad.")
print(f"Morgens: {morning1} Grad, vormittags: "
      f"{late_morning1} Grad, mittags: {noon1} Grad, \nnachmittags: "
      f"{afternoon1} Grad, abends: {evening1} Grad")
print("\nGewittergefahr:")
if periods_formatted1:
    print("Gewittergefahr "+" und".join(periods_formatted1) + ".")
else:
    print("Morgen besteht keine Gewittergefahr.")
print("\nVoraussichtlicher Niederschlag:")
if rain_periods_formatted1:
    rain_message1 = (rainfall_type + " und".join(rain_periods_formatted1) + ".")
else:
    rain_message1 = "Kein Niederschlag morgen."
print(rain_message1)
if wind_speed_tomorrow == "0":
    print("\nWind:\nEs ist windstill.")
else:
    print(f"\nWind:\n{wind_speed_tomorrow} {tomorrow_winddirection}.\n"
          f"Windböen bis zu {gusts_max_tomorrow} km/h, am stärksten" + 
            " und".join(gusts_periods_formatted1) + ".")

#day after tomorrow

print("\nTemperaturen übermorgen: ")
print(f"Es wird zwischen {temp_min2} und {temp_max2} Grad.")
print(f"Morgens: {morning2} Grad, vormittags: "
      f"{late_morning2} Grad, mittags: {noon2} Grad, \nnachmittags: "
      f"{afternoon2} Grad, abends: {evening2} Grad")
print("\nGewittergefahr:")
if periods_formatted2:
    print("Gewittergefahr "+" und".join(periods_formatted2) + ".")
else:
    print("Übermorgen besteht keine Gewittergefahr.")
print("\nVoraussichtlicher Niederschlag:")
if rain_periods_formatted2:
    rain_message2 = (rainfall_type + " und".join(rain_periods_formatted2) + ".")
else:
    rain_message2 = "Kein Niederschlag übermorgen."
print(rain_message2)
if wind_speed_da_tomorrow == "0":
    print("\nWind:\nEs ist windstill.")
else:
    print(f"\nWind:\n{wind_speed_da_tomorrow} {da_tomorrow_winddirection}.\n"
          f"Windböen bis zu {gusts_max_da_tomorrow} km/h, am stärksten" + 
           " und".join(gusts_periods_formatted2) + ".")

#TELEGRAM channel message

today_message = (
    f"Wetter heute, den {today}:\n\n"
    "Temperaturen: "
    f"Es wird zwischen {temp_min0} und {temp_max0} Grad.\n\n"
    f"Morgens: {morning} Grad, vormittags: "
    f"{late_morning} Grad, mittags: {noon} Grad, \nnachmittags: "
    f"{afternoon} Grad, abends: {evening} Grad\n\n"
    f"Gewittergefahr: {thunderstorm_message}\n\n"
    f"Niederschlag: {rain_message}\n\n"
    f"Wind: {wind_speed_today} {today_winddirection}\n"
    f"Windböen bis zu {gusts_max_da_tomorrow} km/h, am stärksten" + 
     " und".join(gusts_periods_formatted2) + ".")

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

if bot_token and channel_id:
    telegram_result = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        data={
            "chat_id": channel_id,
            "text": today_message
        }
    )

    telegram_result.raise_for_status()
