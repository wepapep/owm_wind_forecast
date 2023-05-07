#library import
import requests
import json
import matplotlib as mpl
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
#space delimited!
#each line is a separate entry 
#entries that begin with "#" are skipped
#use google maps or w/e to get coordinates
################################################################

################################################################
#FIGURE AND PLOT CONFIGURATION
#chosen OpenWeatherMap API provides 
#forecast for next 5 days with 3 hour steps
#the x axis is adjusted here accordingly
#x axis grid is adjusted to mark each 24 hour period
xaxis = np.arange(0,120,3);	
xgrid = np.arange(0,120,24);

#variable, change the number of columns in the figure
NumberOfColumns = 3;

#graphics
#line color is specified as a plot parameter later on
mpl.rcParams.update({
	"axes.grid": True,				#display grid lines
	"axes.grid.axis": 'x',			#specify the axis
	"grid.linestyle": ':',			#style of grid lines
	"grid.linewidth": 1,			#size of grid lines
	"grid.color": 'black',			#color of grid lines
	"lines.linestyle": '-',			#style of plot lines
	"lines.linewidth": 2,			#size of plot lines
	"lines.marker": '.',			#style of marker
	"lines.markersize": 5,			#size of marker
	"figure.facecolor": 'silver',	#color outside the plot
})
################################################################
#PLOT INDEXING
FarmIndex = 0;		#needed to display multiple plots
#FIGURE INITIALIZATION 
fig, axs = plt.subplots(3,6, sharex='all',squeeze=True);
################################################################

def readcoordinates(textline):
	return textline.split();

#open the file with coordinates
coordinatelist = open(coordinates_filename, "r");

#iterate through the contents of the file with coordinates
for l in coordinatelist:
	if (l[0] == "#"):
		continue;
	windarray = [];
	RowIndex = FarmIndex%NumberOfColumns;
	ColIndex = FarmIndex//NumberOfColumns;
	
	list_entry = readcoordinates(l);
	print(list_entry[0], "\t", list_entry[1], "\t", list_entry[2]);
	
	apicall = f'https://api.openweathermap.org/data/2.5/forecast?lat={list_entry[1]}&lon={list_entry[2]}&appid={API_KEY}';
	weatherdata = requests.get(apicall).json();
	
	#error message in case API didnt respond correctly
	if (weatherdata["cod"] != "200"):
		print(list_entry[0]," - error accessing data from OpenWeatherMaps");
		continue;
	#pass json results into a list 	
	for i in range(len(weatherdata["list"])):
		windval = weatherdata["list"][i]["wind"]["speed"];
		windarray.append(windval);
	
	#additional chart configuration
	axs[RowIndex, ColIndex].set_xlabel("time");
	axs[RowIndex, ColIndex].set_ylabel("wind speed [m/s]");
	axs[RowIndex, ColIndex].set_title(list_entry[0] + " Weather Forecast" );
	axs[RowIndex, ColIndex].set_xticks(xgrid);
	axs[RowIndex, ColIndex].set_ylim(bottom=0, top=30);
	
	axs[RowIndex, ColIndex].plot(xaxis,windarray, c='magenta');
	FarmIndex += 1;

plt.show();
	


print("\n---------------");
print("FINISHED");
