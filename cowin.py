
import requests 
from datetime import datetime, timedelta
import time

def get_slots_availability(age, pincode, dose):
    try: 
        age = int(age)
        pincode = int(pincode)
        dose = int(dose)
    except Exception as e:
        return "wrong-args"
    
    actual = datetime.today()
    actual_date = actual.strftime("%d-%m-%Y")

    counter = -1
    available_centers = []

    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, actual_date)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
    
    result = requests.get(URL, headers=header)

    if result.ok:
        response = result.json()
        for center in response["centers"]:
            # sessionCounter = 0
            for session in center["sessions"]:
                print(session)
                if (session["min_age_limit"] <= age and session["available_capacity_dose"+str(dose)] > 0 ) :
                    available_centers.append({})
                    available_centers[counter]["center_name"] = center["name"]
                    available_centers[counter]["center_address"] = center["address"]
                    available_centers[counter]["center_pincode"] = center["pincode"]
                    available_centers[counter]["center_id"] = center["center_id"]
                    available_centers[counter]["fee"] = center["fee_type"]
                    print(counter)
                    available_centers[counter]["session"] = []
                    available_centers[counter]["session"].append({})
                    available_centers[counter]["session"][-1]["date"] = session["date"]
                    available_centers[counter]["session"][-1]["vaccine"] = session["vaccine"]
                    available_centers[counter]["session"][-1]["available"] = session["available_capacity_dose"+str(dose)]
                    # sessionCounter = sessionCounter + 1  
                        
            # counter = counter + 1
    else:
        return "no-response"
        
    if not available_centers:
        return "no-slots"
    else:
        return available_centers

result = get_slots_availability("50", "600062", "2")
print(result)