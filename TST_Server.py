import asyncio
import websockets
import hmac
import hashlib
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

# Chaves secretas para HMAC e AES
HMAC_KEY = b'secrethmackey123'  # Deve ter 16 bytes para HMAC
AES_KEY = bytearray([0xfa, 0x27, 0xf2, 0xf5, 0xe4, 0x19, 0x46, 0x77,
                     0x88, 0x96, 0xa6, 0x0B, 0xd9, 0xd7, 0xe5, 0x2F,
                     0xae, 0x14, 0x23, 0x15, 0x45, 0xe7, 0xed, 0xef,
                     0xcc, 0x22, 0xb6, 0xc4, 0xde, 0x34, 0x22, 0x11])

# Função para criptografar mensagens
def encrypt_message(message):
    iv = os.urandom(16)  # Gera um novo IV aleatório
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad message to be a multiple of block size
    padded_message = message + (b'\0' * (16 - len(message) % 16))
    
    encrypted_message = iv + encryptor.update(padded_message) + encryptor.finalize()
    return encrypted_message

# Função para calcular HMAC
def calculate_hmac(message):
    return hmac.new(HMAC_KEY, message, hashlib.sha256).digest()

async def send_sensor_data(sensor_id, value, did):
    uri = "ws://localhost:8765"
    
    async with websockets.connect(uri) as websocket:
        # Preparando a mensagem
        message_data = {
            "sensor_id": sensor_id,
            "value": value,
            "did": did  # Incluindo o DID
        }
        message_json = json.dumps(message_data).encode()
        
        # Criptografando a mensagem
        encrypted_data = encrypt_message(message_json)
        
        # Calculando HMAC
        hmac_value = calculate_hmac(message_json)  # HMAC deve ser calculado a partir da mensagem original
        
        # Combinando HMAC e dados criptografados
        message_to_send = base64.b64encode(hmac_value + encrypted_data)
        
        # Enviando a mensagem ao servidor
        await websocket.send(message_to_send)
        
        # Recebendo a resposta do servidor
        response = await websocket.recv()
        print(f"Response from server: {response}")

if __name__ == "__main__":
    sensors_data = {
        "sensor_1": 25.4,
        "sensor_2": 30.1,
        "sensor_3": 22.7
    }
    
    # Exemplos de DIDs para cada sensor
    sensors_dids = {
        "sensor_1": "did:1234",
        "sensor_2": "did:5678",
        "sensor_3": "did:9012"
    }

    for sensor_id, sensor_value in sensors_data.items():
        did = sensors_dids[sensor_id]  # Obtendo o DID correspondente
        asyncio.run(send_sensor_data(sensor_id, sensor_value, did))
