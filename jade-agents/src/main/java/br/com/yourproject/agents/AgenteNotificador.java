package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;

public class AgenteNotificador extends Agent {

    @Override
    protected void setup() {
        System.out.println("Olá! Eu sou o " + getLocalName() + ", estou pronto para enviar notificações.");

        addBehaviour(new CyclicBehaviour() {
            @Override
            public void action() {
                ACLMessage msg = myAgent.receive();

                if (msg != null) {
                    System.out.println("\n======================================================");
                    System.out.println("== NOTIFICAÇÃO RECEBIDA ==");
                    System.out.println("De: " + msg.getSender().getLocalName());
                    System.out.println("Conteúdo: " + msg.getContent());
                    System.out.println("======================================================");

                } else {
                    block();
                }
            }
        });
    }
}