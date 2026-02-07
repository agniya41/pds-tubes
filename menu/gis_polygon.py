import streamlit as st
import pandas as pd
import folium
import json
import os
import branca.colormap as cm
from streamlit_folium import st_folium

def app():
    st.markdown("## 🗺️ Peta GIS Kecelakaan Lalu Lintas per Provinsi")

    # =========================
    # 🔹 PATH FILE
    # =========================
    BASE_DIR = os.path.dirname(__file__)
    EXCEL_PATH = os.path.join(BASE_DIR, "../data/clean_lakalantas_new.xlsx")
    GEOJSON_PATH = os.path.join(BASE_DIR, "../data/provinsi_indonesia.json")


    # =========================
    # 🔹 LOAD DATA
    # =========================
    
    df = pd.read_excel(EXCEL_PATH)
    df["Provinsi"] = df["Provinsi"].str.upper().str.strip()
    
    data_provinsi = df.groupby("Provinsi").size().to_dict()
    
    st.caption(f"Total data kecelakaan: {len(df)}")
    st.caption(f"Jumlah provinsi terdata: {len(data_provinsi)}")
    
    ##dari agni ambil dan hitung berapa lakalantas setiap prov
    accident_counts = df['Provinsi'].value_counts().reset_index()
    accident_counts.columns = ['Provinsi', 'Jumlah_Kecelakaan']

    # normalisasi nama provisi (di lowercase semua nama prov nya )(agni)
    accident_counts['Provinsi_Lower'] = accident_counts['Provinsi'].str.lower()

    # =========================
    # 🔹 LOAD GEOJSON
    # =========================
    with open(GEOJSON_PATH, encoding="utf-8") as f:
        geojson_data = json.load(f)

    #nambahin isi geojson dengan banyak nya lakalantas per tahun(agni)
    for feature in geojson_data['features']:
        #untuk setiap isi geojson
        province_name = feature['properties']['PROVINSI'].lower()
        match = accident_counts[accident_counts['Provinsi_Lower'] == province_name]
        #apakah sama dengan prov isi accident_counts sama prov geojson
        if not match.empty:
            feature['properties']['Jumlah_Kecelakaan'] = int(match.iloc[0]['Jumlah_Kecelakaan'])
        else:
            feature['properties']['Jumlah_Kecelakaan'] = 0
        #kalau sama isi jumlah kecelakaannya kalau ngga ada isi nol

    
    # =========================
    # 🔹 BUAT PETA
    # =========================
    m = folium.Map(
        location=[-2.5, 118],
        zoom_start=5,
        tiles="cartodbpositron"
    )

    # =========================
    # 🔹 COLORMAP (MERAH MUDA → MERAH → MERAH GELAP)
    # =========================
    min_val = min(data_provinsi.values())
    max_val = max(data_provinsi.values())

    colormap = cm.LinearColormap(
        colors=["#ffc0cb", "#ff0000", "#8b0000"],
        vmin=min_val,
        vmax=max_val
    )
    colormap.caption = "Jumlah Kecelakaan Lalu Lintas"
    colormap.add_to(m)

    # =========================
    # 🔹 STYLE FUNCTION
    # =========================
    def style_function(feature):
        prov = feature["properties"]["PROVINSI"].upper().strip()
        jumlah = data_provinsi.get(prov, 0)

        return {
            "fillColor": colormap(jumlah) if jumlah > 0 else "#eeeeee",
            "color": "black",
            "weight": 0.6,
            "fillOpacity": 0.8,
        }
    

    # =========================
    # 🔹 POLYGON
    # =========================
    folium.GeoJson(
        geojson_data,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['PROVINSI', 'Jumlah_Kecelakaan'],
            aliases=['Provinsi:', 'jumlah lakalantas:'],
            sticky=True
        )
    ).add_to(m)

    # =========================
    # 🔹 TAMPILKAN DI STREAMLIT
    # =========================
    st_folium(m, width=1200, height=600)
