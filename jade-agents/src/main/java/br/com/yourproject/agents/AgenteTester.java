package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.AID;
import jade.core.behaviours.WakerBehaviour;
import jade.lang.acl.ACLMessage;

public class AgenteTester extends Agent {

    @Override
    protected void setup() {
        System.out.println("Olá! Eu sou o " + getLocalName() + ".");
        System.out.println("Vou enviar um pedido de notificação em 5 segundos...");

        // Adiciona um comportamento que vai "acordar" depois de 5000ms (5 segundos)
        addBehaviour(new WakerBehaviour(this, 5000) {
            @Override
            protected void onWake() {
                System.out.println("Ok, acordei! Enviando a mensagem agora...");

                // 1. Criar a mensagem
                ACLMessage msg = new ACLMessage(ACLMessage.REQUEST); // Usamos REQUEST para pedir um serviço

                // 2. Definir o destinatário
                // O AID é o "endereço" do agente.
                // "notificador" é o apelido que daremos ao agente na inicialização.
                AID destinatario = new AID("notificador", AID.ISLOCALNAME);
                msg.addReceiver(destinatario);

                // 3. Definir o conteúdo
                msg.setContent("ALERTA CRÍTICO: Risco de arritmia detectado para o paciente 734!");

                // 4. Enviar a mensagem
                myAgent.send(msg);
            }
        });
    }
}