# Assignment 1 notes

### Installing and Using Postgres 13
Install with homebrew
`brew install postgres@13`
Check to see if other postgres services are running
`brew services list`
Stop other versions of postgres that are running (if any) replacing 12 with the version number listed
`brew servies stop postgres@12`
Start the version of postgres that you would like to connec to replacing 13 with the version you want to run
`brew services start postgres@13`
Export the executable to the $PATH variable so that it will use the correct version
`export PATH="/usr/local/opt/postgresql@13/bin:$PATH"`
To do the initial login use this command. "-d" is the flag to specify the database
`psql -d postgres`

### Navigating Within Psql
List users with: `\du`

: `CREATE ROLE saleco_user;`

Grant superuser (generally not a good practice, but for this assignment it's fine): `ALTER ROLE saleco_user WITH SUPERUSER;`
Grant login (not available by default): `ALTER ROLE saleco_user WITH LOGIN;`
Grant SELECT, INSERT, UPDATE, DELETE: `GRANT ALL PRIVILEGES ON DATABASE <database> TO <user>;`

### Assignment Questions
How many invoices are there?
`SELECT COUNT(*) FROM invoice;`
```
 count
-------
     8
```

List the invoice numbers and invoice dates
`SELECT inv_number, inv_date FROM invoice`
```
 inv_number |  inv_date
------------+------------
       1001 | 2016-01-16
       1002 | 2016-01-16
       1003 | 2016-01-16
       1004 | 2016-01-17
       1005 | 2016-01-17
       1006 | 2016-01-17
       1007 | 2016-01-17
       1008 | 2016-01-17
```

How many customers are there?
`SELECT COUNT(*) FROM customer;`
```
 count
-------
    10
```

`SELECT cus_code, CONCAT(cus_fname, ' ', cus_initial, '. ', cus_lname) as cus_name FROM customer;`
```
 cus_code |     cus_name
----------+-------------------
    10010 | Alfred A. Ramas
    10011 | Leona K. Dunne
    10012 | Kathy W. Smith
    10013 | Paul F. Olowski
    10014 | Myron . Orlando
    10015 | Amy B. O'Brian
    10016 | James G. Brown
    10017 | George . Williams
    10018 | Anne G. Farriss
    10019 | Olette K. Smith
```

`SELECT v_code, v_name FROM vendor;`
```
 v_code |     v_name
--------+-----------------
  21225 | Bryson, Inc.
  21226 | Superloo, Inc.
  21231 | D&E Supply
  21344 | Gomez Bros.
  22567 | Dome Supply
  23119 | Randsets Ltd.
  24004 | Brackman Bros.
  24288 | ORDVA, Inc.
  25443 | B&K, Inc.
  25501 | Damal Supplies
  25595 | Rubicon Systems
```

`SELECT v_state, COUNT(*) FROM vendor GROUP BY v_state;`
```
 v_state | count
---------+-------
 TN      |     5
 FL      |     3
 KY      |     1
 GA      |     2
```

`SELECT p_code, p_descript FROM product ORDER BY p_price LIMIT 1;`
```
  p_code  |         p_descript
----------+-----------------------------
 54778-2T | Rat-tail file, 1/8-in. fine
```

This is not correct :(
`SELECT line_units FROM product JOIN line ON product.p_code = line.p_code ORDER BY p_price LIMIT 1;`
```
 line_units
------------
       2.00
```

`SELECT p_qoh FROM product ORDER BY p_price LIMIT 1`
```
 p_qoh
-------
    43
```

`SELECT p_description, p_qoh, p_price FROM product WHERE p_discount > 0.05;`
```
             p_descript              | p_qoh | p_price
-------------------------------------+-------+---------
 Claw hammer                         |    23 |    9.95
 Steel matting, 4'x8'x1/6", .5" mesh |    18 |  119.95
```

`SELECT v_name, p_code, p_descript FROM product JOIN vendor ON vendor.v_code = product.v_code ORDER BY v_name, p_code;`
```
     v_name      |  p_code  |             p_descript
-----------------+----------+-------------------------------------
 Bryson, Inc.    | 11QER/31 | Power painter, 15 psi., 3-nozzle
 Bryson, Inc.    | 13-Q2/P2 | 7.25-in. pwr. saw blade
 Bryson, Inc.    | 23109-HB | Claw hammer
 Bryson, Inc.    | SM-18277 | 1.25-in. metal screw, 25
 D&E Supply      | SW-23116 | 2.5-in. wd. screw, 50
 Gomez Bros.     | 14-Q1/L3 | 9.00-in. pwr. saw blade
 Gomez Bros.     | 54778-2T | Rat-tail file, 1/8-in. fine
 ORDVA, Inc.     | 2232/QTY | B&D jigsaw, 12-in. blade
 ORDVA, Inc.     | 2232/QWE | B&D jigsaw, 8-in. blade
 ORDVA, Inc.     | 89-WRE-Q | Hicut chain saw, 16 in.
 Randsets Ltd.   | 1546-QQ2 | Hrd. cloth, 1/4-in., 2x50
 Randsets Ltd.   | 1558-QW1 | Hrd. cloth, 1/2-in., 3x50
 Rubicon Systems | 2238/QPD | B&D cordless drill, 1/2-in.
 Rubicon Systems | WR3/TT3  | Steel matting, 4'x8'x1/6", .5" mesh
```

`SELECT v_name AS vendor_name, ROUND(AVG(p_discount), 2) AS average_discount FROM product JOIN vendor ON vendor.v_code = product.v_code GROUP BY v_name;`
```
   vendor_name   | average_discount
-----------------+------------------
 Bryson, Inc.    |             0.04
 Gomez Bros.     |             0.00
 Randsets Ltd.   |             0.00
 D&E Supply      |             0.00
 ORDVA, Inc.     |             0.05
 Rubicon Systems |             0.08
```

`SELECT v_name AS vendor, p_descript AS product, p_qoh AS products_on_hand FROM product JOIN vendor ON product.v_code = vendor.v_code ORDER BY p_qoh DESC LIMIT 1;`
```
   vendor   |        product        | products_on_hand
------------+-----------------------+------------------
 D&E Supply | 2.5-in. wd. screw, 50 |              237
```

`SELECT v_name, SUM(p_qoh) AS total_qoh FROM product JOIN vendor ON product.v_code = vendor.v_code GROUP BY v_name ORDER BY total_qoh DESC LIMIT 1;`
```
   v_name   | total_qoh
------------+-----------
 D&E Supply |       237
 ```

```
SELECT customer.cus_code,
       line.inv_number,
       invoice.inv_date,
       line.line_number,
       line.p_code,
       line.line_units,
       line.line_price,
       CONCAT(customer.cus_fname, ' ', CASE WHEN customer.cus_initial IS NOT NULL THEN CONCAT(customer.cus_initial, '. ') ELSE '' END, customer.cus_lname) AS customer_name,
       ROUND((line_units * line_price), 2) AS Subtotal
FROM line
JOIN invoice ON line.inv_number = invoice.inv_number
JOIN customer ON invoice.cus_code = customer.cus_code
ORDER BY customer.cus_code, invoice.inv_number, line.line_number;
```
```
 cus_code | inv_number |  inv_date  | line_number |  p_code  | line_units | line_price |  customer_name  | subtotal
----------+------------+------------+-------------+----------+------------+------------+-----------------+----------
    10011 |       1002 | 2016-01-16 |           1 | 54778-2T |       2.00 |       4.99 | Leona K. Dunne  |     9.98
    10011 |       1004 | 2016-01-17 |           1 | 54778-2T |       3.00 |       4.99 | Leona K. Dunne  |    14.97
    10011 |       1004 | 2016-01-17 |           2 | 23109-HB |       2.00 |       9.95 | Leona K. Dunne  |    19.90
    10011 |       1008 | 2016-01-17 |           1 | PVC23DRT |       5.00 |       5.87 | Leona K. Dunne  |    29.35
    10011 |       1008 | 2016-01-17 |           2 | WR3/TT3  |       3.00 |     119.95 | Leona K. Dunne  |   359.85
    10011 |       1008 | 2016-01-17 |           3 | 23109-HB |       1.00 |       9.95 | Leona K. Dunne  |     9.95
    10012 |       1003 | 2016-01-16 |           1 | 2238/QPD |       1.00 |      38.95 | Kathy W. Smith  |    38.95
    10012 |       1003 | 2016-01-16 |           2 | 1546-QQ2 |       1.00 |      39.95 | Kathy W. Smith  |    39.95
    10012 |       1003 | 2016-01-16 |           3 | 13-Q2/P2 |       5.00 |      14.99 | Kathy W. Smith  |    74.95
    10014 |       1001 | 2016-01-16 |           1 | 13-Q2/P2 |       1.00 |      14.99 | Myron Orlando   |    14.99
    10014 |       1001 | 2016-01-16 |           2 | 23109-HB |       1.00 |       9.95 | Myron Orlando   |     9.95
    10014 |       1006 | 2016-01-17 |           1 | SM-18277 |       3.00 |       6.99 | Myron Orlando   |    20.97
    10014 |       1006 | 2016-01-17 |           2 | 2232/QTY |       1.00 |     109.92 | Myron Orlando   |   109.92
    10014 |       1006 | 2016-01-17 |           3 | 23109-HB |       1.00 |       9.95 | Myron Orlando   |     9.95
    10014 |       1006 | 2016-01-17 |           4 | 89-WRE-Q |       1.00 |     256.99 | Myron Orlando   |   256.99
    10015 |       1007 | 2016-01-17 |           1 | 13-Q2/P2 |       2.00 |      14.99 | Amy B. O'Brian  |    29.98
    10015 |       1007 | 2016-01-17 |           2 | 54778-2T |       1.00 |       4.99 | Amy B. O'Brian  |     4.99
    10018 |       1005 | 2016-01-17 |           1 | PVC23DRT |      12.00 |       5.87 | Anne G. Farriss |    70.44
```

```
SELECT CONCAT(customer.cus_fname, ' ', CASE WHEN customer.cus_initial IS NOT NULL THEN CONCAT(customer.cus_initial, '. ') ELSE '' END, customer.cus_lname) AS customer_name,
       ROUND(SUM(line.line_units * line.line_price), 2) AS total_amount_spent
FROM invoice
JOIN line ON invoice.inv_number = line.inv_number
JOIN customer ON invoice.cus_code = customer.cus_code
GROUP BY customer.cus_code, customer_name
ORDER BY customer.cus_code;
```
```
  customer_name  | total_amount_spent
-----------------+--------------------
 Leona K. Dunne  |             444.00
 Kathy W. Smith  |             153.85
 Myron Orlando   |             422.77
 Amy B. O'Brian  |              34.97
 Anne G. Farriss |              70.44
```

```
SELECT customer.cus_code,
       CONCAT(customer.cus_fname, ' ', CASE WHEN customer.cus_initial IS NOT NULL THEN CONCAT(customer.cus_initial, '. ') ELSE '' END, customer.cus_lname) AS customer_name
FROM customer
LEFT JOIN invoice ON invoice.cus_code = customer.cus_code
WHERE invoice.cus_code IS NULL
ORDER BY customer.cus_code;
```
```
 cus_code |  customer_name
----------+-----------------
    10010 | Alfred A. Ramas
    10013 | Paul F. Olowski
    10016 | James G. Brown
    10017 | George Williams
    10019 | Olette K. Smith
```

`SELECT SUM(p_price * p_qoh) AS total_value FROM product;`
```
 total_value
-------------
    15084.52
```
