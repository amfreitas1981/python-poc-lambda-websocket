# python-poc-lambda-websocket
Criação de um serviço lambda websocket (POC) em Python, para entender o funcionamento de um AWS Lambda Websocket.

Este projeto implementa uma arquitetura de comunicação em tempo real utilizando WebSocket via API Gateway, AWS Lambda e DynamoDB. Ele permite que sessões conectadas via navegador troquem mensagens em tempo real por meio de um canal centralizado (HUB).

## 🛠️ Tecnologias Utilizadas

- **AWS Lambda (Python 3.10)**
- **Amazon API Gateway (WebSocket)**
- **Amazon DynamoDB**
- **AWS SAM (Serverless Application Model)**

## 📁 Estrutura do Projeto

    python-poc-lambda-websocket/
    │
    ├── connect/ # Lambda: onConnect
    │ └── on_connect_lambda.py
    │
    ├── disconnect/ # Lambda: onDisconnect
    │ └── on_disconnect_lambda.py
    │
    ├── send-message/ # Lambda: messageSender
    │ └── on_send_message_lambda.py
    │
    ├── template.yaml # Definição AWS SAM (CloudFormation)
    └── events/ # Eventos de teste para invocação local

## 🚀 Como fazer o Deploy

1. Instalar o [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

2. Configurar suas credenciais AWS:
```bash
aws configure
```

3. Build e deploy com SAM:
```bash
sam build
sam deploy --guided
```
Durante o deploy, você informará:

- Nome da stack
- Região
- Nome da tabela DynamoDB (TABLE_NAME)
- Endpoint do WebSocket (opcional)

| Rota WebSocket | Função Lambda      | Ação                             |
| -------------- | ------------------ | -------------------------------- |
| `$connect`     | ConnectFunction    | Salva conexão na tabela DynamoDB |
| `$disconnect`  | DisconnectFunction | Remove conexão da tabela         |
| `sendMessage`  | MessageFunction    | Envia mensagens para as conexões |


## 📦 Testes Locais
Utilizar os eventos de teste disponíveis em events/ com o comando:
```bash
sam local invoke ConnectFunction --event events/connect.json
```

## # Especificação Funcional - Serviço python-poc-lambda-websocket

## Visão Geral

O serviço permite a troca de mensagens em tempo real entre usuários conectados a um HUB WebSocket, utilizando AWS Lambda e DynamoDB para persistência e comunicação via API Gateway.

## Funcionalidades

### 1. Conexão WebSocket (`$connect`)

- **Trigger**: Evento de conexão WebSocket.
- **Ação**: A Lambda `ConnectFunction` armazena `connection_id` e `session_id` no DynamoDB.
- **Objetivo**: Registrar usuários para comunicação futura.

### 2. Desconexão WebSocket (`$disconnect`)

- **Trigger**: Encerramento de conexão.
- **Ação**: `DisconnectFunction` remove o `connection_id` da tabela DynamoDB.
- **Objetivo**: Limpar conexões inativas.

### 3. Envio de Mensagem (`sendMessage`)

- **Trigger**: Mensagem do cliente contendo lista de sessões.
- **Ação**:
  - `MessageFunction` busca todos os `connection_id` relacionados aos `session_id` fornecidos.
  - Usa o `apigatewaymanagementapi` para enviar mensagens em tempo real.
- **Objetivo**: Disseminar atualizações entre clientes conectados.

## Estrutura da Tabela DynamoDB

| Atributo      | Tipo |
|---------------|------|
| session_id    | S    |
| connection_id | S    |

## Exceções e Logs

- Todos os handlers capturam erros com `try/except`.
- Logs de eventos e falhas são enviados para o CloudWatch com nível `INFO` e `ERROR`.

## Fluxo Arquitetural

1. Usuário abre navegador com WebSocket.
2. Ao conectar, a `ConnectFunction` registra a sessão.
3. Ao enviar dados para uma sessão, `MessageFunction` envia para todos os `connection_id` daquela `session_id`.
4. Ao desconectar, `DisconnectFunction` remove a conexão.

## Segurança

- A autenticação não está ativada no WebSocket (por padrão).
- Pode-se adicionar autenticação via JWT no futuro.

## Monitoramento

- CloudWatch Logs para cada função.
- Métricas de conexão e envio disponíveis via API Gateway e Lambda Metrics.

---
