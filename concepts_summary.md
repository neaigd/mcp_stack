# Conceitos Fundamentais do MPC-Stack

O MPC-Stack é uma arquitetura de microsserviços projetada para orquestrar e expandir as capacidades de Large Language Models (LLMs) locais, com um foco inicial na aplicação em **análise de jurisprudência**.

## 1. Orquestração de Agentes de IA

O coração do sistema é o serviço `fabric-mcp`, que atua como um orquestrador de agentes de IA. Ele utiliza uma abordagem híbrida:

*   **CrewAI:** Para gerenciar agentes de IA com papéis específicos (ex: Pesquisador Jurídico, Analista de Jurisprudência) que colaboram para resolver tarefas complexas.
*   **LlamaIndex:** Integrado como uma ferramenta para lidar com a recuperação de informações (RAG - Retrieval Augmented Generation) de bases de conhecimento.

## 2. Gestão de Conhecimento Pessoal (PKM)

O sistema integra suas bases de conhecimento pessoal para fornecer contexto aos LLMs:

*   **Obsidian (`obsidian-mcp`):** Permite o acesso programático ao seu vault do Obsidian, transformando suas notas em uma base de dados pesquisável para os agentes de IA.
*   **Zotero (`zotero-mcp`):** Facilita a ingestão e organização de referências e documentos (como acórdãos do STJ), que são então processados e disponibilizados para análise.

## 3. Memória e Contexto

O serviço `memory-mcp` gerencia a memória do sistema:

*   **Memória de Longo Prazo (LTM):** Implementada através de um pipeline de RAG, onde o conteúdo do Obsidian e Zotero é transformado em *embeddings* e armazenado em um banco de dados vetorial (inicialmente **ChromaDB**).
*   **Memória de Curto Prazo (STM):** Gerencia o contexto das conversas atuais, permitindo que os agentes mantenham o fio da meada em interações complexas.

## 4. Comunicação e Integração

A comunicação eficiente entre os microsserviços é crucial:

*   **gRPC:** Utilizado para comunicação síncrona de alta performance entre os serviços, garantindo rapidez e tipagem forte.
*   **NATS:** Empregado para comunicação assíncrona e baseada em eventos, ideal para tarefas em segundo plano (ex: reindexação do vault).
*   **Docker Secrets:** Para gerenciamento seguro de credenciais e informações sensíveis.

## 5. Segurança Ofensiva Controlada (Red Team)

Um pilar fundamental do projeto é a segurança, especialmente ao lidar com dados sensíveis e IA:

*   **Red Teaming:** Simula ameaças reais para testar a resiliência do sistema, identificar vulnerabilidades e garantir a integridade e a ética dos modelos de IA, prevenindo vieses e *prompt injections*.

## 6. O Projeto Prometeus: IA na Jurisprudência

O MPC-Stack está sendo aplicado em um projeto piloto para **transformar a análise de jurisprudência**, com foco em decisões do STJ sobre a validade de documentos eletrônicos. Este projeto demonstra como a IA e a automação podem gerar insights acionáveis e otimizar o trabalho de juristas, utilizando:

*   **Gemini CLI e Model Context Protocol (MCP):** Para acesso rápido e seguro a dados internos (Supabase via Edge Functions), enriquecendo a geração de modelos com informações em tempo real.

Este conjunto de conceitos e tecnologias visa criar um sistema robusto, inteligente e seguro para a gestão de conhecimento e automação de fluxos de trabalho com LLMs.