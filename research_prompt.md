**Assunto:** Pesquisa de Projetos Open Source para Orquestração de Microsserviços de IA e Gestão de Conhecimento Pessoal

**Persona:** Atue como um engenheiro de software sênior, especialista em arquitetura de sistemas distribuídos, IA e projetos open source.

**Contexto:** Estou desenvolvendo um projeto chamado "mpc_stack", que consiste em uma pilha de microsserviços containerizados (Docker Compose) para criar um sistema de gestão de conhecimento pessoal e automação de tarefas. A arquitetura integra várias ferramentas, como Ollama (LLMs locais), Supabase (banco de dados), Obsidian (notas), Zotero (referências), GitHub (código) e Hugo (gerador de site estático). O objetivo é criar fluxos de trabalho inteligentes e automatizados (agentic workflows), possivelmente usando um padrão de Geração Aumentada por Recuperação (RAG).

**Tarefa:** Sua tarefa é realizar uma pesquisa aprofundada para encontrar os melhores e mais relevantes projetos open source, documentações, e padrões de arquitetura que possam me ajudar a implementar e integrar os seguintes componentes do meu "mpc_stack":

1.  **Orquestração de Agentes de IA (`fabric-mcp`):**
    *   Pesquise por frameworks ou bibliotecas (preferencialmente em Python ou Go) para construir agentes de IA que possam orquestrar múltiplos serviços/ferramentas (tools).
    *   Foco em projetos que se integram bem com LLMs locais via Ollama.
    *   Exemplos de busca: "AI agent orchestration framework", "LangChain alternatives", "LlamaIndex", "CrewAI", "open source AI fabric".

2.  **Integração com Bases de Conhecimento (`obsidian-mcp`, `zotero-mcp`):**
    *   Encontre as melhores práticas e bibliotecas para interagir programaticamente com vaults do Obsidian (ler/escrever arquivos markdown, analisar metadados) e com a API do Zotero.
    *   Procure por exemplos de implementação de RAG usando uma base de conhecimento do Obsidian.

3.  **Gerenciamento de Memória (`memory-mcp`):**
    *   Investigue padrões e projetos para gerenciar memória de curto e longo prazo para agentes de IA.
    *   Busque por soluções de bancos de dados vetoriais (vector databases) que sejam leves, auto-hospedadas e que se integrem bem com o ecossistema Docker/Ollama.

4.  **Comunicação entre Microsserviços:**
    *   Sugira padrões de comunicação eficientes para este tipo de arquitetura (ex: REST APIs, gRPC, Filas de Mensagens como RabbitMQ ou NATS).
    *   Forneça exemplos de como gerenciar a configuração (ex: variáveis de ambiente, arquivos `.env`) de forma segura e modular entre os contêineres.

**Critérios de Avaliação para os Projetos Sugeridos:**
*   **Atividade e Manutenção:** O projeto está sendo ativamente desenvolvido? (Verificar data do último commit).
*   **Comunidade:** Possui uma comunidade ativa? (Estrelas no GitHub, forks, issues abertas/fechadas).
*   **Documentação:** A documentação é clara, completa e com exemplos práticos?
*   **Suporte a Docker:** O projeto é "container-friendly" ou possui imagens Docker oficiais?
*   **Licença:** A licença de uso é permissiva (MIT, Apache 2.0, etc.)?

**Formato da Resposta:**
Por favor, estruture a resposta em seções, uma para cada tópico da tarefa. Para cada projeto sugerido, forneça:
*   **Nome do Projeto:**
*   **URL do Repositório:**
*   **Breve Descrição:** O que ele faz e por que é relevante para o "mpc_stack".
*   **Prós e Contras:** Uma análise rápida dos pontos fortes e fracos no contexto do meu projeto.
