import network
import socket
import ujson
import ucryptolib
import hashlib
import time

# Configurações do Wi-Fi
SSID = 'MB_Quarto'
PASSWORD = 'YtR3421mbm17'

# Chaves
HMAC_KEY = b'secrethmackey123'  # Deve ter 16 bytes para HMAC
AES_KEY = bytearray([0xfa, 0x27, 0xf2, 0xf5, 0xe4, 0x19, 0x46, 0x77,
                     0x88, 0x96, 0xa6, 0x0B, 0xd9, 0xd7, 0xe5, 0x2F,
                     0xae, 0x14, 0x23, 0x15, 0x45, 0xe7, 0xed, 0xef,
                     0xcc, 0x22, 0xb6, 0xc4, 0xde, 0x34, 0x22, 0x11])
AES_IV = bytearray([0x1a, 0x25, 0xf1, 0xa3, 0xf4, 0x29, 0x4f, 0x7a,
                    0x82, 0x1d, 0x6f, 0x0B, 0xd4, 0xd1, 0xb5, 0x1F])

# Configuração do servidor WebSocket
SERVER_URI = "192.168.2.101"  # Substitua pelo IP do servidor
SERVER_PORT = 8765

# Função para conectar ao Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        time.sleep(1)

    print("Conectado ao Wi-Fi:", wlan.ifconfig())

# Função para calcular HMAC
def calculate_hmac(key, message):
    block_size = 64  # 64 bytes para SHA-256
    if len(key) > block_size:
        key = hashlib.sha256(key).digest()
    key += b'\x00' * (block_size - len(key))

    o_key_pad = bytes((x ^ 0x5c) for x in key)
    i_key_pad = bytes((x ^ 0x36) for x in key)

    hmac_hash = hashlib.sha256(o_key_pad + hashlib.sha256(i_key_pad + message).digest()).digest()
    return hmac_hash

def pkcs7_pad(data):
    """Aplica o padding PKCS#7 nos dados."""
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data):
    """Remove o padding PKCS#7 dos dados."""
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_message(message):
    """Criptografa a mensagem usando AES CBC."""
    # Aplica o padding
    padded_message = pkcs7_pad(message)

    # Cria o cifrador AES em modo CBC
    cipher = ucryptolib.aes(AES_KEY, 1, AES_IV)  # 1 representa o modo CBC
    
    # Criptografa os dados
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message

def decrypt_message(encrypted_data):
    """Descriptografa os dados usando AES CBC."""
    cipher = ucryptolib.aes(AES_KEY, 1, AES_IV)  # 1 representa o modo CBC
    decrypted_data = cipher.decrypt(encrypted_data)
    return pkcs7_unpad(decrypted_data)

# Função para enviar dados do sensor
def send_sensor_data(sensor_id, value):
    s = None  # Inicializa a variável de socket
    try:
        # Preparando a mensagem
        message_data = {
            "sensor_id": sensor_id,
            "value": value,
            "did": f"did:example:{sensor_id}"  # Exemplo de DID
        }
        message_json = ujson.dumps(message_data).encode()

        # Criptografando a mensagem
        encrypted_data = encrypt_message(message_json)

        # Calculando HMAC
        hmac_value = calculate_hmac(HMAC_KEY, message_json)

        # Combinando HMAC e dados criptografados
        message_to_send = hmac_value + encrypted_data

        # Conectando ao servidor WebSocket
        addr = socket.getaddrinfo(SERVER_URI, SERVER_PORT)[0]
        s = socket.socket()
        s.connect(addr)

        # Enviando a mensagem ao servidor
        s.send(message_to_send)

        # Recebendo a resposta do servidor
        response = s.recv(1024)
        print("Resposta do servidor:", response)

    except Exception as e:
        print("Erro ao enviar dados:", e)
    finally:
        if s:
            s.close() 

# Programa principal
if __name__ == "__main__":
    connect_wifi(SSID, PASSWORD)

    # Dados do sensor
    sensors_data = {
        "sensor_1": 25.4,
        "sensor_2": 30.1,
        "sensor_3": 22.7
    }

    while True:
        for sensor_id, sensor_value in sensors_data.items():
            send_sensor_data(sensor_id, sensor_value)
            time.sleep(2)  # Envia a cada 2 segundos
