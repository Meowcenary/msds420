**1.1 How many invoices are there?**

```
SELECT COUNT(*) FROM invoice;
```

```
 count
-------
    8
```

**1.2 List the invoice numbers and the invoice dates**

```
SELECT inv_number, inv_date FROM invoice
```

```
 inv_number |    inv_date
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

**2.1 How many customers are there?**

```
SELECT COUNT(*) FROM customer;
```

```
 count
-------
    10
```

**2.2 List the customer codes and customer names.**

I didn't realize until later on in the assignment that some of the customers did not have middle initials, but didn't think it was a big deal to just leave the "." character for the single customer with the odd formatting. In later questions I used a conditional to remove the ".", but it resulted in a difficult to format query for the PDF and I didn't want to repeat that here.

```
SELECT cus_code, CONCAT(cus_fname, ' ', cus_initial, '. ', cus_lname) as cus_name FROM customer;
```

```
 cus_code |          cus_name
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

**3.1 List vendor numbers and vendor names**

`SELECT v_code, v_name FROM vendor;`

```
 v_code | v_name
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

**3.2 Show the vendor count per state**

`SELECT v_state, COUNT(*) FROM vendor GROUP BY v_state;`

```
 v_state | count
---------+-------
     TN  |  5
     FL  |  3
     KY  |  1
     GA  |  2
```

**4.1 Based on price, what is the most expensive product?**

```
SELECT p_code, p_descript FROM product ORDER BY p_price LIMIT 1;
```

```
p_code    | p_descript
----------+-----------------------------
 54778-2T | Rat-tail file, 1/8-in. fine
```

**4.2 How much quantity on hand is available for the most expensive product?**

`SELECT p_qoh FROM product ORDER BY p_price LIMIT 1`

```
 p_qoh
-------
        43
```

**5. Display the product description, quantity on hand, and price for all products that have a discount greater than 5%**

```
SELECT p_description, p_qoh, p_price FROM product WHERE p_discount > 0.05;
```

```
         p_descript                  | p_qoh | p_price
-------------------------------------+-------+---------
 Claw hammer                         |    23 |  9.95
 Steel matting, 4'x8'x1/6", .5" mesh |    18 |  119.95
```

**6. Generate a listing of products offered by each vendor. List vendor name, product code and product name. Sort by vendor name and product code**

```
SELECT v_name, p_code, p_descript FROM product JOIN vendor ON vendor.v_code = product.v_code ORDER BY v_name, p_code;
```

```
     v_name      |  p_code  |      p_descript
-----------------+----------+-------------------------------------
 Bryson, Inc.    | 11QER/31 | Power painter, 15 psi., 3-nozzle
 Bryson, Inc.    | 13-Q2/P2 | 7.25-in. pwr. saw blade
 Bryson, Inc.    | 23109-HB | Claw hammer
 Bryson, Inc.    | SM-18277 | 1.25-in. metal screw, 25
 D&E Supply      | SW-23116 | 2.5-in. wd. screw, 50
 Gomez Bros.     | 14-Q1/L3 | 9.00-in. pwr. saw blade
 Gomez Bros.     | 54778-2T | Rat-tail file, 1/8-in. fine
 ORDVA, Inc.     | 2232/QTY | B&D jigsaw, 12-in. blade
 ORDVA, Inc.     | 2232/QWE | B&D jigsaw, 8-in. blade
 ORDVA, Inc.     | 89-WRE-Q | Hicut chain saw, 16 in.
 Randsets Ltd.   | 1546-QQ2 | Hrd. cloth, 1/4-in., 2x50
 Randsets Ltd.   | 1558-QW1 | Hrd. cloth, 1/2-in., 3x50
 Rubicon Systems | 2238/QPD | B&D cordless drill, 1/2-in.
 Rubicon Systems | WR3/TT3  | Steel matting, 4'x8'x1/6", .5" mesh
```

**7. What is the average discount (rounded to the nearest cent) given by each vendor?**

```
SELECT v_name AS vendor_name,
ROUND(AVG(p_discount), 2) AS average_discount
FROM product
JOIN vendor
ON vendor.v_code = product.v_code GROUP BY v_name;
```

```
     vendor_name | average_discount
-----------------+------------------
 Bryson, Inc.    |     0.04
 Gomez Bros.     |     0.00
 Randsets Ltd.   |     0.00
 D&E Supply      |     0.00
 ORDVA, Inc.     |     0.05
 Rubicon Systems |     0.08
```

**8.1 What is the vendor with most "products on hand" for a particular product?**

```
SELECT v_name AS vendor,
p_descript AS product,
p_qoh AS products_on_hand
FROM product
JOIN vendor ON product.v_code = vendor.v_code
ORDER BY p_qoh DESC
LIMIT 1;
````

```
vendor      |     product           | products_on_hand
------------+-----------------------+------------------
 D&E Supply | 2.5-in. wd. screw, 50 |   237
```

**8.2 What is the vendor with most "products on hand" for all its products combined? List both the vendor name and the number of products. Is it the same vendor in both cases?**

```
SELECT v_name, SUM(p_qoh) AS total_qoh
FROM product
JOIN vendor ON product.v_code = vendor.v_code
GROUP BY v_name
ORDER BY total_qoh DESC
LIMIT 1;
```

```
 v_name     | total_qoh
------------+-----------
 D&E Supply |  237
```

It is the same vendor in both cases.

**9. Generate a listing of customer purchases, including the subtotals for each of the invoice line numbers; sort output by customer code, invoice number and the line_number**

Sorry for the ugly output on this query. I had a really hard time formatting the results of this query for the PDF. It might be helpful to copy this out to a text editor.

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
cus_code | inv_number |   inv_date | line_number |    p_code| line_units | line_price |  customer_name  | subtotal
---------+------------+------------+-------------+----------+------------+------------+-----------------+----------
   10011 |       1002 | 2016-01-16 |           1 | 54778-2T |       2.00 |       4.99 | Leona K. Dunne  |      9.98
   10011 |       1004 | 2016-01-17 |           1 | 54778-2T |       3.00 |       4.99 | Leona K. Dunne  |     14.97
   10011 |       1004 | 2016-01-17 |           2 | 23109-HB |       2.00 |       9.95 | Leona K. Dunne  |     19.90
   10011 |       1008 | 2016-01-17 |           1 | PVC23DRT |       5.00 |       5.87 | Leona K. Dunne  |     29.35
   10011 |       1008 | 2016-01-17 |           2 | WR3/TT3  |       3.00 |     119.95 | Leona K. Dunne  |    359.85
   10011 |       1008 | 2016-01-17 |           3 | 23109-HB |       1.00 |       9.95 | Leona K. Dunne  |      9.95
   10012 |       1003 | 2016-01-16 |           1 | 2238/QPD |       1.00 |      38.95 | Kathy W. Smith  |     38.95
   10012 |       1003 | 2016-01-16 |           2 | 1546-QQ2 |       1.00 |      39.95 | Kathy W. Smith  |     39.95
   10012 |       1003 | 2016-01-16 |           3 | 13-Q2/P2 |       5.00 |      14.99 | Kathy W. Smith  |     74.95
   10014 |       1001 | 2016-01-16 |           1 | 13-Q2/P2 |       1.00 |      14.99 | Myron Orlando   |     14.99
   10014 |       1001 | 2016-01-16 |           2 | 23109-HB |       1.00 |       9.95 | Myron Orlando   |      9.95
   10014 |       1006 | 2016-01-17 |           1 | SM-18277 |       3.00 |       6.99 | Myron Orlando   |     20.97
   10014 |       1006 | 2016-01-17 |           2 | 2232/QTY |       1.00 |     109.92 | Myron Orlando   |    109.92
   10014 |       1006 | 2016-01-17 |           3 | 23109-HB |       1.00 |       9.95 | Myron Orlando   |      9.95
   10014 |       1006 | 2016-01-17 |           4 | 89-WRE-Q |       1.00 |     256.99 | Myron Orlando   |    256.99
   10015 |       1007 | 2016-01-17 |           1 | 13-Q2/P2 |       2.00 |      14.99 | Amy B. O'Brian  |     29.98
   10015 |       1007 | 2016-01-17 |           2 | 54778-2T |       1.00 |       4.99 | Amy B. O'Brian  |      4.99
   10018 |       1005 | 2016-01-17 |           1 | PVC23DRT |      12.00 |       5.87 | Anne G. Farriss |     70.44
```

**10. List the total amount spent by each customer who made purchases during the current invoice cycle—that is, for the customers who appear in the INVOICE table; sort by customer code**

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
customer_name   | total_amount_spent
----------------+--------------------
Leona K. Dunne  |  444.00
Kathy W. Smith  |  153.85
Myron Orlando   |  422.77
Amy B. O'Brian  |  34.97
Anne G. Farriss |  70.44
```

**11. Find a listing of customers who did not make purchases during the invoicing period; sort by customer code**

```
SELECT customer.cus_code,
  CONCAT(customer.cus_fname, ' ', CASE WHEN customer.cus_initial IS NOT NULL THEN CONCAT(customer.cus_initial, '. ') ELSE '' END, customer.cus_lname) AS customer_name
FROM customer
LEFT JOIN invoice ON invoice.cus_code = customer.cus_code
WHERE invoice.cus_code IS NULL
ORDER BY customer.cus_code;
```

```
 cus_code |    customer_name
----------+-----------------
    10010 | Alfred A. Ramas
    10013 | Paul F. Olowski
    10016 | James G. Brown
    10017 | George Williams
    10019 | Olette K. Smith
```

**12. Create a query to produce a summary of the value of products currently in inventory**

```
SELECT SUM(p_price * p_qoh) AS total_value FROM product;
```

```
 total_value
-------------
    15084.52
```
