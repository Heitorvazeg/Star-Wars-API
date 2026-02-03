# 🌌 Star Wars Data Hub API - PowerOfData Challenge

## 📝 Descrição do Projeto
Esta API foi desenvolvida como parte do desafio técnico para a **PowerOfData**. O objetivo é fornecer uma plataforma robusta para entusiastas da saga Star Wars explorarem dados sobre personagens, planetas, naves e filmes, consumindo a [SWAPI (The Star Wars API)](https://swapi.dev/).

A solução foi projetada para ser mais do que um simples proxy; ela adiciona camadas de inteligência como **filtros avançados por atributos**, **ordenação dinâmica de tipos mistos** e um sistema de **cache resiliente** para otimizar a performance em ambiente Serverless.

---

## 🛠️ Tecnologias e Ferramentas
* **Linguagem:** Python 3.11+
* **Framework:** FastAPI (Alta performance assíncrona e validação rigorosa com Pydantic).
* **Infraestrutura (GCP):**
    * **Cloud Functions:** Processamento serverless orientado a eventos/HTTP.
    * **API Gateway:** Gerenciamento de segurança, cotas e exposição de endpoints.
* **Bibliotecas Principais:**
    * `HTTPX`: Cliente HTTP assíncrono para comunicação não-bloqueante.
    * `Pydantic`: Definição de Schemas e validação automática de tipos.
    * `Pytest`: Suite de testes unitários.

---

## 🏗️ Arquitetura e Design de Software
A aplicação segue os princípios da **Clean Architecture**, garantindo que a lógica de negócio seja independente de frameworks externos.



1.  **Controller Layer (FastAPI Routes):** Gerencia as definições de rota e utiliza o `Depends()` para injeção de dependência e validação de Query Parameters.
2.  **Service Layer (Business Logic):** Camada onde ocorre a "mágica". Filtra os dados que a SWAPI não provê nativamente e realiza a ordenação lógica.
3.  **Client Layer (Infrastructure):** Abstração do cliente HTTP para garantir que mudanças na API externa impactem o mínimo possível o resto do sistema.
4.  **Cache Layer:** Implementação de cache *in-memory* com TTL, essencial para reduzir a latência de rede e custos de saída de dados (egress).

---

## 🚀 Funcionalidades Principais

### 1. Endpoint Dinâmico de Recursos
`GET /starwars/{resource}`
Suporta: `people`, `planets`, `starships` e `films`.

### 2. Mecanismo de Filtro Avançado
Diferente da API original que possui apenas busca textual básica, esta implementação permite filtrar por aspectos específicos
*Exemplo:* `/starwars/people?gender=female&eye_color=blue`

### 3. Ordenação Dinâmica (Sort)
Implementação de ordenação personalizada via parâmetro `sort_by`.

### 4. Cache com Chaves Compostas
As chaves do cache são geradas através do hash dos parâmetros da query, garantindo que diferentes combinações de filtros sejam cacheadas de forma isolada e precisa.

---

## 🧪 Como Executar os Testes
Para garantir a integridade da lógica de filtros e ordenação:

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar testes
pytest