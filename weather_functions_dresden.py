from statistics import median

#--- Temperature Functions

def temperature_function(times, temps, target_date):
    wf_morning = []
    wf_late_morning = []
    wf_noon = []
    wf_afternoon = []
    wf_evening = []

    for time, temp in zip(times, temps):
        if time.startswith(target_date):
            hour_raw = time[11:13]
            hour = int(hour_raw)

            if hour in range(0, 6):
                wf_morning.append(temp)
            elif hour in range(6, 11):
                wf_late_morning.append(temp)
            elif hour in range(11, 14):
                wf_noon.append(temp)
            elif hour in range(14, 19):
                wf_afternoon.append(temp)
            else:
                wf_evening.append(temp)

    return wf_morning, wf_late_morning, wf_noon, wf_afternoon, wf_evening


#---- Average values 

def average_values(werte):
    average_raw = sum(werte) / len(werte)
    average = round(average_raw, 1)
    return average

#----- Start and end minutes for the time periods in question & breaks

def calculate_total_minutes(minutely_times):
    total_minutes = []
    minutes_raw = []

    for minutely_time in minutely_times:
    
        minutes_raw_calcu = minutely_time[11:16]
        minutes_raw.append(minutes_raw_calcu)

        hour, minute = map(int, minutes_raw_calcu.split(":")) 
        total_minutes_calcu = (hour * 60) + minute
        total_minutes.append(total_minutes_calcu)

    return total_minutes, minutes_raw

def calculate_end_minutes(total_minute):
    end_minutes = total_minute + 15
    end_hour = end_minutes // 60
    end_minute = end_minutes % 60
    end = f"{end_hour:02d}:{end_minute:02d}"
    return end


#---- Probability for a thunderstorm

def thunderstorm_forecast(minutely_times, w_codes_minutely, target_date):
    total_minutes_list, minutes_raw_list = calculate_total_minutes(minutely_times)
    thunderstorm_periods = []

    for minutely_time, code, total_minutes, minutes_raw in zip(minutely_times, w_codes_minutely, total_minutes_list, minutes_raw_list):
        if minutely_time.startswith(target_date):
            if code in (95, 96, 99):
                thunderstorm_periods.append([minutes_raw, total_minutes])
    return thunderstorm_periods

def thunderstorm_times(thunderstorm_forecast):
    if not thunderstorm_forecast:
        return []
    
    start = thunderstorm_forecast[0][0]
    previous_minutes = thunderstorm_forecast[0][1]
    end = calculate_end_minutes(previous_minutes)
    from_to_periods = []

    for time, total_minute in thunderstorm_forecast[1:]:
        difference = total_minute - previous_minutes

        if difference > 15:
            from_to_periods.append([start, end])
            start = time

        end = calculate_end_minutes(total_minute)
        previous_minutes = total_minute

    from_to_periods.append([start, end])

    return from_to_periods

#RAIN & SNOW

def rainfall_forecast(minutely_times, w_codes_minutely, target_date):
    total_minutes_list, minutes_raw_list = calculate_total_minutes(minutely_times)
    rainfall_periods = []

    for minutely_time, code, total_minutes, minutes_raw in zip(minutely_times, w_codes_minutely, total_minutes_list, minutes_raw_list):
        if minutely_time.startswith(target_date):
            if code in(51,53,55):
                rainfall_type = "Nieselregen, am wahrscheinlichsten"
            elif code in(56,57,66):
                rainfall_type = "Eisregen, am wahrscheinlichsten"
            elif code == 67:
                rainfall_type = "starker Eisregen, am wahrscheinlichsten"
            elif code in(61, 63, 80, 81):
                rainfall_type = "Regen, am wahrscheinlichsten"
            elif code in(65, 82):
                rainfall_type = "starker Regen, am wahrscheinlichsten"
            elif code in(71,73,77,85):
                rainfall_type = "Schneefall, am wahrscheinlichsten"
            elif code in(75,86):
                rainfall_type = "starker Schneefall, am wahrscheinlichsten"
            else:
                continue

            rainfall_periods.append([minutes_raw, total_minutes, rainfall_type])
    return rainfall_periods

def rainfall_times(rainfall_forecast):
    if not rainfall_forecast:
        return []

    start = rainfall_forecast[0][0]
    previous_minutes = rainfall_forecast[0][1]
    end = calculate_end_minutes(previous_minutes)
    previous_rainfall_type = rainfall_forecast[0][2]
    from_to_periods = []

    for time, total_minute, rainfall_type in rainfall_forecast[1:]:
        difference = total_minute - previous_minutes

        if difference > 15 or rainfall_type != previous_rainfall_type:
            from_to_periods.append([start, end, previous_rainfall_type])
            start = time

        end = calculate_end_minutes(total_minute)
        previous_minutes = total_minute
        previous_rainfall_type = rainfall_type
        
    from_to_periods.append([start, end, previous_rainfall_type])
        
    return from_to_periods

#WIND------------------------------------------------------------------------

def direction_function(direction):
    direction = float(direction)
    if direction >= 337.5 or direction < 22.5:
        return "Norden"
    elif direction < 67.5:
        return "Nordosten"
    elif direction < 112.5:
        return "Osten"
    elif direction < 157.5:
        return "Südosten"
    elif direction < 202.5:
        return "Süden"
    elif direction < 247.5:
        return "Südwesten"
    elif direction < 292.5:
        return "Westen"
    elif direction < 337.5:
        return "Nordwesten"

#---- Function for wind speed -------------------------------------------------------

def speed_function(speed):
    if speed < 1:
        return "0"
    elif speed < 6:
        return f"Ein leiser Zug mit {speed} km/h aus"
    elif speed < 12:
        return f"Eine leichte Brise mit {speed} km/h aus"
    elif speed < 20:
        return f"Ein schwacher Wind mit {speed} km/h aus"
    elif speed < 29:
        return f"Ein mäßiger Wind mit {speed} km/h aus"
    elif speed < 39:
        return f"Ein frischer Wind mit {speed} km/h aus"
    elif speed < 50:
        return f"Ein starker Wind mit {speed} km/h aus"
    elif speed < 62:
        return f"Ein steifer Wind mit {speed} km/h aus"
    elif speed < 75:
        return f"Ein stürmischer Wind mit {speed} km/h aus"
    elif speed < 89:
        return f"Sturm mit {speed} km/h aus"
    elif speed < 103:
        return f"Schwerer Sturm mit {speed} km/h aus"
    elif speed < 118:
        return f"Ein orkanartiger Sturm mit {speed} km/h aus"
    else:
        return f"Ein Orkan mit {speed} km/h aus"

#---- Function for wind gusts -----------------------------------------------

def wind_gusts_function(minutely_times, gusts, target_date):
    total_minutes_list, minutes_raw_list = calculate_total_minutes(minutely_times)
    gusts_target_date = []
    wind_gusts_periods = []

    for minutely_time, gust, in zip(minutely_times, gusts):
        if minutely_time.startswith(target_date):
            gusts_target_date.append(gust)

    if not gusts_target_date:
        return []

    gusts_median = median(gusts_target_date)

    for minutely_time, gust, total_minutes, minutes_raw in zip(minutely_times, gusts, total_minutes_list,minutes_raw_list):
        if minutely_time.startswith(target_date):
            if gust > gusts_median:
                wind_gusts_periods.append([minutes_raw, total_minutes])
    return wind_gusts_periods

def wind_gusts_times(gusts_forecast):
    if not gusts_forecast:
        return []
    
    start = gusts_forecast[0][0]
    previous_minutes = gusts_forecast[0][1]
    end = calculate_end_minutes(previous_minutes)
    from_to_periods = []

    for time, total_minute in gusts_forecast[1:]:
        difference = total_minute - previous_minutes

        if difference > 15:
            from_to_periods.append([start, end])
            start = time

        end = calculate_end_minutes(total_minute)
        previous_minutes = total_minute

    from_to_periods.append([start, end])

    return from_to_periods