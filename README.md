# Greenland Albedo

## Summary

This page displays Greenland satellite acquired albedo and melt data, temperature data from automated weather stations, and Watson River flux data
on one single page. All data courtesy of [promice.org](https://www.promice.org/PromiceDataPortal/). 

## What to see

These datasets illustrate the mechanisms that cause Greenland ice loss. Ice is protected by snow, which has a high albedo (i.e., it is very bright and reflects
solar radiation well), especially when fresh (powdery). As the snow begins to melt, it also gets darker, causing it to melt even faster. Once the snow has
disappeared, the bare ice is exposed, which is of a very dark, greyish color (there are numerous contributors to that color including algae, rock, and
old, not industrial, soot).

## How to use

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

## The takeaway

The Greenland ice is protected from melting by snow. Once the snow is gone, dark ice is exposed which is very vulnerable to melt due to its dark, high-absorption
color. If the amount of snow falling in winter is becoming lower over time, and/or there are a few very warm days early on in summer, a lot of ice disappears which will
not be replenished, and is lost. This may lead to irreversible loss of the Greenland ice shield.

## Data

This site only shows a subset of data for the years 2012-2014 available from [promice.org](https://www.promice.org/PromiceDataPortal/), which contains data from 2000-2019. Even after processing (removing data N of 70° and altitudes above 1500 m,
and surface conditions being only ice and snow), the data amounted to abut 3 GB (from 150 GB), which was too big for a public
repository.

## Mapping

_"The problem with big data is that there is too much of it"_. To make sense of the data, conditions were mapped to hexagons using
[Uber's H3 library](https://h3geo.org/). An alternative would have been employing [bokeh's datashader](https://examples.pyviz.org/nyc_taxi/nyc_taxi.html) to use "all" datapoints.