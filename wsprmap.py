#!/usr/bin/python3

import arrow
import datetime
import sys
import os
import pandas as pd

#from gmplot import gmplot
# might not use gmplot

import plotly.offline as py

from hamlocation import HamLocation
#
# FIRST TASK - PARSE CSV FILE
# 


pd.set_option('display.max_rows', 30000)
pd.set_option('display.height', 30000)

FILE = 'sampledata.txt'
#FILE = 'N6QB-wsprspots'
DF = pd.read_csv(FILE, sep=',', header=None, names=['SPOTID','TIMESTAMP','REPORTER','REPGRID','SNR','FREQ', \
        'CALL','GRID','POWER','DRIFT','DISTANCE','AZIMUTH','BAND','VERSION','CODE'])

# these times are necessary to define a range
start = datetime.datetime(2018, 5, 1)
end = datetime.datetime(2018, 5, 2)

i = 1
for r in arrow.Arrow.range('hour',start, end):
    
    st = arrow.get(r).span('hour') 
    (tstart, tend) = st
    
    i_start = int(tstart.timestamp)
    i_end = int(tend.timestamp)
    print("###",r, tstart.timestamp, tend.timestamp,"###")
    temp = DF[DF['TIMESTAMP'].between(i_start, i_end, inclusive=True)]
    hourly_map = temp[['REPORTER','REPGRID','FREQ']]
    # need some empty dataframes
    df80 = pd.DataFrame(columns=['CALL','GRID','FREQ','LAT','LON'])
    df40 = pd.DataFrame(columns=['CALL','GRID','FREQ','LAT','LON'])
    df20 = pd.DataFrame(columns=['CALL','GRID','FREQ','LAT','LON'])
    df15 = pd.DataFrame(columns=['CALL','GRID','FREQ','LAT','LON'])
    df10 = pd.DataFrame(columns=['CALL','GRID','FREQ','LAT','LON'])
    for index,row in hourly_map.iterrows():

        h = HamLocation()
        where = h.getCenter(row['REPGRID'])
        (lat, lon) = where
        band = round(float(row['FREQ']))
        if band == 4:
            color = '#C71585'
        elif band == 7:
            color = '#000080'
            entry = pd.DataFrame([[row['REPORTER'],row['REPGRID'],row['FREQ'],lat,lon]],columns=['CALL','GRID','FREQ','LAT','LON'])
            df40 = pd.concat([df40,entry], ignore_index=True)
        elif band == 14:
            color = '#FFFF00'
        elif band == 21:
            color = '#CD853F'
        elif band == 28:
            color = '#FA8072'
        print(row['REPORTER'], row['REPGRID'], band, color, lat, lon) 

    # now we need to build maps for each band/hr
    scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

    data = [ dict(
		type = 'scattergeo',
		locationmode = 'USA-states',
		lon = df40['LON'],
		lat = df40['LAT'],
		text = df40['CALL'],
		mode = 'markers',
		marker = dict(
		size = 8,
		opacity = 0.8,
		reversescale = True,
		autocolorscale = False,
		symbol = 'square',
		line = dict(
			width=1,
			color='rgba(102, 102, 102)'
		),
		colorscale = scl,
		cmin = 0,
		#color = df['cnt'],
		#cmax = df['cnt'].max(),
		#colorbar=dict(
		#	title="Incoming flightsFebruary 2011"
		#)
		))]

    layout = dict(
		title = 'WSPR Data Mapping',
		colorbar = True,
		geo = dict(
		scope='usa',
		projection=dict( type='albers usa' ),
		showland = True,
		landcolor = "rgb(250, 250, 250)",
		subunitcolor = "rgb(217, 217, 217)",
		countrycolor = "rgb(217, 217, 217)",
		countrywidth = 0.5,
		subunitwidth = 0.5
		),
	)
	
    fname = "map"+str(i) + ".html"
    print(fname)
    fig = dict( data=data, layout=layout )
    py.plot( fig, validate=False, filename=fname ) 
    print("#######################################################################")
    i += 1
