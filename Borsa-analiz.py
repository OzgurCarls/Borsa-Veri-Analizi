import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def hisse_verisi_cek(sembol, period="3mo"):
    """Belirtilen hisse için Yahoo Finance'den veri çeker."""
    return yf.download(sembol, period=period)


def temel_istatistikler(df, isim):
    """Kapanış fiyatı için temel istatistikleri yazdırır."""
    print(f"\n=== {isim} - TEMEL İSTATİSTİKLER ===")
    print(df["Close"].describe())


def gunluk_degisim(df):
    """Günlük yüzde değişimi hesaplar ve tabloya ekler."""
    df["Degisim"] = df["Close"].pct_change() * 100
    return df

def volatilite_hesapla(df):
    """Günlük değişimlerin standart sapmasını hesaplar (volatilite)."""
    return df["Degisim"].std()

def rsi_hesapla(df, period=14):
    """RSI (Relative Strength Index) hesaplar."""
    fark = df["Close"].diff()

    kazanc = fark.where(fark > 0, 0)
    kayip = -fark.where(fark < 0, 0)

    ortalama_kazanc = kazanc.rolling(window=period).mean()
    ortalama_kayip = kayip.rolling(window=period).mean()

    rs = ortalama_kazanc / ortalama_kayip
    rsi = 100 - (100 / (1 + rs))

    return rsi

def sonuclari_excele_kaydet(ozet_liste, dosya_adi="rapor.xlsx"):
    """Hisse özetlerini Excel dosyasına kaydeder."""
    ozet_df = pd.DataFrame(ozet_liste)
    ozet_df.to_excel(dosya_adi, index=False)
    print(f"\n✅ Rapor kaydedildi: {dosya_adi}")

def rsi_grafik_ciz(veriler):
    """Tüm hisselerin RSI grafiğini 2x2 ızgarada çizer."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    axes = axes.flatten()

    for i, (isim, df) in enumerate(veriler.items()):
        ax = axes[i]
        ax.plot(df["RSI"], color="purple")
        ax.axhline(70, color="red", linestyle="--", label="Aşırı Alım (70)")
        ax.axhline(30, color="green", linestyle="--", label="Aşırı Satım (30)")
        ax.set_title(f"{isim} - RSI")
        ax.set_ylim(0, 100)
        ax.legend(fontsize=8)
        ax.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    hisseler = {
        "Tupraş": "TUPRS.IS",
        "THY": "THYAO.IS",
        "Garanti": "GARAN.IS",
        "Akbank": "AKBNK.IS"
    }

    veriler = {}
    ozet_liste = []  # Yeni: her hissenin özetini burada toplayacağız

    for isim, sembol in hisseler.items():
        print(f"\n{'='*40}")
        print(f"  {isim} ({sembol})")
        print(f"{'='*40}")

        df = hisse_verisi_cek(sembol)
        veriler[isim] = df

        temel_istatistikler(df, isim)

        df = gunluk_degisim(df)
        print(f"\nEn yüksek günlük değişim: {df['Degisim'].max():.2f}%")
        print(f"En düşük günlük değişim: {df['Degisim'].min():.2f}%")

        vol = volatilite_hesapla(df)
        print(f"Volatilite (std): {vol:.2f}%")

        df["RSI"] = rsi_hesapla(df)
        son_rsi = df["RSI"].iloc[-1]
        print(f"Son RSI değeri: {son_rsi:.2f}")

        if son_rsi > 70:
            sinyal = "AŞIRI ALIM"
        elif son_rsi < 30:
            sinyal = "AŞIRI SATIM"
        else:
            sinyal = "NORMAL"
        print(f"→ Sinyal: {sinyal}")

        # Yeni eklenen kısım: özet bilgileri sakla
        ozet_liste.append({
            "Hisse": isim,
            "Sembol": sembol,
            "Son Kapanış": round(df["Close"].iloc[-1].item(), 2),
            "En Yüksek Değişim (%)": round(df["Degisim"].max(), 2),
            "En Düşük Değişim (%)": round(df["Degisim"].min(), 2),
            "Volatilite (%)": round(vol, 2),
            "RSI": round(son_rsi, 2),
            "Sinyal": sinyal
        })

    # Tüm hisseler işlendikten sonra Excel'e kaydet
    sonuclari_excele_kaydet(ozet_liste)

    rsi_grafik_ciz(veriler)
    sonuclari_excele_kaydet(ozet_liste)

            