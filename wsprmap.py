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
end = datetime.datetime(2018, 5, 16)

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

    data10 = []
    data15 = []
    data20 = []
    data40 = []
    data80 = []

    scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

    for index,row in hourly_map.iterrows():

        h = HamLocation()
        where = h.getCenter(row['REPGRID'])
        (lat, lon) = where
        band = round(float(row['FREQ']))
        if band == 4:
            color = '#C71585'
            entry = pd.DataFrame([[row['REPORTER'],row['REPGRID'],row['FREQ'],lat,lon]],columns=['CALL','GRID','FREQ','LAT','LON'])
            df80 = pd.concat([df80,entry], ignore_index=True)
            data80 = [ dict(
                type = 'scattergeo',
                name = "80m",
                locationmode = 'USA-states',
                lon = df80['LON'],
                lat = df80['LAT'],
                text = df80['CALL'] +" "+ df80['GRID'],
                mode = 'markers',
                marker = dict(
                size = 8,
                color = 'rgba(199,21,133)',
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
                ))]
        elif band == 7:
            color = '#000080'
            entry = pd.DataFrame([[row['REPORTER'],row['REPGRID'],row['FREQ'],lat,lon]],columns=['CALL','GRID','FREQ','LAT','LON'])
            df40 = pd.concat([df40,entry], ignore_index=True)
            data40 = [ dict(
                type = 'scattergeo',
                name = "40m",
                locationmode = 'USA-states',
                lon = df40['LON'],
                lat = df40['LAT'],
                text = df40['CALL'] +" "+ df40['GRID'],
                mode = 'markers',
                marker = dict(
                size = 8,
                color = 'rgba(60,126,183)',
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
                ))]
        elif band == 14:
            color = '#FFFF00'
            entry = pd.DataFrame([[row['REPORTER'],row['REPGRID'],row['FREQ'],lat,lon]],columns=['CALL','GRID','FREQ','LAT','LON'])
            df20 = pd.concat([df20,entry], ignore_index=True)
            data20 = [ dict(
                type = 'scattergeo',
                name = "20m",
                locationmode = 'USA-states',
                lon = df20['LON'],
                lat = df20['LAT'],
                text = df20['CALL'] +" "+ df20['GRID'],
                mode = 'markers',
                marker = dict(
                size = 8,
                color = 'rgba(255,255,0)',
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
                ))]
        elif band == 21:
            color = '#CD853F'
            entry = pd.DataFrame([[row['REPORTER'],row['REPGRID'],row['FREQ'],lat,lon]],columns=['CALL','GRID','FREQ','LAT','LON'])
            df15 = pd.concat([df15,entry], ignore_index=True)
            data15 = [ dict(
                type = 'scattergeo',
                name = "15m",
                locationmode = 'USA-states',
                lon = df15['LON'],
                lat = df15['LAT'],
                text = df15['CALL'] +" "+ df15['GRID'],
                mode = 'markers',
                marker = dict(
                size = 8,
                color = 'rgba(205,133,63)',
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
                ))]
        elif band == 28:
            color = '#FA8072'
            entry = pd.DataFrame([[row['REPORTER'],row['REPGRID'],row['FREQ'],lat,lon]],columns=['CALL','GRID','FREQ','LAT','LON'])
            df10 = pd.concat([df10,entry], ignore_index=True)
            data10 = [ dict(
                type = 'scattergeo',
                name = "10m",
                locationmode = 'USA-states',
                lon = df10['LON'],
                lat = df10['LAT'],
                text = df10['CALL'] +" "+ df10['GRID'],
                mode = 'markers',
                marker = dict(
                size = 8,
                color = 'rgba(250,128,114)',
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
                ))]
        print(row['REPORTER'], row['REPGRID'], band, color, lat, lon) 

    # now we need to build maps for each band/hr

    layout = dict(
		title = 'WSPR Data Mapping - '+str(r),
		colorbar = True,
		geo = dict(
		scope='north america',
		projection=dict( type='azimuthal equal area' ),
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
    fig = dict( data=data80+data40+data20+data15+data10, layout=layout )
    py.plot( fig, validate=False, filename=fname ) 
    print("#######################################################################")
    i += 1
