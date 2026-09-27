# Pengujian prototipe

Pengujian dilakukan menggunakan Playwright dan Chromium di lingkungan lokal. HTML, CSS, JavaScript, dan gambar disertakan ke halaman pengujian secara langsung. Font eksternal tidak dimuat; pengujian visual menggunakan font cadangan Arial/Georgia. Hosting publik, layanan WhatsApp, dan video YouTube tidak diuji sebagai layanan langsung.

## Hasil

Pada lebar 320, 390, 768, dan 1440 piksel:

- Tidak ditemukan halaman melebar horizontal di luar viewport.
- Tidak ditemukan galat JavaScript pada rangkaian interaksi yang diuji.
- Semua gambar pada konten utama berhasil didekode.
- Panel Tahfizh dapat dibuka dan hanya satu panel 4T tetap terbuka.
- Pilihan kegiatan Malam mengganti panel Pagi.
- Kurikulum dapat dibuka dan menampilkan sepuluh program pendukung.
- Galeri membuka pembesaran foto; tombol Escape menutupnya.
- Navigasi seluler terbuka dan dapat ditutup dengan Escape pada lebar 320 dan 390 piksel.

Preferensi pengurangan gerak mencegah aktivasi animasi pengungkapan. Ketika JavaScript dinonaktifkan, judul, keempat panel kegiatan harian, dan tautan kontak tetap tersedia.

Hasil terstruktur: `test-report.json`.

## Batasan

Pengujian ini bukan pengukuran Lighthouse, Core Web Vitals, durasi muat pada jaringan seluler, atau pengujian HP fisik. Safari/iOS, Firefox, pembaca layar, dan semua kombinasi ukuran layar belum diuji. AVIF memerlukan browser yang mendukung format tersebut. Menu, tipografi, foto, dan efek harus diperiksa lagi setelah font daring serta hosting tujuan aktif.
