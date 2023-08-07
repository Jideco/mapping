#WEB MAPPING WITH PYTHON AND FOLIUM
#A BASE LAYER A POLYGON LAYER A MARKER LAYER
import folium
import pandas

data = pandas.read_csv("Volcanoes.txt") #store the volcanoes in data
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
<h4>Volcano information:</h4><br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def colorProducer(elevation):#A function that returns color as the number increases
    if elevation < 1500:
        return 'green'
    elif 1500 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes") #layer 1

for lt,ln,ev,name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, ev), width= 200, height= 80)
    fgv.add_child(folium.CircleMarker(location=[lt,ln],radius=6, popup= folium.Popup(iframe),
    fill_color = colorProducer(ev), color = 'grey', fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population") #layer 2

fgp.add_child(folium.GeoJson(data=open('world.json', 'r' ,encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv) #Add layer1 to map
map.add_child(fgp) #Add layer2 to map

map.add_child(folium.LayerControl()) #Add a control panel

map.save("Map1.html") #Save