
#### Common Table Expression

A Common Table Expression (CTE) in SQL is a named temporary result set that exists only within the execution scope of a single SQL statement. Here are some important points to note about CTEs:

CTEs can be thought of as alternatives to derived tables, inline views, or subqueries.

They can be used in SELECT, INSERT, UPDATE, or DELETE statements.

CTEs help to simplify complex queries, particularly those involving multiple subqueries or recursive queries.

They make your query more readable and easier to maintain.

A CTE is defined using the WITH keyword, followed by the CTE name and a query. The CTE can then be referred to by its name elsewhere in the query.

Here's a basic example of a CTE:
	WITH sales_cte AS (
	SELECT sales_person, SUM(sales_amount) as total_sales
	FROM sales_table
	GROUP BY sales_person
	)
	SELECT sales_person, total_sales
	FROM sales_cte
	WHERE total_sales > 1000;

Recursive CTE: 

This is a CTE that references itself. In other words, the CTE query definition refers back to the CTE name, creating a loop that ends when a certain condition is met. Recursive CTEs are useful for working with hierarchical or tree-structured data.


![DDL](recursive.svg)

Example: 

	WITH RECURSIVE number_sequence AS (
	SELECT 1 AS number
	UNION ALL
	SELECT number + 1
	FROM number_sequence
	WHERE number < 10
	)
	SELECT * FROM number_sequence;