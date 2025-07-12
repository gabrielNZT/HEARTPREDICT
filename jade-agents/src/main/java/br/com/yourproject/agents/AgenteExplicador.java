package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import br.com.yourproject.services.GeminiClient;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

public class AgenteExplicador extends Agent {

    private static final String GEMINI_API_KEY = System.getenv("GEMINI_API_KEY") != null ? 
        System.getenv("GEMINI_API_KEY") : "SUA_CHAVE_DE_API_VAI_AQUI";

    private GeminiClient geminiClient;
    private ObjectMapper objectMapper;

    @Override
    protected void setup() {
        System.out.println("Olá! Eu sou o " + getLocalName() + ", pronto para gerar explicações.");
        this.geminiClient = new GeminiClient(GEMINI_API_KEY);
        this.objectMapper = new ObjectMapper();

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
                        
                        // 3. Envia a explicação de volta
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
            // Parse dos dados do paciente
            JsonNode dadosPaciente = objectMapper.readTree(dadosJson);
            
            // Extrai informações relevantes
            String userId = dadosPaciente.get("user_id").asText();
            double chronicRiskScore = dadosPaciente.get("chronic_risk_score").asDouble();
            
            JsonNode features = dadosPaciente.get("features_used");
            int age = features.get("age").asInt();
            String gender = features.get("gender").asText();
            double bmi = features.get("bmi").asDouble();
            String bloodPressure = features.get("blood_pressure").asText();
            int cholesterolLevel = features.get("cholesterol_level").asInt();
            int glucoseLevel = features.get("glucose_level").asInt();
            
            JsonNode lifestyle = features.get("lifestyle_factors");
            boolean smoking = lifestyle.get("smoking").asBoolean();
            boolean alcohol = lifestyle.get("alcohol").asBoolean();
            boolean physicalActivity = lifestyle.get("physical_activity").asBoolean();
            
            // Cria o prompt detalhado para o Gemini
            String prompt = construirPrompt(userId, chronicRiskScore, age, gender, bmi, 
                                          bloodPressure, cholesterolLevel, glucoseLevel, 
                                          smoking, alcohol, physicalActivity);
            
            // Chama a API do Gemini
            String explicacao = geminiClient.gerarExplicacao(prompt);
            
            System.out.println("[EXPLICADOR] Explicação gerada para paciente: " + userId);
            
            return explicacao;
            
        } catch (Exception e) {
            System.err.println("[EXPLICADOR] Erro ao processar dados do paciente: " + e.getMessage());
            throw e;
        }
    }
    
    private String construirPrompt(String userId, double chronicRiskScore, int age, String gender, 
                                 double bmi, String bloodPressure, int cholesterolLevel, 
                                 int glucoseLevel, boolean smoking, boolean alcohol, 
                                 boolean physicalActivity) {
        
        // Determina o nível de risco
        String nivelRisco;
        if (chronicRiskScore >= 0.8) {
            nivelRisco = "CRÍTICO";
        } else if (chronicRiskScore >= 0.6) {
            nivelRisco = "ALTO";
        } else if (chronicRiskScore >= 0.4) {
            nivelRisco = "MÉDIO";
        } else if (chronicRiskScore >= 0.2) {
            nivelRisco = "BAIXO";
        } else {
            nivelRisco = "MÍNIMO";
        }
        
        // Interpreta os valores categóricos
        String cholesterolDesc = interpretarColesterol(cholesterolLevel);
        String glucoseDesc = interpretarGlicose(glucoseLevel);
        String bmiDesc = interpretarIMC(bmi);
        
        StringBuilder prompt = new StringBuilder();
        prompt.append("Você é um especialista em cardiologia. Analise os dados do paciente e forneça uma explicação detalhada, educativa e empática sobre o risco cardiovascular.\n\n");
        
        prompt.append("**DADOS DO PACIENTE:**\n");
        prompt.append("- ID: ").append(userId).append("\n");
        prompt.append("- Idade: ").append(age).append(" anos\n");
        prompt.append("- Gênero: ").append(gender).append("\n");
        prompt.append("- IMC: ").append(bmi).append(" (").append(bmiDesc).append(")\n");
        prompt.append("- Pressão Arterial: ").append(bloodPressure).append(" mmHg\n");
        prompt.append("- Nível de Colesterol: ").append(cholesterolDesc).append("\n");
        prompt.append("- Nível de Glicose: ").append(glucoseDesc).append("\n");
        prompt.append("- Fumante: ").append(smoking ? "Sim" : "Não").append("\n");
        prompt.append("- Consumo de Álcool: ").append(alcohol ? "Sim" : "Não").append("\n");
        prompt.append("- Atividade Física: ").append(physicalActivity ? "Sim" : "Não").append("\n");
        prompt.append("- **Score de Risco Crônico: ").append(String.format("%.2f", chronicRiskScore)).append(" (").append(nivelRisco).append(")**\n\n");
        
        prompt.append("**SOLICITAÇÃO:**\n");
        prompt.append("Forneça uma explicação abrangente que inclua:\n");
        prompt.append("1. **Interpretação do Score de Risco**: Explique o que significa o score de ").append(String.format("%.2f", chronicRiskScore)).append(" em termos simples\n");
        prompt.append("2. **Principais Fatores de Risco**: Identifique quais fatores mais contribuem para o risco\n");
        prompt.append("3. **Recomendações Personalizadas**: Sugira mudanças específicas no estilo de vida\n");
        prompt.append("4. **Próximos Passos**: Orientações sobre acompanhamento médico\n");
        prompt.append("5. **Prognóstico**: Explique as perspectivas se as recomendações forem seguidas\n\n");
        
        prompt.append("**DIRETRIZES:**\n");
        prompt.append("- Use linguagem clara e acessível\n");
        prompt.append("- Seja empático e encorajador\n");
        prompt.append("- Forneça informações baseadas em evidências\n");
        prompt.append("- Estruture a resposta de forma organizada\n");
        prompt.append("- Limite a resposta a aproximadamente 500 palavras\n");
        
        return prompt.toString();
    }
    
    private String interpretarColesterol(int level) {
        switch (level) {
            case 0: return "Normal";
            case 1: return "Acima do Normal";
            case 2: return "Muito Alto";
            default: return "Não especificado";
        }
    }
    
    private String interpretarGlicose(int level) {
        switch (level) {
            case 0: return "Normal";
            case 1: return "Acima do Normal";
            case 2: return "Muito Alto";
            default: return "Não especificado";
        }
    }
    
    private String interpretarIMC(double bmi) {
        if (bmi < 18.5) {
            return "Abaixo do peso";
        } else if (bmi < 25) {
            return "Peso normal";
        } else if (bmi < 30) {
            return "Sobrepeso";
        } else {
            return "Obesidade";
        }
    }
}