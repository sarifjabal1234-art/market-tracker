import os
import requests

# Konfigurasi Token dan Chat ID dari Environment Variables GitHub
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


def get_crypto_prices():
  try:
    # Mengambil data harga Bitcoin dan Ethereum dari CoinGecko API
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd'
    response = requests.get(url, timeout=10)
    data = response.json()
    btc_price = data['bitcoin']['usd']
    eth_price = data['ethereum']['usd']
    return btc_price, eth_price
  except Exception as e:
    print(f'Gagal ambil data crypto: {e}')
    return None, None


def get_gold_price():
  try:
    # Mengambil data harga Emas (Gold) dari API publik gratis (Yahoo Finance / alternatif)
    url = 'https://query1.finance.com/v8/finance/chart/GC=F?interval=1d&range=1d'
    # Menggunakan header agar tidak diblokir server Yahoo
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()
    gold_price = data['chart']['result'][0]['meta']['regularMarketPrice']
    return gold_price
  except Exception as e:
    print(f'Gagal ambil data emas: {e}')
    return 'Data Emas (Simulasi/Gagal)'


def send_telegram_message(message):
  url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
  payload = {
      'chat_id': TELEGRAM_CHAT_ID,
      'text': message,
      'parse_mode': 'Markdown',
  }
  response = requests.post(url, json=payload)
  return response.json()


if __name__ == '__main__':
  btc, eth = get_crypto_prices()
  gold = get_gold_price()

  # Format pesan laporan
  report = (
      '📊 *LAPORAN ANALISIS PASAR OTOMATIS* 📊\n\n'
      f'🪙 *Bitcoin (BTC):* ${btc:,}\n'
      f'🔹 *Ethereum (ETH):* ${eth:,}\n'
      f'🥇 *Gold (Emas):* ${gold}\n\n'
      '_Pesan ini dikirim otomatis oleh GitHub Actions._'
  )

  if btc and eth:
    send_telegram_message(report)
    print('Laporan berhasil dikirim ke Telegram!')
  else:
    print('Gagal memproses data pasar.')
