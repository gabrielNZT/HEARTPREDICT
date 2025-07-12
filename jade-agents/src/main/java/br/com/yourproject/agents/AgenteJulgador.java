package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.core.AID;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

public class AgenteJulgador extends Agent {
    
    private ObjectMapper objectMapper;
    
    @Override
    protected void setup() {
        System.out.println("Olá! Eu sou o " + getLocalName() + ", pronto para julgar a seriedade dos pacientes.");
        
        objectMapper = new ObjectMapper();
        
        // Comportamento para receber mensagens de dados de pacientes
        addBehaviour(new ReceberDadosPacienteBehaviour());
    }
    
    private class ReceberDadosPacienteBehaviour extends CyclicBehaviour {
        
        @Override
        public void action() {
            // Recebe mensagens com dados de pacientes (apenas do gerenciador)
            MessageTemplate template = MessageTemplate.and(
                MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                MessageTemplate.MatchSender(new AID("gerenciador", AID.ISLOCALNAME))
            );
            ACLMessage msg = myAgent.receive(template);
            
            if (msg != null) {
                System.out.println("\n[JULGADOR] Dados do paciente recebidos de: " + msg.getSender().getLocalName());
                
                try {
                    // Valida se o conteúdo é JSON válido
                    String content = msg.getContent();
                    if (content == null || content.trim().isEmpty()) {
                        System.err.println("[JULGADOR] Mensagem vazia recebida, ignorando...");
                        return;
                    }
                    
                    System.out.println("[JULGADOR] Conteúdo recebido: " + content);
                    
                    // Parse dos dados JSON
                    JsonNode dadosPaciente = objectMapper.readTree(content);
                    
                    // Classifica o nível de seriedade
                    String nivelSeriedade = classificarSeriedade(dadosPaciente);
                    
                    // Realiza ação baseada no nível de seriedade
                    realizarAcao(nivelSeriedade, dadosPaciente);
                    
                } catch (Exception e) {
                    System.err.println("[JULGADOR] Erro ao processar dados do paciente: " + e.getMessage());
                    System.err.println("[JULGADOR] Conteúdo da mensagem: " + msg.getContent());
                    e.printStackTrace();
                }
            } else {
                block();
            }
        }
    }
    
    private String classificarSeriedade(JsonNode dadosPaciente) {
        double chronicRiskScore = dadosPaciente.get("chronic_risk_score").asDouble();
        String userId = dadosPaciente.get("user_id").asText();
        
        String nivelSeriedade;
        
        if (chronicRiskScore >= 0.8) {
            nivelSeriedade = "CRÍTICO";
        } else if (chronicRiskScore >= 0.6) {
            nivelSeriedade = "ALTO";
        } else if (chronicRiskScore >= 0.4) {
            nivelSeriedade = "MÉDIO";
        } else if (chronicRiskScore >= 0.2) {
            nivelSeriedade = "BAIXO";
        } else {
            nivelSeriedade = "MÍNIMO";
        }
        
        System.out.println("\n[JULGADOR] Classificação do paciente " + userId + ":");
        System.out.println("[JULGADOR] Chronic Risk Score: " + chronicRiskScore);
        System.out.println("[JULGADOR] Nível de Seriedade: " + nivelSeriedade);
        
        return nivelSeriedade;
    }
    
    private void realizarAcao(String nivelSeriedade, JsonNode dadosPaciente) {
        String userId = dadosPaciente.get("user_id").asText();
        
        System.out.println("\n[JULGADOR] Realizando ação para nível " + nivelSeriedade + " - Paciente: " + userId);
        
        switch (nivelSeriedade) {
            case "CRÍTICO":
                realizarAcaoCritica(dadosPaciente);
                break;
            case "ALTO":
                realizarAcaoAlta(dadosPaciente);
                break;
            case "MÉDIO":
                realizarAcaoMedia(dadosPaciente);
                break;
            case "BAIXO":
                realizarAcaoBaixa(dadosPaciente);
                break;
            case "MÍNIMO":
                realizarAcaoMinima(dadosPaciente);
                break;
            default:
                System.out.println("[JULGADOR] Nível de seriedade não reconhecido: " + nivelSeriedade);
        }
    }
    
    private void realizarAcaoCritica(JsonNode dadosPaciente) {
        System.out.println("[JULGADOR] AÇÃO CRÍTICA - Paciente necessita atendimento IMEDIATO!");
        System.out.println("[JULGADOR] - Alertar equipe médica de emergência");
        System.out.println("[JULGADOR] - Agendar consulta urgente");
        System.out.println("[JULGADOR] - Enviar notificação para familiares");
        System.out.println("[JULGADOR] - Iniciar monitoramento contínuo");
        
        // Solicita explicação detalhada do AgenteExplicador
        solicitarExplicacao(dadosPaciente);
    }
    
    private void realizarAcaoAlta(JsonNode dadosPaciente) {
        System.out.println("[JULGADOR] AÇÃO ALTA - Paciente necessita atenção médica prioritária!");
        System.out.println("[JULGADOR] - Agendar consulta com cardiologista");
        System.out.println("[JULGADOR] - Solicitar exames complementares");
        System.out.println("[JULGADOR] - Ajustar medicação se necessário");
        System.out.println("[JULGADOR] - Aumentar frequência de monitoramento");
        // TODO: Implementar ações específicas
    }
    
    private void realizarAcaoMedia(JsonNode dadosPaciente) {
        System.out.println("[JULGADOR] AÇÃO MÉDIA - Paciente necessita acompanhamento médico regular!");
        System.out.println("[JULGADOR] - Agendar consulta de rotina");
        System.out.println("[JULGADOR] - Revisar plano de tratamento");
        System.out.println("[JULGADOR] - Orientar sobre mudanças no estilo de vida");
        System.out.println("[JULGADOR] - Monitoramento semanal");
        // TODO: Implementar ações específicas
    }
    
    private void realizarAcaoBaixa(JsonNode dadosPaciente) {
        System.out.println("[JULGADOR] AÇÃO BAIXA - Paciente em situação controlada!");
        System.out.println("[JULGADOR] - Manter rotina de check-ups");
        System.out.println("[JULGADOR] - Continuar medicação atual");
        System.out.println("[JULGADOR] - Incentivar hábitos saudáveis");
        System.out.println("[JULGADOR] - Monitoramento mensal");
        // TODO: Implementar ações específicas
    }
    
    private void realizarAcaoMinima(JsonNode dadosPaciente) {
        System.out.println("[JULGADOR] AÇÃO MÍNIMA - Paciente em baixo risco!");
        System.out.println("[JULGADOR] - Consultas de prevenção");
        System.out.println("[JULGADOR] - Educação sobre prevenção");
        System.out.println("[JULGADOR] - Manter estilo de vida saudável");
        System.out.println("[JULGADOR] - Monitoramento trimestral");
        // TODO: Implementar ações específicas
    }
    
    private void solicitarExplicacao(JsonNode dadosPaciente) {
        try {
            // Cria mensagem para o AgenteExplicador
            ACLMessage msg = new ACLMessage(ACLMessage.REQUEST);
            msg.setContent(dadosPaciente.toString());
            msg.addReceiver(new AID("explicador", AID.ISLOCALNAME));
            
            // Define um timeout para a resposta
            String replyId = "explicacao-" + System.currentTimeMillis();
            msg.setReplyWith(replyId);
            
            // Envia a mensagem
            send(msg);
            
            System.out.println("[JULGADOR] Solicitação de explicação enviada para o AgenteExplicador");
            
            // Adiciona um comportamento específico para aguardar APENAS a resposta da explicação
            addBehaviour(new CyclicBehaviour() {
                @Override
                public void action() {
                    // Filtra apenas respostas do explicador com o ID específico
                    MessageTemplate template = MessageTemplate.and(
                        MessageTemplate.MatchInReplyTo(replyId),
                        MessageTemplate.MatchSender(new AID("explicador", AID.ISLOCALNAME))
                    );
                    ACLMessage reply = receive(template);
                    
                    if (reply != null) {
                        if (reply.getPerformative() == ACLMessage.INFORM) {
                            System.out.println("\n[JULGADOR] Explicação recebida do AgenteExplicador:");
                            System.out.println("========================================");
                            System.out.println(reply.getContent());
                            System.out.println("========================================");
                        } else if (reply.getPerformative() == ACLMessage.FAILURE) {
                            System.err.println("[JULGADOR] Erro ao obter explicação: " + reply.getContent());
                        }
                        
                        // Remove este comportamento após processar a resposta
                        removeBehaviour(this);
                    } else {
                        block();
                    }
                }
            });
            
        } catch (Exception e) {
            System.err.println("[JULGADOR] Erro ao solicitar explicação: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
