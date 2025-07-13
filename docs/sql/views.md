
#### Views

A view in SQL is a virtual table based on the result-set of an SQL statement. It contains rows and columns, just like a real table. The fields in a view are fields from one or more real tables in the database.

Here are some key points about views:

1. You can add SQL functions, WHERE, and JOIN statements to a view and display the data as if the data were coming from one single table.
2. A view always shows up-to-date data. The database engine recreates the data every time a user queries a view.
3. Views can be used to encapsulate complex queries, presenting users with a simpler interface
to the data.
4. They can be used to restrict access to sensitive data in the underlying tables, presenting only non-sensitive data to users.


![DDL](views.svg)

	CREATE VIEW View_Products AS SELECT ProductName, Price FROM Products
	WHERE Price > 30;