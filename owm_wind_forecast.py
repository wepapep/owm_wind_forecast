#library import
import requests
import json
import matplotlib.pyplot as plt
import numpy as np

################################################################
#USER CONFIGURATION
API_KEY = "";
coordinates_filename = "xycoords.txt";
################################################################

################################################################
#xycoords texfile scheme
#3 elements:
#name latitude longitude
#space delimited
#each line is a separate entry 
#entries that begin with "#" are skipped
#use google maps or w/e to get coordinates
################################################################

################################################################
#FIGURE CONFIGURATION

#figure parameters
fig_ls = '-';		#line size
fig_lw = 2.0;		#line width
fig_m = '.';		#marker type
fig_ms = 9.0; 		#marker size
fig_c = 'magenta';	#line color
fig_cb = 'silver';	#background color
#grid lines parameters
grid_ls = ':';		#grid line size
grid_lw = 1.0;		#grid line width
grid_c = 'black';	#grid line color
#axes
#chosen OpenWeatherMap API 
#provides forecast for next 5 days with 3 hour steps
xaxis = np.arange(0,120,3);
xgrid = np.arange(0,120,24);
################################################################


def readcoordinates(textline):
	return textline.split();


coordinatelist = open(coordinates_filename, "r");


for l in coordinatelist:
	if (l[0] == "#"):
		continue;
	windarray = [];
	
	list_entry = readcoordinates(l);
	print(list_entry[0], "\t", list_entry[1], "\t", list_entry[2]);
	
	apicall = f'https://api.openweathermap.org/data/2.5/forecast?lat={list_entry[1]}&lon={list_entry[2]}&appid={API_KEY}';
	weatherdata = requests.get(apicall).json();
	
	#
	if (weatherdata["cod"] != "200"):
		print(list_entry[0]," - error accessing data from OpenWeatherMaps");
		continue;
		
	for i in range(len(weatherdata["list"])):
		windval = weatherdata["list"][i]["wind"]["speed"];
		windarray.append(windval);
		
	fig, ax = plt.subplots();
	ax.set_xlabel("time");
	ax.set_ylabel("wind speed [m/s]");
	ax.set_title(list_entry[0] + " Weather Forecast" );
	fig.set_facecolor(fig_cb);
	plt.ylim([0,30]);
	ax.set_xticks(xgrid);
	plt.grid(visible=True, which='major', axis='x', linestyle=grid_ls, linewidth=grid_lw, color=grid_c);
	ax.plot(xaxis,windarray, ls=fig_ls, lw = fig_lw, c = fig_c, marker = fig_m, markersize=fig_ms);
	plt.show();


print("\n---------------");
print("FINISHED");
