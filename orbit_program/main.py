import ephem
from math import radians, degrees, cos, sin, asin, sqrt

from sense_hat import SenseHat
import os

import datetime
from time import sleep,strftime

import logging
import logzero
from logzero import logger


sense = SenseHat()


name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20032.27814909  .00006838  00000-0  13144-3 0  9998"
line2 = "2 25544  51.6480 305.8711 0003140 212.1605 227.0150 15.49157716210798"

#Here I calculate all the information on the position of the ISS
iss = ephem.readtle(name, line1, line2)

#Same thing but on a bigger object
sun = ephem.Sun()

#Twilight corner go here for more information
# https://www.timeanddate.com/astronomy/astronomical-twilight.html
twilight = 0


minutes = 178
measure = 0


b = (0, 100, 255)
o = (0,0,0)

def firts():
    logo = [
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, b, b, o, o, o,
    o, o, o, b, b, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    ]
    return logo

def second():
    logo = [
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, b, b, b, b, o, o,
    o, o, b, o, o, b, o, o,
    o, o, b, o, o, b, o, o,
    o, o, b, b, b, b, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    ]
    return logo

def third():
    logo = [
    o, o, o, o, o, o, o, o,
    o, b, b, b, b, b, b, o,
    o, b, o, o, o, o, b, o,
    o, b, o, o, o, o, b, o,
    o, b, o, o, o, o, b, o,
    o, b, o, o, o, o, b, o,
    o, b, b, b, b, b, b, o,
    o, o, o, o, o, o, o, o,
    ]
    return logo

def fourth():
    logo = [
    b, b, b, b, b, b, b, b,
    b, o, o, o, o, o, o, b,
    b, o, o, o, o, o, o, b,
    b, o, o, o, o, o, o, b,
    b, o, o, o, o, o, o, b,
    b, o, o, o, o, o, o, b,
    b, o, o, o, o, o, o, b,
    b, b, b, b, b, b, b, b,
    ]
    return logo
    
def fifth():
    logo = [
    o, o, o, o, o, o, o, o,
    o, b, b, b, b, b, b, o,
    o, b, o, o, o, o, b, o,
    o, b, o, o, o, o, b, o,
    o, b, o, o, o, o, b, o,
    o, b, o, o, o, o, b, o,
    o, b, b, b, b, b, b, o,
    o, o, o, o, o, o, o, o,
    ]
    return logo
    
def sixth():
    logo = [
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, b, b, b, b, o, o,
    o, o, b, o, o, b, o, o,
    o, o, b, o, o, b, o, o,
    o, o, b, b, b, b, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    ]
    return logo


def seventh ():
    logo = [
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, b, b, o, o, o,
    o, o, o, b, b, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    ]
    return logo


images = [firts, second, third, fourth, fifth, sixth, seventh ]

#this line is used to know which folder they are in
dir_path = os.path.dirname(os.path.realpath(__file__))
measure_file = dir_path + "/data01.csv"
formatter = logging.Formatter('%(levelname)s, %(message)s');
logzero.formatter(formatter)
logzero.logfile(measure_file)

def get_latlon(time = None):
    
    '''This function calculates the current position of the ISS'''
    
    if(time is None):
        iss.compute()
    else:
        iss.compute(time)
    
    print(iss.elevation)

    #print("ISS position lon {0} lat {1}".format(iss.sublong,iss.sublat))
    return (iss.sublat,iss.sublong,iss.elevation)


def isDayLight(lat,lon,time = None):

    '''I calculate the angle of the sun at the ground point of the ISS if the
    angle is greater than that of dusk I am hit by the sun '''

    observer = ephem.Observer()
    observer.lat = lat
    observer.long = lon
    observer.elevation = 0
    sun.compute(observer)

    sun_angle = degrees(sun.alt)


    return sun_angle,sun_angle > twilight


if __name__ == "__main__":
    #save in a variable when the program has started 
    start_time = datetime.datetime.now()
    #save in a variable the current time
    now_time = datetime.datetime.now()
    
    sense.set_imu_config(True, False, False)

    try:
        while (now_time < start_time + datetime.timedelta(minutes=minutes)):
            try:

                sense.set_pixels(images[measure % len(images)]())
                timer = strftime("%Y%m%d%H%M%S")
                lat,lon,height = get_latlon()
                angle,day = isDayLight(lat,lon)
                
                compass = sense.get_compass_raw()
                logger.info("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",measure,timer,lat,lon,height,angle,day,compass['x'],compass['y'],compass['z'])
                measure += 1
                now_time = datetime.datetime.now()
                sleep(1)
            except(Exception) as e:
                logger.error("An error occurred: " + str(e))
    except (KeyboardInterrupt, SystemExit):
        logger.debug("Kill signal received")
        
    
    sense.clear()
