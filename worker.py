import requests
import psycopg2
import psycopg2.extras
import logging
from datetime import datetime


def fetch_data():
    api_tokens = 'a6056364055960a0'
    url = 'http://api.wunderground.com/api/' + api_tokens + '/conditions/q/CA/San_Francisco.json'
    r = requests.get(url).json()

    data = r['current_observation']
    location = data['observation_location']['full']
    weather = data['weather']
    wind_str = data['wind_string']
    temp = data['temp_c']
    humidity = data['relative_humidity']
    precip = data['precip_1hr_metric']
    icon_url = data['icon_url']
    observation_time = data['observation_time_rfc822']

    #open db
    try:
        conn = psycopg2.connect(dbname='weather', user='postgres', host='localhost', password='root@123')
        print("Open db successfully")
    except:
        print(datetime.now(),"Unable to connect to the database")
        logging.exception("Unable to open database")
        return
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #write data to database
    cur.execute("""INSERT INTO station_reading(location,weather,wind_str,temp,humidity,precip,icon_url,observation_time)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (location,weather,wind_str,temp,humidity,precip,icon_url,observation_time))

    conn.commit()
    cur.close()
    conn.close()

    print("data written:",datetime.now())


fetch_data()