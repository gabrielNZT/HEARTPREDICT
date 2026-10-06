package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.core.AID;

/**
 * Agente que, na arquitetura do TCC, será o Verificador de fidelidade das explicações
 * (ver tcc/00-projeto/decisoes.md, D005 e D019).
 *
 * Estado atual (transição): apenas encaminha o resultado do AgenteClassificador para o
 * AgenteExplicador e registra a resposta. A lógica anterior foi removida porque usava faixas de
 * risco arbitrárias (0,2/0,4/0,6/0,8), inconsistentes com as do serviço de risco, e simulava
 * "ações clínicas" sem fundamento para um risco preventivo em 10 anos.
 */
public class AgenteJulgador extends Agent {

    @Override
    protected void setup() {
        System.out.println("Olá! Eu sou o " + getLocalName() + " (futuro verificador), pronto para encaminhar resultados.");
        addBehaviour(new EncaminharResultadoBehaviour());
    }

    private class EncaminharResultadoBehaviour extends CyclicBehaviour {

        @Override
        public void action() {
            MessageTemplate template = MessageTemplate.and(
                MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                MessageTemplate.MatchSender(new AID("classificador", AID.ISLOCALNAME))
            );
            ACLMessage msg = myAgent.receive(template);

            if (msg != null) {
                String content = msg.getContent();
                if (content == null || content.trim().isEmpty()) {
                    System.err.println("[JULGADOR] Mensagem vazia recebida, ignorando...");
                    return;
                }
                System.out.println("\n[JULGADOR] Resultado recebido de: " + msg.getSender().getLocalName());
                solicitarExplicacao(content);
            } else {
                block();
            }
        }
    }

    private void solicitarExplicacao(String resultadoClassificador) {
        ACLMessage msg = new ACLMessage(ACLMessage.REQUEST);
        msg.setContent(resultadoClassificador);
        msg.addReceiver(new AID("explicador", AID.ISLOCALNAME));

        String replyId = "explicacao-" + System.currentTimeMillis();
        msg.setReplyWith(replyId);
        send(msg);
        System.out.println("[JULGADOR] Solicitação de explicação enviada para o AgenteExplicador");

        // Aguarda apenas a resposta correspondente a esta solicitação.
        // É aqui que a verificação de fidelidade será inserida.
        addBehaviour(new CyclicBehaviour() {
            @Override
            public void action() {
                MessageTemplate template = MessageTemplate.and(
                    MessageTemplate.MatchInReplyTo(replyId),
                    MessageTemplate.MatchSender(new AID("explicador", AID.ISLOCALNAME))
                );
                ACLMessage reply = receive(template);

                if (reply != null) {
                    if (reply.getPerformative() == ACLMessage.INFORM) {
                        System.out.println("\n[JULGADOR] Explicação recebida do AgenteExplicador:");
                        System.out.println(reply.getContent());
                    } else if (reply.getPerformative() == ACLMessage.FAILURE) {
                        System.err.println("[JULGADOR] Erro ao obter explicação: " + reply.getContent());
                    }
                    removeBehaviour(this);
                } else {
                    block();
                }
            }
        });
    }
}
