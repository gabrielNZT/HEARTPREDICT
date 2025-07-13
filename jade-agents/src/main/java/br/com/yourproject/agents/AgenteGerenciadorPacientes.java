package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.AID;
import jade.lang.acl.ACLMessage;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.net.InetSocketAddress;

public class AgenteGerenciadorPacientes extends Agent {

    @Override
    protected void setup() {
        System.out.println("Olá! Eu sou o " + getLocalName() + ", iniciando servidor HTTP na porta 8888.");

        try {
            HttpServer server = HttpServer.create(new InetSocketAddress(8888), 0);
            
            server.createContext("/registrar", new RegistroHttpHandler(this));
            
            server.setExecutor(null); 
            server.start();

        } catch (IOException e) {
            System.err.println("Erro ao iniciar o servidor HTTP: " + e.getMessage());
            e.printStackTrace();
        }

        System.out.println("Servidor iniciado. Aguardando requisições em http://localhost:8888/registrar");
    }

    static class RegistroHttpHandler implements HttpHandler {
        private Agent meuAgente;

        public RegistroHttpHandler(Agent a) {
            this.meuAgente = a;
        }

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String requestBody = "";
            if ("POST".equals(exchange.getRequestMethod())) {
                InputStreamReader isr = new InputStreamReader(exchange.getRequestBody(), "utf-8");
                BufferedReader br = new BufferedReader(isr);
                String line;
                while ((line = br.readLine()) != null) {
                    requestBody += line;
                }

                System.out.println("\n[GATEWAY HTTP] Requisição recebida!");
                System.out.println("[GATEWAY HTTP] Corpo da requisição: " + requestBody);
                     // Envia os dados para o AgenteClassificador
            enviarDadosParaClassificador(requestBody);
            }

            String response = "Requisição recebida com sucesso pelo AgenteGerenciadorPacientes!";
            exchange.sendResponseHeaders(200, response.getBytes("UTF-8").length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
        
        private void enviarDadosParaClassificador(String dadosJson) {
            try {
                // Valida se é JSON válido antes de enviar
                if (dadosJson == null || dadosJson.trim().isEmpty()) {
                    System.err.println("[GATEWAY HTTP] Dados vazios recebidos, não enviando para o AgenteClassificador");
                    return;
                }
                
                // Verifica se é um JSON válido
                ObjectMapper mapper = new ObjectMapper();
                mapper.readTree(dadosJson); // Isso lança exceção se não for JSON válido
                
                // Cria mensagem para o AgenteClassificador
                ACLMessage msg = new ACLMessage(ACLMessage.REQUEST);
                msg.setContent(dadosJson);
                msg.addReceiver(new AID("classificador", AID.ISLOCALNAME));
                
                // Envia a mensagem
                meuAgente.send(msg);
                
                System.out.println("[GATEWAY HTTP] Dados enviados para o AgenteClassificador");
                
            } catch (Exception e) {
                System.err.println("[GATEWAY HTTP] Erro ao enviar dados para o AgenteClassificador: " + e.getMessage());
                System.err.println("[GATEWAY HTTP] Dados recebidos: " + dadosJson);
                e.printStackTrace();
            }
        }
    }
}