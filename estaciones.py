#!/usr/bin/env python3
"""
Created on Wen Aug 26 15:10:59 2020
Script python for mapping seismological stations
the following files are required:
1. ESTACIONES.txt (Estaciones nacionales)
2. ESTACIONES_NOFUNV.txt (Estaciones internacionales)
3. etopo1_bedrock.grd
4. verde.cpt
5. estaciones_legend.txt
6. fallas2015.txt
"""

import pandas as pd
import pygmt

# Seismological stations
# Load station from txt file
estaciones=pd.read_csv("ESTACIONES.txt", sep='\s+') # National stations
estaciones=estaciones[estaciones.COD!='CARV'] # ignore  CARV station
nofun=pd.read_csv("ESTACIONES_NOFUNV.txt", sep='\s+') # International stations


## genera mapa GMT
KWARGS = dict(grid='etopo1_bedrock.grd',region=[-76,-59,5,15],
    projection='M10i', cmap='verde.cpt',frame=0)

fig = pygmt.Figure()

fig.grdimage(shading=True,  **KWARGS)  # Add illumination!

fig.coast(shorelines=True, borders=['1/0.8p','2/0.1p'],frame=True,
    map_scale='-68.5/7.0/7.0/200 ', resolution='f')

# Geological faults
fig.plot(data="fallas2015.txt",pen="1,red")

#Plot national stations
fig.plot(x=estaciones.Lon, y=estaciones.Lat,style="t0.8c",color='yellow',
         pen="black") #sizes=0.02 * 2 ** data.MAG
# Plot code (names) of national stations
fig.text(textfiles=None,x=estaciones.Lon-0.1, y=estaciones.Lat+0.3,
         position=None,text=estaciones.COD, angle=0,
         font='10p,Helvetica-Bold,black', justify='LM')

#Plot international stations
fig.plot(x=nofun.Lon,y=nofun.Lat,style="t0.8c",color='green',
         pen="black")
# Plote code (names) of international stations
fig.text(textfiles=None,x=nofun.Lon-0.1, y=nofun.Lat+0.3,
         position=None,text=nofun.COD, angle=0,
         font='10p,Helvetica-Bold,black', justify='LM')

#texto Mar Caribe
fig.text(x=-68.0, y=13.5,position=None,text='Caribbean Sea', angle=0,
         font='28p,Helvetica-Bold,white', justify='LM')

#legend
fig.legend(spec='estaciones_legend.txt', position='JTL+jTL+o0.5c+w6.3/3.7',
        box='+glavender+p2p+r')


fig.savefig('estaciones_activas.png')
