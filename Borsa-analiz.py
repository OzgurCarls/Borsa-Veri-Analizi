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


def macd_hesapla(df, hizli=12, yavas=26, sinyal_period=9):
    """
    MACD (Moving Average Convergence Divergence) hesaplar.

    İki EMA arasındaki fark momentum'u (ivmeyi) ölçer:
    - Hızlı EMA (12 gün): kısa vadeli trendi yansıtır
    - Yavaş EMA (26 gün): uzun vadeli trendi yansıtır
    MACD çizgisi bu ikisinin farkıdır; sıfırın üstü yükseliş, altı düşüş eğilimi.
    """
    # .squeeze(): yfinance bazen tek sütunlu DataFrame döndürür, Series'e çeviriyoruz
    kapanislar = df["Close"].squeeze()

    # ewm() = Exponential Weighted Mean; son verilere daha fazla ağırlık verir
    hizli_ema = kapanislar.ewm(span=hizli, adjust=False).mean()
    yavas_ema = kapanislar.ewm(span=yavas, adjust=False).mean()

    # MACD çizgisi: iki EMA arasındaki fark
    macd_cizgisi = hizli_ema - yavas_ema

    # Sinyal çizgisi: MACD'nin 9 günlük EMA'sı (daha düzgün bir çizgi)
    sinyal_cizgisi = macd_cizgisi.ewm(span=sinyal_period, adjust=False).mean()

    # Histogram: MACD ile sinyal arasındaki fark (momentum'un gücünü gösterir)
    histogram = macd_cizgisi - sinyal_cizgisi

    return macd_cizgisi, sinyal_cizgisi, histogram


def bollinger_hesapla(df, period=20, carpan=2):
    """
    Bollinger Bantlarını hesaplar.

    Fiyatın ne kadar geniş bir aralıkta hareket ettiğini gösterir:
    - Orta bant: 20 günlük basit hareketli ortalama (SMA)
    - Üst/Alt bantlar: orta ± (2 x standart sapma)
    Fiyat üst banda yaklaşırsa aşırı alım, alt banda yaklaşırsa aşırı satım olabilir.
    """
    kapanislar = df["Close"].squeeze()

    # Basit hareketli ortalama (SMA): son 20 günün ortalaması
    orta_bant = kapanislar.rolling(window=period).mean()

    # Standart sapma: fiyatın ortalamadan ne kadar saptığını ölçer
    std = kapanislar.rolling(window=period).std()

    ust_bant = orta_bant + (carpan * std)
    alt_bant = orta_bant - (carpan * std)

    return ust_bant, orta_bant, alt_bant


def rsi_grafik_ciz(veriler):
    """Tüm hisselerin RSI grafiğini 2x2 ızgarada çizer."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("RSI Göstergesi", fontsize=14)
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


def macd_grafik_ciz(veriler):
    """Tüm hisselerin MACD grafiğini 2x2 ızgarada çizer."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("MACD Göstergesi", fontsize=14)
    axes = axes.flatten()

    for i, (isim, df) in enumerate(veriler.items()):
        ax = axes[i]

        # MACD ve sinyal çizgileri
        ax.plot(df["MACD"], color="blue", label="MACD", linewidth=1.5)
        ax.plot(df["MACD_Sinyal"], color="orange", label="Sinyal", linewidth=1.5)

        # Histogram: pozitif → yeşil (momentum artıyor), negatif → kırmızı (azalıyor)
        pozitif = df["MACD_Histogram"].where(df["MACD_Histogram"] >= 0, 0)
        negatif = df["MACD_Histogram"].where(df["MACD_Histogram"] < 0, 0)
        ax.bar(df.index, pozitif, color="green", alpha=0.4)
        ax.bar(df.index, negatif, color="red", alpha=0.4)

        ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
        ax.set_title(f"{isim} - MACD")
        ax.legend(fontsize=8)
        ax.grid(True)

    plt.tight_layout()
    plt.show()


def bollinger_grafik_ciz(veriler):
    """Tüm hisselerin Bollinger Bantları grafiğini 2x2 ızgarada çizer."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Bollinger Bantları", fontsize=14)
    axes = axes.flatten()

    for i, (isim, df) in enumerate(veriler.items()):
        ax = axes[i]
        kapanislar = df["Close"].squeeze()

        # Fiyat çizgisi
        ax.plot(kapanislar, color="black", label="Kapanış", linewidth=1.5)

        # Bollinger bantları
        ax.plot(df["BB_Ust"], color="red", linestyle="--", label="Üst Bant", linewidth=1)
        ax.plot(df["BB_Orta"], color="blue", linestyle="--", label="SMA 20", linewidth=1)
        ax.plot(df["BB_Alt"], color="green", linestyle="--", label="Alt Bant", linewidth=1)

        # Bantlar arasını hafifçe renklendir (görsel netlik için)
        ax.fill_between(df.index, df["BB_Ust"], df["BB_Alt"], alpha=0.08, color="blue")

        ax.set_title(f"{isim} - Bollinger Bantları")
        ax.legend(fontsize=8)
        ax.grid(True)

    plt.tight_layout()
    plt.show()


def sonuclari_excele_kaydet(ozet_liste, dosya_adi="rapor.xlsx"):
    """Hisse özetlerini Excel dosyasına kaydeder."""
    ozet_df = pd.DataFrame(ozet_liste)
    ozet_df.to_excel(dosya_adi, index=False)
    print(f"\n Rapor kaydedildi: {dosya_adi}")


if __name__ == "__main__":
    hisseler = {
        "Tupraş": "TUPRS.IS",
        "THY": "THYAO.IS",
        "Garanti": "GARAN.IS",
        "Akbank": "AKBNK.IS"
    }

    veriler = {}
    ozet_liste = []

    for isim, sembol in hisseler.items():
        print(f"\n{'='*40}")
        print(f"  {isim} ({sembol})")
        print(f"{'='*40}")

        df = hisse_verisi_cek(sembol)
        veriler[isim] = df  # grafikler için saklıyoruz (referans, sütunlar sonradan eklenir)

        temel_istatistikler(df, isim)

        df = gunluk_degisim(df)
        print(f"\nEn yüksek günlük değişim: {df['Degisim'].max():.2f}%")
        print(f"En düşük günlük değişim: {df['Degisim'].min():.2f}%")

        vol = volatilite_hesapla(df)
        print(f"Volatilite (std): {vol:.2f}%")

        # --- RSI ---
        df["RSI"] = rsi_hesapla(df)
        son_rsi = df["RSI"].iloc[-1].item()
        print(f"Son RSI: {son_rsi:.2f}")

        if son_rsi > 70:
            rsi_sinyal = "AŞIRI ALIM"
        elif son_rsi < 30:
            rsi_sinyal = "AŞIRI SATIM"
        else:
            rsi_sinyal = "NORMAL"
        print(f">> RSI Sinyali: {rsi_sinyal}")

        # --- MACD ---
        df["MACD"], df["MACD_Sinyal"], df["MACD_Histogram"] = macd_hesapla(df)
        son_macd = df["MACD"].iloc[-1].item()
        son_macd_sinyal = df["MACD_Sinyal"].iloc[-1].item()

        # MACD > Sinyal ise yükseliş eğilimi var
        if son_macd > son_macd_sinyal:
            macd_sinyal = "YÜKSELİŞ"
        else:
            macd_sinyal = "DÜŞÜŞ"
        print(f"Son MACD: {son_macd:.4f} | Sinyal: {son_macd_sinyal:.4f} >> {macd_sinyal}")

        # --- Bollinger Bantları ---
        df["BB_Ust"], df["BB_Orta"], df["BB_Alt"] = bollinger_hesapla(df)
        son_kapanis = df["Close"].iloc[-1].item()
        son_ust = df["BB_Ust"].iloc[-1].item()
        son_alt = df["BB_Alt"].iloc[-1].item()

        if son_kapanis > son_ust:
            bb_durum = "UST BANDIN UZERINDE"
        elif son_kapanis < son_alt:
            bb_durum = "ALT BANDIN ALTINDA"
        else:
            bb_durum = "BANT ICINDE"
        print(f"Bollinger Durumu: {bb_durum}")

        ozet_liste.append({
            "Hisse": isim,
            "Sembol": sembol,
            "Son Kapanış": round(son_kapanis, 2),
            "En Yüksek Değişim (%)": round(df["Degisim"].max(), 2),
            "En Düşük Değişim (%)": round(df["Degisim"].min(), 2),
            "Volatilite (%)": round(vol, 2),
            "RSI": round(son_rsi, 2),
            "RSI Sinyali": rsi_sinyal,
            "MACD Sinyali": macd_sinyal,
            "Bollinger Durumu": bb_durum,
        })

    # Tüm hisseler işlendikten sonra Excel'e kaydet (tek seferlik)
    sonuclari_excele_kaydet(ozet_liste)

    # Grafikler
    rsi_grafik_ciz(veriler)
    macd_grafik_ciz(veriler)
    bollinger_grafik_ciz(veriler)
