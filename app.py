import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

df_test = pd.read_csv('data/arts_index.csv')
geo_data_merge = 'hangjeongdong_merge_last.geojson'

center = [37.541, 126.986]

m = folium.Map(location = center, zoom_start = 10)

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
    df_top = df_top.iloc[5:n]
    top = top[5:n]
    radius = 700
    color = 'crimson'
  else:
    radius = 1000
    color = 'pink'

  for i in range(5):
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

with st.sidebar:
    button = st.radio('크기 순으로 보기', ['Top 10 Large Communities', 'Top 5 Large Communities'])
    if button == 'Top 10 Large Communities':
      makeMarker(10)
      st.experimental_rerun()
    elif button == 'Top 5 Large Communities':
      makeMarker(5)
      st.experimental_rerun()
st_data = st_folium(m, width=3000)



