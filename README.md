# teste_rox

Este é um teste da Rox Partner que pede uma infraestrutura na nuvem para engenharia/análise de dados de uma empresa fictícia que produz bicicletas. O teste pede habilidades de Engenharia de Dados para otimizar o processo. Os seguintes itens são solicitados:

1.	Fazer a modelagem conceitual dos dados;
2.	Criação da infraestrutura necessária;
3.	Criação de todos os artefatos necessários para carregar os arquivos para o banco criado;
4.	Desenvolvimento de SCRIPT para análise de dados;
5.	(opcional) Criar um relatório em qualquer ferramenta de visualização de dados.

Foi utilizada a plataforma AWS para criar a infraestrutura necessária pois creio oferecer a melhor solução para a atividade promovida, além de já possuir experiência e certificação Solutions Architect na plataforma. Foram utilizadas as seguintes ferramentas da AWS:

- RDS: Será utilizada uma ferramenta de RDBMS (Sistema de gerenciamento de base de dados relacionais) pois atende melhor à proposta. O banco de dados escolhido foi o MySQL 8.0.33, Single-AZ, db.t2.micro com 20GB de armazenamento General Purpose SSD (gp3) e backup automático, mantendo nossa arquitetura no free-tier. Os dados apresentados não possuem um tamanho considerável então não precisamos de uma base de dados robusta em processamento para atender a situação.
- S3: Será criado um bucket 
- Lambda: 

