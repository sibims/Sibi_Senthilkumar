CREATE DATABASE Organisation;
USE Organisation;

CREATE TABLE Employee (empID INT NOT NULL UNIQUE, empName VARCHAR(20), email VARCHAR(40), mobile VARCHAR(10), doj Date, projectID INT, departmentID INT, managerName VARCHAR(25), salary INT);
DROP TABLE Employee;
INSERT INTO Employee (empID, empName, email, mobile, doj, projectID, departmentID, managerName, salary) 
VALUES (1220, 'Nandha Kumar', 'nandha.kumar@aspiresys.com', '9676456671', '2019-03-02', 145, 576, 'Anushya', 57000);

INSERT INTO Employee (empID, empName, email, mobile, doj, projectID, departmentID, managerName, salary) 
VALUES (1223, 'Vignesh Kannan', 'vignesh.kannan@aspiresys.com', '9689452189', '2019-03-05', 147, 544, 'Silpa', 48000),
(1221, 'James Kumar', 'james.kumar@aspiresys.com', '9656677641', '2019-03-02', 168, 573, 'Savitha', 45000),
(1226, 'Naveen Raj', 'naveen.raj@aspiresys.com', '9342674892', '2019-03-08', 156, 574, 'Saraswathi', 46000),
(1224, 'Nandha Krishnan', 'nandha.krishnan@aspiresys.com', '9656764675', '2019-03-03', 142, 547, 'Sabapathi', 48000),
(1222, 'Kishore Kanth', 'kishore.kanth@aspiresys.com', '9645666771', '2019-03-07', 168, 573, 'Savitha', 45000),
(1225, 'Krish Naveen', 'krish.naveen@aspiresys.com', '9676716456', '2019-03-07', 156, 574, 'Saraswathi', 46000),
(1235, 'Arvind Kishore', 'arvind.kishore@aspiresys.com', '9676471566', '2019-03-09', 149, 564, 'Naveen', 43000),
(1228, 'Priyanka Mohan', 'priya.mohan@aspiresys.com', '9696764571', '2019-03-11', 156, 574, 'Saraswathi', 53000),
(1227, 'Padma Priya', 'padma.priya@aspiresys.com', '9676156674', '2019-03-02', 142, 547, 'Sabapathi', 50000),
(1229, 'Sai Pallavi', 'sai.pallavi@aspiresys.com', '9645667671', '2019-03-02', 149, 564, 'Naveen', 53000),
(1231, 'Jayam Ravi', 'jayam.ravi@aspiresys.com', '9676456671', '2019-03-02', 168, 573, 'Savitha', 51000),
(1230, 'Priya Anand', 'priya.anand@aspiresys.com', '9672415671', '2019-03-02', 147, 544, 'Silpa', 49000),
(1233, 'Prema Priya', 'prema.priya@aspiresys.com', '9676457166', '2019-03-02', 149, 564, 'Naveen', 46000),
(1234, 'Trisha Krishnan', 'trisha.krishnan@aspiresys.com', '9676451287', '2019-03-02', 149, 564, 'Naveen', 53000),
(1236, 'Nandhini Priya', 'nandhini.priya@aspiresys.com', '7250914628', '2019-03-02', 142, 547, 'Sabapathi', 58000);

-- 1. Write a query to display all rows and columns from the employees table.
SELECT * FROM Employee;

-- 2. Retrieve only the name and salary of all employees from the employees table.
SELECT empName, salary FROM Employee;

-- 3. Write a query to find all employees whose salary is greater than 50,000.
SELECT * FROM Employee WHERE SALARY > 50000;

-- 4. List all employees who joined the company in the year 2020.