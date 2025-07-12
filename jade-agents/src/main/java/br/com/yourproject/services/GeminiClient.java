package br.com.yourproject.services;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

/**
 * Cliente responsável por se comunicar com a API do Google Gemini.
 * Esta classe encapsula a lógica de montagem da requisição HTTP,
 * envio para a API e processamento da resposta para extrair o texto gerado.
 */
public class GeminiClient {
    
    private static final String GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent";
    private final String apiKey;
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public GeminiClient(String apiKey) {
        this.apiKey = apiKey;
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(30))
                .build();
        this.objectMapper = new ObjectMapper();
    }
    
    public String gerarExplicacao(String prompt) throws IOException, InterruptedException {
        // Valida a chave da API
        if (apiKey == null || apiKey.trim().isEmpty() || apiKey.equals("SUA_CHAVE_DE_API_VAI_AQUI")) {
            throw new IllegalArgumentException("Chave da API do Gemini não configurada. Configure a variável de ambiente GEMINI_API_KEY.");
        }
        
        // Constrói o payload da requisição
        ObjectNode requestBody = objectMapper.createObjectNode();
        ArrayNode contents = objectMapper.createArrayNode();
        ObjectNode content = objectMapper.createObjectNode();
        ArrayNode parts = objectMapper.createArrayNode();
        ObjectNode part = objectMapper.createObjectNode();
        
        part.put("text", prompt);
        parts.add(part);
        content.set("parts", parts);
        contents.add(content);
        requestBody.set("contents", contents);
        
        // Configurações de geração
        ObjectNode generationConfig = objectMapper.createObjectNode();
        generationConfig.put("temperature", 0.7);
        generationConfig.put("topK", 40);
        generationConfig.put("topP", 0.95);
        generationConfig.put("maxOutputTokens", 2048);
        requestBody.set("generationConfig", generationConfig);
        
        // Configurações de segurança
        ArrayNode safetySettings = objectMapper.createArrayNode();
        String[] categories = {
            "HARM_CATEGORY_HARASSMENT",
            "HARM_CATEGORY_HATE_SPEECH", 
            "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "HARM_CATEGORY_DANGEROUS_CONTENT"
        };
        
        for (String category : categories) {
            ObjectNode safetySetting = objectMapper.createObjectNode();
            safetySetting.put("category", category);
            safetySetting.put("threshold", "BLOCK_MEDIUM_AND_ABOVE");
            safetySettings.add(safetySetting);
        }
        requestBody.set("safetySettings", safetySettings);
        
        // Converte o payload para JSON
        String jsonPayload = objectMapper.writeValueAsString(requestBody);
        
        // Cria a requisição HTTP
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(GEMINI_API_URL + "?key=" + apiKey))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                .timeout(Duration.ofSeconds(60))
                .build();
        
        // Envia a requisição
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        // Processa a resposta
        if (response.statusCode() == 200) {
            return processarResposta(response.body());
        } else {
            System.err.println("Erro na API do Gemini. Status: " + response.statusCode());
            System.err.println("Resposta: " + response.body());
            throw new IOException("Erro na API do Gemini: " + response.statusCode() + " - " + response.body());
        }
    }
    
    private String processarResposta(String jsonResponse) throws IOException {
        try {
            JsonNode responseNode = objectMapper.readTree(jsonResponse);
            
            // Navega pela estrutura da resposta do Gemini
            JsonNode candidates = responseNode.get("candidates");
            if (candidates != null && candidates.isArray() && candidates.size() > 0) {
                JsonNode firstCandidate = candidates.get(0);
                JsonNode content = firstCandidate.get("content");
                if (content != null) {
                    JsonNode parts = content.get("parts");
                    if (parts != null && parts.isArray() && parts.size() > 0) {
                        JsonNode firstPart = parts.get(0);
                        JsonNode text = firstPart.get("text");
                        if (text != null) {
                            return text.asText();
                        }
                    }
                }
            }
            
            // Se não conseguir extrair o texto, retorna uma mensagem padrão
            return "Não foi possível gerar a explicação. Resposta da API: " + jsonResponse;
            
        } catch (Exception e) {
            System.err.println("Erro ao processar resposta da API do Gemini: " + e.getMessage());
            throw new IOException("Erro ao processar resposta da API: " + e.getMessage());
        }
    }
    
    public boolean testarConexao() {
        try {
            String testPrompt = "Olá! Apenas responda 'OK' para testar a conexão.";
            String resposta = gerarExplicacao(testPrompt);
            return resposta != null && !resposta.trim().isEmpty();
        } catch (Exception e) {
            System.err.println("Erro ao testar conexão com Gemini: " + e.getMessage());
            return false;
        }
    }
    
    /**
     * Método legado para compatibilidade
     */
    public String generateContent(String prompt, String apiKey) throws IOException {
        try {
            return gerarExplicacao(prompt);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IOException("Operação interrompida", e);
        }
    }
}