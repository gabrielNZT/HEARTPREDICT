package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.core.AID;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

/**
 * Agente responsável por comunicar-se com o serviço de classificação de risco cardíaco aprimorado (main_enhanced.py).
 * Este agente recebe dados de pacientes do AgenteGerenciadorPacientes,
 * faz a requisição para o serviço de IA e envia o resultado para o AgenteJulgador.
 */
public class AgenteClassificador extends Agent {
    
    private static final String AI_SERVICE_URL = "http://127.0.0.1:8002/predict_risk";
    private HttpClient httpClient;
    
    @Override
    protected void setup() {
        System.out.println("Olá! Eu sou o " + getLocalName() + ", responsável por comunicação com o serviço de IA aprimorado.");
        
        httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(30))
                .build();
        
        // Comportamento para receber solicitações de classificação
        addBehaviour(new ProcessarSolicitacaoClassificacao());
    }
    
    private class ProcessarSolicitacaoClassificacao extends CyclicBehaviour {
        @Override
        public void action() {
            // Recebe mensagens de solicitação de classificação do AgenteGerenciadorPacientes
            MessageTemplate template = MessageTemplate.and(
                MessageTemplate.MatchPerformative(ACLMessage.REQUEST),
                MessageTemplate.MatchSender(new AID("gerenciador", AID.ISLOCALNAME))
            );
            
            ACLMessage msg = myAgent.receive(template);
            
            if (msg != null) {
                System.out.println("\n[CLASSIFICADOR] Solicitação de classificação recebida de: " + msg.getSender().getLocalName());
                
                try {
                    String content = msg.getContent();
                    if (content == null || content.trim().isEmpty()) {
                        System.err.println("[CLASSIFICADOR] Dados vazios recebidos, ignorando...");
                        return;
                    }
                    
                    System.out.println("[CLASSIFICADOR] Dados do paciente recebidos: " + content);
                    
                    // Faz a chamada para o serviço de IA aprimorado
                    String resultadoIA = chamarServicoIA(content);
                    
                    if (resultadoIA != null) {
                        // Envia resultado para o AgenteJulgador
                        enviarResultadoParaJulgador(resultadoIA);
                    } else {
                        System.err.println("[CLASSIFICADOR] Falha na comunicação com o serviço de IA");
                    }
                    
                } catch (Exception e) {
                    System.err.println("[CLASSIFICADOR] Erro ao processar solicitação: " + e.getMessage());
                    e.printStackTrace();
                }
            } else {
                block();
            }
        }
    }
    
    /**
     * Faz a chamada HTTP para o serviço de IA aprimorado (main_enhanced.py)
     */
    private String chamarServicoIA(String dadosPaciente) {
        try {
            System.out.println("[CLASSIFICADOR] Chamando serviço de IA aprimorado...");
            System.out.println("[CLASSIFICADOR] Dados sendo enviados: " + dadosPaciente);
            
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(AI_SERVICE_URL))
                    .version(HttpClient.Version.HTTP_1_1)
                    .header("Content-Type", "application/json")
                    .timeout(Duration.ofSeconds(30))
                    .POST(HttpRequest.BodyPublishers.ofString(dadosPaciente))
                    .build();
            
            // Enviar requisição
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            
            if (response.statusCode() == 200) {
                String responseBody = response.body();
                System.out.println("[CLASSIFICADOR] Resposta da IA recebida com sucesso");
                System.out.println("[CLASSIFICADOR] Dados retornados: " + responseBody);
                return responseBody;
            } else {
                System.err.println("[CLASSIFICADOR] Erro na chamada da IA. Status: " + response.statusCode());
                System.err.println("[CLASSIFICADOR] Resposta: " + response.body());
                return null;
            }
            
        } catch (IOException | InterruptedException e) {
            System.err.println("[CLASSIFICADOR] Erro ao chamar serviço de IA: " + e.getMessage());
            e.printStackTrace();
            return null;
        }
    }
    
    /**
     * Envia o resultado da classificação para o AgenteJulgador
     */
    private void enviarResultadoParaJulgador(String resultadoIA) {
        try {
            // Cria mensagem para o AgenteJulgador
            ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
            msg.setContent(resultadoIA);
            msg.addReceiver(new AID("julgador", AID.ISLOCALNAME));
            
            // Envia a mensagem
            send(msg);
            System.out.println("[CLASSIFICADOR] Resultado enviado para o AgenteJulgador");
            
        } catch (Exception e) {
            System.err.println("[CLASSIFICADOR] Erro ao enviar resultado para AgenteJulgador: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    protected void takeDown() {
        System.out.println("[CLASSIFICADOR] Agente finalizando...");
    }
}
