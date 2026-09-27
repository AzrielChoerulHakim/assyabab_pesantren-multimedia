# Assyabab — Pesantren Multimedia

Prototipe presentasi website Pesantren Multimedia Assyabab, Caringin, Bogor. Rancangan editorial dengan prioritas layar seluler, aksen Al-Qur'an 3D berbasis CSS, dan fotografi asli dari materi profil pesantren.

## Membuka website

Buka `index.html` di browser modern, atau jalankan server lokal dari folder ini:

```sh
python3 -m http.server 3000
```

Kemudian buka `http://localhost:3000`. Tidak memerlukan npm, proses build, database, kunci API, atau langganan layanan. Website dan versi HTML mandiri memakai stack font sistem yang sama (Arial/Helvetica dan Georgia/Times New Roman), tanpa unduhan font eksternal. Perbedaan font cadangan antar sistem operasi tetap mungkin terjadi.

Untuk membuat satu file presentasi yang menyertakan gambar, CSS, dan JavaScript:

```sh
python3 tools/build_offline.py
```

Buka hasilnya, `Assyabab-Prototype.html`, di browser. Versi ini tidak memuat font eksternal; tautan WhatsApp dan YouTube tetap memerlukan internet saat diklik.

## Implementasi

- `index.html`: profil, visi-misi, 4T, kurikulum, multimedia, kegiatan harian, galeri, pengajar, kontak, dan FAQ.
- `styles.css`: tata letak dasar dan ilustrasi Al-Qur'an 3D tanpa WebGL.
- `refinements.css`: peningkatan keterbacaan, pembuka seluler, warna foto, dan diagram 4T revisi 2.
- `app.js`: navigasi seluler, pengungkapan konten saat digulir, pilihan kegiatan harian, galeri, dan pembesaran foto.
- `assets/`: delapan foto AVIF, dua varian detail responsif dari gambar asli PPT, dan ikon SVG konsep.

Tidak menggunakan Three.js, video otomatis, rangkaian frame, framework runtime, pelacakan, atau layanan berbayar. Efek gerak mengikuti preferensi pengurangan animasi; efek kemiringan buku hanya aktif pada perangkat dengan pointer presisi. Konten utama tetap terbaca tanpa JavaScript.

## Sumber dan status

Konten bersumber dari `Pesantren Assyabab Profile and Programs.pptx` yang diberikan pemilik proyek. Kontak dan tahun penerimaan mengikuti brosur pada slide 34. Rincian asal gambar dan batasan verifikasi tercatat dalam `docs/CONTENT-SOURCES.md`.

Ini prototipe antarmuka, bukan sistem pendaftaran daring. Tombol kontak membuka WhatsApp; tidak ada data pendaftaran yang disimpan atau dikirim otomatis. Logo adalah usulan identitas visual untuk prototipe, bukan konfirmasi logo resmi. Metadata `noindex,nofollow` sengaja dipasang selama tahap presentasi.

Nama/jabatan pengelola, nomor kontak, izin penggunaan foto, biaya, kuota, ketentuan bantuan, dan tahun penerimaan harus dikonfirmasi sebelum peluncuran resmi. Unggahan ke repository tidak otomatis mengaktifkan hosting publik. File statis dapat dihosting setelah layanan hosting proyek diaktifkan.

## Pengujian

Lihat `docs/TESTING.md` dan `docs/test-report-v2.json`. Revisi 2 diuji pada Chromium di sepuluh lebar viewport 320–1920 piksel menggunakan HTML mandiri. Tersedia skrip pengujian ulang `tools/test_ui.py`. Ini bukan pengujian hosting publik, seluruh perangkat fisik, atau skor Lighthouse.

Dikembangkan untuk Azriel Choerul Hakim.

## Revisi 2

- Tulisan utama HP 16 px dan tombol utama 14 px; jarak serta keterbacaan kurikulum, pengajar, kontak, dan FAQ disesuaikan.
- Area ilustrasi pembuka HP dipadatkan tanpa menghapus ilustrasi Al-Qur'an; keterangan kecil yang tertutup buku dihapus pada HP.
- Penjelasan pembuka lebih konkret; tombol utama menjadi “Jelajahi program” dan “Tanya pendaftaran”.
- Diagram 4T interaktif dua arah, termasuk pengoperasian keyboard.
- Foto Gunung Salak 780×1020 dan potret Mudir 600×587 diekspor dari gambar sumber yang lebih besar. Versi kecil tetap tersedia melalui srcset.
- Font daring dihilangkan; builder mandiri memuat semua lapisan CSS dalam urutan yang sama.
- Fokus menu, galeri, pengembalian fokus pembesaran foto, dan preferensi pengurangan animasi diperbaiki.

Konten faktual, batasan konfirmasi, kontak, dan periode penerimaan tidak diubah atau diverifikasi ulang oleh revisi visual ini.
