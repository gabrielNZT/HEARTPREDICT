---
chave: fipa2002propose
titulo: FIPA Propose Interaction Protocol Specification (SC00036H)
autores: [Foundation for Intelligent Physical Agents]
ano: 2002
veiculo: FIPA (padrão; hoje sob o IEEE Computer Society)
tipo_bib: misc
url: http://www.fipa.org/specs/fipa00036/SC00036H.html
temas: [protocolos-fipa, comunicacao-agentes]
leitura: resumo
lido_em: 2026-09-29
relevancia: central
---

# FIPA Propose Interaction Protocol Specification (SC00036H)

> **Leitura: resumo/trechos** obtidos na busca de 29/09/2026. Ler na íntegra antes de citar detalhes.

## O que se sabe
O iniciador envia PROPOSE indicando que executará uma ação se o participante concordar; o participante responde com ACCEPT-PROPOSAL ou REJECT-PROPOSAL. Toda interação é identificada por um conversation-id único, com o qual todas as mensagens devem ser marcadas.

## Relação com o meu TCC
**Protocolo que formaliza o ciclo Explicador ↔ Verificador** (D021). Implementado no JADE por jade.proto.ProposeInitiator/ProposeResponder (API JADE 4.6.0).
