package br.com.yourproject.agents;

import jade.core.Agent;
import jade.core.behaviours.TickerBehaviour; // Importamos a classe do comportamento

public class AgenteHelloWorld extends Agent {

    private int contador = 0; // Um contador para vermos a ação acontecendo

    @Override
    protected void setup() {
        System.out.println("Agente " + getLocalName() + " iniciado e pronto.");
        System.out.println("Vou começar a executar minha tarefa periódica...");

        // Adicionamos o comportamento ao agente.
        // O comportamento vai "tocar" (executar) a cada 2000 milissegundos (2 segundos).
        addBehaviour(new TickerBehaviour(this, 2000) {
            
            @Override
            protected void onTick() {
                // Este é o código que será executado a cada "tick" do relógio.
                contador++;
                System.out.println("Estou vivo! Esta é a execução número: " + contador);
                
                // Exemplo de como parar o comportamento se uma condição for atingida
                if (contador >= 10) {
                    System.out.println("Completei 10 execuções. Encerrando meu comportamento periódico.");
                    stop(); // O método stop() encerra este comportamento. O agente continua vivo.
                }
            }
        });
    }
}