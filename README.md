# Assyabab — Pesantren Multimedia

Prototipe presentasi website Pesantren Multimedia Assyabab, Caringin, Bogor. Rancangan editorial dengan prioritas layar seluler, aksen Al-Qur'an 3D berbasis CSS, dan fotografi asli dari materi profil pesantren.

## Membuka website

Buka `index.html` di browser modern, atau jalankan server lokal dari folder ini:

```sh
python3 -m http.server 3000
```

Kemudian buka `http://localhost:3000`. Tidak memerlukan npm, proses build, database, kunci API, atau langganan layanan. Font Google bersifat opsional; Arial dan Georgia digunakan ketika font daring tidak tersedia.

Untuk membuat satu file presentasi yang menyertakan gambar, CSS, dan JavaScript:

```sh
python3 tools/build_offline.py
```

Buka hasilnya, `Assyabab-Prototype.html`, di browser. Versi ini tidak memuat font eksternal; tautan WhatsApp dan YouTube tetap memerlukan internet saat diklik.

## Implementasi

- `index.html`: profil, visi-misi, 4T, kurikulum, multimedia, kegiatan harian, galeri, pengajar, kontak, dan FAQ.
- `styles.css`: tata letak responsif dan ilustrasi Al-Qur'an 3D tanpa WebGL.
- `app.js`: navigasi seluler, pengungkapan konten saat digulir, pilihan kegiatan harian, galeri, dan pembesaran foto.
- `assets/`: delapan foto AVIF yang dioptimalkan dan ikon SVG konsep.

Tidak menggunakan Three.js, video otomatis, rangkaian frame, framework runtime, pelacakan, atau layanan berbayar. Efek gerak mengikuti preferensi pengurangan animasi; efek kemiringan buku hanya aktif pada perangkat dengan pointer presisi. Konten utama tetap terbaca tanpa JavaScript.

## Sumber dan status

Konten bersumber dari `Pesantren Assyabab Profile and Programs.pptx` yang diberikan pemilik proyek. Kontak dan tahun penerimaan mengikuti brosur pada slide 34. Rincian asal gambar dan batasan verifikasi tercatat dalam `docs/CONTENT-SOURCES.md`.

Ini prototipe antarmuka, bukan sistem pendaftaran daring. Tombol kontak membuka WhatsApp; tidak ada data pendaftaran yang disimpan atau dikirim otomatis. Logo adalah usulan identitas visual untuk prototipe, bukan konfirmasi logo resmi. Metadata `noindex,nofollow` sengaja dipasang selama tahap presentasi.

Nama/jabatan pengelola, nomor kontak, izin penggunaan foto, biaya, kuota, ketentuan bantuan, dan tahun penerimaan harus dikonfirmasi sebelum peluncuran resmi. Unggahan ke repository tidak otomatis mengaktifkan hosting publik. File statis dapat dihosting setelah layanan hosting proyek diaktifkan.

## Pengujian

Lihat `docs/TESTING.md` dan `docs/test-report.json`. Pengujian dilakukan pada Chromium dengan lebar 320, 390, 768, dan 1440 piksel; ini bukan klaim pengujian seluruh perangkat fisik atau skor Lighthouse.

Dikembangkan untuk Azriel Choerul Hakim.
