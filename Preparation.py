import pandas as pd

# Membaca file dengan delimiter yang sesuai
file_path = 'Supermarket Sales Cleaned.csv'
data = pd.read_csv(file_path, delimiter=';', engine='python')  # Menggunakan delimiter ;

# Menghapus kolom yang tidak relevan atau muncul sebagai 'Unnamed'
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Menampilkan 5 baris pertama
print("=" * 50)
print("1. 5 Baris Pertama Dataset:")
print(data.head(5).to_string(index=False))  # Menggunakan to_string untuk tampilan rapi

print("=" * 50)
print("\nData Types:")
print(data.dtypes)
print("=" * 50)

# Memeriksa struktur dataset sebelum penyesuaian
print("2. Struktur Dataset Sebelum Penyesuaian:")
print(data.info())
print("-" * 50)

# Konversi kolom 'Date' ke tipe datetime
if 'Date' in data.columns:
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce', format='%d/%m/%Y')

# Tangani nilai `NaT` di kolom `Date` (jika ada)
default_date = pd.Timestamp('2019-01-01')  # Nilai default
data['Date'].fillna(default_date, inplace=True)

# Periksa dan tangani missing values
print("3. Missing Values Sebelum Penanganan:")
print(data.isnull().sum().to_string())
print("-" * 50)

# Pastikan gross margin percentage berupa nilai numerik
if 'gross margin percentage' in data.columns:

    data['gross margin percentage'] = pd.to_numeric(data['gross margin percentage'], errors='coerce')
    
    # Isi nilai NaN dengan rata-rata kolom
    if data['gross margin percentage'].isna().sum() > 0:
        print("Missing values ditemukan pada gross margin percentage. Menanganinya...")
        data['gross margin percentage'].fillna(data['gross margin percentage'].mean(), inplace=True)

# Tangani missing value pada kolom lain
data.fillna(data.mean(numeric_only=True), inplace=True)
for col in data.select_dtypes(include=['object']).columns:
    data[col].fillna(data[col].mode()[0], inplace=True)

# Verifikasi jumlah missing values setelah penanganan
print("Jumlah Missing Values Setelah Penanganan:")
print(data.isnull().sum().to_string())
print("=" * 50)

# Deteksi dan penghapusan duplikat
print("4. Deteksi dan Penghapusan Duplikasi:")
print(f"Jumlah Duplikat Sebelum Penghapusan: {data.duplicated().sum()}")
data = data.drop_duplicates()
print(f"Jumlah Duplikat Setelah Penghapusan: {data.duplicated().sum()}")
print("=" * 50)

# Normalisasi kolom numerik
print("5. Normalisasi Kolom Numerik:")
numeric_columns = ['Total', 'gross income', 'gross margin percentage', 'Tax 5%']
for col in numeric_columns:
    if col in data.columns:
        col_min = data[col].min()
        col_max = data[col].max()
        if col_min == col_max:  # Cek jika nilai konstan
            print(f"Kolom {col} memiliki nilai konstan, diisi dengan 0.5.")
            data[col] = 0.5  # Atur ke nilai tetap (0.5 untuk representasi tengah)
        else:
            # Min-max normalization
            data[col] = ((data[col] - col_min) / (col_max - col_min)).round(2)

print("Contoh Data Setelah Normalisasi:")
print(data.head().to_string(index=False))  # Tampilkan data dengan to_string
print("=" * 50)

#Simpan hasil ke file baru
output_path = 'Supermarket_Sales_Prepared.csv'
data.to_csv(output_path, index=False, sep=';')  # Simpan dengan pemisah ;
print(f"Dataset hasil data preparation telah disimpan ke: {output_path}")
