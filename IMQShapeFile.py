import matplotlib.pyplot as plt
import geopandas as gpd


def run(filepath=""):
    
    plano = gpd.read_file(filepath)
    plano.plot(figsize=(20,40))
    partialTranslation=plano.translate(261.75756,-149.51527,0)
    partialTranslation.plot(figsize=(20,40))
    plt.grid()
    scale = 4500/509.931 #1/193.11
    geometryScaled = partialTranslation.scale(scale,scale,1, origin=(0,0,0)) #-261.75756,149.41021-261.66994,
    geometryTranslated = geometryScaled.translate(249000, 8350500,0) #30.24975, 99.84579
    geometryTranslated.plot(figsize=(20,40))
    plt.grid()
    #apply the new geometry to the geopandas dataframe and apply the EPSG cpde
    plano = gpd.GeoDataFrame(plano, geometry=geometryTranslated)
    plano.crs = {'init':'epsg:24789'}
    plano.plot(figsize=(20,40))
    #filter only the line elements
    planoLines = plano[plano.geometry.type=='LineString']
    #export the spatial as shapefile
    planoLines.to_file('Total.shp')
    return

