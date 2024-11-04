># MackenzieSmartHUB

> Status: Em desenvolvimento..⚠️

Desenvolvimento de arquitetura de segurança robusta para redes I.o.T com AES+HMAC e TLS.

| Tecnologias utilizadas |    Versão    |
|------------------------|--------------|
| Python                 |   3.12.17    |
| Micropython            |   1.24.0     |
| ESP8266                |   2020.07.29 |

## Introdução

Neste projeto de Internet das Coisas (IoT), buscamos integrar uma camada robusta de segurança para garantir a proteção dos dados transmitidos entre dispositivos. Utilizamos o algoritmo de criptografia AES-128 para cifrar as informações, garantindo que apenas dispositivos autorizados possam acessar os dados sensíveis. Além disso, implementamos HMAC (Hash-based Message Authentication Code) para assegurar a integridade e a autenticidade das mensagens trocadas.

Para fortalecer ainda mais a segurança, empregamos o protocolo TLS 1.3, que oferece uma comunicação segura sobre a rede, protegendo os dados contra interceptações e ataques. Combinando essas tecnologias, nosso projeto não só atende às demandas funcionais da IoT, mas também estabelece um padrão elevado de segurança, essencial em um cenário onde a proteção da informação é cada vez mais crítica.

> ## Seção 1: Funcionalidades

- Criptografia de Dados com AES-128: O sistema utiliza o algoritmo AES-128 para cifrar todos os dados transmitidos entre os dispositivos. Isso assegura que as informações sensíveis permaneçam protegidas contra acessos não autorizados.

- Autenticação e Integridade com HMAC: Implementamos HMAC para verificar a integridade das mensagens. Isso garante que os dados não sejam alterados durante a transmissão e que o remetente seja autenticado, evitando ataques de falsificação.

- Comunicação Segura com TLS 1.3: O uso do protocolo TLS 1.3 proporciona uma camada adicional de segurança nas comunicações, garantindo que todos os dados trocados entre os dispositivos sejam criptografados e protegidos contra interceptações.

- Monitoramento em Tempo Real: O sistema permite monitorar dados em tempo real, possibilitando a coleta e visualização de informações cruciais sobre o ambiente ou processos que estão sendo geridos.

> ## Seção 2: Certificado Autoassinado com OpenSSL

Este guia fornece um passo a passo para criar um certificado autoassinado usando a ferramenta `OpenSSL`. Um certificado autoassinado é útil para ambientes de desenvolvimento e teste, onde não é necessário um certificado assinado por uma Autoridade Certificadora (CA).

Aqui está o passo a passo para criar um certificado autoassinado usando `OpenSSL`.

### 1. Instale o OpenSSL

Em muitos sistemas, o OpenSSL já vem instalado. Para verificar, execute:

```bash
openssl version
```

Se não estiver instalado, você pode instalá-lo usando o gerenciador de pacotes do sistema:

- **Ubuntu/Debian**:

    ```bash
    sudo apt update
    sudo apt install openssl
    ```

- **MacOS** (usando Homebrew):

    ```bash
    brew install openssl
    ```

### 2. Gere um Certificado Autoassinado

Aqui está o comando para criar um certificado e uma chave privada com validade de 365 dias:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server_key.pem -out server_cert.pem -days 365 -nodes
```

**Explicação dos parâmetros**:

- `req`: Indica que estamos gerando uma solicitação de assinatura de certificado.
- `x509`: Especifica que o certificado será autoassinado (não precisa de uma CA externa).
- `newkey rsa:4096`: Cria uma nova chave privada RSA com comprimento de 4096 bits.
- `keyout server_key.pem`: Especifica o arquivo onde será salva a chave privada.
- `out server_cert.pem`: Especifica o arquivo onde será salvo o certificado gerado.
- `days 365`: Define a validade do certificado (neste caso, 1 ano).
- `nodes`: Evita criptografia na chave privada, permitindo seu uso sem senha (útil para testes, mas não seguro para produção).

### 3. Preencha as Informações do Certificado

Depois de executar o comando, você será solicitado a fornecer informações para o certificado. Exemplos de informações solicitadas:

```plaintext
Country Name (2 letter code) [AU]: BR
State or Province Name (full name) [Some-State]: São Paulo
Locality Name (eg, city) []: São Paulo
Organization Name (eg, company) [Internet Widgits Pty Ltd]: Minha Empresa
Organizational Unit Name (eg, section) []: TI
Common Name (e.g. server FQDN or YOUR name) []: localhost
Email Address []: admin@minhaempresa.com
```

**Dica**: Use `localhost` para o **Common Name** caso o certificado seja para testes locais, pois ele deverá coincidir com o nome do host acessado no navegador ou aplicação.

### 4. Verifique os Arquivos Criados

Após completar o processo, você deverá ter dois arquivos:

- `server_cert.pem`: O certificado autoassinado.
- `server_key.pem`: A chave privada associada ao certificado.

Esses arquivos podem agora ser usados para configurar um servidor com SSL/TLS.

### 5. Como Usar o Certificado Autoassinado

Para usar esse certificado autoassinado em um servidor, como o servidor WebSocket do exemplo anterior, você só precisa apontar o caminho para esses arquivos ao configurar o SSL/TLS.

Por exemplo:

```python
python
Copiar código
ssl_context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
```

### Observação para Navegadores

Em ambientes de desenvolvimento, ao acessar o servidor via HTTPS em um navegador, você provavelmente verá um aviso de "conexão não segura" porque o certificado não é de uma CA confiável. No entanto, você pode ignorar esse aviso para testes locais, e alguns navegadores oferecem a opção de "Avançar para o site" após clicar em "Avançado".

### Resumo dos Comandos

```bash
# Gerar o certificado e chave privados
openssl req -x509 -newkey rsa:4096 -keyout server_key.pem -out server_cert.pem -days 365 -nodes

# Arquivos gerados:
# - server_key.pem (chave privada)
# - server_cert.pem (certificado autoassinado)
```

> ## Seção 3: Configuração do ESP8266

Para este projeto será utilizado a versão python para micro controladores popularmente conhecido como MicroPython. Em um ESP8266 você pode seguir este passo a passo:

### Requisitos

- **ESP8266 NodeMCU**
- **Cabo micro-USB** (para conectar o ESP8266 ao seu computador)
- **Software de comunicação serial** (como o [esptool.py](https://github.com/espressif/esptool) para gravar o firmware)
- **Firmware MicroPython** específico para o ESP8266 (disponível no site oficial do MicroPython)

### Passo a Passo

### 1. **Baixar o Firmware do MicroPython**

- Acesse a página de downloads de firmware para o ESP8266.
- Baixe a versão mais recente do firmware para o ESP8266 (arquivo `.bin`).

### 2. **Instalar o esptool.py**

O esptool.py é uma ferramenta Python usada para gravar firmware no ESP8266.

- Instale o esptool usando o pip (supondo que o Python já esteja instalado):

```bash
    pip install esptool
```

### 3. **Conectar o ESP8266 ao Computador**

- Conecte o ESP8266 ao seu computador usando um cabo micro-USB.
- Verifique qual porta serial o dispositivo está usando:
  - No Windows: Verifique no **Gerenciador de Dispositivos** em **Portas (COM & LPT)**.
  - No macOS e Linux: Use o comando no terminal:

    ```bash
    ls /dev/tty.*
    ```

### 4. **Apagar a Memória Flash do ESP8266**

Antes de gravar o novo firmware, apague a memória flash do ESP8266:

```bash
esptool.py --port <porta_serial> erase_flash
```

> Substitua <porta_serial> pela porta onde o ESP8266 está conectado, por exemplo, /dev/ttyUSB0 no Linux ou COM3 no Windows.
>

### 5. **Gravar o Firmware MicroPython no ESP8266**

Com o flash limpo, agora é possível gravar o firmware MicroPython:

```bash
esptool.py --port <porta_serial> --baud 115200 write_flash --flash_size=detect 0 <caminho_para_firmware.bin>

```

- `<porta_serial>`: a porta do ESP8266.
- `<caminho_para_firmware.bin>`: o caminho do arquivo de firmware baixado.

Exemplo:

```bash
esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect 0 esp8266-20220117-v1.18.bin
```

### 6. **Conectar-se ao MicroPython**

Após gravar o firmware, você pode se conectar ao console REPL do MicroPython usando uma ferramenta como o [PuTTY](https://www.putty.org/) (Windows) ou screen (macOS/Linux).

- Usando o screen no macOS/Linux:

    ```bash
    screen /dev/ttyUSB0 115200
    ```

- Usando o PuTTY no Windows:
  - Abra o PuTTY, selecione **Serial** como tipo de conexão.
  - Configure a **porta** e **velocidade** (115200) e clique em **Open**.

### 7. **Testar o MicroPython no REPL**

Após conectar, você deve ver o prompt `>>>`. Para testar, digite um comando simples, como:

```python
print("Hello, MicroPython!")
```

Se aparecer `Hello, MicroPython!`, o MicroPython foi instalado com sucesso no seu ESP8266

> ## Seção 4: Explicação dos arquivos

### 1. WebSocket_Server.py

- Arquivo que instancia o servidor websocket para receber a comunicação dos sensores, é responsavel por receber e descriptografar as mensagens e identificar os DIDs respectivos.

### 2. TST_Server.py

- Arquivo de testes para a comunicação do servidor websocket, tem a função de verificar a funcionalidade do servidor e garantir seu funcionamento de forma adequada.

### 3. ESP_Client.py

- Arquivo de configuração e comnunicação dos sensores ESP8266, devido ao uso da biblioteca micropython o programa só pode ser executado dentro dos dispositivos ESP.
