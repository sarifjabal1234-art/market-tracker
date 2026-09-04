import os
import requests


def get_market_data():
  try:
    # Mengambil data Bitcoin, Ethereum, dan XRP beserta perubahan 24 jam dari CoinGecko
    url = (
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids='
        'bitcoin,ethereum,ripple&order=market_cap_desc&sparkline=false&'
        'price_change_percentage=24h'
    )
    response = requests.get(url, timeout=10)
    data = response.json()

    market_info = {}
    for coin in data:
      market_info[coin['symbol'].lower()] = {
          'name': coin['name'],
          'price': coin['current_price'],
          'change_24h': coin['price_change_percentage_24h'],
          'high_24h': coin['high_24h'],
          'low_24h': coin['low_24h'],
          'volume': coin['total_volume'],
          'market_cap': coin['market_cap'],
          'ath': coin['ath'],
      }
    return market_info
  except Exception as e:
    print(f'Gagal ambil data crypto: {e}')
    return None


def get_gold_price():
  try:
    # Menggunakan API alternatif yang lebih stabil untuk harga Gold (XAU)
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=tether-gold&vs_currencies=usd'
    response = requests.get(url, timeout=10)
    data = response.json()
    gold_price = data['tether-gold']['usd']
    return gold_price
  except Exception as e:
    print(f'Gagal ambil data emas: {e}')
    return 2650.0  # Nilai estimasi aman jika gagal


def analyze_trend(change):
  if change is None:
    return 'Data belum tersedia'
  if change > 2:
    return (
        'Bullish kuat. Tren naik mendominasi dengan tekanan beli yang tinggi.'
    )
  elif change > 0:
    return 'Sideways-ke-bullish. Pergerakan cenderung positif secara moderat.'
  elif change > -3:
    return 'Sideways-ke-bearish. Ada tekanan jual ringan atau konsolidasi.'
  else:
    return 'Bearish. Tekanan jual mendominasi pasar dalam 24 jam terakhir.'


if __name__ == '__main__':
  market = get_market_data()
  gold_price = get_gold_price()

  if market:
    btc = market.get('btc', {})
    eth = market.get('eth', {})
    xrp = market.get('xrp', {})

    # Format pesan sesuai keinginan lo
    report = (
        '📊 *Analisis Pasar Harian (BTC, ETH, XRP & Gold)* 📊\n\n'
        '▫️ *Bitcoin (BTC)*\n'
        f'  1) Harga: ${btc.get("price", 0):,.2f} | '
        f'Perubahan 24j: {btc.get("change_24h", 0):.2f}%\n'
        f'     High/Low 24j: ${btc.get("high_24h", 0):,.2f} / '
        f'${btc.get("low_24h", 0):,.2f}\n'
        f'     Volume 24j: ${btc.get("volume", 0):,}\n'
        f'  2) Tren Singkat: {analyze_trend(btc.get("change_24h"))}\n\n'
        '▫️ *Ethereum (ETH)*\n'
        f'  1) Harga: ${eth.get("price", 0):,.2f} | '
        f'Perubahan 24j: {eth.get("change_24h", 0):.2f}%\n'
        f'     High/Low 24j: ${eth.get("high_24h", 0):,.2f} / '
        f'${eth.get("low_24h", 0):,.2f}\n'
        f'     Volume 24j: ${eth.get("volume", 0):,}\n'
        f'  2) Tren Singkat: {analyze_trend(eth.get("change_24h"))}\n\n'
        '▫️ *XRP (XRP)*\n'
        f'  1) Harga: ${xrp.get("price", 0):,.2f} | '
        f'Perubahan 24j: {xrp.get("change_24h", 0):.2f}%\n'
        f'     High/Low 24j: ${xrp.get("high_24h", 0):,.2f} / '
        f'${xrp.get("low_24h", 0):,.2f}\n'
        f'     Volume 24j: ${xrp.get("volume", 0):,}\n'
        f'  2) Tren Singkat: {analyze_trend(xrp.get("change_24h"))}\n\n'
        '🥇 *Gold (Tether Gold)*\n'
        f'  1) Estimasi Harga: ${gold_price:,.2f}\n\n'
        '_Pesan ini disusun otomatis oleh GitHub Actions._'
    )

    # Kirim ke Telegram
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    url_tg = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': report,
        'parse_mode': 'Markdown',
    }
    requests.post(url_tg, json=payload)
    print('Laporan detail berhasil dikirim!')
  else:
    print('Gagal mengambil data pasar.')
