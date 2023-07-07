import streamlit as st
import folium
from streamlit_folium import st_folium

m = folium.Map(location = center, zoom_start = 10)
st_data = st_folium(m, width=725)

st.sidebar.title("The Arts Vibrancy in Busan & Seoul")

if st.button("Top 10 Large Communities"):
  makeMarker(10)
elif st.button("Top 5 Large Communities"):
  makeMarker(5)

st.title("This is Title")
