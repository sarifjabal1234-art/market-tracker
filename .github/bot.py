import os
import requests


def get_crypto_data():
  try:
    url = (
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids='
        'bitcoin,ripple&order=market_cap_desc&sparkline=false&'
        'price_change_percentage=24h'
    )
    response = requests.get(url, timeout=10)
    data = response.json()
    result = {}
    for coin in data:
      result[coin['symbol'].lower()] = coin
    return result
  except Exception as e:
    print(f'Gagal ambil data: {e}')
    return None


if __name__ == '__main__':
  data = get_crypto_data()

  if data and 'btc' in data and 'xrp' in data:
    btc = data['btc']
    xrp = data['xrp']

    # Hitung estimasi perubahan 7 jam atau narasi tren berbasis data nyata
    btc_change = btc.get('price_change_percentage_24h', 0)
    xrp_change = xrp.get('price_change_percentage_24h', 0)

    btc_trend = (
        'sideways-ke-bearish' if btc_change < 0 else 'sideways-ke-bullish'
    )
    xrp_trend = 'bearish' if xrp_change < 0 else 'bullish'

    report = (
        '📊 *Analisis Kripto Harian (BTC & XRP)*\n\n'
        '*- Bitcoin (BTC)*\n'
        f'  1) Harga & perubahan utama: ${btc["current_price"]:,}. '
        f'Perubahan 24 jam: {btc_change:.2f}%. '
        f'High/Low 24j: ${btc["high_24h"]:,} / ${btc["low_24h"]:,}. '
        f'Volume 24j ≈ ${btc["total_volume"]:,}; '
        f'Market cap ≈ ${btc["market_cap"]:,}.\n'
        f'  2) Tren singkat: {btc_trend}. Pergerakan harian menunjukkan '
        'tekanan pasar yang sedang berlangsung.\n'
        '  3) Sinyal umum: netral–cenderung '
        f'{"bearish" if btc_change < 0 else "bullish"}.\n\n'
        '*- XRP (XRP)*\n'
        f'  1) Harga & perubahan utama: ${xrp["current_price"]:,}. '
        f'Perubahan 24 jam: {xrp_change:.2f}%. '
        f'High/Low 24j: ${xrp["high_24h"]:,} / ${xrp["low_24h"]:,}. '
        f'Volume 24j ≈ ${xrp["total_volume"]:,}; '
        f'Market cap ≈ ${xrp["market_cap"]:,}.\n'
        f'  2) Tren singkat: {xrp_trend}.\n'
        '  3) Sinyal umum: '
        f'{"bearish" if xrp_change < 0 else "bullish"}.\n\n'
        '_Pesan otomatis dari GitHub Actions._'
    )

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    url_tg = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': report, 'parse_mode': 'Markdown'}
    requests.post(url_tg, json=payload)
    print('Berhasil kirim laporan detail!')
  else:
    print('Gagal memproses data.')
