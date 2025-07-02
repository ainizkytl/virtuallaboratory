import streamlit as st

def solve_splvd_substitution(a1_val, b1_val, c1_val, a2_val, b2_val, c2_val, pilihan_persamaan_awal, pilihan_variabel_awal):
    """
    Melakukan perhitungan SPLDV dengan metode substitusi secara internal.
    Input adalah float untuk akurasi perhitungan, meskipun ditampilkan sebagai int.
    """
    st.markdown("---")
    st.subheader("💡 Langkah-langkah Penyelesaian (Metode Substitusi)")
    
    st.write("### Persamaan Anda:")
    st.latex(f"1) {a1_val:.0f}x + {b1_val:.0f}y = {c1_val:.0f}")
    st.latex(f"2) {a2_val:.0f}x + {b2_val:.0f}y = {c2_val:.0f}")

    # --- Langkah 1: Mengisolasi Variabel ---
    st.markdown("---")
    st.markdown("### 1. Mengisolasi Variabel")
    
    if pilihan_persamaan_awal == 1:
        a, b, c = a1_val, b1_val, c1_val
        nama_persamaan_isolasi = "Persamaan 1"
        target_a, target_b, target_c = a2_val, b2_val, c2_val
        nama_target_persamaan = "Persamaan 2"
    else:
        a, b, c = a2_val, b2_val, c2_val
        nama_persamaan_isolasi = "Persamaan 2"
        target_a, target_b, target_c = a1_val, b1_val, c1_val
        nama_target_persamaan = "Persamaan 1"

    ekspresi_isolasi = None # Tuple: (konstanta, koefisien variabel lain, pembagi)
    diisolasi_variabel = pilihan_variabel_awal

    with st.expander(f"Lihat detail isolasi {diisolasi_variabel} dari {nama_persamaan_isolasi}"):
        if pilihan_variabel_awal == 'x':
            if a == 0:
                st.error(f"Koefisien **x** di **{nama_persamaan_isolasi}** adalah **0**. Anda tidak bisa mengisolasi **x** dari persamaan ini karena akan menyebabkan pembagian oleh nol. Coba pilih variabel atau persamaan lain.")
                return None, None
            ekspresi_isolasi_str = f"x = \\frac{{{c:.0f} - {b:.0f}y}}{{{a:.0f}}}"
            st.write(f"Dari **{nama_persamaan_isolasi}**, kita isolasi **x**:")
            st.latex(ekspresi_isolasi_str)
            ekspresi_isolasi = (c, -b, a) # Tetap float untuk perhitungan akurat
        else: # pilihan_variabel_awal == 'y'
            if b == 0:
                st.error(f"Koefisien **y** di **{nama_persamaan_isolasi}** adalah **0**. Anda tidak bisa mengisolasi **y** dari persamaan ini karena akan menyebabkan pembagian oleh nol. Coba pilih variabel atau persamaan lain.")
                return None, None
            ekspresi_isolasi_str = f"y = \\frac{{{c:.0f} - {a:.0f}x}}{{{b:.0f}}}"
            st.write(f"Dari **{nama_persamaan_isolasi}**, kita isolasi **y**:")
            st.latex(ekspresi_isolasi_str)
            ekspresi_isolasi = (c, -a, b) # Tetap float untuk perhitungan akurat

    if ekspresi_isolasi is None:
        return None, None

    # --- Langkah 2: Mensubstitusikan dan Menyederhanakan ---
    st.markdown("---")
    st.markdown("### 2. Mensubstitusikan dan Menyederhanakan")
    st.write(f"Sekarang kita substitusikan ekspresi untuk **'{diisolasi_variabel}'** ke dalam **{nama_target_persamaan}**.")
    
    konst_expr, koef_expr, pembagi_expr = ekspresi_isolasi

    with st.expander(f"Lihat detail substitusi ke {nama_target_persamaan}"):
        if diisolasi_variabel == 'x':
            st.markdown(f"Ganti `x` di `{target_a:.0f}x + {target_b:.0f}y = {target_c:.0f}` dengan `({konst_expr:.0f} - {koef_expr:.0f}y) / {pembagi_expr:.0f}`:")
            st.latex(f"{target_a:.0f} \\left(\\frac{{{konst_expr:.0f} - {koef_expr:.0f}y}}{{{pembagi_expr:.0f}}}\\right) + {target_b:.0f}y = {target_c:.0f}")
            
            # Simplifikasi: target_a * konst_expr - target_a * koef_expr * y + target_b * pembagi_expr * y = target_c * pembagi_expr
            # y * (target_b * pembagi_expr - target_a * koef_expr) = target_c * pembagi_expr - target_a * konst_expr
            koef_y_baru = target_b * pembagi_expr - target_a * koef_expr
            konst_baru = target_c * pembagi_expr - target_a * konst_expr

            st.write("Dengan mengalikan dan menggabungkan suku-suku yang serupa, kita dapatkan persamaan dengan satu variabel:")
            st.latex(f"{koef_y_baru:.0f}y = {konst_baru:.0f}")

            if koef_y_baru == 0:
                if konst_baru == 0:
                    st.info("Ini berarti ada **tak terhingga solusi** (kedua garis berimpit).")
                else:
                    st.info("Ini berarti **tidak ada solusi** (kedua garis sejajar dan tidak berpotongan).")
                return None, None
            else:
                nilai_y = konst_baru / koef_y_baru
                st.success(f"Maka, **y = {nilai_y:.0f}**")
                
        else: # diisolasi_variabel == 'y'
            st.markdown(f"Ganti `y` di `{target_a:.0f}x + {target_b:.0f}y = {target_c:.0f}` dengan `({konst_expr:.0f} - {koef_expr:.0f}x) / {pembagi_expr:.0f}`:")
            st.latex(f"{target_a:.0f}x + {target_b:.0f} \\left(\\frac{{{konst_expr:.0f} - {koef_expr:.0f}x}}{{{pembagi_expr:.0f}}}\\right) = {target_c:.0f}")
            
            # Simplifikasi: target_a * pembagi_expr * x + target_b * konst_expr - target_b * koef_expr * x = target_c * pembagi_expr
            # x * (target_a * pembagi_expr - target_b * koef_expr) = target_c * pembagi_expr - target_b * konst_expr
            koef_x_baru = target_a * pembagi_expr - target_b * koef_expr
            konst_baru = target_c * pembagi_expr - target_b * konst_expr

            st.write("Dengan mengalikan dan menggabungkan suku-suku yang serupa, kita dapatkan persamaan dengan satu variabel:")
            st.latex(f"{koef_x_baru:.0f}x = {konst_baru:.0f}")

            if koef_x_baru == 0:
                if konst_baru == 0:
                    st.info("Ini berarti ada **tak terhingga solusi** (kedua garis berimpit).")
                else:
                    st.info("Ini berarti **tidak ada solusi** (kedua garis sejajar dan tidak berpotongan).")
                return None, None
            else:
                nilai_x = konst_baru / koef_x_baru
                st.success(f"Maka, **x = {nilai_x:.0f}**")

    # --- Langkah 3: Substitusi Balik untuk Menemukan Variabel Lain ---
    st.markdown("---")
    st.markdown("### 3. Substitusi Balik untuk Menemukan Variabel Lain")
    
    if diisolasi_variabel == 'x': # Kita sudah punya y, cari x
        st.write(f"Substitusikan nilai **y = {nilai_y:.0f}** kembali ke ekspresi yang telah kita isolasi:")
        st.latex(f"x = \\frac{{{konst_expr:.0f} - {koef_expr:.0f}({nilai_y:.0f})}}{{{pembagi_expr:.0f}}}")
        
        nilai_x = (konst_expr + koef_expr * nilai_y) / pembagi_expr
        st.success(f"Didapatkan **x = {nilai_x:.0f}**")
        return nilai_x, nilai_y
    else: # Kita sudah punya x, cari y
        st.write(f"Substitusikan nilai **x = {nilai_x:.0f}** kembali ke ekspresi yang telah kita isolasi:")
        st.latex(f"y = \\frac{{{konst_expr:.0f} - {koef_expr:.0f}({nilai_x:.0f})}}{{{pembagi_expr:.0f}}}")
        
        nilai_y = (konst_expr + koef_expr * nilai_x) / pembagi_expr
        st.success(f"Didapatkan **y = {nilai_y:.0f}**")
        return nilai_x, nilai_y


# --- Tampilan Utama Aplikasi Streamlit ---
st.set_page_config(
    page_title="Kalkulator SPLDV - Metode Substitusi",
    page_icon="🔢",
    layout="centered", # Menggunakan layout centered untuk tampilan yang lebih rapi
    initial_sidebar_state="expanded"
)

st.title("🔢 Kalkulator SPLDV Interaktif")
st.markdown("---")
st.markdown("""
    Selamat datang di **Kalkulator SPLDV** dengan **Metode Substitusi**!
    Aplikasi ini akan memandu Anda memahami cara kerja metode substitusi untuk menyelesaikan sistem persamaan linear dua variabel.

    **Bentuk umum persamaan:** $ax + by = c$
""")

# --- Input Persamaan ---
st.header("Masukkan Koefisien Persamaan Anda")
st.info("💡 Masukkan nilai bilangan bulat untuk a, b, dan c. Jika hasil perhitungan bukan bilangan bulat, akan dibulatkan di tampilan akhir.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Persamaan 1")
    st.latex("a_1x + b_1y = c_1")
    a1 = st.number_input("Koefisien a₁ (untuk x)", value=2, step=1, key="a1_input")
    b1 = st.number_input("Koefisien b₁ (untuk y)", value=3, step=1, key="b1_input")
    c1 = st.number_input("Konstanta c₁", value=10, step=1, key="c1_input")

with col2:
    st.subheader("Persamaan 2")
    st.latex("a_2x + b_2y = c_2")
    a2 = st.number_input("Koefisien a₂ (untuk x)", value=1, step=1, key="a2_input")
    b2 = st.number_input("Koefisien b₂ (untuk y)", value=-1, step=1, key="b2_input")
    c2 = st.number_input("Konstanta c₂", value=0, step=1, key="c2_input")

st.markdown("---")

# --- Strategi Substitusi ---
st.header("Pilih Strategi Substitusi")
st.write("Tentukan dari persamaan mana dan variabel mana yang ingin Anda isolasi terlebih dahulu.")

col_radio1, col_radio2 = st.columns(2)

with col_radio1:
    pilihan_persamaan = st.radio(
        "Pilih Persamaan untuk diisolasi:",
        options=[1, 2],
        index=0, # Default: Persamaan 1
        format_func=lambda x: f"Persamaan {x}",
        key="pilih_persamaan_sub"
    )

with col_radio2:
    pilihan_variabel = st.radio(
        "Pilih Variabel yang akan diisolasi:",
        options=['x', 'y'],
        index=0, # Default: x
        key="pilih_variabel_sub"
    )

st.markdown("---")

if st.button("🚀 Hitung Solusi!", type="primary"):
    # Pastikan input dikonversi ke float untuk perhitungan di dalam fungsi
    x_sol, y_sol = solve_splvd_substitution(
        float(a1), float(b1), float(c1),
        float(a2), float(b2), float(c2),
        pilihan_persamaan, pilihan_variabel
    )
    
    if x_sol is not None and y_sol is not None:
        st.markdown("---")
        st.balloons() # Efek balon saat solusi ditemukan
        st.subheader("🎉 Solusi Ditemukan!")
        st.success(f"Nilai **x** = **{x_sol:.0f}**")
        st.success(f"Nilai **y** = **{y_sol:.0f}**")
        st.info("Anda bisa mengubah input di atas dan klik 'Hitung Solusi!' lagi untuk mencoba contoh lain.")
    else:
        st.warning("Perhitungan tidak menghasilkan solusi unik atau ada kendala dalam isolasi variabel. Silakan periksa koefisien Anda dan coba strategi substitusi yang berbeda.")

st.markdown("---")
st.markdown("Dibuat yuniraraaini")
