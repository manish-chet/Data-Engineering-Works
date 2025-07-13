#### Functions

Functions in MySQL are reusable blocks of code that perform a specific task and return a single value.

Purpose: Simplify complex calculations, enhance code reusability, and improve query performance.

Types: Built-in Functions and User-Defined Functions (UDFs).

1. Built-in Functions

	a. String Functions (e.g., CONCAT, LENGTH, SUBSTRING)

	b. Numeric Functions (e.g., ABS, ROUND, CEIL)

	c. Date and Time Functions (e.g., NOW, DATE_FORMAT, DATEDIFF)
    
	d. Aggregate Functions (e.g., COUNT, SUM, AVG)

2. User-Defined Functions (UDFs) Custom functions created by users to perform specific operations. It is customizable,
reusable, and encapsulate complex logic.

					DELIMITER $$
					CREATE FUNCTION function_name(parameter(s))
					RETURNS data_type
					DETERMINISTIC
					BEGIN
					-- function body
					RETURN value;
					END $$
					DELIMITER ;
