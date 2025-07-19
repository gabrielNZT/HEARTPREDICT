package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import br.com.yourproject.services.GeminiClient;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;

public class AgenteExplicador extends Agent {

    private static final String GEMINI_API_KEY = System.getenv("GEMINI_API_KEY") != null ? 
        System.getenv("GEMINI_API_KEY") : "SUA_CHAVE_DE_API_VAI_AQUI";
    
    private static final String BACKEND_GATEWAY_URL = "http://localhost:8000";

    private GeminiClient geminiClient;
    private ObjectMapper objectMapper;
    private HttpClient httpClient;

    @Override
    protected void setup() {
        System.out.println("Olá! Eu sou o " + getLocalName() + ", pronto para gerar explicações.");
        this.geminiClient = new GeminiClient(GEMINI_API_KEY);
        this.objectMapper = new ObjectMapper();
        this.httpClient = HttpClient.newHttpClient();

        // Adiciona um comportamento para ouvir continuamente por pedidos de explicação
        addBehaviour(new CyclicBehaviour() {
            @Override
            public void action() {
                // 1. Tenta receber uma mensagem do tipo REQUEST
                MessageTemplate template = MessageTemplate.MatchPerformative(ACLMessage.REQUEST);
                ACLMessage msg = myAgent.receive(template);
                
                if (msg != null) {
                    System.out.println("\n[EXPLICADOR] Pedido de explicação recebido de: " + msg.getSender().getLocalName());
                    
                    try {
                        // 2. Processa o pedido de explicação
                        String explicacao = gerarExplicacao(msg.getContent());
                        
                        // 3. Extrair user_id dos dados
                        JsonNode dadosPaciente = objectMapper.readTree(msg.getContent());
                        String userId = dadosPaciente.get("user_id").asText();
                        
                        // 4. Envia explicação para o backend-gateway
                        enviarExplicacaoParaBackend(userId, explicacao);
                        
                        // 5. Envia a explicação de volta para o agente solicitante
                        ACLMessage reply = msg.createReply();
                        reply.setPerformative(ACLMessage.INFORM);
                        reply.setContent(explicacao);
                        send(reply);
                        
                        System.out.println("[EXPLICADOR] Explicação enviada com sucesso!");
                        
                    } catch (Exception e) {
                        System.err.println("[EXPLICADOR] Erro ao gerar explicação: " + e.getMessage());
                        e.printStackTrace();
                        
                        // Envia mensagem de erro
                        ACLMessage errorReply = msg.createReply();
                        errorReply.setPerformative(ACLMessage.FAILURE);
                        errorReply.setContent("Erro ao gerar explicação: " + e.getMessage());
                        send(errorReply);
                    }
                } else {
                    block();
                }
            }
        });
    }
    
    private String gerarExplicacao(String dadosJson) throws Exception {
        try {
            // Parse dos dados do paciente com novo formato
            JsonNode dadosPaciente = objectMapper.readTree(dadosJson);
            
            // Extrai informações do novo formato JSON
            String userId = dadosPaciente.get("user_id").asText();
            double chronicRiskScore = dadosPaciente.get("chronic_risk_score").asDouble();
            String riskLevel = dadosPaciente.get("risk_level").asText();
            int riskPrediction = dadosPaciente.get("risk_prediction").asInt();
            
            // Informações do modelo
            JsonNode modelInfo = dadosPaciente.get("model_info");
            String modelName = modelInfo.get("model_name").asText();
            double rocAuc = modelInfo.get("roc_auc").asDouble();
            
            // Features clínicas
            JsonNode clinicalFeatures = dadosPaciente.get("clinical_features");
            double bmi = clinicalFeatures.get("bmi").asDouble();
            String bmiCategory = clinicalFeatures.get("bmi_category").asText();
            String bloodPressureCategory = clinicalFeatures.get("blood_pressure_category").asText();
            String ageCategory = clinicalFeatures.get("age_category").asText();
            int lifestyleScore = clinicalFeatures.get("lifestyle_score").asInt();
            int pressurePulse = clinicalFeatures.get("pressure_pulse").asInt();
            
            // Interpretações automáticas do modelo
            JsonNode interpretation = dadosPaciente.get("interpretation");
            String bmiInterpretation = interpretation.get("bmi").asText();
            String bloodPressureInterpretation = interpretation.get("blood_pressure").asText();
            String lifestyleInterpretation = interpretation.get("lifestyle").asText();
            String overallInterpretation = interpretation.get("overall").asText();
            
            // Cria o prompt otimizado para o Gemini
            String prompt = construirPromptOtimizado(userId, chronicRiskScore, riskLevel, 
                                                   riskPrediction, modelName, rocAuc,
                                                   bmi, bmiCategory, bloodPressureCategory, 
                                                   ageCategory, lifestyleScore, pressurePulse,
                                                   bmiInterpretation, bloodPressureInterpretation,
                                                   lifestyleInterpretation, overallInterpretation);
            
            // Chama a API do Gemini
            String explicacao = geminiClient.gerarExplicacao(prompt);
            
            System.out.println("[EXPLICADOR] Explicação gerada para paciente: " + userId + " (Risco: " + riskLevel + ")");
            
            return explicacao;
            
        } catch (Exception e) {
            System.err.println("[EXPLICADOR] Erro ao processar dados do paciente: " + e.getMessage());
            throw e;
        }
    }
    
    private String construirPromptOtimizado(String userId, double chronicRiskScore, String riskLevel,
                                          int riskPrediction, String modelName, double rocAuc,
                                          double bmi, String bmiCategory, String bloodPressureCategory,
                                          String ageCategory, int lifestyleScore, int pressurePulse,
                                          String bmiInterpretation, String bloodPressureInterpretation,
                                          String lifestyleInterpretation, String overallInterpretation) {
        
        StringBuilder prompt = new StringBuilder();
        prompt.append("Você é um cardiologista experiente. Forneça uma explicação CONCISA e CLARA sobre o risco cardiovascular do paciente.\n\n");
        
        prompt.append("**DADOS ANALISADOS:**\n");
        prompt.append("• Paciente: ").append(userId).append("\n");
        prompt.append("• Score de Risco: ").append(String.format("%.2f", chronicRiskScore)).append(" (").append(riskLevel).append(")\n");
        prompt.append("• Predição: ").append(riskPrediction == 1 ? "POSITIVO para doença cardiovascular" : "NEGATIVO para doença cardiovascular").append("\n");
        prompt.append("• Modelo: ").append(modelName).append(" (Precisão: ").append(String.format("%.1f%%", rocAuc * 100)).append(")\n\n");
        
        prompt.append("**ACHADOS CLÍNICOS:**\n");
        prompt.append("• IMC: ").append(bmi).append(" (").append(bmiCategory).append(")\n");
        prompt.append("• Pressão Arterial: ").append(bloodPressureCategory.replace("_", " ")).append("\n");
        prompt.append("• Categoria Etária: ").append(ageCategory.replace("_", " ")).append("\n");
        prompt.append("• Score de Estilo de Vida: ").append(lifestyleScore).append("\n");
        prompt.append("• Pressão de Pulso: ").append(pressurePulse).append(" mmHg\n\n");
        
        prompt.append("**INTERPRETAÇÕES AUTOMÁTICAS:**\n");
        prompt.append("• IMC: ").append(bmiInterpretation).append("\n");
        prompt.append("• Pressão Arterial: ").append(bloodPressureInterpretation).append("\n");
        prompt.append("• Estilo de Vida: ").append(lifestyleInterpretation).append("\n");
        prompt.append("• Avaliação Geral: ").append(overallInterpretation).append("\n\n");
        
        prompt.append("**TAREFA:**\n");
        prompt.append("Baseado nos dados acima, forneça uma explicação em linguagem simples que inclua:\n");
        prompt.append("1. **O que significa o score ").append(String.format("%.2f", chronicRiskScore)).append("?**\n");
        prompt.append("2. **Principais fatores contribuindo para o risco**\n");
        prompt.append("3. **2-3 recomendações práticas específicas**\n");
        prompt.append("4. **Urgência do acompanhamento médico**\n\n");
        
        prompt.append("**DIRETRIZES:**\n");
        prompt.append("• Seja direto e objetivo (máximo 400 palavras)\n");
        prompt.append("• Use linguagem acessível\n");
        prompt.append("• Foque no que é mais importante\n");
        prompt.append("• Seja empático mas realista\n");
        
        return prompt.toString();
    }
    
    private void enviarExplicacaoParaBackend(String userId, String explicacao) {
        try {
            // Prepara os dados para envio
            Map<String, String> data = new HashMap<>();
            data.put("explanation", explicacao);
            
            String jsonData = objectMapper.writeValueAsString(data);
            
            System.out.println("[EXPLICADOR] Enviando dados para backend: " + jsonData);
            
            // Cria a requisição HTTP com HTTP/1.1 explícito
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(BACKEND_GATEWAY_URL + "/explanation/" + userId))
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .version(HttpClient.Version.HTTP_1_1)  // Força HTTP/1.1
                    .POST(HttpRequest.BodyPublishers.ofString(jsonData))
                    .build();
            
            // Envia a requisição
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            
            System.out.println("[EXPLICADOR] Response status: " + response.statusCode());
            System.out.println("[EXPLICADOR] Response body: " + response.body());
            
            if (response.statusCode() == 200) {
                System.out.println("[EXPLICADOR] Explicação enviada com sucesso para backend-gateway (userId: " + userId + ")");
            } else {
                System.err.println("[EXPLICADOR] Erro ao enviar explicação para backend: " + response.statusCode());
                System.err.println("[EXPLICADOR] Response: " + response.body());
            }
            
        } catch (Exception e) {
            System.err.println("[EXPLICADOR] Erro ao enviar explicação para backend: " + e.getMessage());
            e.printStackTrace();
        }
    }
}