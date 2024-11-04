import asyncio
import websockets
import hmac
import hashlib
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

# Chaves secretas para HMAC e AES
HMAC_KEY = b'secrethmackey123'  # Deve ter 16 bytes para HMAC
AES_KEY = bytearray([0xfa, 0x27, 0xf2, 0xf5, 0xe4, 0x19, 0x46, 0x77,
                     0x88, 0x96, 0xa6, 0x0B, 0xd9, 0xd7, 0xe5, 0x2F,
                     0xae, 0x14, 0x23, 0x15, 0x45, 0xe7, 0xed, 0xef,
                     0xcc, 0x22, 0xb6, 0xc4, 0xde, 0x34, 0x22, 0x11])
# Status dos sensores e DIDs
sensors_status = {}
sensors_dids = {}  # Dicionário para armazenar DIDs

active_tls = False  # Controle de TLS

# Função para descriptografar mensagens
def decrypt_message(encrypted_message):
    try:
        # O IV está contido nos primeiros 16 bytes
        iv = encrypted_message[:16]
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
        return decrypted_message.rstrip(b'\0')  # Remove padding nulo, se necessário
    except Exception as e:
        print(f"Erro ao descriptografar mensagem: {e}")
        return None

# Função para verificar HMAC
def verify_hmac(message, hmac_received):
    hmac_calculated = hmac.new(HMAC_KEY, message, hashlib.sha256).digest()
    return hmac.compare_digest(hmac_calculated, hmac_received)

async def handle_connection(websocket, path):
    global sensors_status, sensors_dids

    async for message in websocket:
        try:
            # Decodificando a mensagem recebida
            decoded_message = base64.b64decode(message)
            
            # Extraindo HMAC e dados criptografados
            hmac_received = decoded_message[:32]  # 32 bytes para HMAC SHA-256
            encrypted_data = decoded_message[32:]

            # Descriptografando a mensagem
            decrypted_message = decrypt_message(encrypted_data)
            if decrypted_message is None:
                continue  # Se houver erro na descriptografia, ignorar a mensagem

            # Verificando HMAC
            if not verify_hmac(decrypted_message, hmac_received):
                print("Falha na verificação do HMAC")
                continue

            # Processando a mensagem
            message_data = json.loads(decrypted_message.decode())
            sensor_id = message_data.get('sensor_id')
            sensor_value = message_data.get('value')
            sensor_did = message_data.get('did')  # Obtendo o DID

            if sensor_id is None or sensor_value is None or sensor_did is None:
                print("Dados do sensor inválidos")
                continue

            # Atualizando o status do sensor
            sensors_status[sensor_id] = sensor_value
            sensors_dids[sensor_id] = sensor_did  # Associando o sensor ao seu DID

            # Imprimindo informações no terminal
            print(f"Recebendo de {sensor_id} (DID: {sensor_did}): {sensor_value}")
            print(f"Status atual do sensor: {sensors_status}")
            print(f"DIDs dos sensores: {sensors_dids}")

            # Enviando resposta para o sensor
            response = {"status": "Received", "sensors": sensors_status}
            await websocket.send(json.dumps(response))

        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

async def start_server():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Servidor instanciado em ws://localhost:8765")
        print(f"TLS ativo: {active_tls}")  # Imprime se o TLS está ativo
        await asyncio.Future()  # Executa indefinidamente

if __name__ == "__main__":
    asyncio.run(start_server())
