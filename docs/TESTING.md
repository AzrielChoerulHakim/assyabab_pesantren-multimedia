# Pengujian prototipe — revisi 2

## Metode

Pengujian benar-benar dijalankan menggunakan Playwright dan Chromium 144.0.7559.96. Builder menggabungkan HTML, kedua stylesheet, JavaScript, dan gambar ke satu HTML, lalu Chromium merendernya melalui `page.set_content`.

Navigasi HTTP lokal tidak tersedia di lingkungan pengujian. CLI agent-browser juga tidak tersedia, sehingga pengujian menggunakan Playwright yang tersedia. Ini **bukan** pengujian hosting publik, pengukuran jaringan seluler, Lighthouse, atau HP fisik. Ukuran viewport bukan nama/model perangkat yang diuji.

## Cakupan yang lulus

Lebar viewport: **320, 360, 390, 430, 700, 701, 768, 1024, 1440, dan 1920 piksel**.

Pada seluruh ukuran tersebut:

- Tidak ada halaman melebar horizontal, termasuk setelah kurikulum dibuka.
- Tidak ditemukan galat JavaScript pada rangkaian interaksi yang diuji.
- Semua gambar konten utama berhasil didekode; semua rujukan berkas dan srcset pada sumber tersedia.
- Paragraf pembuka 15–16 px; tombol utama 14 px. Pada lebar HP 320–430 px, paragraf pembuka 16 px.
- Diagram 4T membuka program yang tepat, memperbarui penanda dan label, dan mengikuti pembukaan/penutupan accordion. Tombol panah keyboard juga diuji.
- Pilihan Malam dan navigasi keyboard kembali ke Pagi bekerja.
- Sepuluh program pendukung tampil ketika kurikulum dibuka.
- Tombol galeri maju/mundur bekerja; pembesaran foto terbuka dan tertutup dengan Escape, fokus kembali ke foto, serta kunci gulir dibersihkan.
- Menu pada lebar <=700 px mengisolasi fokus, menutup dengan Escape, dan mengarahkan fokus ke tujuan navigasi.
- FAQ dapat dibuka.

Pengujian tambahan: konten, semua panel hari, accordion asli, serta tiga tautan WhatsApp tetap tersedia tanpa JavaScript. Perubahan preferensi pengurangan animasi menonaktifkan efek gerak dan mereset kemiringan buku. Tidak ada permintaan jaringan otomatis dalam pengujian HTML mandiri.

Hasil terstruktur tersimpan di `test-report-v2.json`. `test-report.json` dipertahankan sebagai arsip revisi 1.

## Menjalankan ulang

Persyaratan pengujian: Python >=3.10, paket `playwright`, dan Chromium. Dependensi ini hanya untuk pengembangan; **website tidak membutuhkan paket tersebut**.

```sh
python3 tools/test_ui.py --browser /usr/bin/chromium
# Opsional: simpan tangkapan layar
python3 tools/test_ui.py --browser /usr/bin/chromium --screenshots ./screenshots
```

## Batasan dan pemeriksaan lanjutan

Safari/iOS, Firefox, pembaca layar, semua HP fisik, performa jaringan, serta WhatsApp/YouTube sebagai layanan langsung belum diuji. Format foto AVIF memerlukan browser yang mendukungnya. Pemilihan kandidat srcset oleh jaringan browser belum diuji; keberadaan dan integritas berkasnya diperiksa secara lokal.

Website dan ekspor HTML memakai stack font sistem yang sama tanpa font daring. Dengan browser dan perangkat yang sama, keduanya tidak bergantung pada unduhan font. Sistem operasi berbeda dapat memilih font cadangan yang berbeda; ini bukan jaminan tampilan piksel-identik antarperangkat.
