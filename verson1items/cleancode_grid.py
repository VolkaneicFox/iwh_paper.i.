# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 09:01:49 2024

@author: nb
"""

## dependencies ##
import numpy as np
import geopandas as gpd
import xarray as xr
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
import pandas as pd
import hvplot.pandas
import os, pickle
import matplotlib.colors as mcolors
import matplotlib.cm as cm

pathname="D:\\archive\\weather_grid_data\\"
#%% Part 1. Making the daily histories of county data 

#assigning the coordinates from the netcdf to the county shape files

from shapely.geometry import Point
ncdf=xr.open_dataset(pathname+"tas_raw_grid_DE.nc")
ncdf_present=ncdf.sel(time=ncdf.time.dt.year>=1950)

x_list,y_list=np.arange(0,ncdf.x.shape[0],1),np.arange(0,ncdf.y.shape[0],1)
coords_list=[[x,y] for x in x_list for y in y_list]

drive='D:'
kreise_file=gpd.read_file(drive+'\\official_de_shapefiles.gk3.shape.ebenen\\vg5000_ebenen_1231\\VG5000_KRS.shp',crs=4326)
kreise_file['Kreise_Code']=kreise_file['ARS'].astype(int)
kreise_crs=kreise_file.to_crs(epsg=3034)
kreise_crs=kreise_crs[['Kreise_Code','geometry']]
kreise_list=list(kreise_crs['Kreise_Code'])
kreise_crs=kreise_crs.set_index('Kreise_Code')

## step 1: select the coordinates in the ncdf that are from the (multi)polygon 
## geometry of the kreies_crs shapefile

kreise_coords={}
ix=0
for kreise in kreise_list:
    kreise_geo=kreise_crs.loc[kreise,'geometry']
    found={'coords_3034':[],
           'xy_axis':[]}
    for coords in coords_list:
        j,i=coords[0],coords[1]
        make_point=(ncdf.x.values[j],ncdf.y.values[i]) #<-- finding the points that are in the ncdf
        if kreise_geo.contains(Point(make_point)) or kreise_geo.touches(Point(make_point)):
            found['coords_3034']=found['coords_3034']+[[int(make_point[0]),int(make_point[1])]]#<-- the points in the ncdf that correspond to the polygon in the shapefile
            found['xy_axis']=found['xy_axis']+[[j,i]]
    kreise_coords[kreise]=found
    print(str(ix)+': '+str(kreise))
    ix=ix+1
    
## step 2. 
with open('D:\\weather_grid_data\\kreise_coords_tas.pickle','rb') as infile:
    kreise_coords=pickle.load(infile)
size_list={item:len(kreise_coords[item]['xy_axis']) for item in kreise_coords}
c_small=[item for item in kreise_coords if len(kreise_coords[item]['xy_axis'])<50]

c_mid1=[item for item in kreise_coords if len(kreise_coords[item]['xy_axis'])>=50]
c_mid1=[item for item in c_mid1 if len(kreise_coords[item]['xy_axis'])<70]
c_mid1=[i for i in c_mid1 if i!=1055]

c_mid2=[item for item in kreise_coords if len(kreise_coords[item]['xy_axis'])>=70]
c_mid2=[item for item in c_mid2 if len(kreise_coords[item]['xy_axis'])<90]

c_large=[item for item in kreise_coords if len(kreise_coords[item]['xy_axis'])>=90]

## step 3.

def catchtas():
    ix=1
    done=os.listdir(drive+'//weather_grid_data/kreise_grid_daily/')
    left=[item for item in kreise_coords if str(item)+'.txt' not in done]    
    console_1=left[1:17]
    for kreise in console_1:
        if str(kreise)+'.txt' not in done:
            print('Here with: ',kreise)
            inkreise=kreise_coords[kreise]['xy_axis']
            kreise_ncdf=ncdf_present.isel(x=[cd[0] for cd in inkreise],y=[cd[1] for cd in inkreise])
            weights = np.cos(np.deg2rad(kreise_ncdf.lat))
            weights.name = "weights"
            kreise_ncdf_weighted=kreise_ncdf.tas.weighted(weights)
            kreise_ncdf_fin=kreise_ncdf_weighted.mean(('y','x'))
            kreise_ncdf_pd=kreise_ncdf_fin.to_dataframe()
            kreise_ncdf_pd=kreise_ncdf_pd.reset_index()
            kreise_ncdf_pd['MESS_DATUM']=kreise_ncdf_pd['time'].apply(lambda x: str(x).split(' ')[0])
            kreise_ncdf_pd['MESS_DATUM']=kreise_ncdf_pd['MESS_DATUM'].apply(lambda x: int(x.replace('-','')))
            kreise_ncdf_pd.to_csv(drive+'\\weather_grid_data\\kreise_grid_daily\\'+str(kreise)+'.txt')
            print(ix,': ',kreise)
            ix=ix+1
with open('<path>kreise_coords_tas.pickle', 'rb') as handle:
    kreise_coords=pickle.load(handle)

kreise_size={}
for kreise in kreise_coords:
    kreise_size[kreise]=len(kreise_coords[kreise]['xy_axis'])
    
def catch_rain(kreise):
        inkreise=kreise_coords[kreise]['xy_axis']
        kreise_ncdf=ncdf_present.isel(x=[cd[0] for cd in inkreise],y=[cd[1] for cd in inkreise])
        #kreise_ncdf_df=pd.DataFrame(index=range(kreise_ncdf.time.values.shape[0]))
        weights = np.cos(np.deg2rad(kreise_ncdf.lat))
        weights.name = "weights"
        kreise_ncdf_weighted=kreise_ncdf.tasmax.weighted(weights)
        kreise_ncdf_fin=kreise_ncdf_weighted.mean(('y','x'))
        kreise_ncdf_pd=kreise_ncdf_fin.to_dataframe()
        kreise_ncdf_pd=kreise_ncdf_pd.reset_index()
        kreise_ncdf_pd['MESS_DATUM']=kreise_ncdf_pd['time'].apply(lambda x: str(x).split(' ')[0])
        kreise_ncdf_pd['MESS_DATUM']=kreise_ncdf_pd['MESS_DATUM'].apply(lambda x: int(x.replace('-','')))
        return kreise_ncdf_pd   
    
for kreise in {kreise: size for kreise, size in kreise_size.items() if 0< size <= 30}:
        print(kreise)
        console1df=catch_rain(kreise)
        consolde1df=console1df[['MESS_DATUM','tasmax']]
        console1df['Kreise_Code']=kreise
        console1df.to_csv('<savepath>'+str(kreise)+'.txt',index=False)
        ix=ix+1
        
#%% Converting daily histories to annual dataframes

tasdf=pd.DataFrame()
kreisefiles=os.listdir("D://archive/weather_grid_data/tasfull/")
for file in kreisefiles:
    inkreise=pd.read_csv("D://archive/weather_grid_data/tasfull/"+file)
    inkreise['year']=(inkreise['MESS_DATUM']/10000).astype(int)
    inkreise=inkreise[inkreise['year']>=2000]
    inkreise=inkreise[['year','tas']].groupby(by='year').mean().reset_index()
    inkreise['Kreise_Code']=int(file.split('.')[0])
    tasdf=pd.concat([tasdf,inkreise],axis=0)
tasdf['tas2']=tasdf['tas']**2

precdf=pd.DataFrame()
kreisefiles=os.listdir("D://archive/weather_grid_data/kreise_daily_pr/")
for file in kreisefiles:
    inkreise=pd.read_csv("D://archive/weather_grid_data/kreise_daily_pr/"+file)
    inkreise=inkreise[inkreise['year']>=2000]
    inkreise=inkreise[['year','prec']].groupby(by='year').sum().reset_index()
    inkreise['Kreise_Code']=int(file.split('.')[0])
    precdf=pd.concat([precdf,inkreise],axis=0)
precdf['prec2']=precdf['prec']**2
    
season_dict={1:1,2:1,3:2,4:2,5:2,6:3,7:3,8:3,9:4,10:4,11:4,12:1}
season_name={1:'winter',2:'spring',3:'summer',4:'autumn'}
tailsdf=pd.DataFrame()
for file in kreisefiles:    
    indf=pd.read_csv('D://archive/weather_grid_data//tasfull//'+file)
    indf['year']=(indf['MESS_DATUM']/10000).astype(int)
    indf['month']=((indf['MESS_DATUM']%10000)/100).astype(int)
    indf['season']=indf['month'].apply(lambda x: season_dict[x])
    filldf=pd.DataFrame()
    for year in range(21):
        year=2000+year
        hist0,hist1=year-35,year-5
        tempdf=indf[indf['year']>=hist0]
        tempdf=tempdf[tempdf['year']<=hist1][['tas','season']]
        filldf.loc[year,'hist0']=hist0
        filldf.loc[year,'hist1']=hist1
        for season in range(4):
            season=season+1
            dist=tempdf[tempdf['season']==season]['tas']
            low,high=dist.quantile(0.05),dist.quantile(0.95)
            filldf.loc[year,season_name[season]+'05']=low
            filldf.loc[year,season_name[season]+'95']=high
    filldf['Kreise_Code']=int(file.split('.')[0])
    filldf=filldf.reset_index()
    tailsdf=pd.concat([filldf,tailsdf],axis=0)
tailsdf=tailsdf.rename(columns={'index':'year'})

extremedf=pd.DataFrame()
for file in kreisefiles:
    kreise=int(file.split('.')[0])
    tail=tailsdf[tailsdf['Kreise_Code']==kreise].set_index('year')
    indf=pd.read_csv('D://archive/weather_grid_data//tasfull//'+file)
    indf['year']=(indf['MESS_DATUM']/10000).astype(int)
    indf['month']=((indf['MESS_DATUM']%10000)/100).astype(int)
    indf['season']=indf['month'].apply(lambda x: season_dict[x])
    filldf=pd.DataFrame()
    for year in range(21):
        year=year+2000
        temp=indf[indf['year']==year][['tas','season']]
        hotdays,colddays=0,0
        for season in range(4):
            dist=temp[temp['season']==season+1]['tas']
            dist=list(dist)
            season=season_name[season+1]
            low,high=tail.loc[year,season+'05'],tail.loc[year,season+'95']
            hotdays,colddays=hotdays+sum([int(i>=high) for i in dist]),colddays+sum([int(i<=low) for i in dist])
        filldf.loc[year,'hotday.d']=hotdays
        filldf.loc[year,'coldday.d']=colddays
    filldf['Kreise_Code']=kreise
    filldf=filldf.reset_index()
    extremedf=pd.concat([extremedf,filldf],axis=0)
extremedf=extremedf.rename(columns={'index':'year'})
        
precpd=pd.DataFrame()
for file in kreisefiles:
    kreisecode=int(file.split('.')[0])
    infile=pd.read_csv("D://archive/weather_grid_data/kreise_daily_pr/"+file)
    infile=infile[infile['year']>=2000]
    df=pd.DataFrame()
    for year in range(21):
        year = 2000+year
        temp=infile[infile['year']==year]
        temp=temp[temp['prec']>0]['prec'].mean()
        df.loc[year,'precpd']=temp
    df=df.reset_index()
    df['Kreise_Code']=kreisecode
    precpd=pd.concat([precpd,df],axis=0)
precpd=precpd.rename(columns={'index':'year'})

def makelagsanddiffs(indf,cols,laglim=2):
    '''
    the indf is taken for each county
    then set the year as index,
    then take first difference,and take upto laglim of first diff
    then take upto laglim of the columns
    ['tas','tas2','prec','prec2','precpd','hotday.d','coldday.d']
    '''
    
    indf=indf.set_index('year')
    for col in cols:
        indf[col+'.D1']=indf[col].diff(1)
        cols=cols+[col+'.D1']
    for col in cols:
        for i in range(laglim):
            indf[col+'.L'+str(i+1)]=indf[col].shift(1)
    indf=indf.reset_index()
    return indf

kreiselist=list(set(tasdf['Kreise_Code']))
tasdfv1=pd.DataFrame()
for kreise in kreiselist:
    temp=makelagsanddiffs(indf=tasdf[tasdf['Kreise_Code']==kreise],cols=['tas','tas2'])
    tasdfv1=pd.concat([tasdfv1,temp],axis=0)
    
kreiselist=list(set(precdf['Kreise_Code']))
precdfv1=pd.DataFrame()
for kreise in kreiselist:
    temp=makelagsanddiffs(indf=precdf[precdf['Kreise_Code']==kreise],cols=['prec','prec2'])
    precdfv1=pd.concat([precdfv1,temp],axis=0)
    
kreiselist=list(set(extremedf['Kreise_Code']))
extremedfv1=pd.DataFrame()
for kreise in kreiselist:
    temp=makelagsanddiffs(indf=extremedf[extremedf['Kreise_Code']==kreise],cols=['hotday.d','coldday.d'])
    extremedfv1=pd.concat([extremedfv1,temp],axis=0)
    
kreiselist=list(set(extremedf['Kreise_Code']))
extremedfv1=pd.DataFrame()
for kreise in kreiselist:
    temp=makelagsanddiffs(indf=extremedf[extremedf['Kreise_Code']==kreise],cols=['hotday.d','coldday.d'])
    extremedfv1=pd.concat([extremedfv1,temp],axis=0)

kreiselist=list(set(precpd['Kreise_Code']))
precpdv1=pd.DataFrame()
for kreise in kreiselist:
    temp=makelagsanddiffs(indf=precpd[precpd['Kreise_Code']==kreise],cols=['precpd'])
    precpdv1=pd.concat([precpdv1,temp],axis=0)

p1=pd.DataFrame()
p1=pd.merge(tasdfv1,precdfv1,on=['year','Kreise_Code'])   
p1=pd.merge(p1,extremedfv1,on=['year','Kreise_Code'])
p1=pd.merge(p1,precpdv1,on=['year','Kreise_Code'])

econdf=pd.read_csv("D://archive/weather_grid_data/model_df/fulldf/fulleconJanv2.csv")
econdf['ln.GVAREALPW']=np.log(econdf['GVAREALPW'])
econdf['ln.CAPPW']=np.log(econdf['CAPPW'])
kreiselist=list(set(econdf['Kreise_Code']))
outdf=pd.DataFrame()
for kreise in kreiselist:
    temp=econdf[econdf['Kreise_Code']==kreise].set_index('year')
    temp['ln.GVAREALPW.D1']=temp['ln.GVAREALPW'].diff(1)
    temp['ln.CAPPW.D1']=temp['ln.CAPPW'].diff(1)
    outdf=pd.concat([outdf,temp],axis=0)
    
p1=pd.merge(p1,outdf,on=['year','Kreise_Code'])

p1.to_csv('D://archive/weather_grid_data/model_df/fulldf/panelreg_c1.csv',index=False)

from numpy import log
cols=['Kreise_Code','GVAREALPW','tas','tas2','hotday.d','coldday.d','prec','precpd','CAPPW']
p1=pd.read_csv('D://archive/weather_grid_data/model_df/fulldf/panelreg_c1.csv')
part1=p1[p1['year']<=2004][cols]
part1=part1.groupby('Kreise_Code').mean()
part1['GVAREALPWln']=log(part1['GVAREALPW'])
part1['CAPPWln']=log(part1['CAPPW'])
part1['GVAREALPWln0']=part1['GVAREALPWln']
part2=p1[p1['year']<=2012]
part2=part2[part2['year']>=2008][cols]
part2=part2.groupby('Kreise_Code').mean()
part2['GVAREALPWln']=log(part2['GVAREALPW'])
part2['CAPPWln']=log(part2['CAPPW'])
part2['GVAREALPWln0']=part2['GVAREALPWln']
part3=p1[p1['year']>=2016][cols]
part3=part3.groupby('Kreise_Code').mean()
part3['CAPPWln']=log(part2['CAPPW'])
part3['GVAREALPWln']=log(part3['GVAREALPW'])

cols=['GVAREALPWln','tas','tas2','hotday.d','coldday.d','prec','precpd','CAPPWln']
diff21=part2[cols]-part1[cols]
diff21=pd.concat([diff21,part1['GVAREALPWln0']],axis=1)
diff32=part3[cols]-part2[cols]
diff32=pd.concat([diff32,part2['GVAREALPWln0']],axis=1)
diff31=part3[cols]-part1[cols]
diff31=pd.concat([diff31,part1['GVAREALPWln0']],axis=1)

diffcols=['GVAREALPWln','tas','tas2','hotday.d','coldday.d','prec','precpd','CAPPWln']
for col in diffcols:
    diff21=diff21.rename(columns={col:'D.'+col})
    diff32=diff32.rename(columns={col:'D.'+col})
    diff31=diff31.rename(columns={col:'D.'+col})

diff21=diff21.reset_index()
diff31=diff31.reset_index()
diff32=diff32.resent_index()

diff21.to_csv('D://archive/weather_grid_data/model_df/longdiff/diff21vAug_c1.csv',index=False)
diff31.to_csv('D://archive/weather_grid_data/model_df/longdiff/diff31vAug_c1.csv',index=False)
diff32.to_csv('D://archive/weather_grid_data/model_df/longdiff/diff32vAug_c1.csv',index=False)
