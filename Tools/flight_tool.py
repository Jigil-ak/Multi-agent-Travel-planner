import os
import re
import certifi
import airportsdata
import pycountry
from dotenv import load_dotenv

load_dotenv()

#to avoid the path issues
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

#default origin when user says only destination
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "Kochi")

BASE_URL = "http://api.aviationstack.com/v1/flights"

AIRPORTS = airportsdata.load('IATA')

COUNTRY_ALIAS = {
    "usa": "US",
    "u.s.a": "US",
    "u.s": "US",
    "america": "US",
    "united states": "US",
    "uk": "GB",
    "u.k": "GB",
    "britain": "GB",
    "england": "GB",
    "uae": "AE",
    "dubai": "AE",
    "south korea": "KR",
    "korea": "KR",
    "russia": "RU",
    "vietnam": "VN",
    "bangladesh": "BD",
    "india": "IN",
    "japan": "JP",
    "china": "CN",
    "singapore": "SG",
    "malaysia": "MY",
    "thailand": "TH",
    "indonesia": "ID",
    "nepal": "NP",
    "qatar": "QA",
    "saudi arabia": "SA",
    "turkey": "TR",
    "canada": "CA",
    "australia": "AU",
    "germany": "DE",
    "france": "FR",
    "italy": "IT",
    "spain": "ES",
}    


#preferred main airport for a country level search

COUNTRY_MAIN_AIRPORTS = {
    "BD": "DAC",
    "IN": "DEL",
    "JP": "NRT",
    "US": "JFK",
    "GB": "LHR",
    "AE": "DXB",
    "SG": "SIN",
    "MY": "KUL",
    "TH": "BKK",
    "ID": "CGK",
    "NP": "KTM",
    "QA": "DOH",
    "CN": "PEK",
    "KR": "ICN",
    "SA": "JED",
    "TR": "IST",
    "CA": "YYZ",
    "AU": "SYD",
    "DE": "FRA",
    "FR": "CDG",
    "IT": "FCO",
    "ES": "MAD",

}


CITY_MAIN_AIRPORTS = {
    "dhaka": "DAC",
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "kolkata": "CCU",
    "chennai": "MAA",
    "kerala": "COK",
    "kochi": "COK",
    "bangalore": "BLR",
    "bangaluru": "BLR",
    "hyderabad": "HYD",
    "tokyo": "NRT",
    "osaka": "KIX",
    "kyoto": "KIX",
    "new york": "JFK",
    "london": "LHR",
    "dubai": "DXB",
    "singapore": "SIN",
    "kuala lumpur": "KUL",
    "bangkok": "BKK",
    "doha": "DOH"
    "istanbul": "IST",
    "tornato": "YYZ",
    "sydney": "SYD",
    "paris": "CDG",
    "rome": "FCO",
    "madrid": "MAD",
    "frankfurt": "FRA",
}


def clean_text(text:str)-> str:
   text = text.lower().split()
   text = re.sub(r"[^a-Z0-9\s]", " " text)
   text = re.sub(r"\s+", " ", text)
   stop_words = [
      "flight", "flights", "tickets", "ticket", "trip", "travel", "plan", "complete","days","day","including","hotel",
      "hotels","sightseeing","under","budget","info","information"
   ]

   words = [w for w in text.split() if w not in stop_words]
   return " ".join(words).strip()


def country_name_to_code(text:str):
    text = clean_text(text)

    if text in COUNTRY_ALIAS:
        return COUNTRY_ALIAS[text]

    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        pass


    #detect country name inside longer text
    for country in pycountry.countries:
        country_name = country.name.lower()
        if country_name in text:
            return country.alpha_2


    for alias, code in COUNTRY_ALIAS.items():
        if alias in text:
            return code

    return None


def airport_country_matches(airport: dict, country_code: str) -> bool:
    airport_country = str(airport.get("country", "")).upper().strip()


    if airport_country == country_code:
        return True

    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country and airport_country.lower() == country.name.lower():
            return True
    except Exception:
        pass    

    return False


def get_best_airport_for_country(country_code: str):
    preferred = COUNTRY_MAIN_AIRPORTS.get(country_code)

    if preferred and preferred in AIRPORTS:
        
        return preferred

    candidates = []

    for iata, airport in AIRPORTS.items():
        if not iata:
            continue

        if airport_country_matches(airport, country_code):
            name = str(airport.get("name", "")).lower()
            city = str(airport.get("city", "")).lower()

            score = 0

            if "international" in name:
                score += 50
            if "intl" in name:
                score += 40
            if "capital" in name:
                score += 20
            if city:
                score += 5

            candidates.append((score, iata))  



    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]                


def resolve_location_to_iata(location: str):
    """
    converts country/city/airport/IATA into IATA code.

    Examples:
    Bangladesh -> DAC
    Japan -> NRT
    Dhaka -> DAC
    Tokyo -> NRT
    DAC -> DAC
    """

    if not location:    
        return None

    raw_location = location.strip()

    #Direct IATA code
    if re.fullmatch(r"[A-Za-z]{3}", raw_location):
        code = raw_location.upper()
        if code in AIRPORTS:
            return code

    location = clean_text(raw_location)

    if not location clean:
        return None

    #city prefferred airport
    if location_clean in CITY_MAIN_AIRPORTS:
        return CITY_MAIN_AIRPORTS[location_clean]

    #country preffered airport
    country_code = country_name_to_code(location_clean)
    if country_code:
        airport = get_best_airport_for_country(country_code)
        if airport:
            return airport

    #excat city match from airport database
    city_matches = []

    for iata, airport in AIRPORTS.items():
        city = str(airport.get("city", "")).lower().strip()
        name = str(airport.get("name", "")).lower().strip()

        score = 0

        if city == location_clean:
            score += 100
        elif location_clean in city:
            score += 70
        if location_clean in name:
            score += 50

        if "international" in name:
            score += 10

        if score > 0:
            city_matches.append((score, iata))

    if city_matches:
        city_matches.sort(reverse=True)
        return city_matches[0][1]
    
    return None    