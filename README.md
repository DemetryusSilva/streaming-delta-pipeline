# Real-Time Clickstream Pipeline with Delta Lake 🚀

Este projeto demonstra um pipeline de engenharia de dados ponta a ponta para processar eventos de cliques (logs) em tempo real usando a arquitetura de Lakehouse.

## 🛠 Tecnologias
- **Linguagem:** Python (PySpark)
- **Processamento:** Spark Structured Streaming
- **Storage:** Delta Lake (ACID Transactions)
- **Infra:** Docker

## 📈 O que este projeto faz?
1. **Geração de Dados:** Um script Python simula cliques de usuários em um e-commerce.
2. **Streaming:** O Spark monitora a chegada de novos arquivos e os processa instantaneamente.
3. **Agregação:** O pipeline calcula a contagem de eventos por janela de tempo (Windowing).
4. **Persistência:** Os dados são salvos em formato **Delta**, permitindo auditoria e versionamento (Time Travel).

## 🚀 Como rodar
1. Suba o container: `docker-compose up -d`
2. Instale as dependências: `pip install -r requirements.txt`
3. Inicie o gerador: `python app/generator.py`
4. Em outro terminal, inicie o pipeline: `python app/pipeline.py`

## 📊 Estrutura Delta
Os dados são salvos em `data/delta/`, onde você pode consultar as tabelas Bronze (Raw) e Gold (Aggregated).
