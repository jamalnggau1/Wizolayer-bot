Berikut adalah contoh lengkap file `README.md` yang bisa kamu gunakan untuk proyek GitHub-mu:

---

# 🧠 Wizolayer Auto Task & Mining Bot

Skrip otomatisasi ini digunakan untuk menyelesaikan task dan melakukan mining secara bergantian untuk banyak akun di situs [wizolayer.xyz](https://wizolayer.xyz?ref=5380869432).

## 🚀 Fitur

* Menyelesaikan semua task 1x di awal untuk semua akun.
* Melakukan proses mining setiap 5 menit secara bergiliran dari akun pertama hingga terakhir, lalu mengulang.
* Otomatis refresh token jika sudah expired.
* Dukungan multi-akun (disimpan dalam satu file JSON Lines).

---

## 📁 Struktur File

```bash
.
├── main.py                  # File utama bot
├── config.json              # API key Supabase (jangan diupload)
├── multi_token.jsonl        # Daftar akun/token (jangan diupload)
├── config.example.json      # Contoh format config.json
├── multi_token.example.jsonl# Contoh format multi_token.jsonl
└── README.md                # Dokumentasi proyek
```

---

## ⚙️ Instalasi

1. Clone repo:

```bash
git clone https://github.com/namauser/wizolayer-bot.git
cd wizolayer-bot
```

2. Install dependensi:

```bash
pip install requests urllib3
```

3. Siapkan file konfigurasi:

### `config.json`

```json
{
  "apikey": "ISI_APIKEY_KAMU_DISINI"
}
```

### `multi_token.jsonl`

Berisi banyak akun dengan format JSON Lines (1 akun per baris):

```json
{"access_token": "TOKEN1", "refresh_token": "REFRESH1", "expires_in": 3600, "token_type": "bearer", "expires_at": 1752318580}
{"access_token": "TOKEN2", "refresh_token": "REFRESH2", "expires_in": 3600, "token_type": "bearer", "expires_at": 1752318580}
```

> 🔒 **PERINGATAN**: Jangan upload `config.json` dan `multi_token.jsonl` ke GitHub!

---

## ▶️ Menjalankan Bot

```bash
python main.py
```

* Semua akun akan menyelesaikan task (sekali).
* Lalu mining akan berjalan terus-menerus, bergiliran per akun setiap 5 menit.
* Tekan `Ctrl+C` untuk menghentikan program.

---

## 🛡️ Tips Keamanan

* Tambahkan ini ke `.gitignore`:

```
config.json
multi_token.jsonl
```

* Gunakan `config.example.json` dan `multi_token.example.jsonl` sebagai template saja.

---

## 📄 Lisensi

Proyek ini bersifat open-source dan bebas digunakan, tetapi **dilarang memperjualbelikan token atau kode pribadi** orang lain.

---

Jika kamu butuh bantuan untuk menyiapkan `.gitignore`, `example.json`, atau membuat versi release di GitHub, tinggal bilang ya.
