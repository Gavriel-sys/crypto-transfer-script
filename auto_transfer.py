from web3 import Web3
import time

# Koneksi ke node Ethereum (gunakan Infura atau node Anda sendiri)
infura_url = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'  # Ganti dengan URL Infura atau node lokal Anda
web3 = Web3(Web3.HTTPProvider(infura_url))

# Verifikasi koneksi
if web3.isConnected():
    print("Terhubung ke Ethereum")
else:
    print("Tidak terhubung ke Ethereum")

# Informasi wallet
private_key = 'YOUR_PRIVATE_KEY'  # Ganti dengan private key wallet yang diretas
wallet_address = 'YOUR_WALLET_ADDRESS'  # Ganti dengan address wallet yang diretas
new_wallet_address = 'NEW_WALLET_ADDRESS'  # Ganti dengan address wallet baru Anda

# Fungsi untuk memeriksa saldo gas fee dan melakukan transfer koin
def check_and_transfer():
    balance = web3.eth.get_balance(wallet_address)
    gas_price = web3.eth.gas_price
    gas_limit = 21000  # Gas limit untuk transaksi dasar

    # Jika saldo cukup untuk gas fee
    if balance > gas_price * gas_limit:
        # Buat transaksi
        nonce = web3.eth.get_transaction_count(wallet_address)
        tx = {
            'nonce': nonce,
            'to': new_wallet_address,
            'value': balance - gas_price * gas_limit,  # Transfer semua koin yang tersisa kecuali gas fee
            'gas': gas_limit,
            'gasPrice': gas_price
        }

        # Tanda tangani transaksi
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        # Kirim transaksi
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaksi terkirim dengan hash: {web3.to_hex(tx_hash)}")

        return True
    return False

# Jalankan loop untuk memantau saldo dan melakukan transfer otomatis
while True:
    if check_and_transfer():
        print("Transfer berhasil, script berhenti.")
        break
    else:
        print("Saldo tidak cukup untuk gas fee, cek ulang dalam 30 detik.")
        time.sleep(30)
