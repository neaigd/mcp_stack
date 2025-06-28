

# **Um Blueprint Arquitetural para o mpc\_stack: Uma Análise Técnica de Frameworks Open Source para Workflows Agênticos e Gestão de Conhecimento Pessoal**

## **Introdução**

Este relatório apresenta uma avaliação técnica aprofundada de projetos open source, bibliotecas e padrões arquiteturais para orientar o desenvolvimento do projeto "mpc\_stack". O objetivo é delinear um caminho para a construção de um sistema de Gestão de Conhecimento Pessoal (PKM) resiliente, modular e inteligente, totalmente containerizado e centrado em Modelos de Linguagem Grandes (LLMs) locais. A arquitetura visada segue um padrão de microsserviços, integrando um conjunto diversificado de ferramentas, incluindo Ollama, Obsidian, Zotero e outras, para habilitar "workflows agênticos" complexos e automatizados.  
A análise aqui contida é fundamentada em uma revisão detalhada da documentação de projetos, discussões da comunidade e artigos técnicos. Cada recomendação é ponderada em relação aos critérios especificados de Atividade e Manutenção, Comunidade, Documentação, Suporte a Docker e Licença de uso. É importante notar que o link para o caso de uso prático (share.note.sx/mqah0q7m) estava inacessível durante a pesquisa.1 Consequentemente, esta análise procede com base na descrição detalhada do projeto fornecida na consulta, tratando-a como a principal fonte de requisitos funcionais. O resultado é um blueprint arquitetural coeso, projetado para um engenheiro sênior, que aborda desde a orquestração de IA de alto nível até as decisões de implementação de baixo nível.

## **Seção 1: Arquitetando a Camada de Orquestração de IA (fabric-mcp)**

Esta seção aborda o núcleo do sistema inteligente: o serviço fabric-mcp, responsável por orquestrar agentes de IA e suas ferramentas. A escolha feita aqui ditará todo o paradigma de desenvolvimento, influenciando a flexibilidade, a velocidade de desenvolvimento e a performance do sistema.

### **1.1. Princípios Fundamentais: Orquestração Baseada em Toolkit vs. Baseada em Equipe**

No design de sistemas agênticos, duas filosofias dominantes emergem, e a escolha entre elas representa uma decisão arquitetural fundamental.  
A primeira abordagem é a **orquestração baseada em toolkit**, exemplificada por frameworks como LangChain 2 e LlamaIndex.3 Estes fornecem um conjunto modular de primitivas de baixo nível — como cadeias (chains), recuperadores (retrievers) e ferramentas (tools) — que o desenvolvedor conecta para formar Grafos Acíclicos Dirigidos (DAGs) complexos. Esta abordagem oferece máxima flexibilidade, permitindo a construção de lógicas de raciocínio personalizadas (por exemplo, padrões ReAct usando LangGraph). No entanto, ela coloca o ônus do design arquitetural inteiramente sobre o desenvolvedor, exigindo um entendimento profundo de como compor esses blocos de construção de forma eficaz.  
A segunda abordagem é a **orquestração baseada em equipe**, que é a filosofia central de frameworks como o CrewAI.3 Em vez de expor primitivas de baixo nível, o CrewAI abstrai a complexidade ao introduzir o conceito de "agentes" com papéis, objetivos e histórias de fundo predefinidos, que colaboram em uma "tripulação" (crew). Esta é uma abstração de nível superior que pode simplificar drasticamente o desenvolvimento de tarefas que se mapeiam bem para uma estrutura de equipe do mundo real, como pesquisa, análise e redação.  
A decisão para o fabric-mcp não é apenas sobre qual biblioteca usar, mas sobre qual paradigma de "inteligência" adotar. É a escolha entre construir o "cérebro" do agente a partir de componentes fundamentais ou adotar um modelo cognitivo colaborativo pré-construído.

### **1.2. Análise de Frameworks de Orquestração Baseados em Python**

Python é o padrão de fato para o desenvolvimento de IA/ML, oferecendo o ecossistema mais rico de bibliotecas e o maior suporte da comunidade. A preferência por Python na consulta torna esta a principal área de investigação.  
LangChain  
É um framework maduro e altamente modular para construir aplicações com LLMs.4 Sua principal força reside na flexibilidade incomparável, em um vasto ecossistema de integrações e em uma comunidade massiva. O  
LangChain Expression Language (LCEL) permite a composição fluida de cadeias de processamento.10 Sua abstração de  
Tools é fundamental e extremamente bem documentada, permitindo a criação fácil de funções personalizadas para os agentes invocarem.11 A integração com Ollama é direta e bem estabelecida.2 No entanto, sua flexibilidade tem um custo: pode ser verboso e complexo para tarefas simples 3, e sem uma gestão cuidadosa, pode levar a um código mal estruturado.4  
LlamaIndex  
Este é um framework de dados projetado especificamente para construir aplicações de LLM com aumento de contexto, se destacando em pipelines de Geração Aumentada por Recuperação (RAG).3 Sua maior vantagem é a capacidade de primeira classe para indexação e recuperação de dados de fontes diversas.6 É altamente escalável para casos de uso com grande volume de documentos e é considerado leve, integrando-se bem com outras ferramentas, incluindo Docker e o próprio LangChain.3 A desvantagem é que ele é menos versátil para tarefas agênticas de propósito geral em comparação com LangChain ou CrewAI 3, e sua retenção de contexto para conversas complexas e de múltiplos passos pode ser menos robusta que a do LangChain.5  
CrewAI  
Um framework mais recente focado na orquestração de agentes de IA autônomos e baseados em papéis que colaboram para resolver tarefas complexas.7 Sua abordagem de papéis é um mapeamento intuitivo para a arquitetura de microsserviços do  
mpc\_stack, onde obsidian-mcp e zotero-mcp poderiam ser implementados como ferramentas para agentes especializados (ex: um Pesquisador). Ele simplifica a orquestração de múltiplos agentes 7 e possui padrões claros para a criação de ferramentas personalizadas 13 e integração com Ollama.9 Como contrapartida, por ser mais novo, seu ecossistema é menos maduro que o do LangChain.7 Sua abordagem estruturada pode ser menos flexível para fluxos de trabalho que não se encaixam na metáfora de "equipe" e pode introduzir uma sobrecarga para tarefas mais simples de um único agente.3

| Framework | Filosofia Principal | Integração com Ollama | Criação de Ferramentas Personalizadas | Comunidade e Atividade | Amigável ao Docker | Melhor Caso de Uso para mpc\_stack |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **LangChain** | Toolkit modular de primitivas para construir qualquer aplicação de LLM. | Excelente. Suportado nativamente através do langchain-ollama.2 | Muito flexível. Suporta criação via decorador @tool ou subclasses de BaseTool.11 | Enorme e muito ativa. Ecossistema mais maduro.4 | Sim. Vários exemplos e tutoriais usam Docker. | Para controle máximo e flexibilidade na definição de cadeias de raciocínio complexas. |
| **LlamaIndex** | Framework de dados otimizado para RAG e indexação. | Excelente. Ollama é um provedor de LLM e embedding suportado.6 | Suportado. Ferramentas podem ser criadas e usadas por agentes, mas o foco principal é na recuperação de dados.3 | Grande e ativa, com foco em RAG. Lançamentos frequentes.6 | Sim. Mencionado como uma integração fácil.6 | Para construir o componente de recuperação de dados (RAG) da forma mais eficiente e escalável possível. |
| **CrewAI** | Orquestração de múltiplos agentes colaborativos baseados em papéis. | Excelente. Ollama pode ser configurado como o LLM para qualquer agente.9 | Ponto forte. Padrões claros com decorador @tool ou subclasses de BaseTool.13 | Crescente e muito ativa. Lançamentos frequentes.9 | Sim. Sendo uma biblioteca Python, é facilmente containerizável. | Para orquestrar o fluxo de trabalho entre diferentes "especialistas" (agentes) que usam as ferramentas (microsserviços). |

### **1.3. Análise de Frameworks de Orquestração Baseados em Go**

Go é uma escolha excelente para construir microsserviços concorrentes e de alta performance. Embora o ecossistema de IA seja menos maduro que o de Python, alguns frameworks promissores surgiram.  
Eino (by Cloudwego/ByteDance)  
Inspirado em LangChain e LlamaIndex, mas projetado com padrões idiomáticos de Go, Eino enfatiza simplicidade, escalabilidade e um poderoso sistema de orquestração baseado em grafos.15 Suas principais vantagens são a tipagem forte e o gerenciamento de concorrência e processamento de stream, que são tratados pelo próprio framework.15 Ele suporta explicitamente Ollama 15 e, por ser parte do ecossistema Cloudwego, foi projetado com microsserviços em mente. A principal desvantagem é sua comunidade muito menor em comparação com os equivalentes em Python.15  
Anyi  
Este é um framework de agente de IA autônomo para Go que foca em fluxos de trabalho robustos com validação e novas tentativas, além de desenvolvimento orientado por configuração.17 Ele suporta uma vasta gama de provedores de LLM, incluindo Ollama.17 A abordagem orientada por configuração é excelente para um ambiente de microsserviços, pois permite alterar fluxos de trabalho sem recompilar o código. No entanto, sua comunidade é muito pequena e o projeto parece ser mais recente e menos maduro.17

### **1.4. Recomendação Arquitetural para fabric-mcp**

A escolha do framework de orquestração não é apenas uma questão de preferência de biblioteca; ela define a arquitetura cognitiva do sistema. A análise revela que uma abordagem híbrida, combinando os pontos fortes de diferentes frameworks, é não apenas viável, mas também uma prática poderosa. A documentação mostra que ferramentas baseadas em LlamaIndex podem ser perfeitamente integradas em uma configuração do CrewAI.5  
Para o mpc\_stack, isso sugere um padrão arquitetural potente: usar o LlamaIndex dentro de uma ferramenta personalizada para lidar com a "Recuperação" (o 'R' do RAG) a partir do Obsidian, e usar o CrewAI para gerenciar o "Agente" (o 'A' do RAG) que utiliza essa ferramenta para raciocinar e gerar respostas. Isso combina as melhores características de ambos os frameworks, criando um sistema mais robusto do que usar qualquer um deles isoladamente.  
**Recomendação:** Para o serviço fabric-mcp, adote uma **abordagem híbrida baseada em Python, utilizando o CrewAI para a orquestração de agentes e o LlamaIndex para a implementação de ferramentas focadas em RAG**.  
**Justificativa:** Esta abordagem aproveita o melhor do ecossistema Python. O modelo baseado em papéis do CrewAI é um ajuste natural para os microsserviços nomeados do projeto (obsidian-mcp, zotero-mcp), que podem ser implementados como ferramentas personalizadas para agentes específicos (por exemplo, um AgenteDePesquisa usa a ferramenta\_zotero e a ferramenta\_rag\_obsidian). O LlamaIndex fornece a funcionalidade mais poderosa e especializada para construir o pipeline de RAG sobre o vault do Obsidian, que é um requisito central. Este modelo híbrido 5 oferece um nível de abstração mais alto que o LangChain, potencialmente acelerando o desenvolvimento, enquanto ainda fornece as capacidades profundas de integração de dados do LlamaIndex.

## **Seção 2: Construindo a Ponte de Integração de Conhecimento (obsidian-mcp, zotero-mcp)**

Estes serviços são os provedores de dados para os agentes de IA, atuando como os "sentidos" que conectam o sistema às suas bases de conhecimento. A sua implementação robusta é crucial para a eficácia do padrão RAG.

### **2.1. Acesso Programático aos Vaults do Obsidian**

O Obsidian utiliza arquivos Markdown locais, não um banco de dados ou uma API formal, o que torna o acesso programático um desafio. A interação direta com o sistema de arquivos pode ser frágil.  
Uma análise das bibliotecas disponíveis revela um caminho claro. Bibliotecas mais antigas como py-obsidianmd 18 não são atualizadas desde 2022, representando um risco de manutenção.18 Outras, como  
pyobsidian, estavam com o repositório inacessível.20  
A abordagem mais promissora e robusta é o **obsidian-plugin-python-bridge**.21 Este é um plugin para o Obsidian, ativamente mantido, que expõe um servidor local. Isso permite que scripts Python interajam com o vault através de uma interface semelhante a uma API para ler/escrever notas, gerenciar metadados e muito mais. Este método desacopla o serviço  
obsidian-mcp do sistema de arquivos bruto, fornecendo um ponto de integração mais estável e rico em recursos.  
**Recomendação:** Utilizar o **obsidian-plugin-python-bridge**.21 O serviço  
obsidian-mcp faria requisições HTTP para a ponte local fornecida pelo plugin, abstraindo a complexidade da manipulação de arquivos.

### **2.2. Interface com o Zotero**

Para a interação com o Zotero, a biblioteca **Pyzotero** é o padrão claro, bem mantido e aceito pela comunidade para interagir com a API do Zotero em Python.22 Ela oferece métodos abrangentes para recuperar itens, coleções, tags e conteúdo de texto completo, bem como para criar e atualizar itens.23  
A implementação é direta: o serviço zotero-mcp usará Pyzotero para criar um cliente para a API do Zotero. Este serviço irá expor funções de alto nível, como get\_references\_by\_tag ou get\_pdf\_for\_item, que podem então ser encapsuladas em uma Tool para uso pelo agente no fabric-mcp.

### **2.3. Implementando um Pipeline de RAG Local com Obsidian e Ollama**

Este é o fluxo de trabalho mais crítico para o mpc\_stack. A arquitetura deve sintetizar padrões de múltiplos tutoriais e exemplos.25 O processo é o seguinte:

1. **Carregamento de Documentos:** O serviço obsidian-mcp, usando a ponte recomendada 21, lê o conteúdo das notas especificadas (ou do vault inteiro).  
2. **Divisão (Chunking):** O texto Markdown bruto é dividido em pedaços menores e semanticamente significativos. Um RecursiveCharacterTextSplitter (como visto em exemplos do LangChain 30) ou um divisor específico para Markdown 27 é ideal para preservar a estrutura.  
3. **Embedding:** Cada pedaço de texto é então convertido em um vetor numérico (embedding). Como a pilha utiliza Ollama, um modelo de embedding local como nomic-embed-text 29 ou  
   mxbai-embed-large 2 deve ser usado. Este processo será gerenciado pelo serviço  
   memory-mcp.  
4. **Armazenamento:** Os embeddings e os pedaços de texto correspondentes são armazenados no banco de dados vetorial escolhido (discutido na Seção 3).  
5. **Recuperação:** Quando o agente no fabric-mcp recebe uma consulta do usuário, ele primeiro a envia para o serviço memory-mcp. Este serviço gera o embedding da consulta usando o mesmo modelo e realiza uma busca por similaridade no banco de dados vetorial para encontrar os pedaços de texto mais relevantes.  
6. **Aumento:** Os pedaços de texto recuperados são formatados em um bloco de contexto e adicionados ao prompt original do usuário.  
7. **Geração:** Este prompt aumentado é enviado ao LLM local (ex: llama3.2) via Ollama 2 para gerar uma resposta final que é fundamentada no conhecimento do vault.

### **2.4. Padrão de Integração para Fontes de Conhecimento**

Uma mudança de paradigma é necessária aqui: as fontes de conhecimento não devem ser tratadas apenas como endpoints de dados, mas sim como **Ferramentas** abstratas. Em vez de o fabric-mcp chamar diretamente um endpoint REST genérico como /get\_note no obsidian-mcp, a arquitetura deve definir uma ObsidianSearchTool de nível superior. A descrição desta ferramenta informaria ao agente *o que ela pode fazer* (ex: "Use esta ferramenta para buscar notas relevantes na base de conhecimento pessoal sobre um tópico específico.").  
Internamente, esta ferramenta encapsularia a lógica de comunicação com os serviços obsidian-mcp e memory-mcp para realizar a busca RAG. Este design alinha-se perfeitamente com o paradigma agêntico do CrewAI 13 ou LangChain 11, tornando o sistema mais inteligente, descritível e extensível.  
Padrão de Integração Recomendado:  
Os serviços obsidian-mcp e zotero-mcp devem expor uma API simples e robusta (preferencialmente gRPC, veja a Seção 4). Dentro do serviço fabric-mcp, classes Python dedicadas (ex: ZoteroTool, ObsidianRAGTool) devem ser criadas, herdando da BaseTool do framework escolhido. Essas classes de ferramentas encapsularão a lógica de chamada dos respectivos microsserviços, fornecendo uma interface limpa e de alto nível para o agente de IA utilizar.

## **Seção 3: Projetando o Sistema de Memória do Agente (memory-mcp)**

Este serviço atua como o hipocampo do sistema de IA, responsável tanto pelo conhecimento de longo prazo (via RAG) quanto pelo contexto conversacional de curto prazo.

### **3.1. Padrões para Memória de Agente**

* **Memória de Longo Prazo (LTM):** Refere-se ao conhecimento persistente recuperado do vault do Obsidian e outras fontes. É implementada através do pipeline de RAG e armazenada no banco de dados vetorial.  
* **Memória de Curto Prazo (STM):** Refere-se ao contexto da conversa atual. Frameworks como LangChain e CrewAI possuem sistemas de gerenciamento de memória embutidos (ex: ConversationBufferMemory) que armazenam o histórico de interações para manter o contexto em um diálogo de múltiplos turnos. Para uma arquitetura de microsserviços, centralizar o estado da sessão no memory-mcp (talvez usando um simples armazenamento de chave-valor como Redis ao lado do banco de dados vetorial) é um padrão mais escalável do que mantê-lo apenas no estado do orquestrador fabric-mcp.

### **3.2. Avaliação de Bancos de Dados Vetoriais Auto-hospedados**

Os requisitos principais para o mpc\_stack são: ser leve, auto-hospedado e amigável para contêineres.  
ChromaDB  
É um banco de dados vetorial AI-nativo e open source, projetado para simplicidade e desenvolvimento local.33 É frequentemente a escolha padrão para prototipagem rápida de RAG.28 Sua principal vantagem é a extrema facilidade de configuração e uso, com uma API Python simples e uma arquitetura "embedded-first" perfeita para um projeto pessoal.35 A desvantagem é que ele é menos rico em recursos em comparação com concorrentes em termos de filtragem avançada, escalabilidade e operações de nível de produção.36  
Qdrant  
Este é um motor de busca de similaridade vetorial pronto para produção, com foco em performance e filtragem avançada.34 Escrito em Rust para alta performance, ele oferece filtragem robusta, escalonamento horizontal e snapshots para backups.36 Fornece imagens Docker oficiais e documentação clara para o cliente.38 A desvantagem é que sua configuração e gerenciamento são mais complexos que os do Chroma, e seus recursos avançados podem ser excessivos para a fase inicial de um projeto pessoal como o  
mpc\_stack.36  
Milvus Lite  
É uma versão leve e de binário único do poderoso e altamente escalável banco de dados vetorial Milvus.39 Ele oferece um caminho claro para escalar para a versão distribuída completa, se necessário, e é rico em recursos.39 No entanto, mesmo no modo "Lite", pode ser mais intensivo em recursos e complexo que o Chroma. Ele foi projetado como um ponto de entrada para um sistema muito maior, o que pode não se alinhar com a filosofia de "pilha pessoal".

| Banco de Dados | Filosofia Principal | Facilidade de Configuração (Docker) | Pegada de Recursos | Recursos Avançados (ex: Filtragem) | Caminho de Escalabilidade | Licença |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **ChromaDB** | AI-nativo, "embedded-first", simplicidade para desenvolvedores.37 | Muito Alta. docker-compose simples ou pip install.35 | Baixa. Ideal para desenvolvimento local.33 | Básico. Suporta filtragem de metadados. | Limitada. Focado em uso em uma única máquina. | Apache 2.0.34 |
| **Qdrant** | Pronto para produção, alta performance, filtragem avançada.36 | Média. Requer mais configuração para produção.38 | Média. Otimizado para performance. | Excelente. Filtragem de payload, sharding.36 | Alta. Projetado para escalonamento horizontal.36 | Apache 2.0.37 |
| **Milvus Lite** | Ponto de entrada para um banco de dados de escala massiva.39 | Média. pip install para a versão lite. | Média a Alta. Mais complexo que Chroma. | Excelente. Herda recursos da versão completa. | Excelente. Migração transparente para Milvus distribuído.39 | Apache 2.0.34 |

### **3.3. Recomendação Arquitetural para memory-mcp**

A escolha do "melhor" banco de dados vetorial depende da fase atual do projeto e de sua ambição futura. O Chroma é descrito como ideal para "prototipagem" e "uso local" 33, enquanto o Qdrant é "pronto para produção".34 O  
mpc\_stack é um projeto pessoal, o que se alinha com a filosofia do Chroma. No entanto, o fato de ser uma pilha de microsserviços construída por um engenheiro sênior sugere um desejo de robustez que se alinha com o Qdrant.  
Uma abordagem pragmática é começar com a ferramenta mais simples que atenda à necessidade (Chroma), mas projetar o serviço memory-mcp com uma interface clara (por exemplo, uma classe VectorStoreRepository) que permitiria a troca do backend para o Qdrant no futuro, sem reescrever a lógica de orquestração.  
**Recomendação:** Iniciar com **ChromaDB** para o serviço memory-mcp.  
**Justificativa:** Para um projeto pessoal e auto-hospedado, minimizar a complexidade operacional é primordial. A simplicidade do Chroma, sua baixa pegada de recursos e a integração perfeita com o ecossistema de IA em Python o tornam a escolha ideal para colocar o pipeline de RAG em funcionamento rapidamente.35 É improvável que o  
mpc\_stack atinja uma escala onde os recursos avançados de sharding do Qdrant ou as capacidades de bilhões de vetores do Milvus sejam necessários em um futuro próximo. A arquitetura do memory-mcp deve abstrair o banco de dados vetorial, permitindo uma futura migração para o Qdrant se os requisitos de performance ou filtragem evoluírem.

## **Seção 4: Engenharia de Comunicação e Configuração Robusta de Microsserviços**

Esta seção cobre os requisitos não funcionais que garantem que o mpc\_stack seja seguro, manutenível e eficiente.

### **4.1. Selecionando Padrões de Comunicação**

Um sistema de microsserviços possui diferentes necessidades de comunicação: chamadas internas rápidas, tarefas assíncronas em segundo plano, etc. A escolha da ferramenta certa para cada trabalho é crucial para evitar gargalos de performance ou inflexibilidade arquitetural.  
Comunicação Síncrona (Requisição/Resposta): gRPC vs. REST  
REST é universal e bem compreendido, mas seu formato baseado em texto (JSON) sobre HTTP/1.1 pode ser lento para comunicação interna de alto volume.40 O gRPC, por outro lado, é um framework RPC de alta performance que usa HTTP/2 e serialização binária com Protocol Buffers (Protobuf). Isso o torna significativamente mais rápido e eficiente para a comunicação interna entre serviços.41 Suas definições de serviço fortemente tipadas e o suporte a streaming bidirecional são ideais para uma arquitetura de microsserviços. A recomendação é usar  
**gRPC** para toda a comunicação interna e de alta vazão.  
Comunicação Assíncrona (Eventos/Mensagens): NATS vs. RabbitMQ  
RabbitMQ é um message broker maduro e rico em recursos, mas sua complexidade pode ser excessiva para projetos menores.43 O NATS é um sistema de mensagens leve, de alta performance e projetado para aplicações nativas da nuvem.43 Ele prioriza a simplicidade e a velocidade, tem uma pegada de recursos muito pequena e é fácil de implantar com Docker.45 A recomendação é usar  
**NATS** para qualquer comunicação assíncrona necessária, como o disparo de tarefas de longa duração (por exemplo, reindexação do vault).

| Protocolo | Paradigma | Formato de Dados | Performance | Característica Chave | Melhor Caso de Uso para mpc\_stack |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **gRPC** | Síncrono (RPC) | Binário (Protobuf) | Muito Alta | Contratos de API fortemente tipados, streaming bidirecional.40 | Comunicação interna entre todos os microsserviços. |
| **REST** | Síncrono (Recurso) | Texto (JSON) | Média | Universalidade, legibilidade humana.40 | Exposição de uma API pública externa (se necessário no futuro). |
| **NATS** | Assíncrono (Pub/Sub) | Binário | Muito Alta | Simplicidade, baixa latência, pegada mínima.44 | Para tarefas em segundo plano e notificações de eventos. |
| **RabbitMQ** | Assíncrono (Broker) | Binário (AMQP) | Alta | Roteamento complexo, garantias de entrega.43 | Exagerado para a escala atual; considerar apenas se houver necessidade de roteamento complexo. |

### **4.2. Uma Estratégia de Configuração Modular**

Para configurações não sensíveis, como nomes de modelos, portas de serviço ou caminhos de arquivo, a abordagem padrão e recomendada é usar uma combinação de um arquivo .env na raiz do projeto com a interpolação de variáveis do Docker Compose (${VAR}).48 Isso separa a configuração do código e permite substituições fáceis por ambiente.  
Exemplo de docker-compose.yml:

YAML

services:  
  ollama:  
    image: ollama/ollama  
    environment:  
      \- OLLAMA\_MODEL=${OLLAMA\_MODEL\_DEFAULT}

Exemplo de arquivo .env:

OLLAMA\_MODEL\_DEFAULT=llama3.2

### **4.3. Melhores Práticas para Gerenciamento de Segredos**

A pesquisa é unânime e clara: usar variáveis de ambiente para segredos (chaves de API, senhas) é um risco de segurança significativo.51 Eles podem ser expostos em logs e são acessíveis a todos os processos dentro de um contêiner.  
O Docker Compose fornece uma maneira nativa e segura de gerenciar segredos através do mecanismo secrets.53 Segredos são definidos em um bloco  
secrets: de nível superior no docker-compose.yml, apontando para arquivos no host. Eles são então montados como arquivos somente leitura em um sistema de arquivos temporário em /run/secrets/\<secret\_name\> dentro dos contêineres que recebem acesso explícito. As vantagens são o controle de acesso granular e a não exposição através de variáveis de ambiente.53  
**Padrão Recomendado:**

1. Crie um diretório secrets/ na raiz do projeto e adicione-o ao .gitignore.  
2. Armazene cada segredo em um arquivo separado dentro deste diretório (ex: secrets/zotero\_api\_key).  
3. No docker-compose.yml, defina os segredos e monte-os nos serviços necessários.  
4. No código da aplicação, adapte-o para ler os segredos primeiro do caminho do arquivo, recorrendo a uma variável de ambiente apenas como fallback para desenvolvimento local fora do Compose.51

Exemplo de docker-compose.yml:

YAML

services:  
  zotero-mcp:  
    image: my-zotero-mcp  
    secrets:  
      \- zotero\_api\_key

secrets:  
  zotero\_api\_key:  
    file:./secrets/zotero\_api\_key

## **Conclusão: Uma Visão Arquitetural Coesa para o mpc\_stack**

A análise detalhada das tecnologias open source disponíveis leva a um blueprint arquitetural coeso e robusto para o mpc\_stack. Este blueprint prioriza a modularidade, a segurança e a utilização de ferramentas de ponta, adequadas para um projeto pessoal sofisticado.  
A síntese das recomendações-chave é a seguinte:

* **Orquestração:** Um serviço fabric-mcp baseado em Python, utilizando **CrewAI** para a orquestração de agentes e ferramentas personalizadas construídas com **LlamaIndex** para tarefas de RAG.  
* **Conhecimento:** Um serviço obsidian-mcp que interage com o vault através do **obsidian-plugin-python-bridge** e um serviço zotero-mcp que utiliza a biblioteca **Pyzotero**.  
* **Memória:** Um serviço memory-mcp utilizando **ChromaDB** como banco de dados vetorial, com uma camada de abstração para permitir futuras migrações.  
* **Comunicação:** **gRPC** para chamadas internas síncronas entre serviços e **NATS** para tarefas assíncronas e baseadas em eventos.  
* **Configuração e Segredos:** Uma combinação de **arquivos .env** para configurações não sensíveis e o mecanismo nativo de **Docker secrets** para todas as credenciais.

O fluxo de dados de alto nível seria o seguinte: uma consulta do usuário inicia um fluxo de trabalho no fabric-mcp. O agente CrewAI determina a necessidade de informação, invoca a ObsidianRAGTool, que por sua vez faz uma chamada gRPC para o memory-mcp para recuperar contexto do ChromaDB. O agente aumenta seu prompt com este contexto, envia-o para o Ollama, processa a resposta e, se necessário, usa a ZoteroTool (que chama o zotero-mcp via gRPC) para obter citações antes de compor a resposta final.  
Para o desenvolvimento, uma abordagem em fases é aconselhável: começar com o pipeline RAG principal (obsidian-mcp \-\> memory-mcp \-\> fabric-mcp) antes de adicionar ferramentas mais complexas. A arquitetura de microsserviços é inerentemente extensível, permitindo que futuros serviços (github-mcp, hugo-mcp) sejam adicionados simplesmente criando um novo serviço e uma Tool correspondente, sem alterar a infraestrutura central. As escolhas de gRPC e NATS fornecem uma base sólida para futuras necessidades de escalabilidade e performance.

#### **Referências citadas**

1. acessado em dezembro 31, 1969, [https://share.note.sx/mqah0q7m](https://share.note.sx/mqah0q7m)  
2. Build a Local AI Agent with Python, Ollama, LangChain and SingleStore, acessado em junho 27, 2025, [https://www.singlestore.com/blog/build-a-local-ai-agent-python-ollama-langchain-singlestore/](https://www.singlestore.com/blog/build-a-local-ai-agent-python-ollama-langchain-singlestore/)  
3. Griptape vs. LangChain, CrewAI, and LlamaIndex: Which AI Framework Performs Best?, acessado em junho 27, 2025, [https://dev.to/griptape/griptape-vs-langchain-crewai-and-llamaindex-which-ai-framework-performs-best-354j](https://dev.to/griptape/griptape-vs-langchain-crewai-and-llamaindex-which-ai-framework-performs-best-354j)  
4. Top 9 AI Agent Frameworks as of June 2025 \- Shakudo, acessado em junho 27, 2025, [https://www.shakudo.io/blog/top-9-ai-agent-frameworks](https://www.shakudo.io/blog/top-9-ai-agent-frameworks)  
5. A Detailed Comparison of Top 6 AI Agent Frameworks in 2025 \- Turing, acessado em junho 27, 2025, [https://www.turing.com/resources/ai-agent-frameworks](https://www.turing.com/resources/ai-agent-frameworks)  
6. run-llama/llama\_index: LlamaIndex is the leading ... \- GitHub, acessado em junho 27, 2025, [https://github.com/run-llama/llama\_index](https://github.com/run-llama/llama_index)  
7. Langchain vs CrewAI: Comparative Framework Analysis | Generative AI Collaboration Platform \- Orq.ai, acessado em junho 27, 2025, [https://orq.ai/blog/langchain-vs-crewai](https://orq.ai/blog/langchain-vs-crewai)  
8. Top 10 Open-Source AI Agent Frameworks to Know in 2025, acessado em junho 27, 2025, [https://opendatascience.com/top-10-open-source-ai-agent-frameworks-to-know-in-2025/](https://opendatascience.com/top-10-open-source-ai-agent-frameworks-to-know-in-2025/)  
9. crewAIInc/crewAI: Framework for orchestrating role-playing ... \- GitHub, acessado em junho 27, 2025, [https://github.com/joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI)  
10. How-to guides \- Python LangChain, acessado em junho 27, 2025, [https://python.langchain.com/docs/how\_to/](https://python.langchain.com/docs/how_to/)  
11. Tools \- Python LangChain, acessado em junho 27, 2025, [https://python.langchain.com/docs/concepts/tools/](https://python.langchain.com/docs/concepts/tools/)  
12. How to create tools \- Python LangChain, acessado em junho 27, 2025, [https://python.langchain.com/docs/how\_to/custom\_tools/](https://python.langchain.com/docs/how_to/custom_tools/)  
13. Create Custom Tools \- CrewAI, acessado em junho 27, 2025, [https://docs.crewai.com/learn/create-custom-tools](https://docs.crewai.com/learn/create-custom-tools)  
14. Tools \- CrewAI, acessado em junho 27, 2025, [https://docs.crewai.com/concepts/tools](https://docs.crewai.com/concepts/tools)  
15. cloudwego/eino: The ultimate LLM/AI application ... \- GitHub, acessado em junho 27, 2025, [https://github.com/cloudwego/eino](https://github.com/cloudwego/eino)  
16. Eino: User Manual | CloudWeGo, acessado em junho 27, 2025, [https://www.cloudwego.io/docs/eino/](https://www.cloudwego.io/docs/eino/)  
17. jieliu2000/anyi: A Golang autonomous AI agent framework ... \- GitHub, acessado em junho 27, 2025, [https://github.com/jieliu2000/anyi](https://github.com/jieliu2000/anyi)  
18. py-obsidianmd \- PyPI, acessado em junho 27, 2025, [https://pypi.org/project/py-obsidianmd/](https://pypi.org/project/py-obsidianmd/)  
19. selimrbd/py-obsidianmd: Python interface to your Obsidian notes \- GitHub, acessado em junho 27, 2025, [https://github.com/selimrbd/py-obsidianmd](https://github.com/selimrbd/py-obsidianmd)  
20. acessado em dezembro 31, 1969, [https://github.com/matheussrod/pyobsidian](https://github.com/matheussrod/pyobsidian)  
21. mathe00/obsidian-plugin-python-bridge \- GitHub, acessado em junho 27, 2025, [https://github.com/mathe00/obsidian-plugin-python-bridge](https://github.com/mathe00/obsidian-plugin-python-bridge)  
22. urschrei/pyzotero: Pyzotero: a Python client for the Zotero API \- GitHub, acessado em junho 27, 2025, [https://github.com/urschrei/pyzotero](https://github.com/urschrei/pyzotero)  
23. Description — Pyzotero 1.6.12.dev12+g8141d57 documentation, acessado em junho 27, 2025, [https://pyzotero.readthedocs.io/](https://pyzotero.readthedocs.io/)  
24. Index — Pyzotero 1.6.11 documentation \- Read the Docs, acessado em junho 27, 2025, [https://pyzotero.readthedocs.io/en/stable/genindex.html](https://pyzotero.readthedocs.io/en/stable/genindex.html)  
25. Obsidian RAG Plugin \- Thomas Auriel \- GitLab, acessado em junho 27, 2025, [https://gitlab.com/ThomasAuriel/obsidian-rag-plugin](https://gitlab.com/ThomasAuriel/obsidian-rag-plugin)  
26. Retrieval Augmented Generation \- mrd-external-brain \- Obsidian Publish, acessado em junho 27, 2025, [https://publish.obsidian.md/mrd-brain/Knowledge+Base/Artificial+Intelligence/Retrieval+Augmented+Generation](https://publish.obsidian.md/mrd-brain/Knowledge+Base/Artificial+Intelligence/Retrieval+Augmented+Generation)  
27. Talking to your second brain: Build a Flowise RAG to chat with your Obsidian Vault \- Medium, acessado em junho 27, 2025, [https://medium.com/@martk/talking-to-your-second-brain-build-a-flowise-rag-to-chat-with-your-obsidian-vault-00645106e73b](https://medium.com/@martk/talking-to-your-second-brain-build-a-flowise-rag-to-chat-with-your-obsidian-vault-00645106e73b)  
28. Building RAG Applications with Ollama and Python: Complete 2025 Tutorial \- Collabnix, acessado em junho 27, 2025, [https://collabnix.com/building-rag-applications-with-ollama-and-python-complete-2025-tutorial/](https://collabnix.com/building-rag-applications-with-ollama-and-python-complete-2025-tutorial/)  
29. Run a fully local AI Search / RAG pipeline using llama:3.2 with Ollama using 4GB of memory and no GPU : r/LocalLLaMA \- Reddit, acessado em junho 27, 2025, [https://www.reddit.com/r/LocalLLaMA/comments/1i916on/run\_a\_fully\_local\_ai\_search\_rag\_pipeline\_using/](https://www.reddit.com/r/LocalLLaMA/comments/1i916on/run_a_fully_local_ai_search_rag_pipeline_using/)  
30. End To End RAG Agent With DeepSeek-R1 And Ollama: A Technical Deep Dive \- Collabnix, acessado em junho 27, 2025, [https://collabnix.com/end-to-end-rag-agent-with-deepseek-r1-and-ollama-a-technical-deep-dive/](https://collabnix.com/end-to-end-rag-agent-with-deepseek-r1-and-ollama-a-technical-deep-dive/)  
31. Run a fully local AI Search / RAG pipeline using Ollama with 4GB of memory and no GPU, acessado em junho 27, 2025, [https://www.reddit.com/r/LLMDevs/comments/1i8aqxj/run\_a\_fully\_local\_ai\_search\_rag\_pipeline\_using/](https://www.reddit.com/r/LLMDevs/comments/1i8aqxj/run_a_fully_local_ai_search_rag_pipeline_using/)  
32. AI Agents XI : OpenAI Agents SDK with Ollama | by DhanushKumar \- Medium, acessado em junho 27, 2025, [https://medium.com/@danushidk507/openai-agents-sdk-with-ollama-fc85da11755d](https://medium.com/@danushidk507/openai-agents-sdk-with-ollama-fc85da11755d)  
33. Open-Source Vector Search Engines (Self-Hostable) \- Benchmark Six Sigma, acessado em junho 27, 2025, [https://www.benchmarksixsigma.com/forum/topic/40325-open-source-vector-search-engines-self-hostable/?do=findComment\&comment=61532](https://www.benchmarksixsigma.com/forum/topic/40325-open-source-vector-search-engines-self-hostable/?do=findComment&comment=61532)  
34. Top 10 open source vector databases \- NetApp Instaclustr, acessado em junho 27, 2025, [https://www.instaclustr.com/education/vector-database/top-10-open-source-vector-databases/](https://www.instaclustr.com/education/vector-database/top-10-open-source-vector-databases/)  
35. chroma-core/chroma: the AI-native open-source ... \- GitHub, acessado em junho 27, 2025, [https://github.com/chroma-core/chroma](https://github.com/chroma-core/chroma)  
36. Chroma DB Vs Qdrant \- Key Differences \- Airbyte, acessado em junho 27, 2025, [https://airbyte.com/data-engineering-resources/chroma-db-vs-qdrant](https://airbyte.com/data-engineering-resources/chroma-db-vs-qdrant)  
37. Qdrant vs Chroma \- Zilliz, acessado em junho 27, 2025, [https://zilliz.com/comparison/qdrant-vs-chroma](https://zilliz.com/comparison/qdrant-vs-chroma)  
38. qdrant/qdrant: Qdrant \- High-performance, massive-scale ... \- GitHub, acessado em junho 27, 2025, [https://github.com/qdrant/qdrant](https://github.com/qdrant/qdrant)  
39. Milvus | High-Performance Vector Database Built for Scale, acessado em junho 27, 2025, [https://milvus.io/](https://milvus.io/)  
40. gRPC vs REST \- Difference Between Application Designs \- AWS, acessado em junho 27, 2025, [https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/](https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/)  
41. gRPC vs. REST \- IBM, acessado em junho 27, 2025, [https://www.ibm.com/think/topics/grpc-vs-rest](https://www.ibm.com/think/topics/grpc-vs-rest)  
42. REST or gRPC? A Guide to Efficient API Design | Zuplo Blog, acessado em junho 27, 2025, [https://zuplo.com/blog/2025/03/24/rest-or-grpc-guide](https://zuplo.com/blog/2025/03/24/rest-or-grpc-guide)  
43. Rabbitmq vs NATS | Svix Resources, acessado em junho 27, 2025, [https://www.svix.com/resources/faq/rabbitmq-vs-nats/](https://www.svix.com/resources/faq/rabbitmq-vs-nats/)  
44. Comparison of NATS, RabbitMQ, NSQ, and Kafka \- Gcore, acessado em junho 27, 2025, [https://gcore.com/learning/nats-rabbitmq-nsq-kafka-comparison](https://gcore.com/learning/nats-rabbitmq-nsq-kafka-comparison)  
45. NATS vs Apache Kafka vs RabbitMQ: Messaging Showdown | sanj.dev, acessado em junho 27, 2025, [https://sanj.dev/post/nats-kafka-rabbitmq-messaging-comparison](https://sanj.dev/post/nats-kafka-rabbitmq-messaging-comparison)  
46. NATS Docs: Welcome, acessado em junho 27, 2025, [https://docs.nats.io/](https://docs.nats.io/)  
47. NATS and Docker \- NATS Docs, acessado em junho 27, 2025, [https://docs.nats.io/running-a-nats-service/nats\_docker](https://docs.nats.io/running-a-nats-service/nats_docker)  
48. Understanding the Role of Environment Variables in Docker Compose \- LabEx, acessado em junho 27, 2025, [https://labex.io/tutorials/docker-understanding-the-role-of-environment-variables-in-docker-compose-398444](https://labex.io/tutorials/docker-understanding-the-role-of-environment-variables-in-docker-compose-398444)  
49. Set environment variables \- Docker Docs, acessado em junho 27, 2025, [https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/)  
50. Set, use, and manage variables in a Compose file with interpolation \- Docker Docs, acessado em junho 27, 2025, [https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)  
51. Managing Secrets in Docker Compose — A Developer's Guide | Phase Blog, acessado em junho 27, 2025, [https://phase.dev/blog/docker-compose-secrets/](https://phase.dev/blog/docker-compose-secrets/)  
52. Docker Secrets Management: Essential Practices for Container Security \- DEV Community, acessado em junho 27, 2025, [https://dev.to/rajeshgheware/docker-secrets-management-essential-practices-for-container-security-5efp](https://dev.to/rajeshgheware/docker-secrets-management-essential-practices-for-container-security-5efp)  
53. Secrets in Compose | Docker Docs, acessado em junho 27, 2025, [https://docs.docker.com/compose/how-tos/use-secrets/](https://docs.docker.com/compose/how-tos/use-secrets/)