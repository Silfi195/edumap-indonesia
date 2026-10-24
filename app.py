import os
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# =========================
# KONFIGURASI
# =========================
st.set_page_config(
    page_title="EduMap Indonesia",
    page_icon="🗺️",
    layout="wide"
)


# DESAIN DASHBOARD EDUMAP INDONESIA
st.markdown("""
<style>
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    h1 {
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        font-weight: 650;
    }

    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.22);
        padding: 16px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        font-weight: 700;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div.stDownloadButton) {
        margin-top: 8px;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.2);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# MEMUAT DATA
# =========================
@st.cache_data
def load_data():
    lokasi_file = (
        "/content/data_edumap.csv"
        if os.path.exists("/content/data_edumap.csv")
        else "data_edumap.csv"
    )

    df = pd.read_csv(lokasi_file)
    df["Provinsi"] = df["Provinsi"].astype(str).str.strip().str.upper()
    df["Cluster"] = df["Cluster"].astype(str)

    kolom_numerik = [
        "IPM",
        "Tidak_Belum_Pernah_Sekolah",
        "Masih_Bersekolah",
        "Tidak_Sekolah_Lagi",
        "Rumah_Sendiri",
        "Bukan_Rumah_Sendiri",
        "Kantor",
        "Sekolah",
        "Tempat_Umum",
        "Kendaraan_Berjalan"
    ]

    for kolom in kolom_numerik:
        df[kolom] = pd.to_numeric(df[kolom], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Data gagal dimuat: {e}")
    st.info(
        "Pastikan data_edumap.csv tersedia di /content "
        "dan berisi kolom hasil pengolahan data."
    )
    st.stop()

kolom_wajib = [
    "Provinsi", "Cluster", "IPM",
    "Tidak_Belum_Pernah_Sekolah",
    "Masih_Bersekolah", "Tidak_Sekolah_Lagi",
    "Rumah_Sendiri", "Bukan_Rumah_Sendiri",
    "Kantor", "Sekolah", "Tempat_Umum",
    "Kendaraan_Berjalan"
]

kolom_hilang = [k for k in kolom_wajib if k not in df.columns]

if kolom_hilang:
    st.error(f"Kolom berikut tidak ditemukan: {kolom_hilang}")
    st.stop()

# =========================
# KOORDINAT PERKIRAAN PROVINSI
# =========================
koordinat = {
    "ACEH": (4.7, 96.7),
    "SUMATERA UTARA": (2.5, 99.0),
    "SUMATERA BARAT": (-0.7, 100.4),
    "RIAU": (0.5, 101.8),
    "JAMBI": (-1.6, 103.6),
    "SUMATERA SELATAN": (-3.0, 104.7),
    "BENGKULU": (-3.8, 102.3),
    "LAMPUNG": (-4.9, 105.0),
    "KEPULAUAN BANGKA BELITUNG": (-2.2, 106.1),
    "KEPULAUAN RIAU": (3.9, 108.2),
    "DKI JAKARTA": (-6.2, 106.8),
    "JAWA BARAT": (-6.9, 107.6),
    "JAWA TENGAH": (-7.2, 110.1),
    "DI YOGYAKARTA": (-7.8, 110.4),
    "JAWA TIMUR": (-7.7, 112.5),
    "BANTEN": (-6.4, 106.1),
    "BALI": (-8.4, 115.2),
    "NUSA TENGGARA BARAT": (-8.7, 117.4),
    "NUSA TENGGARA TIMUR": (-9.5, 120.0),
    "KALIMANTAN BARAT": (0.0, 110.0),
    "KALIMANTAN TENGAH": (-1.6, 113.5),
    "KALIMANTAN SELATAN": (-3.0, 115.4),
    "KALIMANTAN TIMUR": (0.5, 116.5),
    "KALIMANTAN UTARA": (3.0, 116.2),
    "SULAWESI UTARA": (1.3, 124.8),
    "SULAWESI TENGAH": (-1.4, 121.4),
    "SULAWESI SELATAN": (-3.7, 119.9),
    "SULAWESI TENGGARA": (-4.0, 122.5),
    "GORONTALO": (0.6, 123.0),
    "SULAWESI BARAT": (-2.5, 119.3),
    "MALUKU": (-3.2, 129.0),
    "MALUKU UTARA": (1.5, 127.8),
    "PAPUA BARAT": (-1.3, 133.5),
    "PAPUA BARAT DAYA": (-1.1, 132.0),
    "PAPUA": (-4.0, 138.5),
    "PAPUA SELATAN": (-7.5, 139.5),
    "PAPUA TENGAH": (-3.5, 136.5),
    "PAPUA PEGUNUNGAN": (-4.0, 139.0)
}

df["Koordinat"] = df["Provinsi"].map(koordinat)


import streamlit as st
import base64

# Baca foto banner
with open("/content/Pendidkan indonesia.png", "rb") as file:
    foto = base64.b64encode(file.read()).decode()

# Banner dengan tulisan langsung di atas gambar
st.markdown(
    f"""
    <div style="
        position: relative;
        width: 100%;
        height: 280px;
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 20px;
    ">
        <img src="data:image/png;base64,{foto}"
             style="
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
             ">
        <div style="
            position: absolute;
            inset: 0;
            background: linear-gradient(
                90deg,
                rgba(5, 28, 57, 0.78),
                rgba(5, 28, 57, 0.12)
            );
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 35px;
        ">
            <div style="
                color: white;
                font-size: 16px;
                letter-spacing: 4px;
                font-weight: 600;
            ">WELCOME TO OUR WEB</div>
            <div style="
                color: white;
                font-size: 36px;
                font-weight: 800;
                margin-top: 10px;
            ">EduMap Indonesia</div>
            <div style="
                color: white;
                font-size: 15px;
                margin-top: 8px;
            ">Dashboard Peta Pendidikan Digital Indonesia</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# MENU NAVIGASI
# =========================

menu_halaman = [
    "Beranda",
    "Profil Provinsi",
    "Analisis Data",
    "Analisis Cluster",
    "Perbandingan Provinsi",
    "Rekomendasi",
    "Data dan Unduhan"
]

if "halaman_aktif" not in st.session_state:
    st.session_state["halaman_aktif"] = "Beranda"

# Desain tombol navigasi
st.markdown("""
<style>
/* Tampilan tombol navigasi */
div[data-testid="stHorizontalBlock"] div.stButton > button {
    background-color: #123B66;
    color: white;
    border: 1px solid #123B66;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    min-height: 43px;
    padding: 5px 6px;
    white-space: normal;
}

div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
    background-color: #2878B5;
    color: white;
    border-color: #2878B5;
}

div[data-testid="stHorizontalBlock"] div.stButton > button:focus {
    background-color: #2878B5;
    color: white;
    border: 2px solid #7DB8F0;
    box-shadow: none;
}
</style>
""", unsafe_allow_html=True)

# Tujuh menu navigasi
kolom_menu = st.columns(7, gap="small")

for i, nama_menu in enumerate(menu_halaman):
    with kolom_menu[i]:
        if st.button(
            nama_menu,
            key=f"nav_{i}",
            use_container_width=True
        ):
            st.session_state["halaman_aktif"] = nama_menu
            st.rerun()

# Halaman aktif
halaman = st.session_state["halaman_aktif"]

st.divider()



st.sidebar.markdown("---")
st.sidebar.caption("Sumber indikator: BPS 2024")

st.info(
    "Cluster merupakan hasil pengelompokan statistik, bukan "
    "peringkat resmi pendidikan."
)

# Filter provinsi untuk halaman yang membutuhkan pilihan
daftar_provinsi = sorted(df["Provinsi"].dropna().unique())

if not daftar_provinsi:
    st.error("Data provinsi tidak ditemukan.")
    st.stop()

if "provinsi_pilihan" not in st.session_state:
    st.session_state["provinsi_pilihan"] = daftar_provinsi[0]

if st.session_state["provinsi_pilihan"] not in daftar_provinsi:
    st.session_state["provinsi_pilihan"] = daftar_provinsi[0]

provinsi = st.sidebar.selectbox(
    "Pilih provinsi",
    daftar_provinsi,
    key="provinsi_pilihan"
)

data = df[df["Provinsi"] == provinsi].iloc[0]
ipm_rata = df["IPM"].mean()
# =========================
# PROFIL TIM DEVELOPER
# =========================
st.sidebar.markdown("---")
st.sidebar.markdown("### 👩‍💻 Our Developer Team")

anggota_tim = [
    {
        "nama": "Irman Wahyudi",
        "nim": "24337008",
        "prodi": "S1 Statistika",
        "fakultas": "FMIPA",
        "universitas": "Universitas Negeri Padang",
        "foto": "/content/Irman.jpeg"
    },
    {
        "nama": "Silfi Zona Sakinah",
        "nim": "24337020",
        "prodi": "S1 Statistika",
        "fakultas": "FMIPA",
        "universitas": "Universitas Negeri Padang",
        "foto": "/content/Silfi.jpeg"
    },
    {
        "nama": "Cahaya Stevany Putri",
        "nim": "24337053",
        "prodi": "S1 Statistika",
        "fakultas": "FMIPA",
        "universitas": "Universitas Negeri Padang",
        "foto": "/content/Cahaya.jpeg"
    }
]

with st.sidebar.expander("Lihat Profil Anggota", expanded=False):
    for anggota in anggota_tim:
        st.image(anggota["foto"], use_container_width=True)
        st.markdown(f"### {anggota['nama']}")
        st.write(f"**{anggota['nim']}**")
        st.write(anggota["prodi"])
        st.write(anggota["fakultas"])
        st.write(anggota["universitas"])
        st.markdown("---")
# =========================
# HALAMAN BERANDA
# =========================

# =========================
# PETA INDONESIA INTERAKTIF
# =========================

if halaman == "Beranda":
    st.subheader("Peta Pendidikan Digital Indonesia")

    st.write(
        "Klik titik provinsi pada peta untuk melihat "
        "informasi IPM, cluster, dan indikatornya."
    )

    # Salin data agar data utama tidak berubah
    data_peta = df.copy()

    # Normalisasi nama provinsi
    data_peta["Nama_Peta"] = (
        data_peta["Provinsi"].astype(str).str.strip().str.upper()
    )

    data_peta["Koordinat_Peta"] = data_peta["Nama_Peta"].map(
        koordinat
    )

    data_peta = data_peta.dropna(subset=["Koordinat_Peta"])

    # Pusat peta Indonesia
    peta = folium.Map(
        location=[-2.5, 118],
        zoom_start=4,
        tiles="OpenStreetMap",
        control_scale=True
    )

    # Warna untuk cluster
    warna_cluster = {
        0: "#2878B5",
        1: "#E67E22"
    }

    # Tambahkan titik provinsi
    for _, baris in data_peta.iterrows():
        lat, lon = baris["Koordinat_Peta"]

        nama = str(baris["Provinsi"])
        ipm = pd.to_numeric(baris["IPM"], errors="coerce")
        cluster = baris["Cluster"]

        try:
            cluster_int = int(cluster)
            warna = warna_cluster.get(cluster_int, "#7B61A8")
            label_cluster = str(cluster_int)
        except (ValueError, TypeError):
            warna = "#7B61A8"
            label_cluster = str(cluster)

        nilai_ipm = (
            f"{ipm:.2f}" if pd.notna(ipm) else "Tidak tersedia"
        )

        popup_html = f"""
        <div style="font-family: Arial; width: 190px;">
            <h4 style="margin-bottom: 8px;">{nama}</h4>
            <p style="margin: 4px 0;">IPM: <b>{nilai_ipm}</b></p>
            <p style="margin: 4px 0;">
                Cluster: <b>{label_cluster}</b>
            </p>
            <p style="font-size: 11px; color: #666;">
                Koordinat merupakan titik perkiraan provinsi.
            </p>
        </div>
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=warna,
            weight=2,
            fill=True,
            fill_color=warna,
            fill_opacity=0.85,
            tooltip=nama,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(peta)

    # Legenda cluster
    legenda = """
    <div style="
        position: fixed;
        bottom: 25px;
        left: 25px;
        z-index: 9999;
        background-color: white;
        padding: 10px 13px;
        border: 1px solid #cccccc;
        border-radius: 8px;
        font-size: 13px;
        color: #222222;
    ">
        <b>Legenda Cluster</b><br>
        <span style="color:#2878B5;">●</span> Cluster 0<br>
        <span style="color:#E67E22;">●</span> Cluster 1<br>
        <span style="color:#7B61A8;">●</span>
        Cluster lainnya / tidak diketahui
    </div>
    """

    peta.get_root().html.add_child(
        folium.Element(legenda)
    )

    # Tampilkan peta
    hasil_peta = st_folium(
        peta,
        width=None,
        height=520,
        key="peta_interaktif_edumap",
        returned_objects=["last_object_clicked"]
    )

    # Informasi detail titik yang diklik
    titik_diklik = (
        hasil_peta.get("last_object_clicked")
        if hasil_peta
        else None
    )

    if titik_diklik and not data_peta.empty:
        lat_klik = titik_diklik.get("lat")
        lon_klik = titik_diklik.get("lng")

        if lat_klik is not None and lon_klik is not None:
            data_peta["Jarak_Klik"] = data_peta[
                "Koordinat_Peta"
            ].apply(
                lambda titik: (
                    (titik[0] - lat_klik) ** 2
                    + (titik[1] - lon_klik) ** 2
                )
            )

            provinsi_klik = data_peta.loc[
                data_peta["Jarak_Klik"].idxmin()
            ]

            st.divider()
            st.subheader(
                f"Informasi Provinsi: {provinsi_klik['Provinsi']}"
            )

            nilai_ipm = pd.to_numeric(
                provinsi_klik["IPM"], errors="coerce"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Indeks Pembangunan Manusia (IPM)",
                    f"{nilai_ipm:.2f}"
                    if pd.notna(nilai_ipm)
                    else "Tidak tersedia"
                )

            with col2:
                st.metric(
                    "Cluster",
                    str(provinsi_klik["Cluster"])
                )

            kolom_detail = [
                "Tidak_Belum_Pernah_Sekolah",
                "Masih_Bersekolah",
                "Tidak_Sekolah_Lagi",
                "Rumah_Sendiri",
                "Bukan_Rumah_Sendiri",
                "Kantor",
                "Sekolah",
                "Tempat_Umum",
                "Kendaraan_Berjalan"
            ]

            label_detail = {
                "Tidak_Belum_Pernah_Sekolah":
                    "Tidak/belum pernah sekolah",
                "Masih_Bersekolah": "Masih bersekolah",
                "Tidak_Sekolah_Lagi": "Tidak sekolah lagi",
                "Rumah_Sendiri": "Rumah sendiri",
                "Bukan_Rumah_Sendiri": "Rumah bukan milik sendiri",
                "Kantor": "Kantor",
                "Sekolah": "Sekolah",
                "Tempat_Umum": "Tempat umum",
                "Kendaraan_Berjalan": "Kendaraan berjalan"
            }

            detail_tersedia = [
                kolom for kolom in kolom_detail
                if kolom in df.columns
            ]

            tabel_detail = pd.DataFrame({
                "Indikator": [
                    label_detail[kolom]
                    for kolom in detail_tersedia
                ],
                "Nilai": [
                    provinsi_klik[kolom]
                    for kolom in detail_tersedia
                ]
            })

            st.dataframe(
                tabel_detail,
                use_container_width=True,
                hide_index=True
            )

    st.caption(
        "Catatan: titik peta menunjukkan lokasi perkiraan, "
        "bukan batas administratif provinsi. Warna menunjukkan "
        "hasil cluster, bukan peringkat kualitas pendidikan."
    )

    st.divider()
   

    # Memastikan dataset tersedia
    if df.empty:
        st.warning("Dataset belum memiliki data.")
    else:
        # Ringkasan utama
        jumlah_provinsi = df["Provinsi"].nunique()
        rata_ipm = pd.to_numeric(
            df["IPM"], errors="coerce"
        ).mean()

        jumlah_cluster = df["Cluster"].nunique()
        jumlah_c0 = (df["Cluster"] == 0).sum()
        jumlah_c1 = (df["Cluster"] == 1).sum()

        st.subheader("Ringkasan Data Nasional")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Jumlah Provinsi",
            f"{jumlah_provinsi}"
        )

        c2.metric(
            "Rata-rata IPM",
            f"{rata_ipm:.2f}" if pd.notna(rata_ipm) else "-"
        )

        c3.metric(
            "Jumlah Cluster",
            f"{jumlah_cluster}"
        )

        c4.metric(
            "Jumlah Indikator",
            f"{len([
                col for col in df.columns
                if col not in ["Provinsi", "Cluster"]
            ])}"
        )

        st.divider()

        # Distribusi cluster
        st.subheader("Distribusi Provinsi per Cluster")

        distribusi = (
            df.groupby("Cluster")["Provinsi"]
            .nunique()
            .sort_index()
        )

        distribusi_df = distribusi.rename(
            "Jumlah Provinsi"
        ).to_frame()

        st.bar_chart(distribusi_df)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Provinsi di Cluster 0", int(jumlah_c0))

        with col2:
            st.metric("Provinsi di Cluster 1", int(jumlah_c1))

        st.caption(
            "Cluster merupakan hasil pengelompokan statistik "
            "K-Means, bukan peringkat resmi pendidikan."
        )

        st.divider()

        # Provinsi dengan IPM tertinggi dan terendah
        st.subheader("Gambaran IPM Antarprovinsi")

        data_ipm = df.copy()
        data_ipm["IPM"] = pd.to_numeric(
            data_ipm["IPM"], errors="coerce"
        )
        data_ipm = data_ipm.dropna(subset=["IPM"])

        if not data_ipm.empty:
            prov_ipm_tertinggi = data_ipm.loc[
                data_ipm["IPM"].idxmax()
            ]
            prov_ipm_terendah = data_ipm.loc[
                data_ipm["IPM"].idxmin()
            ]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**IPM Tertinggi dalam Dataset**")
                st.write(
                    str(prov_ipm_tertinggi["Provinsi"])
                )
                st.metric(
                    "Nilai IPM",
                    f"{prov_ipm_tertinggi['IPM']:.2f}"
                )

            with col2:
                st.markdown("**IPM Terendah dalam Dataset**")
                st.write(
                    str(prov_ipm_terendah["Provinsi"])
                )
                st.metric(
                    "Nilai IPM",
                    f"{prov_ipm_terendah['IPM']:.2f}"
                )

            st.bar_chart(
                data_ipm.set_index("Provinsi")[["IPM"]]
                .sort_values("IPM", ascending=False)
                .head(10)
            )

            st.caption(
                "Grafik menunjukkan 10 provinsi dengan nilai IPM "
                "tertinggi berdasarkan dataset yang digunakan."
            )

        st.divider()

        # Temuan otomatis
        st.subheader("Temuan Awal")

        st.write(
            f"Dataset mencakup {jumlah_provinsi} provinsi "
            f"dengan rata-rata IPM sebesar "
            f"{rata_ipm:.2f}."
            if pd.notna(rata_ipm)
            else f"Dataset mencakup {jumlah_provinsi} provinsi."
        )

        if jumlah_cluster == 2:
            st.write(
                f"Hasil pengelompokan membagi data menjadi "
                f"dua cluster: Cluster 0 berisi {jumlah_c0} "
                f"provinsi dan Cluster 1 berisi {jumlah_c1} provinsi."
            )
        else:
            st.write(
                f"Dataset memiliki {jumlah_cluster} kelompok "
                f"(cluster) hasil pengelompokan."
            )

        st.info(
            "Interpretasi: IPM dan lokasi penggunaan internet "
            "merupakan indikator yang membantu menggambarkan "
            "karakteristik provinsi. Indikator tersebut tidak "
            "secara langsung mengukur kualitas internet di sekolah "
            "atau mutu pembelajaran. Temuan ini bersifat deskriptif "
            "dan perlu ditafsirkan sesuai definisi data sumber."
        )

        st.divider()

        st.subheader("Jelajahi Dashboard")

        st.write(
            "Gunakan menu di sebelah kiri untuk membuka profil "
            "provinsi, analisis data, analisis cluster, perbandingan "
            "provinsi, rekomendasi, dan data yang tersedia."
        )

# =========================
# HALAMAN PROFIL PROVINSI
# =========================
elif halaman == "Profil Provinsi":
    st.header("Profil Provinsi")
    st.subheader(provinsi)

    c1, c2, c3 = st.columns(3)
    c1.metric("Indeks Pembangunan Manusia", f"{data['IPM']:.2f}")
    c2.metric("Cluster K-Means", str(data["Cluster"]))
    c3.metric(
        "Masih Bersekolah (%)",
        f"{data['Masih_Bersekolah']:.2f}%"
    )

    selisih = float(data["IPM"] - ipm_rata)

    st.markdown("### Perbandingan IPM")
    pembanding = pd.DataFrame({
        "Wilayah": [provinsi, "Rata-rata 38 Provinsi"],
        "IPM": [float(data["IPM"]), float(ipm_rata)]
    })

    st.bar_chart(pembanding.set_index("Wilayah"), y="IPM")

    if selisih > 0:
        st.write(
            f"IPM provinsi ini {selisih:.2f} poin di atas "
            "rata-rata provinsi dalam dataset."
        )
    elif selisih < 0:
        st.write(
            f"IPM provinsi ini {abs(selisih):.2f} poin di bawah "
            "rata-rata provinsi dalam dataset."
        )
    else:
        st.write("IPM provinsi ini sama dengan rata-rata dataset.")

    st.markdown("### Indikator penggunaan internet")

    indikator = {
        "Tidak/Belum Pernah Sekolah": "Tidak_Belum_Pernah_Sekolah",
        "Masih Bersekolah": "Masih_Bersekolah",
        "Tidak Sekolah Lagi": "Tidak_Sekolah_Lagi",
        "Rumah Sendiri": "Rumah_Sendiri",
        "Bukan Rumah Sendiri": "Bukan_Rumah_Sendiri",
        "Kantor": "Kantor",
        "Sekolah": "Sekolah",
        "Tempat Umum": "Tempat_Umum",
        "Kendaraan Berjalan": "Kendaraan_Berjalan"
    }

    detail = pd.DataFrame({
        "Indikator": list(indikator.keys()),
        "Nilai (%)": [data[k] for k in indikator.values()]
    })

    st.bar_chart(detail.set_index("Indikator"), y="Nilai (%)")
    st.dataframe(detail, use_container_width=True, hide_index=True)

    st.caption(
        "Persentase mengikuti definisi tabel BPS tentang penggunaan "
        "internet menurut status sekolah atau lokasi akses; bukan "
        "pengukuran langsung kualitas internet sekolah."
    )

# =========================
# HALAMAN ANALISIS DATA
# =========================
elif halaman == "Analisis Data":
    st.header("Analisis Data")

    st.markdown("### Distribusi IPM antarprovinsi")
    ipm_df = (
        df[["Provinsi", "IPM"]]
        .dropna()
        .sort_values("IPM", ascending=False)
        .set_index("Provinsi")
    )
    st.bar_chart(ipm_df, y="IPM", height=500)

    st.markdown("### IPM dan penggunaan internet di sekolah")
    scatter_df = df[["Provinsi", "IPM", "Sekolah"]].dropna()
    st.scatter_chart(
        scatter_df,
        x="IPM",
        y="Sekolah",
        height=400
    )

    st.write(
        "Grafik ini digunakan untuk mengamati pola hubungan IPM "
        "dengan indikator penggunaan internet di sekolah. Pola "
        "hubungan tidak dengan sendirinya membuktikan sebab-akibat."
    )

    st.markdown("### Ringkasan statistik")
    st.dataframe(
        df[["IPM", "Rumah_Sendiri", "Sekolah",
            "Tempat_Umum", "Masih_Bersekolah"]].describe().T,
        use_container_width=True
    )

# =========================
# HALAMAN ANALISIS CLUSTER
# =========================
elif halaman == "Analisis Cluster":
    st.header("Analisis Cluster K-Means")

    st.write(
        "Halaman ini membandingkan karakteristik Cluster 0 dan Cluster 1 "
        "berdasarkan rata-rata IPM dan indikator penggunaan internet."
    )

    # Kolom yang digunakan untuk perbandingan
    kolom_indikator = [
        "IPM",
        "Tidak_Belum_Pernah_Sekolah",
        "Masih_Bersekolah",
        "Tidak_Sekolah_Lagi",
        "Rumah_Sendiri",
        "Bukan_Rumah_Sendiri",
        "Kantor",
        "Sekolah",
        "Tempat_Umum",
        "Kendaraan_Berjalan"
    ]

    # Menghitung rata-rata indikator setiap cluster
    ringkasan = (
        df.groupby("Cluster")[kolom_indikator]
        .mean()
        .round(2)
    )

    # Pastikan kedua cluster tersedia
    if "0" not in ringkasan.index or "1" not in ringkasan.index:
        st.warning(
            "Data harus memiliki Cluster 0 dan Cluster 1 "
            "agar perbandingan dapat ditampilkan."
        )
    else:
        # Ringkasan jumlah anggota
        jumlah = (
            df.groupby("Cluster")
            .size()
            .reindex(["0", "1"], fill_value=0)
        )

        col1, col2 = st.columns(2)

        col1.metric("Jumlah Provinsi Cluster 0", int(jumlah["0"]))
        col2.metric("Jumlah Provinsi Cluster 1", int(jumlah["1"]))

        st.markdown("---")

        # GRAFIK 1: PERBANDINGAN RATA-RATA IPM
        st.subheader("1. Perbandingan Rata-rata IPM")

        grafik_ipm = ringkasan[["IPM"]].rename(
            index={"0": "Cluster 0", "1": "Cluster 1"}
        )

        st.bar_chart(
            grafik_ipm,
            y="IPM",
            height=300
        )

        selisih_ipm = (
            ringkasan.loc["0", "IPM"]
            - ringkasan.loc["1", "IPM"]
        )

        if selisih_ipm > 0:
            st.write(
                f"Rata-rata IPM Cluster 0 lebih tinggi "
                f"{selisih_ipm:.2f} poin dibandingkan Cluster 1."
            )
        elif selisih_ipm < 0:
            st.write(
                f"Rata-rata IPM Cluster 1 lebih tinggi "
                f"{abs(selisih_ipm):.2f} poin dibandingkan Cluster 0."
            )
        else:
            st.write(
                "Rata-rata IPM kedua cluster sama berdasarkan "
                "pembulatan dua angka desimal."
            )

        st.markdown("---")

        # GRAFIK 2: INDIKATOR PARTISIPASI SEKOLAH
        st.subheader("2. Perbandingan Indikator Menurut Status Sekolah")

        indikator_sekolah = [
            "Tidak_Belum_Pernah_Sekolah",
            "Masih_Bersekolah",
            "Tidak_Sekolah_Lagi"
        ]

        nama_sekolah = {
            "Tidak_Belum_Pernah_Sekolah": "Tidak/Belum Pernah Sekolah",
            "Masih_Bersekolah": "Masih Bersekolah",
            "Tidak_Sekolah_Lagi": "Tidak Sekolah Lagi"
        }

        grafik_sekolah = ringkasan[indikator_sekolah].T
        grafik_sekolah.index = [
            nama_sekolah[k] for k in grafik_sekolah.index
        ]
        grafik_sekolah.columns = [
            f"Cluster {c}" for c in grafik_sekolah.columns
        ]

        st.bar_chart(
            grafik_sekolah,
            height=350
        )

        st.markdown("---")

        # GRAFIK 3: INDIKATOR LOKASI AKSES INTERNET
        st.subheader("3. Perbandingan Lokasi Akses Internet")

        indikator_lokasi = [
            "Rumah_Sendiri",
            "Bukan_Rumah_Sendiri",
            "Kantor",
            "Sekolah",
            "Tempat_Umum",
            "Kendaraan_Berjalan"
        ]

        nama_lokasi = {
            "Rumah_Sendiri": "Rumah Sendiri",
            "Bukan_Rumah_Sendiri": "Bukan Rumah Sendiri",
            "Kantor": "Kantor",
            "Sekolah": "Sekolah",
            "Tempat_Umum": "Tempat Umum",
            "Kendaraan_Berjalan": "Kendaraan Berjalan"
        }

        grafik_lokasi = ringkasan[indikator_lokasi].T
        grafik_lokasi.index = [
            nama_lokasi[k] for k in grafik_lokasi.index
        ]
        grafik_lokasi.columns = [
            f"Cluster {c}" for c in grafik_lokasi.columns
        ]

        st.bar_chart(
            grafik_lokasi,
            height=400
        )

        st.markdown("---")

        # TABEL PERBANDINGAN NILAI AKTUAL
        st.subheader("4. Tabel Perbandingan Rata-rata")

        tabel_perbandingan = ringkasan.T.rename(
            columns={
                "0": "Cluster 0",
                "1": "Cluster 1"
            }
        )

        tabel_perbandingan.index.name = "Indikator"
        st.dataframe(
            tabel_perbandingan,
            use_container_width=True
        )

        # ANGGOTA CLUSTER
        st.markdown("---")
        st.subheader("5. Daftar Provinsi dalam Setiap Cluster")

        cluster_dipilih = st.selectbox(
            "Pilih cluster untuk melihat anggotanya",
            ["0", "1"],
            format_func=lambda x: f"Cluster {x}"
        )

        anggota = df.loc[
            df["Cluster"] == cluster_dipilih,
            ["Provinsi", "IPM", "Cluster"]
        ].sort_values(
            "IPM",
            ascending=False
        )

        st.dataframe(
            anggota,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Interpretasi: grafik menunjukkan rata-rata indikator "
            "masing-masing kelompok. Nilai lebih tinggi tidak selalu "
            "berarti kondisi pendidikan lebih baik. Makna setiap indikator "
            "harus mengikuti definisi tabel sumber BPS."
        )

# HALAMAN PERBANDINGAN DUA PROVINSI
elif halaman == "Perbandingan Provinsi":
    st.title("Perbandingan Dua Provinsi")
    st.write(
        "Bandingkan indikator pembangunan manusia, "
        "partisipasi sekolah, dan lokasi akses internet "
        "antara dua provinsi di Indonesia."
    )

    # Memastikan data memiliki kolom yang dibutuhkan
    kolom_wajib = [
        "Provinsi",
        "IPM",
        "Tidak_Belum_Pernah_Sekolah",
        "Masih_Bersekolah",
        "Tidak_Sekolah_Lagi",
        "Rumah_Sendiri",
        "Bukan_Rumah_Sendiri",
        "Kantor",
        "Sekolah",
        "Tempat_Umum",
        "Kendaraan_Berjalan",
        "Cluster"
    ]

    kolom_tersedia = [
        kolom for kolom in kolom_wajib
        if kolom in df.columns
    ]

    kolom_tidak_ada = [
        kolom for kolom in kolom_wajib
        if kolom not in df.columns
    ]

    if kolom_tidak_ada:
        st.error(
            "Beberapa kolom belum ditemukan pada dataset: "
            + ", ".join(kolom_tidak_ada)
        )

    elif df["Provinsi"].dropna().nunique() < 2:
        st.warning(
            "Dataset harus memiliki minimal dua provinsi "
            "untuk melakukan perbandingan."
        )

    else:
        daftar_provinsi = sorted(
            df["Provinsi"].dropna().astype(str).unique()
        )

        # Pilihan provinsi
        st.subheader("Pilih Provinsi")

        col1, col2 = st.columns(2)

        with col1:
            provinsi_1 = st.selectbox(
                "Provinsi pertama",
                daftar_provinsi,
                index=0,
                key="banding_provinsi_1"
            )

        with col2:
            indeks_kedua = 1 if len(daftar_provinsi) > 1 else 0

            provinsi_2 = st.selectbox(
                "Provinsi kedua",
                daftar_provinsi,
                index=indeks_kedua,
                key="banding_provinsi_2"
            )

        if provinsi_1 == provinsi_2:
            st.warning(
                "Pilih dua provinsi yang berbeda agar "
                "perbandingan lebih bermakna."
            )

        else:
            data_1 = df.loc[
                df["Provinsi"].astype(str) == provinsi_1
            ].iloc[0]

            data_2 = df.loc[
                df["Provinsi"].astype(str) == provinsi_2
            ].iloc[0]

            st.divider()

            # Ringkasan IPM dan cluster
            st.subheader("Ringkasan Perbandingan")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### {provinsi_1}")

                st.metric(
                    "Indeks Pembangunan Manusia (IPM)",
                    f"{float(data_1['IPM']):.2f}"
                )

                st.write(
                    f"Cluster: {int(data_1['Cluster'])}"
                )

            with col2:
                st.markdown(f"### {provinsi_2}")

                st.metric(
                    "Indeks Pembangunan Manusia (IPM)",
                    f"{float(data_2['IPM']):.2f}"
                )

                st.write(
                    f"Cluster: {int(data_2['Cluster'])}"
                )

            # Grafik perbandingan IPM
            st.divider()
            st.subheader("1. Perbandingan IPM")

            data_ipm = pd.DataFrame({
                "Provinsi": [provinsi_1, provinsi_2],
                "IPM": [
                    float(data_1["IPM"]),
                    float(data_2["IPM"])
                ]
            }).set_index("Provinsi")

            st.bar_chart(data_ipm)

            selisih_ipm = abs(
                float(data_1["IPM"]) - float(data_2["IPM"])
            )

            if float(data_1["IPM"]) > float(data_2["IPM"]):
                ipm_lebih_tinggi = provinsi_1
            elif float(data_2["IPM"]) > float(data_1["IPM"]):
                ipm_lebih_tinggi = provinsi_2
            else:
                ipm_lebih_tinggi = None

            if ipm_lebih_tinggi:
                st.write(
                    f"IPM {ipm_lebih_tinggi} lebih tinggi "
                    f"dengan selisih {selisih_ipm:.2f} poin."
                )
            else:
                st.write("Nilai IPM kedua provinsi sama.")

            # Grafik indikator partisipasi sekolah
            st.divider()
            st.subheader("2. Perbandingan Indikator Sekolah")

            kolom_sekolah = [
                "Tidak_Belum_Pernah_Sekolah",
                "Masih_Bersekolah",
                "Tidak_Sekolah_Lagi"
            ]

            label_sekolah = {
                "Tidak_Belum_Pernah_Sekolah":
                    "Tidak/Belum Pernah Sekolah",
                "Masih_Bersekolah":
                    "Masih Bersekolah",
                "Tidak_Sekolah_Lagi":
                    "Tidak Sekolah Lagi"
            }

            data_sekolah = pd.DataFrame({
                "Indikator": [
                    label_sekolah[k] for k in kolom_sekolah
                ],
                provinsi_1: [
                    float(data_1[k]) for k in kolom_sekolah
                ],
                provinsi_2: [
                    float(data_2[k]) for k in kolom_sekolah
                ]
            }).set_index("Indikator")

            st.bar_chart(data_sekolah)

            st.caption(
                "Nilai mengikuti satuan pada dataset sumber. "
                "Jika datanya berupa persentase, nilai ditampilkan "
                "dalam satuan persen."
            )

            # Grafik lokasi akses internet
            st.divider()
            st.subheader("3. Perbandingan Lokasi Akses Internet")

            kolom_internet = [
                "Rumah_Sendiri",
                "Bukan_Rumah_Sendiri",
                "Kantor",
                "Sekolah",
                "Tempat_Umum",
                "Kendaraan_Berjalan"
            ]

            label_internet = {
                "Rumah_Sendiri": "Rumah sendiri",
                "Bukan_Rumah_Sendiri": "Rumah bukan milik sendiri",
                "Kantor": "Kantor",
                "Sekolah": "Sekolah",
                "Tempat_Umum": "Tempat umum",
                "Kendaraan_Berjalan": "Kendaraan berjalan"
            }

            data_internet = pd.DataFrame({
                "Lokasi": [
                    label_internet[k] for k in kolom_internet
                ],
                provinsi_1: [
                    float(data_1[k]) for k in kolom_internet
                ],
                provinsi_2: [
                    float(data_2[k]) for k in kolom_internet
                ]
            }).set_index("Lokasi")

            st.bar_chart(data_internet)

            # Tabel perbandingan seluruh indikator
            st.divider()
            st.subheader("4. Tabel Perbandingan")

            tabel_perbandingan = pd.DataFrame({
                "Indikator": [
                    "IPM",
                    "Tidak/Belum Pernah Sekolah",
                    "Masih Bersekolah",
                    "Tidak Sekolah Lagi",
                    "Rumah sendiri",
                    "Rumah bukan milik sendiri",
                    "Kantor",
                    "Sekolah",
                    "Tempat umum",
                    "Kendaraan berjalan",
                    "Cluster"
                ],
                provinsi_1: [
                    data_1["IPM"],
                    data_1["Tidak_Belum_Pernah_Sekolah"],
                    data_1["Masih_Bersekolah"],
                    data_1["Tidak_Sekolah_Lagi"],
                    data_1["Rumah_Sendiri"],
                    data_1["Bukan_Rumah_Sendiri"],
                    data_1["Kantor"],
                    data_1["Sekolah"],
                    data_1["Tempat_Umum"],
                    data_1["Kendaraan_Berjalan"],
                    data_1["Cluster"]
                ],
                provinsi_2: [
                    data_2["IPM"],
                    data_2["Tidak_Belum_Pernah_Sekolah"],
                    data_2["Masih_Bersekolah"],
                    data_2["Tidak_Sekolah_Lagi"],
                    data_2["Rumah_Sendiri"],
                    data_2["Bukan_Rumah_Sendiri"],
                    data_2["Kantor"],
                    data_2["Sekolah"],
                    data_2["Tempat_Umum"],
                    data_2["Kendaraan_Berjalan"],
                    data_2["Cluster"]
                ]
            })

            st.dataframe(
                tabel_perbandingan,
                use_container_width=True,
                hide_index=True
            )

            # Interpretasi otomatis
            st.divider()
            st.subheader("5. Interpretasi Perbandingan")

            st.write(
                f"Perbandingan dilakukan antara {provinsi_1} "
                f"dan {provinsi_2}. Selisih IPM kedua provinsi "
                f"adalah {selisih_ipm:.2f} poin."
            )

            if data_1["Cluster"] == data_2["Cluster"]:
                st.write(
                    "Kedua provinsi berada dalam cluster yang sama "
                    "berdasarkan hasil pengelompokan K-Means."
                )
            else:
                st.write(
                    "Kedua provinsi berada dalam cluster yang berbeda "
                    "berdasarkan hasil pengelompokan K-Means."
                )

            st.info(
                "Catatan: cluster merupakan hasil pengelompokan "
                "statistik, bukan peringkat resmi pendidikan. "
                "Indikator lokasi akses internet tidak secara langsung "
                "mengukur kualitas internet di sekolah. Interpretasi "
                "perlu mempertimbangkan definisi dan satuan data sumber."
            )

# =========================
# HALAMAN REKOMENDASI
# =========================

elif halaman == "Rekomendasi":
    st.title("Rekomendasi Pendidikan Digital")
    st.write(
        "Rekomendasi awal disusun berdasarkan karakteristik "
        "indikator setiap cluster dan provinsi yang dipilih."
    )

    # Kolom indikator yang digunakan
    indikator_sekolah = [
        "Tidak_Belum_Pernah_Sekolah",
        "Masih_Bersekolah",
        "Tidak_Sekolah_Lagi"
    ]

    indikator_internet = [
        "Rumah_Sendiri",
        "Bukan_Rumah_Sendiri",
        "Kantor",
        "Sekolah",
        "Tempat_Umum",
        "Kendaraan_Berjalan"
    ]

    label_indikator = {
        "Tidak_Belum_Pernah_Sekolah": "Tidak/belum pernah sekolah",
        "Masih_Bersekolah": "Masih bersekolah",
        "Tidak_Sekolah_Lagi": "Tidak sekolah lagi",
        "Rumah_Sendiri": "Rumah sendiri",
        "Bukan_Rumah_Sendiri": "Rumah bukan milik sendiri",
        "Kantor": "Kantor",
        "Sekolah": "Sekolah",
        "Tempat_Umum": "Tempat umum",
        "Kendaraan_Berjalan": "Kendaraan berjalan"
    }

    # Pastikan kolom tersedia
    kolom_rekomendasi = [
        "Provinsi", "Cluster", "IPM"
    ] + indikator_sekolah + indikator_internet

    kolom_hilang = [
        kolom for kolom in kolom_rekomendasi
        if kolom not in df.columns
    ]

    if kolom_hilang:
        st.error(
            "Kolom berikut tidak ditemukan: "
            + ", ".join(kolom_hilang)
        )

    elif df.empty:
        st.warning("Dataset belum memiliki data.")

    else:
        # Pilih provinsi
        daftar_provinsi = sorted(
            df["Provinsi"].dropna().unique().tolist()
        )

        provinsi_pilihan = st.selectbox(
            "Pilih provinsi",
            daftar_provinsi,
            key="provinsi_rekomendasi"
        )

        data_provinsi = df[
            df["Provinsi"] == provinsi_pilihan
        ].iloc[0]

        cluster_pilihan = data_provinsi["Cluster"]

        data_cluster = df[
            df["Cluster"] == cluster_pilihan
        ].copy()

        st.divider()
        st.subheader("Profil Provinsi")

        c1, c2, c3 = st.columns(3)

        c1.metric("Provinsi", provinsi_pilihan)
        c2.metric("Cluster", str(cluster_pilihan))
        c3.metric(
            "IPM",
            f"{float(data_provinsi['IPM']):.2f}"
        )

        st.write(
            f"Provinsi {provinsi_pilihan} termasuk dalam "
            f"Cluster {cluster_pilihan}, yang terdiri dari "
            f"{data_cluster['Provinsi'].nunique()} provinsi "
            "dalam dataset."
        )

        # Rata-rata indikator cluster
        kolom_numerik = indikator_sekolah + indikator_internet + ["IPM"]

        for kolom in kolom_numerik:
            data_cluster[kolom] = pd.to_numeric(
                data_cluster[kolom], errors="coerce"
            )

        rata_cluster = data_cluster[kolom_numerik].mean()

        st.divider()
        st.subheader("Karakteristik Rata-rata Cluster")

        st.write(
            "Grafik berikut menunjukkan rata-rata indikator "
            "pada kelompok provinsi yang sama."
        )

        st.bar_chart(
            rata_cluster[indikator_sekolah].rename(
                index=label_indikator
            ).to_frame("Rata-rata")
        )

        st.bar_chart(
            rata_cluster[indikator_internet].rename(
                index=label_indikator
            ).to_frame("Rata-rata")
        )

        # Rekomendasi berbasis indikator
        st.divider()
        st.subheader("Rekomendasi Awal")

        st.write(
            "Rekomendasi di bawah merupakan arahan awal berdasarkan "
            "indikator yang tersedia. Rekomendasi ini bukan hasil "
            "pengukuran langsung terhadap mutu sekolah atau kualitas "
            "jaringan internet."
        )

        # IPM: bandingkan dengan rata-rata seluruh provinsi
        ipm_provinsi = pd.to_numeric(
            df["IPM"], errors="coerce"
        )
        rata_ipm_nasional = ipm_provinsi.mean()
        ipm_pilihan = float(data_provinsi["IPM"])

        if pd.notna(rata_ipm_nasional):
            if ipm_pilihan < rata_ipm_nasional:
                st.markdown("**1. Penguatan dukungan pendidikan**")
                st.write(
                    f"IPM provinsi ini berada di bawah rata-rata "
                    f"IPM dalam dataset ({rata_ipm_nasional:.2f}). "
                    "Pemerintah daerah dapat menelaah kebutuhan "
                    "layanan pendidikan, akses belajar, dan dukungan "
                    "bagi kelompok masyarakat yang membutuhkan."
                )
            else:
                st.markdown("**1. Mempertahankan dan memperluas praktik baik**")
                st.write(
                    f"IPM provinsi ini sama dengan atau di atas "
                    f"rata-rata dataset ({rata_ipm_nasional:.2f}). "
                    "Perlu ditelaah faktor pendukung yang ada dan "
                    "bagaimana layanan pendidikan dapat terus "
                    "ditingkatkan secara merata."
                )

        # Indikator penggunaan internet di sekolah
        nilai_sekolah = rata_cluster["Sekolah"]
        nilai_lokasi = rata_cluster[indikator_internet].dropna()

        if pd.notna(nilai_sekolah) and not nilai_lokasi.empty:
            nilai_lokasi_lain = nilai_lokasi.drop(
                labels=["Sekolah"], errors="ignore"
            )

            if (
                not nilai_lokasi_lain.empty
                and nilai_sekolah < nilai_lokasi_lain.max()
            ):
                st.markdown("**2. Menelaah akses internet untuk belajar**")
                st.write(
                    "Nilai rata-rata indikator penggunaan internet "
                    "di sekolah pada cluster ini lebih rendah daripada "
                    "setidaknya satu indikator lokasi lainnya. "
                    "Perlu diteliti lebih lanjut apakah sekolah "
                    "memerlukan dukungan akses atau fasilitas belajar "
                    "digital tambahan."
                )
            else:
                st.markdown("**2. Mempertahankan dukungan belajar digital**")
                st.write(
                    "Berdasarkan indikator lokasi yang tersedia, "
                    "penggunaan internet di sekolah tidak lebih rendah "
                    "daripada seluruh lokasi pembanding. Data ini tetap "
                    "belum cukup untuk menyimpulkan kualitas jaringan "
                    "atau pemanfaatannya dalam pembelajaran."
                )

        # Status partisipasi sekolah
        nilai_status = rata_cluster[indikator_sekolah].dropna()

        if not nilai_status.empty:
            indikator_tertinggi = nilai_status.idxmax()
            indikator_terendah = nilai_status.idxmin()

            st.markdown("**3. Menelaah partisipasi sekolah**")
            st.write(
                f"Di antara indikator status sekolah yang tersedia, "
                f"nilai rata-rata tertinggi adalah "
                f"'{label_indikator[indikator_tertinggi]}', sedangkan "
                f"yang terendah adalah "
                f"'{label_indikator[indikator_terendah]}'. "
                "Perbedaan ini dapat menjadi titik awal untuk "
                "menentukan analisis lanjutan."
            )

        st.divider()
        st.subheader("Provinsi Lain dalam Cluster yang Sama")

        anggota_cluster = data_cluster[
            ["Provinsi", "IPM", "Cluster"]
        ].sort_values("IPM", ascending=False)

        st.dataframe(
            anggota_cluster,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Catatan metodologi: rekomendasi ini bersifat eksploratif. "
            "Nilai indikator perlu ditafsirkan berdasarkan definisi, "
            "satuan, dan tahun data sumber. Indikator penggunaan "
            "internet bukan ukuran langsung kualitas internet sekolah."
        )

# =========================
# HALAMAN DATA DAN UNDUHAN
# =========================

elif halaman == "Data dan Unduhan":
    st.title("Data dan Unduhan")
    st.write(
        "Lihat, filter, dan unduh data indikator pendidikan "
        "digital dari seluruh provinsi yang tersedia."
    )

    # Salinan data agar dataset asli tidak berubah
    data_tampil = df.copy()

    # Filter cluster
    st.subheader("Filter Data")

    pilihan_cluster = sorted(
        data_tampil["Cluster"].dropna().unique().tolist()
    )

    cluster_dipilih = st.multiselect(
        "Pilih cluster yang ingin ditampilkan",
        options=pilihan_cluster,
        default=pilihan_cluster
    )

    data_tampil = data_tampil[
        data_tampil["Cluster"].isin(cluster_dipilih)
    ]

    # Filter nama provinsi
    pilihan_provinsi = st.multiselect(
        "Pilih provinsi (kosongkan untuk menampilkan semua)",
        options=sorted(data_tampil["Provinsi"].dropna().unique()),
        default=[]
    )

    if pilihan_provinsi:
        data_tampil = data_tampil[
            data_tampil["Provinsi"].isin(pilihan_provinsi)
        ]

    # Ringkasan jumlah data
    st.divider()
    st.subheader("Ringkasan Data Terpilih")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Jumlah Provinsi",
            data_tampil["Provinsi"].nunique()
        )

    with col2:
        st.metric(
            "Jumlah Cluster",
            data_tampil["Cluster"].nunique()
        )

    # Tabel data
    st.divider()
    st.subheader("Tabel Data")

    st.dataframe(
        data_tampil,
        use_container_width=True,
        hide_index=True
    )

    # Unduh data CSV
    st.divider()
    st.subheader("Unduh Data")

    csv_data = data_tampil.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Unduh Data CSV",
        data=csv_data,
        file_name="edumap_indonesia.csv",
        mime="text/csv"
    )

    st.caption(
        "File CSV berisi data sesuai filter yang dipilih. "
        "Data sumber dan hasil cluster tidak diubah oleh filter ini."
    )

