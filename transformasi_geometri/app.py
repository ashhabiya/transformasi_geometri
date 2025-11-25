import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- 1. SETUP HALAMAN & KONSTANTA ---

# Mengatur tata letak halaman menjadi 'wide' agar grafik dapat terlihat besar
st.set_page_config(layout="wide", page_title="Virtual Lab Transformasi Geometri")

st.title("🔬 Virtual Lab Transformasi Geometri Interaktif")
st.markdown("Visualisasikan Rotasi, Dilatasi, Refleksi, dan Translasi pada bangun datar.")
st.markdown("---")

# Objek Awal (Persegi)
# Didefinisikan sebagai array NumPy (2 baris: x, y).
# Koordinat: (1,1), (4,1), (4,4), (1,4)
INITIAL_POINTS = np.array([
    [1, 4, 4, 1],  # Koordinat x
    [1, 1, 4, 4]   # Koordinat y
])

# --- 2. FUNGSI VISUALISASI ---

def plot_object(ax, points, color='blue', label='Objek Awal', marker='o'):
    """Fungsi untuk menggambar bangun datar (menghubungkan titik dan menutupnya)."""
    # Menutup objek dengan menghubungkan titik terakhir ke titik pertama
    closed_points = np.hstack([points, points[:, 0].reshape(-1, 1)])
    
    # Plotting garis penghubung
    ax.plot(closed_points[0, :], closed_points[1, :], 
            color=color, linestyle='-', linewidth=2, label=label)
            
    # Plotting titik-titik
    ax.scatter(points[0, :], points[1, :], color=color, marker=marker, s=50) 
    
    # Menambahkan label koordinat di dekat titik (untuk kejelasan)
    for i in range(points.shape[1]):
        x = points[0, i]
        y = points[1, i]
        ax.text(x + 0.1, y + 0.1, f'({x:.1f}, {y:.1f})', fontsize=8)

def setup_plot(ax, title):
    """Fungsi untuk mengatur sumbu dan tampilan plot."""
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(title, fontsize=16)
    ax.grid(True, linestyle=':', alpha=0.6)


# --- 3. FUNGSI TRANSFORMASI MATEMATIS ---

def transform_rotation(points, angle_deg):
    """Rotasi (Perputaran) terhadap (0,0) menggunakan matriks rotasi."""
    angle_rad = np.deg2rad(angle_deg)
    R = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])
    # Perkalian matriks R @ points secara otomatis diterapkan ke semua titik
    return R @ points

def transform_dilation(points, k):
    """Dilatasi (Perkalian) terhadap (0,0) menggunakan matriks skala."""
    D = np.array([
        [k, 0],
        [0, k]
    ])
    return D @ points

def transform_reflection(points, axis):
    """Refleksi (Pencerminan) menggunakan matriks refleksi."""
    if axis == 'Sumbu X (y=0)':
        R = np.array([[1, 0], [0, -1]])
    elif axis == 'Sumbu Y (x=0)':
        R = np.array([[-1, 0], [0, 1]])
    elif axis == 'Garis y=x':
        R = np.array([[0, 1], [1, 0]])
    else: # Garis y=-x
        R = np.array([[0, -1], [-1, 0]])
    return R @ points

def transform_translation(points, tx, ty):
    """Translasi (Pergeseran) dengan menambahkan vektor."""
    T = np.array([[tx], [ty]])
    # Translasi: P' = P + T. Penjumlahan ini diterapkan ke semua kolom (titik)
    return points + T


# --- 4. LOGIKA UTAMA APLIKASI (Tabs dan Columns) ---

# Membuat navigasi tab di bagian atas layar
tab_rotasi, tab_dilatasi, tab_refleksi, tab_translasi = st.tabs(
    ["🔄 Rotasi", "⚖️ Dilatasi", "🪞 Refleksi", "➡️ Translasi"]
)

# A. ROTASI
with tab_rotasi:
    # Mengatur 2 kolom: 1 untuk input (kecil), 2 untuk grafik (besar)
    col_input, col_graph = st.columns([1, 2])
    
    with col_input:
        st.subheader("⚙️ Atur Sudut Rotasi")
        st.markdown("---")
        angle = st.slider("Sudut Rotasi (°)", -360, 360, 90, 5)
        st.info("Rotasi **positif** berlawanan arah jarum jam. Rotasi di pusat **(0,0)**.")

    with col_graph:
        transformed_points = transform_rotation(INITIAL_POINTS, angle)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        setup_plot(ax, f"Rotasi Sebesar {angle}°")
        plot_object(ax, INITIAL_POINTS, color='blue', label='Objek Awal')
        plot_object(ax, transformed_points, color='red', label='Hasil Rotasi', marker='s')
        ax.legend(loc='upper left')
        st.pyplot(fig)


# B. DILATASI
with tab_dilatasi:
    col_input, col_graph = st.columns([1, 2])
    
    with col_input:
        st.subheader("⚙️ Atur Faktor Skala")
        st.markdown("---")
        k = st.slider("Faktor Skala (k)", 0.1, 5.0, 2.0, 0.1)
        st.info("k > 1: Pembesaran. k < 1: Pengecilan. Dilatasi di pusat **(0,0)**.")

    with col_graph:
        transformed_points = transform_dilation(INITIAL_POINTS, k)

        fig, ax = plt.subplots(figsize=(8, 8))
        setup_plot(ax, f"Dilatasi dengan Faktor Skala k = {k}")
        plot_object(ax, INITIAL_POINTS, color='blue', label='Objek Awal')
        plot_object(ax, transformed_points, color='red', label='Hasil Dilatasi', marker='s')
        ax.legend(loc='upper left')
        st.pyplot(fig)


# C. REFLEKSI
with tab_refleksi:
    col_input, col_graph = st.columns([1, 2])
    
    with col_input:
        st.subheader("⚙️ Pilih Sumbu Refleksi")
        st.markdown("---")
        axis = st.selectbox("Pilih Sumbu Pencerminan", 
                                ('Sumbu X (y=0)', 'Sumbu Y (x=0)', 'Garis y=x', 'Garis y=-x'))
        st.info(f"Objek dicerminkan terhadap **{axis}**.")

    with col_graph:
        transformed_points = transform_reflection(INITIAL_POINTS, axis)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        setup_plot(ax, f"Refleksi terhadap {axis}")
        plot_object(ax, INITIAL_POINTS, color='blue', label='Objek Awal')
        plot_object(ax, transformed_points, color='red', label='Hasil Refleksi', marker='s')
        
        # Gambar garis refleksi
        if axis == 'Sumbu X (y=0)':
            ax.axhline(0, color='purple', linestyle='-', linewidth=2, label='Sumbu Refleksi')
        elif axis == 'Sumbu Y (x=0)':
            ax.axvline(0, color='purple', linestyle='-', linewidth=2, label='Sumbu Refleksi')
        elif axis == 'Garis y=x':
            ax.plot([-10, 10], [-10, 10], color='purple', linestyle='--', linewidth=2, label='Sumbu Refleksi')
        elif axis == 'Garis y=-x':
            ax.plot([-10, 10], [10, -10], color='purple', linestyle='--', linewidth=2, label='Sumbu Refleksi')
            
        ax.legend(loc='upper left')
        st.pyplot(fig)


# D. TRANSLASI
with tab_translasi:
    col_input, col_graph = st.columns([1, 2])
    
    with col_input:
        st.subheader("⚙️ Atur Vektor Translasi")
        st.markdown("---")
        tx = st.slider("Pergeseran Horizontal (tx)", -5, 5, 2)
        ty = st.slider("Pergeseran Vertikal (ty)", -5, 5, 3)
        st.info(f"Vektor Translasi T = **({tx}, {ty})**.")

    with col_graph:
        transformed_points = transform_translation(INITIAL_POINTS, tx, ty)

        fig, ax = plt.subplots(figsize=(8, 8))
        setup_plot(ax, f"Translasi Vektor ({tx}, {ty})")
        plot_object(ax, INITIAL_POINTS, color='blue', label='Objek Awal')
        plot_object(ax, transformed_points, color='red', label='Hasil Translasi', marker='s')
        
        # Gambar contoh vektor translasi dari salah satu titik
        ax.arrow(INITIAL_POINTS[0, 0], INITIAL_POINTS[1, 0], tx, ty, 
                 head_width=0.3, head_length=0.5, fc='green', ec='green', linewidth=1.5,
                 label='Vektor Translasi')
                 
        ax.legend(loc='upper left')
        st.pyplot(fig)

# --- INFO FOOTER ---
st.markdown("---")
st.markdown("ℹ️ **Informasi Objek Awal:** Bangun datar yang digunakan adalah **Persegi** dengan koordinat titik (1,1), (4,1), (4,4), dan (1,4).")
