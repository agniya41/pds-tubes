import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

def app():
    # Judul Dan Impor Data
    df = pd.read_excel("data/clean_lakalantas_new.xlsx")
    st.title("Informasi Lakalantas dari Detik.com")
    st.markdown("---")

    # Data Yang Dipakai
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Data yang Dipakai", len(df), delta=None)
    with col2:
        st.metric("Jumlah Provinsi", len(df['Provinsi'].unique()), delta=None)
    with col3:
        st.metric(
            "Range Tahun Data",
            f"{df['Tahun'].min()}-{df['Tahun'].max()}",
            delta=None
        )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Headline yang Paling Sering Dipakai**")

        # Ambil Semua Teks Headline
        all_text = ' '.join(df['Headline'].str.lower()).split()

        # Filter Kata Penghubung / Umum
        stopwords = {
            'usai', 'dan', 'di', 'ke', 'dari',
            'oleh', 'yang', 'untuk', 'dengan',
            'adalah', 'dalam'
        }

        # Ambil Kata Kunci
        keywords = [w for w in all_text if len(w) > 3 and w not in stopwords]

        # Ambil Kata Terbanyak
        top_keywords = Counter(keywords).most_common(10)

        # Masukkan ke DataFrame
        keywords_df = pd.DataFrame(
            top_keywords,
            columns=['kata_kunci', 'frekuensi']
        )

        fig_keywords = px.bar(
            keywords_df,
            x='frekuensi',
            y='kata_kunci',
            orientation='h',
            title='Kata Kunci Terbanyak',
            color='frekuensi',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig_keywords, use_container_width=True)

    with col2:
        st.write("**Beberapa Judul Berita yang Ada**")
        sample_headlines = df['Headline'].sample(min(10, len(df)))
        for i, headline in enumerate(sample_headlines, 1):
            st.write(f"{i}. {headline}")

    st.markdown("---")
    st.subheader("Ekspor Semua Data")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    # Impor Data Rekap
    df2 = pd.read_excel("data/rekap_kasus_per_provinsi.xlsx")

    # Ekspor Data Scraping
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Data Scraping",
            data=csv,
            mime="text/csv"
        )

    # Lihat Data
    with col2:
        if st.button("Lihat Data Scraping"):
            st.dataframe(df, use_container_width=True)

    # Download Rekap Data
    with col3:
        csv = df2.to_csv(index=False)
        st.download_button(
            label="Download Rekap Data per Provinsi",
            data=csv,
            mime="text/csv"
        )

