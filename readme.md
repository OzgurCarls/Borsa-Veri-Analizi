# 📊 BIST Hisse Senedi Analiz Aracı

Python ile gerçek zamanlı borsa verisi çekip teknik analiz yapan bir araç. Birden fazla hisseyi otomatik analiz eder, RSI hesaplar, alım/satım sinyalleri üretir ve sonuçları Excel raporu olarak kaydeder.

## Özellikler

- 📈 Yahoo Finance API üzerinden gerçek hisse verisi çekme (`yfinance`)
- 📊 Temel istatistiksel özet (ortalama, std, min/max)
- 📉 Günlük yüzde değişim hesaplama
- ⚡ Volatilite (risk) ölçümü
- 🎯 RSI (Relative Strength Index) hesaplama ve aşırı alım/satım sinyalleri
- 🔄 Birden fazla hisseyi tek seferde analiz etme
- 📑 Sonuçları Excel raporu olarak kaydetme (`rapor.xlsx`)
- 📊 2x2 grid'de RSI grafikleri (matplotlib subplots)

## Kullanılan Teknolojiler

- Python 3.12
- pandas
- yfinance
- matplotlib
- openpyxl

## Kurulum

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
python Borsa-analiz.py
```

## Analiz Edilen Hisseler

Varsayılan olarak şu BIST hisseleri analiz edilir (kolayca değiştirilebilir):
- Tupraş (TUPRS.IS)
- Türk Hava Yolları (THYAO.IS)
- Garanti BBVA (GARAN.IS)
- Akbank (AKBNK.IS)

## Örnek Çıktı

Her hisse için terminal çıktısı: