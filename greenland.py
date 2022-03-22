import streamlit as st 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import matplotlib as mpl
import pandas as pd
import geopandas as gpd
import datetime
import numpy as np
from glob import glob
import warnings
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg
import time

class GREENLAND():
    def __init__(self):
        self.gdfGreenland = gpd.read_parquet("./data/gdfGreenland.parquet")
        self.dfAllBasins = pd.read_parquet("./data/t_greenland_basins.parquet")
        self.gdfHexagons = gpd.read_parquet("./data/t_greenland_hexagons.parquet")

class ALBEDO():
    def __init__(self,greenland):
        self.greenland = greenland
    
    def get_data(self,yyyy,doy):
        #df = pd.read_parquet(f"./data/albedo_{yyyy}.parquet")
        df = pd.read_parquet("./data/albedo", filters=[('yyyy','=',yyyy),('doy','=',doy)])
        #df = df[df.doy==doy]

        self.lat = df.lat.values
        self.lon = df.lon.values
        self.elev = df.elev.values
        self.albedo = df.albedo.values
        self.temp = df.temp.values

        df = pd.read_pickle("./data/histogram_rects.pickled.gz",compression="gzip")
        self.rectangles = df[(df.yyyy == yyyy)&(df.doy == doy)].histogram.values[0]

def get_KAN_x_temps(station_id):
    df = pd.read_parquet(f"./data/KAN_{station_id}_day.parquet")
    df_h = pd.read_parquet(f"./data/KAN_{station_id}_hour.parquet")

    return df,df_h

def get_Watson_River_fluxes(datetime_date):
    df = pd.read_parquet("./data/t_greenland_watson_river_hourly.parquet")
    
    from_dt = datetime_date-datetime.timedelta(days=7)
    to_dt = datetime_date+datetime.timedelta(days=7)

    df = df[(df.date >= from_dt) & (df.date <= to_dt)]

    return df

def get_albedobands_hexbins(datetime_date):
    yyyy = datetime_date.year
    gdf = gpd.read_parquet(f"./data/t_albedobands_hexmapped_{yyyy}.parquet")
    gdf = gdf[gdf.datetime_date == pd.to_datetime(datetime_date)]
    return gdf

st.cache(GREENLAND.__init__,persist=True,show_spinner=True)
st.cache(ALBEDO.__init__,persist=True,show_spinner=True)
st.cache(ALBEDO.get_data,persist=True,show_spinner=True)
st.cache(get_KAN_x_temps,persist=True,show_spinner=True)

plt.style.use('ggplot')
COLOR = 'white'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
greenland = GREENLAND()
albedo = ALBEDO(greenland)

st.header("""Greenland Change of Albedo S of 70°N""")

with st.expander("How to use this page"):
    st.write("""# Summary

This page displays Greenland satellite acquired albedo and melt data, temperature data from automated weather stations, and Watson River flux data
on one single page. All data courtesy of [promice.org](https://www.promice.org/PromiceDataPortal/).

# What to see

These datasets illustrate the mechanisms that cause Greenland ice loss. Ice is protected by snow, which has a high albedo (i.e., it is very bright and reflects
solar radiation well), especially when fresh (powdery). As the snow begins to melt, it also gets darker, causing it to melt even faster. Once the snow has
disappeared, the bare ice is exposed, which is of a very dark, greyish color (there are numerous contributors to that color including algae, rock, and
old, not industrial, soot).

# How to use

Start with a known date of interest, this page defaults to 2012-07-12, the day the Watson River bridge was almost washed away due to an extreme level of
meltwater. The scatter plot (red) shows you the distribution of albedo over the elevation, which on that day will indicate a lot of dark ice, also shown 
in the vertical histogram. The image shown gives an indication of how most of Greenland may have looked like on that day for altitudes up those shown on 
the scatter plot.

The maps show abundance of dark ice, wet snow, and fresh snow in Greenland below 70° N, with a blue-yellow low-high color scheme. 

The line plots show the situation at that day, i.e. temperatures and river fluxes before and after the selected date. This way you can navigate to earlier or later
dates to study the effects of melting, or snow fall yourself.

Select an earlier date, and the abundance of dark ice should reduce as there was likely more snow if the temperatures were lower, and earlier in the year. 
Select a later date, the abundance of dark ice should increase or remain constant. Selecting
an even later date (like, September), it is likely that there will have been fresh snow fallen, and the melt cycle resets.

# The takeaway

The Greenland ice is protected from melting by snow. Once the snow is gone, dark ice is exposed which is very vulnerable to melt due to its dark, high-absorption
color. If the amount of snow falling in winter is becoming lower over time, and/or there are a few very warm days early on in summer, a lot of ice disappears which will
not be replenished, and is lost. This may lead to irreversible loss of the Greenland ice shield.

""")

mindate = datetime.datetime(2012, 1, 1, 0, 0)
maxdate = datetime.datetime(2014, 12, 31, 23, 59)

selected_date = st.sidebar.date_input("Select Date",min_value=mindate,max_value=maxdate,value=datetime.date(2012,7,12))

st.sidebar.text("Temps KAN_B/L Greenland 67.1252°N,50.1832°W")


dfKAN_B,dfKAN_B_h = get_KAN_x_temps("B")
dfKAN_L,dfKAN_L_h = get_KAN_x_temps("L")
fig,ax = plt.subplots(figsize=(10,6))
ax.scatter(dfKAN_B.dayofyear,dfKAN_B.airtemperature_c,alpha=0.75,s=10,c="lightgreen",marker="+",edgecolors=None)
ax.scatter(dfKAN_L.dayofyear,dfKAN_L.airtemperature_c,alpha=0.25,s=10,c="forestgreen",marker="x",edgecolors=None)

ax.scatter(dfKAN_B[dfKAN_B.year==selected_date.year].dayofyear,dfKAN_B[dfKAN_B.year==selected_date.year].airtemperature_c,
    alpha=1.0,s=15,marker="+",color="black")
ax.scatter(dfKAN_L[dfKAN_L.year==selected_date.year].dayofyear,dfKAN_L[dfKAN_L.year==selected_date.year].airtemperature_c,
    alpha=1.0,s=15,marker="x",color="black")

ax.axvline(selected_date.timetuple().tm_yday,color="grey")
plt.xlabel("Day of the Year")
plt.ylabel("Ambient Temperature [°C]")
plt.title("Temperatures at KAN_B(+) KAN_L(x) Greenland 67.1252°N,50.1832°W")
fig.patch.set_facecolor('#3A3A4A')
st.sidebar.pyplot(fig)


fig,ax = plt.subplots(figsize=(10,6))
ddfKAN_B_h = dfKAN_B_h[(pd.to_datetime(selected_date)-pd.Timedelta(days=14)<=dfKAN_B_h.datetime_date)&
                    (dfKAN_B_h.datetime_date<=pd.to_datetime(selected_date)+pd.Timedelta(days=14))]
ax.plot(ddfKAN_B_h.datetime_date,ddfKAN_B_h.ta,
    alpha=1.0,color="maroon")


ddfKAN_L_h = dfKAN_L_h[(pd.to_datetime(selected_date)-pd.Timedelta(days=14)<=dfKAN_L_h.datetime_date)&
                    (dfKAN_L_h.datetime_date<=pd.to_datetime(selected_date)+pd.Timedelta(days=14))]
ax.plot(ddfKAN_L_h.datetime_date,ddfKAN_L_h.ta,
    alpha=1.0,color="coral")

ax.axvline(selected_date,color="grey")
plt.xlabel("Date")
plt.ylabel("Ambient Temperature [°C]")
plt.title("Temperatures at KAN_B(+) KAN_L(x) Greenland 67.1252°N,50.1832°W")
fig.patch.set_facecolor('#3A3A4A')
st.sidebar.pyplot(fig)

st.sidebar.text("Watson River Flux 67.005159°N, -50.686733°W")
fig,ax = plt.subplots(figsize=(10,6))
dfWatsonRiver = get_Watson_River_fluxes(selected_date)
ax.plot(dfWatsonRiver.datetime_date,dfWatsonRiver.flux,alpha=1.0,color="black")
ax.axvline(selected_date,color="grey")
plt.xlabel("Date")
plt.ylabel("Flux [m³/s]")
plt.title("Watson River Flux 67.005159°N, -50.686733°W")
fig.patch.set_facecolor('#3A3A4A')
st.sidebar.pyplot(fig)

st.sidebar.image("https://www.researchgate.net/profile/Katrin-Lindbaeck/publication/303686346/figure/fig1/AS:367768626057217@1464694281221/Photograph-taken-at-1800-West-Greenland-Summer-Time-on-11-July-2012-during-the-flood.png")

st.sidebar.text("Klaus G. Paul, 2021-2022")

albedo.get_data(selected_date.year,selected_date.timetuple().tm_yday)

fig,(ax,ax2,ax3) = plt.subplots(1,3,figsize=(14,6),gridspec_kw={'width_ratios': [5, 1,3]})
dfTmp = pd.DataFrame({"elev":albedo.elev,"albedo":albedo.albedo})
sns.histplot(dfTmp,x="elev",y="albedo",ax=ax,cbar=True)
ax.set_ylim(0,100)
maxy = 0
image_file = ""
for rectangle in albedo.rectangles:
    ax2.add_patch(Rectangle((0,rectangle["yfrom"]),rectangle["w"],rectangle["h"],edgecolor="white",facecolor="grey"))
    if rectangle["w"]>maxy:
        if rectangle["yfrom"] == 60:
            image_file = "./resources/FreshSnow.jpg"
            title = "Mostly Fresh Snow"
        elif rectangle["yfrom"] == 40:
            image_file = "./resources/WetSnow.jpg"
            title = "Mostly Wet Snow"
        else:
            image_file = "./resources/DarkIce.jpg"
            title = "Mostly Dark, Bare Ice"
    maxy = max(maxy,rectangle["w"])

ax2.set_ylim(0,100)
ax2.yaxis_inverted()
ax2.set_xlim(0,maxy)

if len(image_file)>0:
    img = mpimg.imread(image_file)
    ax3.imshow(img)
ax3.axis("off")
ax3.set_title(title)

fig.patch.set_facecolor('#3A3A4A')
st.pyplot(fig)

gdfHexagons = get_albedobands_hexbins(selected_date)

fig,((axl,axc),(axr,axempty)) = plt.subplots(2,2,figsize=(20,18))

greenland.gdfGreenland.plot(alpha=0.2,facecolor="grey",edgecolor="tomato",ax=axl)
gdfHexagons.plot(ax=axl,column="darkice",edgecolor="#A0A0De")
axl.set_ylim((59,72))
axl.set_xlim((-60,-20))
axl.axhline(67.1252,color="darkgrey",alpha=0.8)
axl.axvline(-50.1832,color="darkgrey",alpha=0.8)
axl.set_title("Dark Ice rel.")

greenland.gdfGreenland.plot(alpha=0.2,facecolor="grey",edgecolor="tomato",ax=axc)
gdfHexagons.plot(ax=axc,column="wetsnow",edgecolor="#A0A0De")
axc.set_ylim((59,72))
axc.set_xlim((-60,-20))
axc.axhline(67.1252,color="darkgrey",alpha=0.8)
axc.axvline(-50.1832,color="darkgrey",alpha=0.8)
axc.set_title("Wet Snow rel.")

greenland.gdfGreenland.plot(alpha=0.2,facecolor="grey",edgecolor="tomato",ax=axr)
gdfHexagons.plot(ax=axr,column="snow",edgecolor="#A0A0De")
axr.set_ylim((59,72))
axr.set_xlim((-60,-20))
axr.axhline(67.1252,color="darkgrey",alpha=0.8)
axr.axvline(-50.1832,color="darkgrey",alpha=0.8)
axr.set_title("White Snow rel.")

axempty.axis("off")

fig.patch.set_facecolor('#3A3A4A')
plt.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)

st.pyplot(fig)



