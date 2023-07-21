# teste-rox

Este é um teste da Rox Partner que pede uma infraestrutura na nuvem para engenharia/análise de dados de uma empresa fictícia que produz bicicletas. O teste pede habilidades de Engenharia de Dados para otimizar o processo. Os seguintes itens são solicitados:

1.	Fazer a modelagem conceitual dos dados;
2.	Criação da infraestrutura necessária;
3.	Criação de todos os artefatos necessários para carregar os arquivos para o banco criado;
4.	Desenvolvimento de SCRIPT para análise de dados;
5.	(opcional) Criar um relatório em qualquer ferramenta de visualização de dados.

Foi utilizada a plataforma AWS para criar a infraestrutura necessária pois creio oferecer a melhor solução para a atividade promovida, além de já possuir experiência e certificação Solutions Architect na plataforma. Foram utilizadas as seguintes ferramentas da AWS:

- RDS: Será utilizada uma ferramenta de RDBMS (Sistema de gerenciamento de base de dados relacionais) pois atende melhor à proposta. O banco de dados escolhido foi o MySQL 8.0.33, Single-AZ, db.t3.micro com 20GB de armazenamento General Purpose SSD (gp3), backup automático e acesso com IP público, mantendo nossa arquitetura no free-tier. Os dados apresentados não possuem um tamanho considerável então não precisamos de uma base de dados robusta em processamento para atender a situação.
- S3: Será criado um bucket para armazenar os [arquivos](https://github.com/leorickli/teste_rox/tree/main/arquivos_csv) fornecidos para o teste.
- Lambda: Utilizaremos Lambda para executarmos triggers para as ações de PUT no S3.
- Pandas: Será utilizado apenas para EDA (Análise Exploratória de Dados) básica.

Foi feita uma pequena EDA nos arquivos .csv fornecidos para contextualização dos dados fornecidos e para analisasr se há a necessidade de uma limpeza prévia nos mesmos.

--- INSERIR OS DADOS AQUI

Não foi encontrada a necessidade de limpeza ou problemas com relação à governança de dados. 

### Fazer a modelagem conceitual dos dados

De acordo com a topologia enviada juntamente com a documentação do teste, as databases foram divididas entre "Person", "Production" e "Sales". A modelagem foi feita da seguinte maneira:

1. Person
   - Person
2. Production
   - Product
3. Sales
   - Customer
   - SalesOrderDetail
   - SalesOrderHeader
   - SpecialOfferProduct

Analisando os arquivos .csv, encontramos as colunas, primary e foreign keys das tabelas. Foi feito um [script Python](https://github.com/leorickli/teste-rox/blob/main/criar_tabelas.py) para a conexão com a base de dados MySQL dentro da RDS para podermos executar as queries [neste repositório](https://github.com/leorickli/teste-rox/tree/main/arquivos_sql). Para um schema mais leve, foi contada a quantidade de caracteres por coluna para termos datatypes mais eficiente, reduzindo o número de bytes por coluna e aumentando a performance das queries e armazenamento. Interessante observar que a arquitetura oferecida pelo cliente mostra situações de primary key composta nas tabelas "sales.specialOrderProduct" e "sales.salesOrderDetail". Uma primary key composta permite identificar exclusivamente um registro com base na combinação de valores em várias colunas. Isso é útil quando nenhuma coluna única pode identificar exclusivamente as linhas, mas sim a combinação de várias colunas. Importante notar que, para que o script Python seja executado localmente em sua máquina, é necessário atualizarmos as inbound rules do security group alocado para a instância RDS, selecionando a porta 3306 (MySQL) e inserindo o IP de sua máquina. Não é boa prática utilizar o IP "0.0.0.0/0" pois ele é muito genérico, reduzindo a segurança em sua instância. Far-se-á também necessária a criação de um IP público no momento de criação da instância.

O ERD abaixo mostra a relação entre as tabelas:

--- INSERIR ERD

Foi feito um outro [script Python](https://github.com/leorickli/teste-rox/blob/main/upload_s3.py) para fazer o upload da layer utilizada para o trigger Lambda e dos [arquivos .csv](https://github.com/leorickli/teste-rox/tree/main/arquivos_csv) fornecidos para o teste.

Uma função Lambda é invocada através deste [script Python] cada vez que um arquivo é enviado para o bucket S3. Desta forma, toda a vez que um arquivo inserido no bucket, ele irá automaticamente alimentar a nossa base de dados no RDS.




