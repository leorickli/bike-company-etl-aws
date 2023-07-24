# teste-rox

--- INSERIR DIAGRAMA DA ARQUITETURA

Este é um teste da Rox Partner que pede uma infraestrutura na nuvem para engenharia/análise de dados de uma empresa fictícia que produz bicicletas. O teste pede habilidades de Engenharia de Dados para otimizar o processo. Os seguintes itens são solicitados:

1.	Fazer a modelagem conceitual dos dados;
2.	Criação da infraestrutura necessária;
3.	Criação de todos os artefatos necessários para carregar os arquivos para o banco criado;
4.	Desenvolvimento de SCRIPT para análise de dados;
5.	(opcional) Criar um relatório em qualquer ferramenta de visualização de dados.

Foi utilizada a plataforma AWS para criar a infraestrutura necessária pois creio oferecer a melhor solução para a atividade promovida, além de já possuir experiência e certificação Solutions Architect na plataforma. Foram utilizadas as seguintes ferramentas da AWS e outras:

- RDS: Será utilizada uma ferramenta de RDBMS (Sistema de gerenciamento de base de dados relacionais) pois atende melhor à proposta. O banco de dados escolhido foi o MySQL 8.0.33, Single-AZ, db.t3.micro com 20GB de armazenamento General Purpose SSD (gp3), backup automático e acesso com IP público, mantendo nossa arquitetura no free-tier. Os dados apresentados não possuem um tamanho considerável então não precisamos de uma base de dados robusta em processamento para atender a situação.
- S3: Será criado um bucket para armazenar os [arquivos limpos](https://github.com/leorickli/teste-rox/tree/main/arquivos_limpos) fornecidos para o teste.
- Lambda: Utilizaremos Lambda para executarmos triggers para as ações de PUT no S3.
- IAM: Será usada para darmos roles à função Lambda para que tenhamos acesso às ferramentas S3, CloudWatch e RDS.
- CloudWatch: Será usada para verificarmos logs da nossa função Lambda, para verificar o progresso da mesma. É aqui que iremos verificar se os triggers realmente estão funcionando, após a etapa de testes dentro da própria Lambda.
- Excel: Usado apenas para análise preliminar de dados com um pouco de EDA (Análise Exploratória de Dados).
- Pandas: Será utilizado para data cleaning dos arquivos fornecidos no teste.
- Lucidchart: Usado para fazer o diagrama da arquitetura utilizada neste teste.
- DBeaver: Usado para criar a base de dados on-premises para testes e para verificar a ingestão dos arquivos no RDS.
- Tableau: Usado para visualização de dados.

### Data Cleaning

---

### Data Modeling

De acordo com a topologia enviada juntamente com a documentação do teste, a database ficou da seguinte maneira:

- testeRox
   - Customer
   - Person
   - Product
   - SalesOrderDetail
   - SalesOrderHeader
   - SpecialOfferProduct

Analisando os arquivos .csv, encontramos as colunas, primary e foreign keys das tabelas. Foi feito um [script Python](https://github.com/leorickli/teste-rox/blob/main/criar_tabelas.py) para a conexão com a base de dados MySQL dentro da RDS para podermos executar as queries [nesta pasta de arquivos SQL](https://github.com/leorickli/teste-rox/tree/main/arquivos_sql). Estas queries servem para criarmos o schema dentro da base de dados MySQL. Importante notar que, para que o script Python seja executado localmente em sua máquina, é necessário atualizarmos as inbound rules do security group alocado para a instância RDS, selecionando a porta 3306 (MySQL) e inserindo o IP de sua máquina. Não é boa prática utilizar o IP "0.0.0.0/0" pois ele é muito genérico, reduzindo a segurança em sua instância. Far-se-á também necessária a criação de um IP público no momento de criação da instância.

O ERD abaixo mostra a relação entre as entidades (tabelas):

<img width="892" alt="Screenshot 2023-07-22 at 10 04 32" src="https://github.com/leorickli/teste-rox/assets/106999054/67ffc189-f23e-414f-b8d1-8766214e370c">

Foi necessário uma atenção especial aos dadatypes de certas colunas, principalmente nas colunas em que há datas. Um caso especial é na tabela Person, nela encontramos as colunas "AdditionalContactInfo" e "Demographics", foi necessário colocar a datatype longtext por serem longas linhas de texto em formato xml.

Foi feito um outro [script Python](https://github.com/leorickli/teste-rox/blob/main/upload_s3.py) para fazer o upload dos [arquivos .csv](https://github.com/leorickli/teste-rox/tree/main/arquivos_limpos) já limpos através de Data Cleaning.

Uma função Lambda é invocada através deste [script Python](https://github.com/leorickli/teste-rox/blob/main/funcao_lambda.py) cada vez que um arquivo é enviado para o bucket S3. Desta forma, toda a vez que um arquivo é inserido no bucket, ele irá automaticamente alimentar a nossa base de dados no RDS.


### Análise de Dados

Com base na solução implantada responda aos seguintes questionamentos:

1.	Escreva uma query que retorna a quantidade de linhas na tabela Sales.SalesOrderDetail pelo campo SalesOrderID, desde que tenham pelo menos três linhas de detalhes.

```
SELECT 
	SalesOrderID as id, 
	COUNT(*) AS qtd 
FROM testeRox.SalesOrderDetail as sod
GROUP BY SalesOrderID
HAVING qtd >= 3
```

2.	Escreva uma query que ligue as tabelas Sales.SalesOrderDetail, Sales.SpecialOfferProduct e Production.Product e retorne os 3 produtos (Name) mais vendidos (pela soma de OrderQty), agrupados pelo número de dias para manufatura (DaysToManufacture).

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

3.	Escreva uma query ligando as tabelas Person.Person, Sales.Customer e Sales.SalesOrderHeader de forma a obter uma lista de nomes de clientes e uma contagem de pedidos efetuados.

```
SELECT c.CustomerID AS id,
       CONCAT(p.FirstName, ' ', p.LastName) AS nome, 
       COUNT(*) AS qtd
FROM testeRox.SalesOrderHeader soh
JOIN testeRox.Customer c ON soh.CustomerID = c.CustomerID
JOIN testeRox.Person p ON c.PersonID = p.BusinessEntityID 
GROUP BY c.CustomerID, p.FirstName, p.LastName
ORDER BY qtd DESC;
```

4.	Escreva uma query usando as tabelas Sales.SalesOrderHeader, Sales.SalesOrderDetail e Production.Product, de forma a obter a soma total de produtos (OrderQty) por ProductID e OrderDate.

```
SELECT 
    sod.ProductID AS id, 
    p.Name AS name,
    SUM(OrderQty) OVER(PARTITION BY sod.ProductID) AS qtd_id,
    CAST(soh.OrderDate AS DATE) AS data_pedido,  
    SUM(OrderQty) OVER(PARTITION BY CAST(soh.OrderDate AS DATE)) AS soma_produtos
FROM testeRox.SalesOrderDetail sod
JOIN testeRox.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID 
JOIN testeRox.Product p ON sod.ProductID = p.ProductID 
ORDER BY soh.OrderDate, sod.ProductID;
```

5.	Escreva uma query mostrando os campos SalesOrderID, OrderDate e TotalDue da tabela Sales.SalesOrderHeader. Obtenha apenas as linhas onde a ordem tenha sido feita durante o mês de setembro/2011 e o total devido esteja acima de 1.000. Ordene pelo total devido decrescente.
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

### Visualização de Dados

### Outras Arquiteturas

