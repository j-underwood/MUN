"""
General weather commands and weather display functions for the Weather application in MUN.

Note:
Use of global variable terminal throughout many functions, altered in Main and used to mark whether or not the runtime is in pure terminal mode.
"""

import requests
import datetime
import random

import Memory
import Utilities
import Screen

weather_name_icon_conversion = {
    'Day Sunny': 'cld',
    'Night Clear': 'cln',
    'Day Mostly Sunny': 'mld',
    'Day Partly Sunny': 'pld',
    'Night Mostly Clear': 'mln',
    'Night Partly Cloudy': 'pon',
    'Day Slight Chance Showers': 'mod',
    'Day Slight Chance Rain Showers': 'mod',
    'Night Slight Chance Showers': 'mon',
    'Night Slight Chance Rain Showers': 'mon',
    'Day Patchy Smoke': 'mld',
    'Night Patchy Smoke': 'mln',
    'Day Isolated Showers': 'mod',
    'Night Isolated Showers': 'mon',
    'Day Scattered Showers': 'mod',
    'Night Scattered Showers': 'mon',
    'Day Chance Showers': 'mod',
    'Night Chance Showers': 'mon'
}

#Day: Sunny, Mostly Sunny, Partly Sunny, Isolated Showers and Thunderstorms, Scattered Showers and Thunderstorms
#Night: Clear, Mostly Clear, Partly Cloudy, Isolated Showers and Thunderstorms, Scattered Showers and Thunderstorms ? Patchy Smoke

display_mode = 0

terminal = False

class Icon:
    """Class for creating visual representation of weather by using basic symbols such as numbers."""

    #symbol dictionary
    #Boxing symbols use the Q-W-E-A-D-Z-X-C square on Qwerty (A=D, W=X)
    symd = {"0": " ", "1": "░", "2": "▒", "3": "▓", "s": "●", "m": "○", "/": "/", "q": "┌", "w": "─", "e": "┐", "a": "│", "z": "└", "c": "┘"}

    def __init__(self, icon):
        """
        Initializes the class by setting the basic icon that will be used, which is a series of symbols in the 'Icon.symd' variable.
        Creates width and height variable based on the icon provided.

        icon: string (character of string in Icon.symd)
        """
        self.icon = icon
        #Icons should be rectangles
        self.width = len(icon.split('/')[0])
        self.height = len(icon.split('/'))

    def generate(self):
        """
        Takes the icon attribute of the instance of the class and runs through every character, using the symd to convert them to a visual representation of the symbol.
        Places a '?' character when there is no valid entry in the dictionary for the character.

        return: string
        """
        generated_icon = ""
        for pixel in self.icon:
            #generated pixel
            try:
                gp = self.symd[pixel]
            except:
                gp = "?"
            generated_icon += gp
        return generated_icon

    def gsplit(self):
        """
        Does 'Icon.generate' but splits the result by the given '/' characters.

        return: list
        """
        #generated split
        generated_icon = self.generate()
        #generated icon
        gi_split = generated_icon.split("/")
        return gi_split

    def box(self):
        """
        Boxes a non-generated Icon instance by putting symbols that represent different parts of the rim of squares.

        return: Icon
        """
        icon = "q" + ("w" * self.width) + "e/"
        #index
        for row in self.icon.split('/'):
            icon += "a" + row + "a/"
        icon += "z" + ("w" * self.width) + "c"
        return Icon(icon)

def weatherdisplay(size=2, location_name=None):
    """
    Generates the display to be used when putting weather information on the screen.

    Size 0: Smallest, fills up 1/3 of half the screen. 1: Medium, fills up 1/2 of half of the screen, 2: Largest, fills up an entire half of the screen
    Global Display Mode 0: Small displays focus on daily. 1: Small displays focus on hourly

    size: int
    location_name: string

    return: string (size=2) or list (size=0,1)

    *Opens memory.
    """

    global display_mode

    Memory.memory.open()
    if not location_name:
        location_name = getcurrentlocation()

    if not location_name == None:
        deleteoldweatherinformation()

        weather = getweathercache(location_name)
        message = 'Weather Unknown'
    else:
        #input('You have no current location so weather could not be found. (enter) ')
        message = 'Location Unknown'

        weather = None
    if not weather:
        return Screen.sizedependentmessage(message, size)
        #if size == 2:
            #return 'Weather Unknown' + Utilities.empty(size)[15:]
        #    return Utilities.centeredmessage('Weather Unknown', 101, 17)
        #elif size == 1:
        #    return Utilities.centeredmessage('Weather Unknown', 50, 17, True)
        #elif size == 0:
        #    return Utilities.centeredmessage('Weather Unknown', 33, 17, True)
        #else:
            #return ['Weather Unknown' + Utilities.empty(size)[0][15:]] + Utilities.empty(size)[1:]
    daily = weather['daily']
    hourly = weather['hourly']

    while True:
        try:
            daily_weather_name_list = [daily[index]['name'].center(15)[:15] for index in range(0,size+2)]
            daily_weather_icon_list = [createicon(weather_name_icon_conversion[composeshortforecast(daily[index])]).box().gsplit() for index in range(0,size+2)]
            daily_weather_information_list = [Utilities.conformtolistlength(Utilities.centerlist(Utilities.divideup(daily[index]['detailedForecast'], 13), 15), 9, 15, True) for index in range(0,size+2)]
        except IndexError:
            weather = getweather(location_name)
            daily = weather['daily']
            hourly = weather['hourly']
        else:
            break

    display_left = ""

    for name in daily_weather_name_list:
        display_left += name

    display_left += "/"

    for index in range(0,7):
        for icon_list in daily_weather_icon_list:
            display_left += icon_list[index]
        display_left += "/"

    for index in range(0,9):
        for information_list in daily_weather_information_list:
            display_left += information_list[index]
        display_left += "/"

    display_left = display_left[:-1]

    if size == 1 and not display_mode:
        display_left = display_left.split("/")
        display_left = Utilities.centerlist(display_left, 50)
        Memory.memory.close()
        return display_left
    elif size == 0 and not display_mode:
        display_left = display_left.split("/")
        display_left = Utilities.centerlist(display_left, 33)
        Memory.memory.close()
        return display_left

    if size == 0:
        display_right = " Hour" + "Forecast".center(28) + "/"
    elif size == 1:
        display_right = " Hour" + "Forecast".center(33) + "Temperature /"
    elif size == 2:
        display_right = " Hour" + (" " * 8) + "Forecast" + (" " * 8) + "Temperature /"

    timezone = gettimezone(location_name)
    now = datetime.datetime.now(timezone)
    current_hour = now.hour

    while True:
        try:
            if size == 0:
                #Old Behavior: hour_list = [(" " * 7) + Utilities.centerstring(str((index+current_hour) % 24), 2) + "  " for index in range(0,16)]
                hourly_weather_forecast_list = [Utilities.centerstringatindex(composeshortforecast(hourly[index]), 26, 12)[:26] + " " for index in range(0,16)]
            elif size == 1:
                hourly_weather_forecast_list = [Utilities.centerstringatindex(composeshortforecast(hourly[index]), 34, 14)[:34] for index in range(0,16)]
            elif size == 2:
                hourly_weather_forecast_list = [Utilities.centerstringatindex(composeshortforecast(hourly[index]), 25, 10)[:25] for index in range(0,16)]
            hour_list = ["  " + str((index+current_hour) % 24).center(2) + "  " for index in range(0,16)]
            hourly_weather_temperature_list = ["  " + str(hourly[index]['temperature']).center(3) + "     " for index in range(0,16)]
        except IndexError:
            weather = getweather(location_name)
            daily = weather['daily']
            hourly = weather['hourly']
        else:
            break

    for index in range(0,16):
        display_right += hour_list[index]
        display_right += hourly_weather_forecast_list[index]
        if size:
            display_right += hourly_weather_temperature_list[index]
        display_right += "/"

    if (size == 1 or size == 0) and display_mode:
        display_right = display_right.split("/")
        #Old behavior based on different if statements for each size
        #Old Behavior: display_right = Utilities.centerlist(display_right, 50)
        #Old Behavior: display_right = Utilities.centerlist(display_right, 33)
        Memory.memory.close()
        return display_right

    #Removing the last character ("/") or preventing it using an if statement in for 262 and for 287?

    dispaly_right = display_right[:-1]

    display = ""

    for index in range(0,17):
        display += display_left.split("/")[index]
        display += display_right.split("/")[index]

    Memory.memory.close()
    return display

def composeshortforecast(weather_list):
    """
    Takes a general weather dictionary and return back a shortened version of the short forecast for that weather dictionary.
    Works with the global weather_name_icon_conversion dictionary.

    weather_list: dict

    return: str
    """
    #short forecast
    sf = weather_list['shortForecast']
    #If there is no name, the weather_list provided is hourly
    if weather_list['name']:
        if weather_list['isDaytime']:
            time = 'Day '
        else:
            time = 'Night '
    else:
        time = ''
    if 'then' in sf:
        if len(sf.split(' then ')[0]) > len(sf.split(' then ')[1]):
            return time + sf.split(' then ')[1]
        else:
            return time + sf.split(' then ')[0]
    elif 'And' in sf:
        return time + sf.split(' And ')[0]
    else:
        return time + sf

def getcurrentlocation(open=False):
    """
    Gets the current location from memory, and if it can not be found, asks for it.
    Open is used when memory only needs to be opened once.

    open: bool

    return: str

    *Memory should be open.
    """
    #if open:
        #Memory.memory.open()
    try:
        current_location = Memory.mu.lfm(['currentlocation'], open)
    except:
        #if not terminal: Screen.inputscreen("Location")
        #current_location = input("Location: ")
        #Memory.mu.atm(['currentlocation'], current_location)
        #if open:
            #Memory.memory.close()
        return None
    #if open:
        #Memory.memory.close()
    return current_location

def getweathercache(location_name=None):
    """
    Returns weather information from user memory, giving the full weather dictionary.

    location_name: str

    return: dictionary

    *Memory should be open.
    """
    if not location_name:
        location_name = getcurrentlocation()
    try:
        weather_dictionary = Memory.mu.lfm(['locations',location_name,'weather'])
        return weather_dictionary
    except:
        #print(f"Error in getweathercache, no such location name {location_name} in memory.")
        return getweather(location_name)

def deleteoldweatherinformation(location_name=None):
    """
    Using the current time, removes old weather information from cache  to clear up memory.

    location_name: str

    *Memory should be open.
    """
    if not location_name:
        location_name = getcurrentlocation()

    weather = getweathercache(location_name)

    if not weather:
        return

    daily = weather['daily']
    hourly = weather['hourly']
    timezone = gettimezone(location_name)
    now = datetime.datetime.now(timezone)

    current_day = findoffset(now, daily)
    current_hour = findoffset(now, hourly)

    #Does this work if none of the weather data applies to the current time, therefore meaning all of it needs to be overwritten?
    if current_day == None or current_hour == None:
        getweather(location_name)
        return

    for _ in range(0,current_day):
        Memory.mu.rfm(['locations',location_name,'weather','daily',0])

    for _ in range(0,current_hour):
        Memory.mu.rfm(['locations',location_name,'weather','hourly',0])

def gettimezone(location_name=None):
    """
    Gets the current time zone from memory or asks about it if it is not recognized.

    location_name: str

    return: datetime.timezone

    *Memory should be open.
    """
    #Possible update: the lists that have the actual weather contain times with the offset
    if not location_name:
        location_name = getcurrentlocation()
    #coordinate dictionary
    cd = getcoordinatescache(location_name)
    x = cd['x']
    y = cd['y']

    #API link inputting the previously gotten coordinates
    weather_location = requests.get("https://api.weather.gov/points/"+str(y)+","+str(x))
    #Get the timezone name
    timezone_name = weather_location.json()['properties']['timeZone']
    #Checks if this timezone has a corresponding memory entry to give the offset and three letter name
    try:
        timezone_dictionary = Memory.memory.retrieve(['timezoneconversion',timezone_name])
    except:
        if not terminal: Screen.inputscreen("Timezone")
        while True:
            offset = input(f'What is the offset of {timezone_name} (+#/-#)? ')
            if offset.isdecimal():
                break
            #try:
            #    offset = int(offset)
            #except:
            #    continue
            #else:
            #    break
        while True:
            timezone_abbreviation = input(f'What is the abbreviation for the timezone {timezone_name} (AAA)? ')
            if len(timezone_abbreviation) == 3 and timezone_abbreviation.isalpha():
                break
        timezone_dictionary = {'offset': offset, 'timezone abbreviation': timezone_abbreviation}
        Memory.memory.store(['timezoneconversion',timezone_name], timezone_dictionary)

    timezone = datetime.timezone(datetime.timedelta(hours=timezone_dictionary['offset']), timezone_dictionary['timezone abbreviation'])

    return timezone

def getcoordinatescache(location_name=None):
    """
    Returns coordinate information from user memory, previously retrieved using the 'getcoordinates' function.

    location_name: str

    return: dictionary (x,y)

    *Memory should be open.
    """
    if not location_name:
        location_name = getcurrentlocation()
    try:
        coordinates = Memory.mu.lfm(['locations',location_name,'coordinates'])
        return coordinates
    except:
        return getcoordinates(location_name)

def findoffset(now, weather_information):
    """
    Finds the difference in between the weather information that is stored up and the current time.
    Used to determine which information from memory can be removed because it is outdated.

    now: datetime.datetime(.now)
    weather_information: dictionary (hourly or daily, not both)

    return: dictionary (with some information deleted)

    *Memory should be open.
    """
    for time_period,time_period_weather in enumerate(weather_information):
        start_time = time_period_weather['startTime']
        end_time = time_period_weather['endTime']
        #Convert to datetime objects
        start_time = datetime.datetime.fromisoformat(start_time)
        end_time = datetime.datetime.fromisoformat(end_time)
        if start_time < now < end_time:
            return time_period

def askaddress():
    """
    Asks the user their address information and compiles a dictionary of that information, while imposing restraints on what the user can enter.

    return: dictionary ('Street name', 'City', 'Zip code', 'State')
    """
    if not terminal: Screen.inputscreen("Address")
    while True:
        street_name = input("Street name (#### Direction Name Type): ")
        if street_name.count(" ") in [2, 3] and street_name[:4].isdecimal() and not (False in [street_name.split(" ")[index].isalpha() for index in range(1,len(street_name.split(" ")))]):
            break
    while True:
        city = input("City (Name): ")
        if city.isalpha():
            break
    while True:
        state = input("State (AA): ")
        if len(state) == 2 and state.isalpha():
            break
    while True:
        zip_code = input ("Zip code (#####): ")
        if len(zip_code) == 5 and zip_code.isdecimal():
            break
    return {'Street name': street_name, 'City': city, 'State': state, 'Zip code': zip_code}

def createicon(id):
    """
    Provides an icon based on the id provided that is randomly generated with different cloud levels.
    Works with the weather_name_icon_conversion global variable.

    id: str

    return: Icon
    """
    #c: completely, m: mostly, p: partly
    #l: clear, o: cloudy
    #d: day, n: night
    if id == 'cld':
        return Icon(curvecg(cloudgenerator(5, 13, 19, "s")))
    elif id == 'mld':
        return Icon(curvecg(cloudgenerator(5, 13, 39, "s")))
    elif id == 'pld':
        return Icon(curvecg(cloudgenerator(5, 13, 59, "s")))
    elif id == 'pod':
        return Icon(curvecg(cloudgenerator(5, 13, 79, "s")))
    elif id == 'mod':
        return Icon(curvecg(cloudgenerator(5, 13, 99, "s")))
    elif id == 'cln':
        return Icon(curvecg(cloudgenerator(5, 13, 19, "m")))
    elif id == 'mln':
        return Icon(curvecg(cloudgenerator(5, 13, 39, "m")))
    elif id == 'pln':
        return Icon(curvecg(cloudgenerator(5, 13, 59, "m")))
    elif id == 'pon':
        return Icon(curvecg(cloudgenerator(5, 13, 79, "m")))
    elif id == 'mon':
        return Icon(curvecg(cloudgenerator(5, 13, 99, "m")))

def cloudgenerator(height, length, level, extra=False):
    """
    Returns a random cloud, used for icon generation, with a possible extra symbol mixed in (like a sun or moon).

    height: int
    length: int
    level: int (1-99)
    extra: str (see Icon.symd, such as 'm' or 's')

    return: str
    """
    #Level is a number between and including 1 and 99 (though usually would be at least 75)
    cloud = ""
    for _ in range(height):
        for __ in range(length):
            random_int = random.randint(0, level)
            #cloud pixel
            cp = random_int/25
            #Remove the decimals
            cp = int(cp)
            cloud += str(cp)
        cloud += "/"
    cloud = cloud[0:len(cloud)-1]
    if extra:
        #random index
        ri = random.randrange(1, len(cloud))
        while "/" in cloud[ri-1:ri+2]:
            ri = random.randrange(1, len(cloud))
        cloud = Utilities.sir(cloud, ri, extra)
        cloud = Utilities.sir(cloud, ri-1, "0")
        cloud = Utilities.sir(cloud, ri+1, "0")
    return cloud

def curvecg(cg):
    """
    Curves a generated cloud, specifically for (height = 5, length = 13) though it could be used for other sizes, putting blank spaces on the corners.

    cg: str

    return: str
    """
    #cg: cloud generator
    #split cloud generator
    scg = cg.split("/")
    #last index (for the whole list)
    scgli = len(scg) - 1
    #index to use
    itu = 0
    #character whitelist
    cwl = ["0", "1", "2", "3"]
    for _ in range(2):
        scg[itu] = Utilities.sir(scg[itu], 0, "0", cwl)
        scg[itu] = Utilities.sir(scg[itu], 1, "0", cwl)
        scg[itu] = Utilities.sir(scg[itu], len(scg[itu])-1, "0", cwl)
        scg[itu] = Utilities.sir(scg[itu], len(scg[itu])-2, "0", cwl)
        itu = scgli
    itu = 1
    for _ in range(2):
        scg[itu] = Utilities.sir(scg[itu], 0, "0", cwl)
        scg[itu] = Utilities.sir(scg[itu], len(scg[itu])-1, "0", cwl)
        itu = scgli - 1
    return "/".join(scg)

def addaddress(location_name=None):
    """
    Asks address and stores the information given in the user's memory.

    location_name: str

    *Memory should be open.
    """
    if not location_name:
        location_name = getcurrentlocation()
    print(f"The following questions are for the location '{location_name}'.")
    location_address = askaddress()
    Memory.mu.atm(['locations',location_name,'address'], location_address)

def updatecurrentlocation(location_name, open=False):
    """
    Changes the current user's current location in memory.
    Open is used when memory only needs to be opened once.

    location_name: str
    open: bool

    *Memory should be open.
    """
    if open:
        Memory.memory.open()
    Memory.mu.atm(['currentlocation'], location_name)
    if open:
        Memory.memory.close()


def getcoordinates(location_name=None):
    """
    Gets the coordinates for the location name provided, then stores it in memory by location name that can later be used by the 'getcoordinatescache' function.

    location_name: str

    return: dict ('x','y')

    *Memory should be open.
    *Accesses an API (geocoding census.gov).
    *Access the Internet.
    """
    if not location_name:
        location_name = getcurrentlocation()
    while True:
        try:
            street_name = Memory.mu.lfm(['locations',location_name,'address','Street name']).replace(' ', '+')
            city = Memory.mu.lfm(['locations',location_name,'address','City'])
            state = Memory.mu.lfm(['locations',location_name,'address','State'])
            zip_code = Memory.mu.lfm(['locations',location_name,'address','Zip code'])
        except:
            addaddress(location_name)
            continue
        else:
            break
    #comma plus
    cp = "%2C+"
    #plus
    p = "+"
    #Formatted address
    address = street_name + cp + city + cp + state + p + zip_code

    #API link using Public AR and the 2010 Census formatted with json
    location = requests.get("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address="+address+"&benchmark=Public_AR_Census2010&format=json")
    #Get the coordinates from location
    coordinates = location.json()['result']['addressMatches'][0]['coordinates']
    #coordinate dictionary
    cd = {'x':coordinates['x'],'y':coordinates['y']}

    #Store the information
    Memory.mu.atm(['locations',location_name,'coordinates'], cd)
    return cd

def getweather(location_name=None):
    """
    Returns a dictionary containing hourly and daily weather in a dictionary and stores the information in memory for 'getweathercache' to access later.

    location_name: str

    return: dict ('daily','hourly')

    *Memory should be open.
    *Accesses an API (weather.gov).
    *Access the Internet.
    """
    if not location_name:
        location_name = getcurrentlocation()
    #coordinate dictionary
    cd = getcoordinatescache(location_name)
    x = cd['x']
    y = cd['y']

    #try:
    #API link inputting the previously gotten coordinates
    weather_location = requests.get("https://api.weather.gov/points/"+str(y)+","+str(x))
    #Gets the link for the hourly weather based on the coordinates that provides the actual weather information
    weather_hourly_link = weather_location.json()['properties']['forecastHourly']
    #Gets the link for the daily weather based on the coordinates that provides the actual weather information
    weather_daily_link = weather_location.json()['properties']['forecast']

    #API link received from weather.gov for hourly weather
    weather_hourly_full = requests.get(weather_hourly_link)
    #Get the hourly weather list from the json, starting hour retrieve using [0], second hour with [1], etc.
    try:
        weather_hourly = weather_hourly_full.json()["properties"]["periods"]
    except:
        input('Getting new weather is not possible at this moment, please try again later. (enter) ')
        return

    #API link received from weather.gov for daily weather
    weather_daily_full = requests.get(weather_daily_link)
    #Get the daily weather list from the json, starting day or night retrieve using [0], second period with [1], etc.
    weather_daily = weather_daily_full.json()['properties']['periods']

    weather_dictionary = {"hourly": weather_hourly, "daily": weather_daily}

    #Cache the information
    Memory.mu.atm(['locations',location_name,'weather'], weather_dictionary)
    #except KeyError:
        #print("KeyError in getweather.")
        #Old behavior was to return the cached weather
        #weather_dictionary = getweathercache(location_name)
    #except:
        #print("Other error in getweather.")

    return weather_dictionary
