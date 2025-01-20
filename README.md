# 🎮 **Twitch Chat Bot Manager - Neuralis** 🤖

O **Twitch Chat Bot Manager - Neuralis** é uma ferramenta poderosa para gerenciar múltiplas contas no chat da Twitch utilizando proxies. Com ele, você pode automatizar interações em canais e personalizar o comportamento do bot com facilidade.

## 🚀 **Instalação** 

Para instalar as dependências do projeto, basta rodar o seguinte comando:

```bash
pip install -r requirements.txt
```

## ⚙️ **Configuração**

Antes de rodar o bot, é necessário configurar alguns arquivos. Siga os passos abaixo:

1. 🔑 Adicione seus tokens de autenticação em `configs/tokens.txt`
2. 🌐 Adicione seus proxies em `configs/proxy.txt`
3. 🖥️ Configure os canais nos quais o bot irá interagir em `configs/channels.txt`
4. 💬 Adicione as mensagens personalizadas que o bot usará em `configs/messages.txt`

**Exemplo de estrutura dos arquivos:**

- `tokens.txt`: Um token por linha, cada um representando uma conta da Twitch.
- `proxy.txt`: Uma lista de proxies para esconder o IP real.
- `channels.txt`: Nome dos canais onde o bot deve atuar.
- `messages.txt`: Mensagens que o bot enviará aleatoriamente nos chats.

## 🏃 **Uso**

Para rodar o bot, execute o comando abaixo:

```bash
python main.py
```

Isso inicializará o bot com as configurações que você definiu. A interface em tempo real aparecerá, e o bot começará a interagir nos canais da Twitch conforme o configurado.

## 🎯 **Recursos**

- **Interface em tempo real** 🖥️: Acompanhe as interações e status do bot ao vivo.
- **Suporte a múltiplos tokens** 🔑: Gerencie várias contas no chat da Twitch simultaneamente.
- **Sistema de proxy** 🌍: Utilize proxies para esconder a origem das interações e evitar bloqueios.
- **Mensagens aleatórias** 🎲: Envie mensagens aleatórias definidas por você nos canais configurados.
- **Gerenciamento de delays** ⏳: Controle os tempos de espera entre as interações para simular comportamento humano e evitar detecção.

## 📄 **Licença**

Este projeto **Neuralis** está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
