# (Nome do sistema)

## Índice

- **Nome da aplicação:** (Nome do sistema)
- **Integrantes do grupo:**
  - Jhuan Carlos Sabaini Dassie
  - Rafaella Maciel Pereira Leite
  - Vitor Gabriel Firmino
- [**Descrição do projeto**](#descrição-do-projeto)
- **Tecnologias utilizadas:**
  - Django
  - SQLite/PostgreSQL
  - Bootstrap
  - Tema Customizado do Admin como Jazzmin ou Unfold
- [**Instruções para instalação**](#instruções-para-instalação)
- [**Instruções para execução**](#como-executar)
- [**Principais funcionalidades**](#principais-funcionalidades)
- [**Estrutura do projeto**](#estrutura-do-projeto)

## Descrição do projeto

O **(Nome do sistema)** é uma plataforma web para gestão de eventos e venda de ingressos. O sistema funciona como ponte tecnológica, um SaaS (Software as a Service) onde vendedores da plataforma comercializam a solução para produtoras de eventos. O sistema gerencia todo o ciclo de vida do evento, desde a sua criação pelos coordenadores da produtora, a configuração e venda de ingressos para os participantes, até a validação das entradas no dia do evento pelos organizadores.

## Instruções para instalação

### Execução com Docker Compose

1. Copie `.env.example` para `.env` e altere `SECRET_KEY` para um valor
   exclusivo em ambientes não locais.
2. Construa e inicie a aplicação:

   ```bash
   docker compose up --build -d
   ```

3. Acesse <http://localhost:8000/>. As migrações são executadas
   automaticamente antes do servidor iniciar.

O banco SQLite é persistido no volume Docker `sqlite_data`. Para parar os
serviços, execute `docker compose down`; para remover também os dados,
execute `docker compose down -v`.

## Como executar

## Principais funcionalidades

O sistema foi projetado com divisão de permissões e módulos focados em atender tanto a administração da plataforma quanto o público final.

### Autenticação e Controle de Acesso**

- **Sistema de Contas:** Cadastro de novos usuários (participantes), login e logout de contas na plataforma.
- **Perfis de Usuário:** Controle de permissões de acesso baseado nos papéis de Administrador, Vendedor, Coordenador, Organizador (Staff) e Participante.
- **Painel Administrativo Customizado:** Área restrita para gestão global da plataforma, utilizando tema personalizado para melhor usabilidade.

### Gestão da Plataforma (SaaS)

- **Gestão de Produtoras:** Funcionalidade exclusiva para Vendedores e Administradores cadastrarem novas produtoras de eventos.
- **Gestão de Coordenadores:** Vínculo de usuários coordenadores às suas respectivas produtoras autorizadas.

### Produção de Eventos (Área do Coordenador)**

- **CRUD de Eventos:** Cadastro, consulta, edição e exclusão de eventos da produtora.
- **Gestão de Ingressos e Lotes:** Criação e configuração de diferentes tipos de ingressos, preços e capacidade para cada evento.
- **Alocação de Staff:** Designação de Organizadores específicos para trabalharem na validação de ingressos de um determinado evento.

### Área do Participante (Usuário Final)**

- **Catálogo de Eventos:** Vitrine pública para visualização dos eventos disponíveis e detalhes das atrações.
- **Compra de Ingressos:** Fluxo de seleção de ingressos e geração de pedido/ticket único para o usuário.
- **Carteira Digital:** Área logada do participante para visualizar e acessar todos os ingressos adquiridos.

### Validação na Portaria (Área do Organizador)**

- **Lista de Presença:** Visualização dos ingressos vendidos e participantes esperados para o evento em que o staff está alocado.
- **Check-in de Ingressos:** Validação individual (baixa) dos tickets na porta do evento, com bloqueio automático contra uso duplicado.

### Perfis de usuário e controle de acesso

- **Administrador (ADM):** Possui acesso total ao sistema através do painel administrativo (Django Admin personalizado). Pode gerenciar todos os usuários, produtoras, eventos e vendas.
- **Vendedor da Plataforma:** Acessa o painel administrativo com permissões limitadas. Sua função é cadastrar e gerenciar as **Produtoras** e os **Coordenadores** que adquiriram a solução.
- **Coordenador (Produtora):** Acessa a área restrita da aplicação web. É responsável pelo CRUD (cadastro, leitura, edição e exclusão) de **Eventos** e **Ingressos**. Também cadastra os **Organizadores** que trabalharão no dia do evento.

- **Organizador (Staff):** Acessa a aplicação web no dia do evento. Sua única permissão é visualizar a lista de ingressos vendidos para o seu evento e validar (dar "baixa" ou "check-in") na entrada do participante.
- **Participante (Usuário Final):** Acessa a área pública e a área de cliente da aplicação. Pode visualizar eventos disponíveis, realizar o próprio cadastro, comprar ingressos e visualizar sua carteira de ingressos adquiridos.

### Regras de negócio principais

1. **Hierarquia de Criação:** Um evento só pode existir se estiver vinculado a uma Produtora e criado por um Coordenador.
2. **Vínculo de Staff:** Organizadores só podem validar ingressos de eventos para os quais foram explicitamente designados pelo Coordenador.
3. **Compra de Ingressos:** Um participante pode comprar múltiplos ingressos, mas cada ingresso deve gerar um ticket único (com um identificador ou QR Code simples) para validação individual na porta.
4. **Validação:** Um ingresso só pode ser validado uma única vez. Uma vez que o Organizador marca o ticket como "utilizado", o sistema deve bloquear novas tentativas de entrada.

## Estrutura do projeto

### Divisão de plicativos

- **`accounts` (ou `users`): Gestão de Identidade e Perfis:** focado exclusivamente no requisito de autenticação e perfis distintos.

  - Gerencia o modelo de Usuário Customizado (Custom User) e o login/logout.
  - Contém os perfis (Participante, Organizador, Coordenador, Vendedor) e a qual Produtora um usuário pertence.

- **`events` (Gestão de Catálogo e Produção):**
  - Focado no CRUD de entidades do negócio.
  - É o domínio do Coordenador.
  - Contém os modelos de **Evento** (nome, data, local, descrição) e os **Tipos de Ingressos/Lotes** (Pista Lote 1 - R$ 50, Camarote VIP - R$ 100).
  - Contém a relação de quais Organizadores (staff) estão alocados para trabalhar em qual Evento.

- **`tickets` (ou `checkout` / `sales`): Motor de Vendas e Validação**
  - É aqui que o Participante e o Organizador interagem com o sistema.
  - Contém o modelo de **Pedido/Venda** (transação do comprador).
  - Contém o modelo do **Ingresso Gerado** (o ticket individual único do participante, vinculado a um Tipo de Ingresso do app `events`).
  - Gerencia a lógica de validação na porta (o check-in feito pelo Organizador mudando o status do ingresso para "utilizado").

Essa abordagem de 3 apps atende com folga a exigência técnica de possuir pelo menos dois aplicativos, evita que o código vire uma "salada" e demonstra para o professor que o grupo compreendeu o conceito de separação de responsabilidades (cada app cuida de uma parte do fluxo de dados, independente de quem está logado).
