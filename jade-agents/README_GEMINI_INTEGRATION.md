# Integração com AgenteExplicador e API do Gemini

## Visão Geral

O AgenteExplicador foi implementado para fornecer explicações detalhadas sobre o risco cardiovascular dos pacientes, utilizando a API do Google Gemini para gerar análises personalizadas e educativas.

## Configuração

### 1. Obter Chave da API do Gemini

1. Acesse o [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

### 2. Configurar Variável de Ambiente

```bash
# No Linux/Mac
export GEMINI_API_KEY='sua_chave_da_api_aqui'

# No Windows
set GEMINI_API_KEY=sua_chave_da_api_aqui
```

### 3. Compilar o Projeto

```bash
mvn clean package
```

## Executando os Agentes

### Opção 1: Todos os Agentes (Recomendado)

```bash
./run-agents-with-explicador.sh
```

Este script inicia:
- **AgenteGerenciadorPacientes** (servidor HTTP na porta 8888)
- **AgenteJulgador** (classifica risco e executa ações)
- **AgenteExplicador** (gera explicações com Gemini)

### Opção 2: Apenas Gerenciador e Julgador

```bash
./run-agents.sh
```

## Fluxo de Funcionamento

1. **Recepção de Dados**: O AgenteGerenciadorPacientes recebe dados via HTTP POST
2. **Classificação**: O AgenteJulgador classifica o nível de risco
3. **Explicação**: Para casos críticos, o AgenteJulgador solicita explicação ao AgenteExplicador
4. **Geração**: O AgenteExplicador usa a API do Gemini para gerar explicação detalhada

## Exemplo de Uso

### 1. Preparar Dados de Teste

```bash
./test-integration.sh
```

Este script cria um arquivo `test_patient_data.json` com dados de exemplo.

### 2. Enviar Requisição

```bash
curl -X POST http://localhost:8888/registrar \
  -H 'Content-Type: application/json' \
  -d @test_patient_data.json
```

### 3. Observar Logs

No console onde os agentes estão executando, você verá:
- Recepção dos dados pelo AgenteGerenciadorPacientes
- Classificação do risco pelo AgenteJulgador
- Solicitação de explicação ao AgenteExplicador
- Geração da explicação via API do Gemini

## Exemplo de Explicação Gerada

```
[JULGADOR] Explicação recebida do AgenteExplicador:
----------------------------------------
**ANÁLISE DO RISCO CARDIOVASCULAR**

**Interpretação do Score de Risco:**
Seu score de risco crônico de 0.86 indica um risco CRÍTICO para doenças cardiovasculares. 
Este é um nível que requer atenção médica imediata...

**Principais Fatores de Risco:**
- Pressão arterial elevada (140/90 mmHg)
- Colesterol muito alto
- Falta de atividade física regular
- Idade (55 anos) e gênero masculino

**Recomendações Personalizadas:**
1. Procure um cardiologista imediatamente
2. Inicie atividade física leve sob supervisão médica
3. Adote uma dieta rica em vegetais e pobre em sódio
...
----------------------------------------
```

## Configuração Avançada

### Personalizar Prompts

Para modificar o estilo das explicações, edite o método `construirPrompt()` no arquivo:
`src/main/java/br/com/yourproject/agents/AgenteExplicador.java`

### Ajustar Parâmetros do Gemini

No arquivo `GeminiClient.java`, você pode ajustar:
- `temperature`: Criatividade da resposta (0.0-1.0)
- `maxOutputTokens`: Tamanho máximo da resposta
- `topK` e `topP`: Controle de diversidade

### Tratamento de Erros

O sistema inclui tratamento robusto de erros:
- Validação da chave da API
- Timeouts para requisições HTTP
- Fallbacks para casos de falha na API

## Monitoramento

### Logs Importantes

- `[EXPLICADOR] Pedido de explicação recebido`: Indica que o agente recebeu uma solicitação
- `[EXPLICADOR] Explicação gerada`: Confirma que a explicação foi criada com sucesso
- `[EXPLICADOR] Erro ao gerar explicação`: Indica problemas na integração

### Testando a Conexão

```java
GeminiClient client = new GeminiClient("sua_chave");
boolean conectado = client.testarConexao();
```

## Limitações e Considerações

- **Quota da API**: O Gemini tem limites de requisições por minuto
- **Latência**: As explicações podem demorar 2-10 segundos para serem geradas
- **Custo**: Verificar os preços da API do Gemini no Google Cloud
- **Privacidade**: Os dados dos pacientes são enviados para a API do Google

## Troubleshooting

### Erro: "Chave da API não configurada"
- Verifique se a variável `GEMINI_API_KEY` está configurada
- Certifique-se que a chave não contém espaços extras

### Erro: "Timeout na requisição"
- Verifique sua conexão com a internet
- A API do Gemini pode estar temporariamente indisponível

### Agente não inicia
- Compile o projeto: `mvn clean package`
- Verifique se todas as dependências estão instaladas

## Próximos Passos

1. **Persistência**: Salvar explicações em banco de dados
2. **Cache**: Implementar cache para explicações similares
3. **Múltiplos Modelos**: Suporte a outros LLMs além do Gemini
4. **Interface Web**: Criar interface para visualizar explicações
5. **Notificações**: Enviar explicações por email ou SMS
