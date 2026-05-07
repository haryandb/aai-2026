Tentu, berikut adalah profil dataset **Online Retail** dan rencana pengembangan sistem rekomendasi yang disusun secara sistematis dalam format Markdown (`.md`).

---

# Profil Dataset & Rencana Pengembangan Sistem Rekomendasi

## 1. Profil Dataset (Online Retail)

Dataset ini berisi data transaksi lintas batas dari toko retail online yang berbasis di Inggris (UK) antara tanggal 01/12/2010 hingga 09/12/2011.

### A. Atribut Data
| Kolom | Deskripsi | Tipe Data |
| :--- | :--- | :--- |
| **InvoiceNo** | Nomor unik transaksi. Jika diawali 'C', berarti pembatalan (return). | Nominal |
| **StockCode** | Kode unik produk. | Nominal |
| **Description** | Nama atau deskripsi singkat produk. | Tekstual |
| **Quantity** | Jumlah unit per transaksi. | Numerik |
| **InvoiceDate** | Tanggal dan waktu transaksi terjadi. | Datetime |
| **UnitPrice** | Harga produk per unit (Sterling). | Numerik |
| **CustomerID** | Nomor unik identitas pelanggan. | Nominal |
| **Country** | Negara asal pelanggan. | Nominal |

### B. Karakteristik & Tantangan Data
* **Missing Values**: Terdapat banyak nilai kosong pada kolom `CustomerID`. Untuk analisis personalisasi, data tanpa ID ini biasanya harus difilter.
* **Transaksi Pembatalan**: Nilai negatif pada `Quantity` menunjukkan retur, yang penting untuk dianalisis guna mengetahui tingkat kepuasan pelanggan.
* **Dominasi Geografis**: Mayoritas transaksi berasal dari United Kingdom, sehingga perlu pertimbangan khusus jika ingin melakukan segmentasi berdasarkan negara.

---

## 2. Analisis RFM (Recency, Frequency, Monetary)

Sebelum membangun sistem rekomendasi, dilakukan segmentasi pelanggan menggunakan metode RFM untuk memahami perilaku belanja mereka.



* **Recency (R)**: Seberapa baru pelanggan melakukan pembelian terakhir.
* **Frequency (F)**: Seberapa sering pelanggan melakukan pembelian dalam periode tertentu.
* **Monetary (M)**: Total nilai uang yang dihabiskan oleh pelanggan.

**Segmentasi Pelanggan:**
1.  **Champions**: Belanja baru-baru ini, sangat sering, dan belanja banyak. (Target: Hadiah & Produk Baru).
2.  **Loyal Customers**: Belanja secara teratur. (Target: Program loyalitas).
3.  **At Risk**: Sudah lama tidak belanja, tapi dulu sering belanja banyak. (Target: Kampanye re-aktivasi/diskon besar).

---

## 3. Rencana Sistem Rekomendasi

Berdasarkan data yang tersedia, berikut adalah tiga strategi rekomendasi yang diusulkan:

### Strategi A: Collaborative Filtering (User-Based)
Sistem ini merekomendasikan produk kepada pengguna berdasarkan kesamaan profil dengan pengguna lain.
* **Logika**: Jika Pengguna A dan Pengguna B memiliki pola pembelian yang mirip, maka produk yang dibeli Pengguna A (tapi belum dibeli B) akan direkomendasikan kepada B.
* **Matriks**: Membuat matriks `User-Item` dengan nilai berupa total `Quantity`.



![Image of Collaborative Filtering vs Content-Based Filtering](rekomendasi%20sistem.jpeg)


### Strategi B: Market Basket Analysis (Association Rules)
Menggunakan algoritma **Apriori** untuk menemukan hubungan antar produk dalam satu keranjang belanja.
* **Tujuan**: Menampilkan fitur *"Sering dibeli bersamaan"* (Frequently Bought Together).
* **Metrik**: Support, Confidence, dan Lift.
* **Contoh**: Jika pelanggan membeli "LUNCH BAG RED RETROSPOT", sistem akan merekomendasikan "STRAWBERRY LUNCH BOX".

### Strategi C: Content-Based Filtering (NLP)
Menggunakan kolom `Description` untuk mencari kemiripan produk secara semantik.
* **Metode**: TF-IDF atau Word Embeddings pada deskripsi produk.
* **Tujuan**: Rekomendasi berdasarkan kemiripan fisik atau fungsi produk, sangat berguna untuk pelanggan baru yang belum memiliki riwayat transaksi (mengatasi *Cold Start Problem*).

---

## 4. Alur Implementasi (Pipeline)

1.  **Data Cleaning**: 
    * Menghapus baris dengan `CustomerID` null.
    * Memisahkan transaksi sukses dengan pembatalan (C).
    * Menghapus outliers pada `Quantity` dan `UnitPrice`.
2.  **Feature Engineering**:
    * Menghitung skor RFM untuk setiap pelanggan.
    * Membuat matriks interaksi produk.
3.  **Modeling**:
    * Implementasi algoritma SVD (Singular Value Decomposition) untuk Collaborative Filtering.
    * Implementasi algoritma Apriori untuk aturan asosiasi.
4.  **Evaluation**:
    * Menggunakan metrik **RMSE** (Root Mean Square Error) untuk model prediksi rating/kuantitas.
    * Menggunakan **Precision@K** untuk melihat relevansi daftar rekomendasi.

---

## 5. Kesimpulan
Dataset Online Retail sangat kaya untuk pengembangan sistem rekomendasi. Dengan mengkombinasikan **Analisis RFM** dan **Hybrid Recommender System** (Collaborative + Association Rules), sistem dapat memberikan rekomendasi yang tidak hanya akurat secara personal, tetapi juga relevan secara konteks keranjang belanja.

---