import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = "Supermarket_Sales_Prepared.csv"  # Ganti dengan path file Anda
data = pd.read_csv(file_path, delimiter=';')

# 1. Pahami Struktur Dataset
print("Dataset Overview:")
print(data.head())
print("\nDataset Shape:", data.shape)
print("\nData Types:")
print(data.dtypes)

# 2. Analisis Statistik Deskriptif
print("\nNumerical Summary:")
numerical_stats = data.describe()
print(numerical_stats)

# 3. Identifikasi Missing Values
missing_values = data.isnull().sum()
missing_percent = (missing_values / len(data)) * 100
print("\nMissing Values Summary:")
print(pd.DataFrame({
    "Missing Values": missing_values,
    "Percentage (%)": missing_percent
}))

# 4. Distribusi Data (Numerik)
numerical_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'gross income', 'Rating']
data[numerical_cols].hist(figsize=(12, 8), bins=20, color='skyblue', edgecolor='black')
plt.suptitle('Histograms of Numerical Columns', fontsize=16)
plt.tight_layout()
plt.show()

# 5. Analisis Data Kategori
categorical_cols = ['Branch', 'City', 'Customer type', 'Gender', 'Payment']
for col in categorical_cols:
    print(f"\nValue Counts for {col}:")
    print(data[col].value_counts())
    data[col].value_counts().plot(kind='bar', color='coral', edgecolor='black')
    plt.title(f"Bar Chart of {col}")
    plt.ylabel("Count")
    plt.xlabel(col)
    plt.show()

# 6. Analisis Hubungan Antar Variabel
plt.figure(figsize=(10, 6))
corr_matrix = data[numerical_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Correlation Heatmap')
plt.show()

# Scatter plot untuk dua variabel dengan korelasi tertinggi
strongest_corr = corr_matrix.unstack().sort_values(ascending=False).drop_duplicates()
var1, var2 = strongest_corr.index[1]  # Index 0 adalah korelasi diri sendiri
print(f"\nStrongest Correlation: {var1} and {var2} ({strongest_corr[1]:.2f})")

plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x=var1, y=var2, alpha=0.7)
plt.title(f"Scatter Plot: {var1} vs {var2}")
plt.show()

# 7. Outlier Detection
for col in numerical_cols:
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data, y=col, color='orange')
    plt.title(f'Box Plot of {col}')
    plt.show()

# Outlier count for a specific column
selected_col = 'Tax 5%'
q1, q3 = data[selected_col].quantile(0.25), data[selected_col].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = data[(data[selected_col] < lower_bound) | (data[selected_col] > upper_bound)]
print(f"\nNumber of Outliers in {selected_col}: {len(outliers)}")

# 8. Pola atau Tren Berdasarkan Waktu
if 'Date' in data.columns:
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Pastikan format Date valid
    data['Month'] = data['Date'].dt.month  # Ambil bulan dari kolom Date
    
    # Hitung total penjualan per bulan
    monthly_sales = data.groupby('Month')['Total'].sum()

    # Visualisasi Penjualan per Bulan
    plt.figure(figsize=(10, 6))
    monthly_sales.plot(kind='bar', color='lightgreen', edgecolor='black')
    plt.title("Monthly Sales")
    plt.ylabel("Total Sales")
    plt.xlabel("Month")
    plt.xticks(rotation=0)  # Mengatur agar label bulan tidak miring
    plt.tight_layout()
    plt.show()

    # Menampilkan statistik penjualan per bulan
    print("\nMonthly Sales Summary:")
    print(monthly_sales)

    # Grafik Trend Penjualan per Bulan (Line Plot)
    plt.figure(figsize=(10, 6))
    monthly_sales.plot(kind='line', marker='o', color='blue')
    plt.title("Monthly Sales Trend")
    plt.ylabel("Total Sales")
    plt.xlabel("Month")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Opsional: Jika ingin menambahkan analisis lebih lanjut per tahun atau membandingkan antar kota/branch, bisa ditambahkan analisis serupa.
