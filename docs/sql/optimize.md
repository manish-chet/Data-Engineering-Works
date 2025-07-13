#### Query Optimizations 

1. Use Column Names Instead of * in a SELECT Statement

Avoid including a HAVING clause in SELECT statements

The HAVING clause is used to filter the rows after all the rows are selected and it is used like a filter. It is quite useless in a SELECT statement. It works by going through the final result table of the query parsing out the rows that don’t meet the HAVING condition.

Example:

	Original query:
	SELECT s.cust_id,count(s.cust_id)
	FROM SH.sales s
	GROUP BY s.cust_id
	HAVING s.cust_id != '1660' AND s.cust_id != '2';

	Improved query:
	SELECT s.cust_id,count(cust_id)
	FROM SH.sales s
	WHERE s.cust_id != '1660'
	AND s.cust_id !='2'
	GROUP BY s.cust_id;


3. Eliminate Unnecessary DISTINCT Conditions

Considering the case of the following example, the DISTINCT keyword in the original query is unnecessary because the table_name contains the primary key p.ID, which is part of the result set.

Example:

	Original query:
	SELECT DISTINCT * FROM SH.sales s
	JOIN SH.customers c
	ON s.cust_id= c.cust_id
	WHERE c.cust_marital_status = 'single';
	
	Improved query:
	SELECT * FROM SH.sales s JOIN
	SH.customers c
	ON s.cust_id = c.cust_id
	WHERE c.cust_marital_status='single';

4. Consider using an IN predicate when querying an indexed column

The IN-list predicate can be exploited for indexed retrieval and also, the optimizer can sort the IN-list to match the sort sequence of the index, leading to more efficient retrieval.
Example:

	Original query:
	SELECT s.*
	FROM SH.sales s
	WHERE s.prod_id = 14
	OR s.prod_id = 17;

	Improved query:
	SELECT s.*
	FROM SH.sales s
	WHERE s.prod_id IN (14, 17);

5. Try to use UNION ALL in place of UNION

The UNION ALL statement is faster than UNION, because UNION ALL statement does not consider duplicate s, and UNION statement does look for duplicates in a table while selection of rows, whether or not they exist.
Example:

	Original query:
	SELECT cust_id
	FROM SH.sales
	UNION
	SELECT cust_id
	FROM customers;

	Improved query:
	SELECT cust_id
	FROM SH.sales
	UNION ALL
	SELECT cust_id
	FROM customers;