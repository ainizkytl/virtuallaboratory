import streamlit as st

def solve_splvd_substitution(a1, b1, c1, a2, b2, c2, pilihan_persamaan_awal, pilihan_variabel_awal):
    """
    Melakukan perhitungan SPLDV dengan metode substitusi secara internal.
    Fungsi ini dirancang untuk eksekusi non-interaktif setelah input dari Streamlit.
    """
    st.markdown("---")
    st.subheader("💡 Langkah-langkah Penyelesaian (Metode Substitusi)")
    
    # Menampilkan persamaan
    st.write(f"**Persamaan Anda:**")
    st.latex(f"1) {a1}x + {b1}y = {c1}")
    st.latex(f"2) {a2}x + {b2}y = {c2}")

    # Langkah 1: Isolasi Variabel
    st.markdown("---")
    st.markdown("#### 1. Mengisolasi Variabel")
    
    if pilihan_persamaan_awal == 1:
        a, b, c = a1, b1, c1
        nama_persamaan_isolasi = "Persamaan 1"
        persamaan_target_substitusi_idx = 2
        target_a, target_b, target_c = a2, b2, c2
        nama_target_persamaan = "Persamaan 2"
    else:
        a, b, c = a2, b2, c2
        nama_persamaan_isolasi = "Persamaan 2"
        persamaan_target_substitusi_idx = 1
        target_a, target_b, target_c = a1, b1, c1
        nama_target_persamaan = "Persamaan 1"

    ekspresi_isolasi = None
    diisolasi_variabel = pilihan_variabel_awal

    if pilihan_variabel_awal == 'x':
        if a == 0:
            st.error(f"Koefisien x di {nama_persamaan_isolasi} adalah 0. Tidak bisa mengisolasi x dari persamaan ini.")
            return None, None
        ekspresi_isolasi_str = f"x = \\frac{{{c} - {b}y}}{{{a}}}"
        st.write(f"Dari **{nama_persamaan_isolasi}**, kita isolasi **x**:")
        st.latex(ekspresi_isolasi_str)
        ekspresi_isolasi = (c, -b, a) # (konstanta, koefisien y, pembagi)
    else: # pilihan_variabel_awal == 'y'
        if b == 0:
            st.error(f"Koefisien y di {nama_persamaan_isolasi} adalah 0. Tidak bisa mengisolasi y dari persamaan ini.")
            return None, None
        ekspresi_isolasi_str = f"y = \\frac{{{c} - {a}x}}{{{b}}}"
        st.write(f"Dari **{nama_persamaan_isolasi}**, kita isolasi **y**:")
        st.latex(ekspresi_isolasi_str)
        ekspresi_isolasi = (c, -a, b) # (konstanta, koefisien x, pembagi)

    if ekspresi_isolasi is None:
        return None, None

    # Langkah 2: Substitusikan Ekspresi
    st.markdown("---")
    st.markdown("#### 2. Mensubstitusikan dan Menyederhanakan")
    st.write(f"Sekarang kita substitusikan ekspresi untuk **'{diisolasi_variabel}'** ke dalam **{nama_target_persamaan}**:")
    
    konst_expr, koef_expr, pembagi_expr = ekspresi_isolasi

    if diisolasi_variabel == 'x':
        st.latex(f"{target_a} \\left(\\frac{{{konst_expr} - {koef_expr}y}}{{{pembagi_expr}}}\\right) + {target_b}y = {target_c}")
        
        # Simplifikasi
        koef_y_baru = target_b * pembagi_expr - target_a * koef_expr
        konst_baru = target_c * pembagi_expr - target_a * konst_expr

        st.write("Setelah disederhanakan, kita dapatkan persamaan dengan satu variabel:")
        st.latex(f"{koef_y_baru}y = {konst_baru}")

        if koef_y_baru == 0:
            if konst_baru == 0:
                st.info("Ini berarti ada **tak terhingga solusi** (garis berimpit).")
            else:
                st.info("Ini berarti **tidak ada solusi** (garis sejajar).")
            return None, None
        else:
            nilai_y = konst_baru / koef_y_baru
            st.success(f"Maka, **y = {nilai_y:.4f}**")
            
            # Langkah 3: Substitusi Balik
            st.markdown("---")
            st.markdown("#### 3. Substitusi Balik untuk Menemukan Variabel Lain")
            st.write(f"Substitusikan nilai **y = {nilai_y:.4f}** kembali ke ekspresi awal **x = \\frac{{{konst_expr} - {koef_expr}y}}{{{pembagi_expr}}}**")
            
            nilai_x = (konst_expr + koef_expr * nilai_y) / pembagi_expr
            st.success(f"Didapatkan **x = {nilai_x:.4f}**")
            return nilai_x, nilai_y
    else: # diisolasi_variabel == 'y'
        st.latex(f"{target_a}x + {target_b} \\left(\\frac{{{konst_expr} - {koef_expr}x}}{{{pembagi_expr}}}\\right) = {target_c}")
        
        # Simplifikasi
        koef_x_baru = target_a * pembagi_expr - target_b * koef_expr
        konst_baru = target_c * pembagi_expr - target_b * konst_expr

        st.write("Setelah disederhanakan, kita dapatkan persamaan dengan satu variabel:")
        st.latex(f"{koef_x_baru}x = {konst_baru}")

        if koef_x_baru == 0:
            if konst_baru == 0:
                st.info("Ini berarti ada **tak terhingga solusi** (garis berimpit).")
            else:
                st.info("Ini berarti **tidak ada solusi** (garis sejajar).")
            return None, None
        else:
            nilai_x = konst_baru / koef_x_baru
            st.success(f"Maka, **x = {nilai_x:.4f}**")

            # Langkah 3: Substitusi Balik
            st.markdown("---")
            st.markdown("#### 3. Substitusi Balik untuk Menemukan Variabel Lain")
            st.write(f"Substitusikan nilai **x = {nilai_x:.4f}** kembali ke ekspresi awal **y = \\frac{{{konst_expr} - {koef_expr}x}}{{{pembagi_expr}}}**")
            
            nilai_y = (konst_expr + koef_expr * nilai_x) / pembagi_expr
            st.success(f"Didapatkan **y = {nilai_y:.4f}**")
            return nilai_x, nilai_y


# --- Tampilan Aplikasi Streamlit ---
st.set_page_config(
    page_title="Kalkulator SPLDV - Substitusi",
    page_icon="🔢",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Judul dan Deskripsi
st.title("🔢 Kalkulator SPLDV Interaktif")
st.markdown("---")
st.markdown("""
    Selamat datang di **Kalkulator SPLDV** dengan **Metode Substitusi**!
    Aplikasi ini akan memandu Anda memahami cara kerja metode substitusi untuk menyelesaikan sistem persamaan linear dua variabel.

    **Bentuk umum persamaan:** $ax + by = c$
""")

# Input Persamaan
st.header("Masukkan Persamaan Anda")
st.info("💡 Isi koefisien (a, b) dan konstanta (c) untuk kedua persamaan.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Persamaan 1")
    st.latex("a_1x + b_1y = c_1")
    a1 = st.number_input("Koefisien a₁ (x)", value=2.0, key="a1")
    b1 = st.number_input("Koefisien b₁ (y)", value=3.0, key="b1")
    c1 = st.number_input("Konstanta c₁", value=10.0, key="c1")

with col2:
    st.subheader("Persamaan 2")
    st.latex("a_2x + b_2y = c_2")
    a2 = st.number_input("Koefisien a₂ (x)", value=1.0, key="a2")
    b2 = st.number_input("Koefisien b₂ (y)", value=-1.0, key="b2")
    c2 = st.number_input("Konstanta c₂", value=0.0, key="c2")

st.markdown("---")

# Pilihan untuk Substitusi
st.header("Strategi Substitusi")
st.write("Pilih persamaan dan variabel mana yang ingin Anda isolasi untuk memulai proses substitusi.")

pilihan_persamaan = st.radio(
    "Pilih persamaan untuk mengisolasi variabel:",
    options=[1, 2],
    index=0, # Default pilih Persamaan 1
    format_func=lambda x: f"Persamaan {x}",
    key="pilih_persamaan_sub"
)

pilihan_variabel = st.radio(
    "Pilih variabel yang akan diisolasi:",
    options=['x', 'y'],
    index=0, # Default pilih x
    key="pilih_variabel_sub"
)

if st.button("Hitung Solusi!", type="primary"):
    # Panggil fungsi solver
    x_sol, y_sol = solve_splvd_substitution(a1, b1, c1, a2, b2, c2, pilihan_persamaan, pilihan_variabel)
    
    if x_sol is not None and y_sol is not None:
        st.markdown("---")
        st.balloons() # Efek balon saat solusi ditemukan
        st.subheader("🎉 Solusi Ditemukan!")
        st.success(f"Nilai **x** = **{x_sol:.4f}**")
        st.success(f"Nilai **y** = **{y_sol:.4f}**")
        st.info("Anda bisa mengubah input di atas dan klik 'Hitung Solusi!' lagi untuk mencoba contoh lain.")
    elif x_sol is None and y_sol is None:
        st.warning("Perhitungan tidak menghasilkan solusi unik. Silakan periksa koefisien Anda atau coba pilihan strategi substitusi lainnya.")

st.markdown("---")
st.markdown("Dibuat oleh rarayuniaini")
