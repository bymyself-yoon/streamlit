import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

df_test = pd.read_csv('data/arts_index.csv')
geo_data_merge = 'hangjeongdong_merge_last.geojson'

center = [37.541, 126.986]

m = folium.Map(location = center, zoom_start = 10)
click = folium.LatLngPopup()
click.add_to(m)

def on_map_click(event):
    lat, lon = event['location']
    st.sidebar.write(f'클릭 위치의 위도: {lat}, 경도: {lon}')

folium.Choropleth(
    geo_data = geo_data_merge,
    data = df_test,
    columns = ('구', 'arts_index'),
    key_on = 'feature.properties.sggnm',
    fill_color = 'BuPu',
    legend_name = '문화예술지수',
).add_to(m)

tiles = "CartoDB positron"
folium.TileLayer(tiles=tiles).add_to(m)

def geocoding(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd

def getTop(n):
  top = df_test['arts_index'].sort_values(ascending=False).iloc[0:n]
  df_top = df_test.iloc[top.index]

  result = []
  for i in range(n):
    if df_top.index[i] > 15:
      jiyeok = "서울"
    else:
      jiyeok = "부산"

    geo = jiyeok + " " + df_top['구'].values.tolist()[i]
    crd = geocoding(geo)
    result.append([crd['lat'], crd['lng']])

  return (result, df_top)

def makeMarker(n):
  top, df_top = getTop(n)

  if n == 10:
    df_top = df_top.iloc[0:n]
    top = top[0:n]
    radius = 700
    color = 'crimson'
  else:
    radius = 1000
    color = 'pink'

  for i in range(n):
    folium.Circle(
        location=top[i],
        radius = radius,
        popup=df_top['구'].values.tolist()[i],
        color = color,
        fill = True,
        fill_color = color,
        fill_opacity=100,
    ).add_to(m)

st.sidebar.title("The Arts Vibrancy in Busan & Seoul")

def mapMarker():
    mk = st.session_state.marker
    if mk == "Top 10":
        makeMarker(10)
    elif mk == "Top 5":
        makeMarker(5)
    
with st.sidebar:
    if st.checkbox('Top 10 Large Communities'):
        st.session_state.marker = "Top 10"
        mapMarker()
    if st.checkbox('Top 5 Large Communities'):
        st.session_state.marker = "Top 5"
        mapMarker()

st_folium(m, width=1000, returned_objects=[])


    

   


