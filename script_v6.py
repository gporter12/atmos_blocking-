import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import netCDF4
from netCDF4 import num2date,date2index
import time as python_time
import datetime
from pprint import pprint

def runningmean(height, dates, n):
  means = []
  index = [] # Stores the unique date, lat and lon combination per
             # running mean location
  # Iterate over each n-day period
  for i in range(len(dates))[0::n]:
    dates_to_mean = dates[i:i+n]

    # Extract the heights for each day in the 5-day range
    heights = height.squeeze()[dates_to_mean]
    # Transpose the matrix so that it is latidude oriented - not date oriented
    heights_by_lon = heights.transpose()

    lat_means = []
    index2 = []
    # Iterate over each latitude
    for lat_h in heights_by_lon:
      lon_means = []
      index3 = []
      for lon_h in lat_h:
        # Calculate the running mean for this latitude
        lon_mean = np.mean(lon_h)
        lon_means.append(lon_mean)
        index3.append((dates[i],lat_h,lon_h))
      lat_means.append(lon_means)
      index2.append(index3)
    means.append(lat_means)
    index.append(index2)
  return means, index


def lat2j(lat):
 return float(65-lat) / 2.5

def lon2i(lon):
 return float(lon-305) / 2.5
def calculate_ghgn(col):
 #ghgs(305) = (h(305,60)-h(305,45)/15, h(305,65)-h(305,50)/5, h(305,55)-h(305,40)/15)

 return (col[lat2j(60)] - col[lat2j(45)]/15.0,
  (col[lat2j(65)] - col[lat2j(50)])/15.0,
  (col[lat2j(55)] - col[lat2j(40)])/15.0)

def calculate_ghgs(col):
  #ghgs(305) = (h(305,60)-h(305,45)/15, h(305,65)-h(305,50)/5, h(305,55)-h(305,40)/15)
  #305 (where delta =0) GHGS = h(305,45)-h(305,30)/45-30,  for delta = -5 h(305,40)-h(305,25)/60-45 and for delta = 5 h(305,50)-h(305,35)/50-35
  return ((col[lat2j(45)] - col[lat2j(30)])/15.0,
  (col[lat2j(40)] - col[lat2j(25)])/15.0,
  (col[lat2j(50)] - col[lat2j(35)])/15.0)

def get_gh(means):
  ghgs_store = []
  ghgn_store = []
  for col in means.T:
    ghgs_store.append(calculate_ghgs(col))
    ghgn_store.append(calculate_ghgn(col))
  return ghgs_store, ghgn_store

if __name__ == "__main__":
    # Read all key point files
    filename = ('project_data.nc')
    f = netCDF4.Dataset(filename)
    time = f.variables['time']
    height = f.variables['hgt'][:]
    lon = f.variables['lon']
    lat = f.variables['lat']

    times = num2date(times=time[:], units='hours since 1800-1-1', calendar='standard')

    #define variables in converted time array
    SON =[]
    years = np.arange(1979,2016)
    latitudes = np.arange(37.5,82.5,2.5)
    months = (9,10,11)
    days = np.arange(1,31)
    #nested loop to pull out 3 month period 
    for year in years:
      for month in months:
        for day in days:
                          # create array with intervaled data and corresponding heights 
    dates = date2index(SON, time , select='exact')

    (means,index) = runningmean(height, dates, 5)
    means = np.asarray(means)

print means.shape
#    ts = []
   # for mean in means:
    #  lat_map = {
     #   16: 65, 14: 60, 12: 55, 10: 50, 8: 45, 6: 40, 4: 35, 2: 30, 0: 25
     # }
     # lon_map = {
     #   0: 55, 2: 50, 4: 45, 6: 40, 8: 35
     # }
     # lat_indexes = (16, 14, 12, 10, 8, 6, 4, 2, 0) 
     # lon_indexes = (0, 2, 4, 6, 8) 
     # lats = []
     # for lat_pair in ((, 6), (6, 0)):
     #   lons = []
     #   for lon in lon_indexes: 
      #    phi_0 = lat_pair[0]
      #    height0 = mean[lon][phi_0]
       #   lat0 = lat_map[phi_0]
        #  lon0 = lon_map[lon]
         # phi_s = lat_pair[1]
         # height1 = mean[lon][phi_s]
         # lat1 = lat_map[phi_s]
         # lon1 = lon_map[lon]
         # lons.append(calculate_ghgs(lat0, lon0, height0, lat1, lon1, height1))
       # lats.append(lons)
    #  ts.append(lats)

  #  year_counters = {}
  #  counter = 0
  #  blocked = 0
  #  total_blocked = 0
  #  for (ghgs30, ghgs45) in ts:
  #    current_day = counter * 5
  #    days_per_year = 3 * 30
  #    current_year = int(current_day / days_per_year) + 1979
  #    blocked = False
  #    if (ghgs30[0] > 0 and ghgs30[1] > 0) or (ghgs30[1] and ghgs30[2] > 0):
  #        blocked = True
  #    if (ghgs45[0] > 0 and ghgs45[1] > 0) or (ghgs45[1] and ghgs45[2] > 0):
                                                                               #ghgs_store, ghgn_store = get_gh(means)
#print ghgs_store[lon2i(312.5)]
#print ghgn_store[lon2i(312.5)]

#A = [m[:10] for m in means[:10]]
#pprint(A)

np.asarray(means)
#print means[0][0]
print index[0][0][0]
#print np.shape(means)
#print len(time)
#print len(lat)
#print len(lon)
#print len(height)                                                           
