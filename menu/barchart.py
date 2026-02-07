import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def app():

    st.subheader("📊 Statistik Lakalantas Indonesia")

    df = pd.read_excel("data/clean_lakalantas_new.xlsx")
    df.columns = df.columns.str.lower().str.strip()

    df["provinsi"] = df["provinsi"].astype(str).str.lower().str.strip()
    df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce")
    df["isi berita"] = df["isi berita"].astype(str).str.lower()

    df = df.dropna(subset=["provinsi","tahun"])
    df["tahun"] = df["tahun"].astype(int)

    grouped = (
        df.groupby(["provinsi","tahun"])
        .size()
        .reset_index(name="jumlah")
    )

    all_years = list(range(2010,2027))
    provinsi_list = ["ALL Provinsi"] + sorted(grouped["provinsi"].unique())

    # ================= FILTER =================
    left,right = st.columns([2,1])

    with right:
        chart_type = st.selectbox("",["Provinsi dengan lakalantas terbanyak","Statistik Lakalantas di indonesia per tahun","Persentase kendaraan yang terlibat Lakalantas"],label_visibility="collapsed")

# ================= BAR =================
    if chart_type == "Provinsi dengan lakalantas terbanyak":

        prov_group = (
            grouped.groupby("provinsi")["jumlah"]
            .sum()
            .reset_index()
            .sort_values("jumlah", ascending=True)
        )

        fig = px.bar(
            prov_group,
            x="jumlah",
            y="provinsi",
            orientation="h",
            title="Total Kejadian Lakalantas per Provinsi (2010–2026)",
            height=700
        )


        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            margin=dict(l=60, r=40, t=60, b=40),
            yaxis_title="",
            xaxis_title="Jumlah Kejadian",
            font=dict(size=12)
        )

        st.plotly_chart(fig, use_container_width=True)

        top = prov_group.iloc[-1]     # terbesar
        bottom = prov_group.iloc[0]  # terkecil

        st.success(
            f"🔥 Provinsi tertinggi : {top['provinsi'].title()} "
            f"({int(top['jumlah'])} kejadian)"
        )

        st.warning(
            f"🧊 Provinsi terendah : {bottom['provinsi'].title()} "
            f"({int(bottom['jumlah'])} kejadian)"
        )
        st.markdown(
            "<center style='color:gray;font-size:13px;'>Sumber data: Dilansir dari detik.com</center>",
            unsafe_allow_html=True
        )


    # ================= LINE =================
    elif chart_type=="Statistik Lakalantas di indonesia per tahun":

        with left:
            prov = st.selectbox("",provinsi_list,label_visibility="collapsed")

        if prov=="ALL Provinsi":
            data = grouped.groupby("tahun")["jumlah"].sum().reset_index()
        else:
            data = grouped[grouped["provinsi"]==prov]

        data = pd.DataFrame({"tahun":all_years}).merge(data,on="tahun",how="left").fillna(0)

        fig = plt.figure(figsize=(7,3))
        plt.plot(data["tahun"],data["jumlah"],marker="o")
        plt.xticks(rotation=45,fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        max_row=data.loc[data["jumlah"].idxmax()]

        st.success(
            f"🔥 Tahun tertinggi : {int(max_row['tahun'])} "
            f"({int(max_row['jumlah'])} kejadian)"
        )

        st.info(f"""
    Wilayah : {prov.title()}  
    Total Kejadian : {int(data['jumlah'].sum())}  
    Periode : 2010–2026
    """)
    
        st.markdown(
                "<center style='color:gray;font-size:13px;'>Sumber data: Dilansir dari detik.com</center>",
                unsafe_allow_html=True
            )

    # ================= PIE =================
    else:

        tahun_list = sorted(df["tahun"].unique(), reverse=True)
        options = ["ALL (2010–2026)"] + tahun_list

        tahun = st.selectbox("",options,index=0,label_visibility="collapsed")

        if tahun!="ALL (2010–2026)":
            df_pie = df[df["tahun"]==tahun]
        else:
            df_pie = df.copy()

        motor = df_pie["isi berita"].str.contains("motor",na=False).sum()
        mobil = df_pie["isi berita"].str.contains("mobil",na=False).sum()
        truk  = df_pie["isi berita"].str.contains("truk",na=False).sum()
        bus   = df_pie["isi berita"].str.contains("bus",na=False).sum()

        labels=["Motor","Mobil","Truk","Bus"]
        values=[motor,mobil,truk,bus]

        filtered=[(l,v) for l,v in zip(labels,values) if v>0]

        if not filtered:
            st.warning("⚠️ Tidak ada data kendaraan.")
            return

        labels,values=zip(*filtered)

        total=sum(values)

        fig=plt.figure(figsize=(2.8,2.8))

        if len(values)==1:
            plt.pie([1])
            plt.text(0,0,f"{labels[0]}\n100%",ha="center",va="center",fontsize=14,fontweight="bold")
            kendaraan_max=labels[0]

        else:
            plt.pie(values,labels=labels,autopct="%1.1f%%",startangle=90)
            kendaraan_max=labels[list(values).index(max(values))]

        center=st.columns([2,3,2])[1]
        with center:
            st.pyplot(fig,use_container_width=False)

        plt.close(fig)

        st.success(f"🚗 Kendaraan terbanyak ({tahun}) : {kendaraan_max}")
        st.info(f"Total kejadian kendaraan : {total}")

        st.markdown(
            "<center style='color:gray;font-size:13px;'>Sumber data: Dilansir dari detik.com</center>",
            unsafe_allow_html=True
        )