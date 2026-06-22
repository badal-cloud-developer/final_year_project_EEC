import math

def haversine_distance_time(lat1, lon1, lat2, lon2, avg_speed_kmph=20):
    """
    Calculate the great-circle distance between two points 
    on the Earth (specified in decimal degrees) using the Haversine formula,
    and estimate the driving time.
    
    Parameters:
    lat1, lon1: Latitude and Longitude of Point A
    lat2, lon2: Latitude and Longitude of Point B
    avg_speed_kmph: Average driving speed in kilometers per hour
    
    Returns:
    distance_km: Distance in kilometers
    time_minutes: Estimated driving time in minutes
    """
    
    R = 6371  # Radius of Earth in km

    # Convert degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = R * c

    # Estimated time (in minutes)
    time_hours = distance_km / avg_speed_kmph
    time_minutes = time_hours * 60

    return round(distance_km, 2), round(time_minutes, 2)


from geopy.geocoders import Nominatim

def get_street_location(lat, lon):
    geolocator = Nominatim(user_agent="ride_sharing_app")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location and location.raw.get('address'):
        addr = location.raw['address']
        
        # Extract street info - main street/road
        street = addr.get('road') or addr.get('street') or addr.get('pedestrian') or addr.get('footway') or ''
        
        # Neighborhood or suburb or locality for more detail
        neighborhood = addr.get('neighbourhood') or addr.get('suburb') or addr.get('quarter') or addr.get('locality') or ''
        
        # City or town
        city = addr.get('city') or addr.get('town') or addr.get('village') or ''
        
        # Compose parts, skipping empty strings
        parts = [part for part in [street, neighborhood, city] if part]
        
        if parts:
            return ", ".join(parts)
        else:
            # fallback if no parts found
            return location.address.split(',')[0]  # first part of full address
        
    return "Location not found"


from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

def send_whatsapp_message(numbers, message_text):
    # Credentials (for production, store them securely!)
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    from_whatsapp_number = 'whatsapp:+14155238886'  # Twilio sandbox number

    results = []

    for number in numbers:
        to_whatsapp_number = f'whatsapp:+977{number}'  

        try:
            message = client.messages.create(
                body=message_text,
                from_=from_whatsapp_number,
                to=to_whatsapp_number
            )
            print(f"Sent to {number} - SID: {message.sid}, Status: {message.status}")
            results.append((number, message.sid, message.status))
        except Exception as e:
            print(f"Failed to send to {number}: {e}")
            results.append((number, None, str(e)))

    return results


