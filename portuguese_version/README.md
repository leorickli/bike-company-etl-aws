# bike-company-etl-aws

<img width="1013" alt="Screenshot 2023-07-24 at 09 54 02" src="https://github.com/leorickli/teste-rox/assets/106999054/939b7226-5b37-4c87-b82f-39973cfdd023">

Este é um projeto que cria recursos AWS para engenharia/análise de dados de uma empresa fictícia que produz bicicletas. O teste pede habilidades de Engenharia de Dados para otimizar o processo. Os seguintes itens são solicitados:

1. Fazer a modelagem conceitual dos dados.
2. Criação da infraestrutura necessária.
3. Criação de todos os artefatos necessários para carregar os arquivos para o banco criado.
4. Desenvolvimento de SCRIPT para análise de dados.
5. (opcional) Criar um relatório em qualquer ferramenta de visualização de dados.

Foi utilizada a plataforma AWS para criar a infraestrutura necessária pois creio oferecer a melhor solução para a atividade promovida, além de já possuir experiência e certificação Solutions Architect na plataforma. Foram utilizadas as seguintes ferramentas da AWS e outras:

- **RDS:** Será utilizada uma ferramenta de RDBMS (Sistema de gerenciamento de base de dados relacionais) pois atende melhor à proposta. O banco de dados escolhido foi o MySQL 8.0.33, Single-AZ, db.t3.micro com 20GB de armazenamento General Purpose SSD (gp3), backup automático e acesso com IP público, mantendo nossa arquitetura no free-tier. Os dados apresentados não possuem um tamanho considerável então não precisamos de uma base de dados robusta em processamento para atender a situação.
- **S3:** Será criado um bucket para armazenar os [arquivos limpos](https://github.com/leorickli/teste-rox/tree/main/portuguese_version/arquivos_limpos) fornecidos para o teste.
- **Lambda:** Utilizaremos Lambda para executarmos triggers para as ações de PUT no S3.
- **IAM:** Será usada para darmos roles à função Lambda para que tenhamos acesso às ferramentas S3, CloudWatch e RDS.
- **CloudWatch:** Será usada para verificarmos logs da nossa função Lambda, para verificar o progresso da mesma. É aqui que iremos verificar se os triggers realmente estão funcionando após a etapa de testes dentro da própria Lambda.
- **QuickSight:** Usado para visualização de dados através de conexão feita na base de dados RDS.
- **Excel:** Usado apenas para análise preliminar de dados.
- **Pandas:** Será utilizado para data cleaning e EDA (Análise Exploratória de Dados) dos arquivos fornecidos no teste.
- **DBeaver:** Usado para criar a base de dados on-premises para testes, criar a ERD (Diagrama de Relação de Entidades) para Data Modeling e verificar a ingestão dos arquivos no RDS.
- **Lucidchart:** Usado para fazer o diagrama da arquitetura utilizada neste teste.

### Data Cleaning e EDA

Foi criado um ambiente on-premises de testes onde os dados foram inseridos em uma database MySQL para checar se a base de dados aceitaria ou não os dados apresentados da maneira como está. Muito [data cleaning e EDA](https://github.com/leorickli/teste-rox/tree/main/portuguese_version/cleaning_eda_notebooks) foi feito para vencer as constrições impostas pelo rígido schema da base de dados criada. Estes arquivos estão em formato .ipynb para podermos ver o progresso da exploraçao e limpeza dos dados. Alguns detalhes sobre a limpeza:

- Arquivos estavam com separadores ";", foram modificados para os tradicionais separadores ",".
- Colunas com data e hora foram devidamente alocadas para o formato DATETIME.
- Textos "null" (em qualquer variação de caixa alta ou baixa) foram retirados.
- Foi constadado que há grandes linhas de texto em algumas colunas da tabela "Person", alocando a coluna para o formato LONGTEXT.
- Houveram casos de primary keys com valores repetidos na tabela "SpecialOfferProduct", estas linhas foram retiradas.

### Data Modeling

Esta é a topologia inicial enviada no teste:

<img width="836" alt="Screenshot 2023-07-28 at 15 28 45" src="https://github.com/leorickli/rox-test/assets/106999054/5242b5dc-70fb-40b7-a13d-5ee866ea9c5d">

De acordo com a topologia enviada juntamente com a documentação do teste, a database ficou da seguinte maneira:

- testeRox
   - Customer
   - Person
   - Product
   - SalesOrderDetail
   - SalesOrderHeader
   - SpecialOfferProduct

Analisando os arquivos .csv, encontramos as colunas, primary e foreign keys das tabelas. Foi feito um [script Python](https://github.com/leorickli/teste-rox/blob/main/portuguese_version/criar_tabelas.py) para a conexão com a base de dados MySQL dentro da RDS para podermos executar as queries nesta pasta de [arquivos SQL](https://github.com/leorickli/teste-rox/tree/main/portuguese_version/arquivos_sql). Estas queries servem para criarmos o schema dentro da base de dados MySQL. Importante notar que, para que o script Python seja executado localmente em sua máquina, é necessário atualizarmos as inbound rules do security group alocado para a instância RDS, selecionando a porta 3306 (MySQL) e inserindo o IP de sua máquina. Não é boa prática utilizar o IP "0.0.0.0/0" pois ele é muito genérico, reduzindo a segurança em sua instância. Far-se-á também necessária a criação de um IP público no momento de criação da instância.

O ERD abaixo mostra a relação entre as entidades (tabelas):

<img width="892" alt="Screenshot 2023-07-22 at 10 04 32" src="https://github.com/leorickli/teste-rox/assets/106999054/67ffc189-f23e-414f-b8d1-8766214e370c">

Foi necessário uma atenção especial aos dadatypes de certas colunas, principalmente nas colunas em que há datas. Um caso especial é na tabela Person, nela encontramos as colunas "AdditionalContactInfo" e "Demographics", foi necessário colocar a datatype LONGTEXT por serem longas linhas de texto em formato xml.

### ETL

Foi feito um [script Python](https://github.com/leorickli/teste-rox/blob/main/portuguese_version/upload_s3.py) para fazer o upload dos [arquivos .csv](https://github.com/leorickli/teste-rox/tree/main/portuguese_version/arquivos_limpos) já limpos através de Data Cleaning.

Uma função Lambda é invocada através deste [script Python](https://github.com/leorickli/teste-rox/blob/main/portuguese_version/funcao_lambda.py) cada vez que um arquivo é enviado para o bucket S3. Desta forma, toda a vez que um arquivo é inserido no bucket, ele irá automaticamente alimentar a nossa base de dados no RDS. Também se fez necessário implementar uma [layer do MySQL](https://github.com/leorickli/teste-rox/blob/main/portuguese_version/mysql_layer.zip) com os pacotes necessários para transformar e carregar os arquivos .csv na base de dados RDS através da função Lambda. O timeout da função foi aumentado pois a primeira ETL não foi bem sucedida, ação esta recomendada para quando a função tende a processar uma grande variedade de arquivos, os três segundos que são designados de forma padrão através da plataforma normalmente não são suficientes para este tipo de transformação. É recomendado utilizar environment variables dentro da função Python para proteção de dados pessoais.

<img width="595" alt="Screenshot 2023-07-24 at 09 00 17" src="https://github.com/leorickli/teste-rox/assets/106999054/445149d3-a3bf-479d-b076-3db4251855e3">

Com as devidas permissões estabelecidas via IAM, é possível monitorar o processo de ETL feito pelo Lambda através dos logs do CloudWatch. Isto é ótimo para monitorar os testes iniciais e a ingestão final dos arquivos para a instância RDS após a etapa de testes.

<img width="1143" alt="Screenshot 2023-07-24 at 09 23 30" src="https://github.com/leorickli/teste-rox/assets/106999054/9a08edcb-2ea1-4ddc-9b39-0b623e0e4e92">

### Análise de Dados

Com base na solução implantada responda aos seguintes questionamentos:

1. Escreva uma query que retorna a quantidade de linhas na tabela Sales.SalesOrderDetail pelo campo SalesOrderID, desde que tenham pelo menos três linhas de detalhes.

```
SELECT 
	SalesOrderID as id, 
	COUNT(*) AS qtd 
FROM testeRox.SalesOrderDetail as sod
GROUP BY SalesOrderID
HAVING qtd >= 3
```

<img width="214" alt="Screenshot 2023-07-24 at 08 40 46" src="https://github.com/leorickli/teste-rox/assets/106999054/3e142ee6-a033-410b-a06b-2e3b49f037a4">


2. Escreva uma query que ligue as tabelas Sales.SalesOrderDetail, Sales.SpecialOfferProduct e Production.Product e retorne os 3 produtos (Name) mais vendidos (pela soma de OrderQty), agrupados pelo número de dias para manufatura (DaysToManufacture).

```
SELECT * 
FROM(
  SELECT 
  	ROW_NUMBER() OVER(PARTITION BY p.DaysToManufacture ORDER BY sum(sod.OrderQty) DESC) as pos,
  	p.DaysToManufacture AS dtm,
    	p.Name as nome,
    	SUM(sod.OrderQty) AS qtd
  FROM testeRox.SpecialOfferProduct sop 
  JOIN testeRox.Product p ON sop.ProductID = p.ProductID
  JOIN testeRox.SalesOrderDetail sod ON sop.SpecialOfferID = sod.SalesOrderDetailID
  GROUP BY nome, p.DaysToManufacture
  ) as posicao
WHERE pos <= 3
```

<img width="528" alt="Screenshot 2023-07-24 at 08 41 12" src="https://github.com/leorickli/teste-rox/assets/106999054/83f6bd43-ed68-4469-a20f-41b0b31799b1">

3. Escreva uma query ligando as tabelas Person.Person, Sales.Customer e Sales.SalesOrderHeader de forma a obter uma lista de nomes de clientes e uma contagem de pedidos efetuados.

```
SELECT
	c.CustomerID AS id,
	CONCAT(p.FirstName, ' ', p.LastName) AS nome, 
	COUNT(*) AS qtd
FROM testeRox.SalesOrderHeader soh
JOIN testeRox.Customer c ON soh.CustomerID = c.CustomerID
JOIN testeRox.Person p ON c.PersonID = p.BusinessEntityID 
GROUP BY c.CustomerID, p.FirstName, p.LastName
ORDER BY qtd DESC;
```

<img width="346" alt="Screenshot 2023-07-24 at 08 42 24" src="https://github.com/leorickli/teste-rox/assets/106999054/e5254176-ea58-490e-93e6-a3c06151801f">

4. Escreva uma query usando as tabelas Sales.SalesOrderHeader, Sales.SalesOrderDetail e Production.Product, de forma a obter a soma total de produtos (OrderQty) por ProductID e OrderDate.

```
SELECT
    sod.ProductID AS id,
    p.Name AS nome,
    SUM(sod.OrderQty) AS qtd,
    CAST(soh.OrderDate AS DATE) AS data_pedido
FROM testeRox.SalesOrderDetail sod
JOIN testeRox.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
JOIN testeRox.Product p ON sod.ProductID = p.ProductID
GROUP BY id, nome, data_pedido
ORDER BY data_pedido, qtd DESC;
```

<img width="527" alt="Screenshot 2023-07-26 at 11 45 35" src="https://github.com/leorickli/teste-rox/assets/106999054/8c1fbcd1-dc85-4fc5-bf18-00e8da569364">

5. Escreva uma query mostrando os campos SalesOrderID, OrderDate e TotalDue da tabela Sales.SalesOrderHeader. Obtenha apenas as linhas onde a ordem tenha sido feita durante o mês de setembro/2011 e o total devido esteja acima de 1.000. Ordene pelo total devido decrescente.
```
SELECT 
	SalesOrderID as id,
	CAST(OrderDate AS DATE) AS data, 
	TotalDue AS total_devido
FROM testeRox.SalesOrderHeader
WHERE OrderDate BETWEEN '2011-09-01' AND '2011-09-30' AND TotalDue > 1000
ORDER BY total_devido;
```
*Neste caso, a query não retornou resultados pois não há dados neste intervalo de tempo.*

<img width="362" alt="Screenshot 2023-07-24 at 08 44 47" src="https://github.com/leorickli/teste-rox/assets/106999054/e5ec5004-9ce2-4a83-ab5a-61d51649e492">

### Visualização de Dados

Utilizando a ferramenta AWS QuickSight e certificando-se que as devidas permissões sejam concedidas à IAM através de roles e alinhamento de VPCs, podemos utilizar a ferramenta para conectar-se ao RDS para geração de dashboards. Abaixo estão algumas visualizações.

<img width="760" alt="Screenshot 2023-07-24 at 10 45 08" src="https://github.com/leorickli/teste-rox/assets/106999054/f743d1d2-4db3-432c-98e1-d3cd3adb73a9">
<img width="777" alt="Screenshot 2023-07-24 at 10 49 45" src="https://github.com/leorickli/teste-rox/assets/106999054/acbc55d7-964b-48f5-9611-d50bc567d3f1">

### Outras Arquiteturas

Na concepção do projeto e no decorrer dos processos, surgiram algumas propostas de abordagens e arquiteturas diferentes que poderiam ser discutidas e/ou talvez abordadas futuramente. Seguem abaixo algumas destas abordagens:

1. No momento de testes de transferência de dados on-premisse para a base de dados MySQL na instância RDS, existe a possibilidade de transferência direta dos arquivos on-premises para a base de dados existente na nuvem. Esta medida não é viável pois a transferência dos dados é muito lenta, ela exige que exista um schema já estabelecido na base de dados e a arquitetura é pobre, inviabilizando automações e melhorias futuras.
2. Na documentação da AWS, foi sugerido o backup da base de dados on-premises utilizando a ferramenta XtraBackup da Percona. Esta medida pode ser viável em um evento de transferência direta da base de dados on-premises para a nuvem.
3. Após a concepção deste projeto, é possível criar um template na ferramenta CloudFormation para automatizarmos a criação do stack utilizado neste repositório.
4. É possível que a ingestão de dados dos objetos (arquivos .csv) dentro do S3 seja feita pela ferramenta AWS Glue para realização de ETL. Posteriormente estes dados tratados são enviados para AWS Athena para análise de dados. Athena é facilmente conectada ao Tableau para visualização de dados, além do QuickSight.
