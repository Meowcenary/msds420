**Q1: List the total sales by region and customer. Your output should be sorted by region name and customer code**

```
SELECT SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwcustomer.cus_code,
       dwregion.reg_name
FROM dwdaysalesfact
JOIN dwcustomer ON dwdaysalesfact.cus_code = dwcustomer.cus_code
JOIN dwregion ON dwcustomer.reg_id = dwregion.reg_id
GROUP BY dwcustomer.cus_code, dwregion.reg_name
ORDER BY dwregion.reg_name, dwcustomer.cus_code;
```

```
 total_sales | cus_code | reg_name
-------------+----------+----------
           5 |    10012 | NE
           8 |    10013 | NE
           6 |    10014 | NW
           1 |    10019 | NW
          22 |    10010 | SE
           4 |    10011 | SE
           6 |    10015 | SE
          14 |    10016 | SE
          10 |    10017 | SW
          16 |    10018 | SW
(10 rows)
```

**Q2: Repeat #1 but produce the output using ROLLUP with region name and customer code**

```
SELECT SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwcustomer.cus_code,
       dwregion.reg_name
FROM dwdaysalesfact
JOIN dwcustomer ON dwdaysalesfact.cus_code = dwcustomer.cus_code
JOIN dwregion ON dwcustomer.reg_id = dwregion.reg_id
GROUP BY ROLLUP (dwregion.reg_name, dwcustomer.cus_code)
ORDER BY dwregion.reg_name, dwcustomer.cus_code;
```

```
 total_sales | cus_code | reg_name
-------------+----------+----------
           5 |    10012 | NE
           8 |    10013 | NE
          13 |          | NE
           6 |    10014 | NW
           1 |    10019 | NW
           7 |          | NW
          22 |    10010 | SE
           4 |    10011 | SE
           6 |    10015 | SE
          14 |    10016 | SE
          46 |          | SE
          10 |    10017 | SW
          16 |    10018 | SW
          26 |          | SW
          92 |          |
(15 rows)
```

**Q3: Repeat #1 but product the output using CUBE with region name and customer code**

```
SELECT SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwcustomer.cus_code,
       dwregion.reg_name
FROM dwdaysalesfact
JOIN dwcustomer ON dwdaysalesfact.cus_code = dwcustomer.cus_code
JOIN dwregion ON dwcustomer.reg_id = dwregion.reg_id
GROUP BY CUBE (dwregion.reg_name, dwcustomer.cus_code)
ORDER BY dwregion.reg_name, dwcustomer.cus_code;
```

```
 total_sales | cus_code | reg_name
-------------+----------+----------
           5 |    10012 | NE
           8 |    10013 | NE
          13 |          | NE
           6 |    10014 | NW
           1 |    10019 | NW
           7 |          | NW
          22 |    10010 | SE
           4 |    10011 | SE
           6 |    10015 | SE
          14 |    10016 | SE
          46 |          | SE
          10 |    10017 | SW
          16 |    10018 | SW
          26 |          | SW
          22 |    10010 |
           4 |    10011 |
           5 |    10012 |
           8 |    10013 |
           6 |    10014 |
           6 |    10015 |
          14 |    10016 |
          10 |    10017 |
          16 |    10018 |
           1 |    10019 |
          92 |          |
(25 rows)
```

**Q4: a) Explain the additional information/intelligence gained when using ROLLUP or CUBE**

The ROLLUP function will provide an extra row that shows the total of the aggregrate function results of the grouping of
columns passed to it. In the example above, ROLLUP showed the total sales of all customers in a region and the total
sales for the region in an added row. The CUBE function will provide everything from that ROLLUP does and additionally
generates aggregrate function results for all combinations of the grouping of columns passed to it. In the example above
CUBE shows the totals for the regions as with ROLLUP and also includes rows for each of the customers individual total
sales and the total of all the customer sales.

**Q4: b) Use the output from questions 1, 2 and 3 to explain what the data reveals**
The total sales for all customers is 92, no customer buys outside of a single region, the Southeast is the region that
generates the most sales, the customer with id 10010 has the highest total sales of 22 and is in the Southeast region.

**Q5: List the total sales by customer code, month, and product code. Sort by customer code and month**

Added in product description to make it a little easier to read, but it could easily be omitted for a cleaner output

```
SELECT SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwcustomer.cus_code,
       dwproduct.p_code,
       dwproduct.p_descript,
       dwtime.tm_month
FROM dwdaysalesfact
JOIN dwcustomer ON dwdaysalesfact.cus_code = dwcustomer.cus_code
JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
GROUP BY dwcustomer.cus_code, dwtime.tm_month, dwproduct.p_code
ORDER BY dwcustomer.cus_code, dwtime.tm_month;
```

```
 total_sales | cus_code |  p_code  |             p_descript              | tm_month
-------------+----------+----------+-------------------------------------+----------
           5 |    10010 | 13-Q2/P2 | 7.25-in. pwr. saw blade             |       10
           2 |    10010 | 23109-HB | Claw hammer                         |       10
           3 |    10010 | 54778-2T | Rat-tail file, 1/8-in. fine         |       10
          12 |    10010 | PVC23DRT | PVC pipe, 3.5-in., 8-ft             |       10
           1 |    10011 | 2232/QTY | B\&D jigsaw, 12-in. blade           |       10
           3 |    10011 | SM-18277 | 1.25-in. metal screw, 25            |       10
           3 |    10012 | SM-18277 | 1.25-in. metal screw, 25            |        9
           1 |    10012 | 23109-HB | Claw hammer                         |       10
           1 |    10012 | 89-WRE-Q | Hicut chain saw, 16 in.             |       10
           2 |    10013 | 13-Q2/P2 | 7.25-in. pwr. saw blade             |       10
           1 |    10013 | 54778-2T | Rat-tail file, 1/8-in. fine         |       10
           5 |    10013 | PVC23DRT | PVC pipe, 3.5-in., 8-ft             |       10
           1 |    10014 | 13-Q2/P2 | 7.25-in. pwr. saw blade             |        9
           1 |    10014 | 2232/QTY | B\&D jigsaw, 12-in. blade           |        9
           1 |    10014 | 23109-HB | Claw hammer                         |        9
           3 |    10014 | WR3/TT3  | Steel matting, 4'x8'x1/6", .5" mesh |       10
           1 |    10015 | 2238/QPD | B\&D cordless drill, 1/2-in.        |        9
           1 |    10015 | 23109-HB | Claw hammer                         |        9
           2 |    10015 | 54778-2T | Rat-tail file, 1/8-in. fine         |        9
           1 |    10015 | 89-WRE-Q | Hicut chain saw, 16 in.             |        9
           1 |    10015 | 23109-HB | Claw hammer                         |       10
           7 |    10016 | 13-Q2/P2 | 7.25-in. pwr. saw blade             |        9
           1 |    10016 | 1546-QQ2 | Hrd. cloth, 1/4-in., 2x50           |        9
           1 |    10016 | 54778-2T | Rat-tail file, 1/8-in. fine         |        9
           5 |    10016 | PVC23DRT | PVC pipe, 3.5-in., 8-ft             |        9
           1 |    10017 | 13-Q2/P2 | 7.25-in. pwr. saw blade             |        9
           3 |    10017 | 23109-HB | Claw hammer                         |        9
           3 |    10017 | 54778-2T | Rat-tail file, 1/8-in. fine         |        9
           3 |    10017 | WR3/TT3  | Steel matting, 4'x8'x1/6", .5" mesh |        9
           1 |    10018 | 2238/QPD | B\&D cordless drill, 1/2-in.        |        9
           1 |    10018 | 23109-HB | Claw hammer                         |        9
           2 |    10018 | 54778-2T | Rat-tail file, 1/8-in. fine         |        9
          12 |    10018 | PVC23DRT | PVC pipe, 3.5-in., 8-ft             |        9
           1 |    10019 | 1546-QQ2 | Hrd. cloth, 1/4-in., 2x50           |        9
```

**Q6: Show all purchases (total sales) in September to show which customer bought the most product in September. Show
      customer code, customer name and total sales; sort all output by total sales with the highest sales on top**
```
SELECT dwcustomer.cus_code,
       CONCAT(dwcustomer.cus_fname, ' ',
              CASE WHEN dwcustomer.cus_initial IS NOT NULL
              THEN CONCAT(dwcustomer.cus_initial, '. ')
              ELSE ''
              END,
              dwcustomer.cus_lname) AS customer_name,
       SUM(dwdaysalesfact.sale_units) AS total_sales
FROM dwdaysalesfact
JOIN dwcustomer ON dwdaysalesfact.cus_code = dwcustomer.cus_code
JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
WHERE dwtime.tm_month = 9
GROUP BY dwcustomer.cus_code, dwtime.tm_month
ORDER BY total_sales DESC;
```

```
 cus_code |  customer_name  | total_sales
----------+-----------------+-------------
    10018 | Anne G. Farriss |          16
    10016 | James G. Brown  |          14
    10017 | George Williams |          10
    10015 | Amy B. O'Brian  |           5
    10012 | Kathy W. Smith  |           3
    10014 | Myron Orlando   |           3
    10019 | Olette K. Smith |           1
(7 rows)
```

**Q7: List the total sales by month and product category. Your output should be sorted by month and product category**

```
SELECT SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwtime.tm_month,
       dwproduct.p_category
FROM dwdaysalesfact
JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
GROUP BY dwtime.tm_month, dwproduct.p_category
ORDER BY dwtime.tm_month, dwproduct.p_category;
```

```
 total_sales | tm_month | p_category
-------------+----------+------------
          17 |        9 | CAT1
           4 |        9 | CAT2
          22 |        9 | CAT3
           9 |        9 | CAT4
          11 |       10 | CAT1
           2 |       10 | CAT2
          20 |       10 | CAT3
           7 |       10 | CAT4
(8 rows)
```

**Q8: List the number of product sales (number of rows) and total sales by month. Your output should be sorted by month
      and should show one row per month**

```
SELECT COUNT(dwdaysalesfact.sale_units) AS product_sales,
       SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwtime.tm_month
FROM dwdaysalesfact
JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
GROUP BY dwtime.tm_month
ORDER BY dwtime.tm_month;
```

```
 product_sales | total_sales | tm_month
---------------+-------------+----------
            23 |          52 |        9
            13 |          40 |       10
(2 rows)
```

**Q9: Show product category, product code, product description and units sold (sum). Which product is the best seller
      based on units sold?**

```
SELECT SUM(dwdaysalesfact.sale_units) AS units_sold,
       dwproduct.p_category AS category,
       dwproduct.p_code AS product_code,
       dwproduct.p_descript AS product_description
FROM dwdaysalesfact
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
GROUP BY dwproduct.p_code
ORDER BY units_sold DESC
LIMIT 1;
```

```
 units_sold | category | product_code |   product_description
------------+----------+--------------+-------------------------
         34 | CAT3     | PVC23DRT     | PVC pipe, 3.5-in., 8-ft
(1 row)
```

**Q9: a) Show units sold for September**

```
SELECT SUM(dwdaysalesfact.sale_units) AS units_sold,
       dwproduct.p_category AS category,
       dwproduct.p_code AS product_code,
       dwproduct.p_descript AS product_description
FROM dwdaysalesfact
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
WHERE dwtime.tm_month = 9
GROUP BY dwproduct.p_code
ORDER BY units_sold DESC;
```

```
 units_sold | category | product_code |         product_description
------------+----------+--------------+-------------------------------------
         17 | CAT3     | PVC23DRT     | PVC pipe, 3.5-in., 8-ft
          9 | CAT1     | 13-Q2/P2     | 7.25-in. pwr. saw blade
          8 | CAT1     | 54778-2T     | Rat-tail file, 1/8-in. fine
          6 | CAT4     | 23109-HB     | Claw hammer
          3 | CAT4     | SM-18277     | 1.25-in. metal screw, 25
          3 | CAT3     | WR3/TT3      | Steel matting, 4'x8'x1/6", .5" mesh
          2 | CAT3     | 2238/QPD     | B\&D cordless drill, 1/2-in.
          2 | CAT2     | 1546-QQ2     | Hrd. cloth, 1/4-in., 2x50
          1 | CAT2     | 89-WRE-Q     | Hicut chain saw, 16 in.
          1 | CAT2     | 2232/QTY     | B\&D jigsaw, 12-in. blade
(10 rows)
```

**Q9: b) Show units sold for October**

```
SELECT SUM(dwdaysalesfact.sale_units) AS units_sold,
       dwproduct.p_category AS category,
       dwproduct.p_code AS product_code,
       dwproduct.p_descript AS product_description
FROM dwdaysalesfact
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
WHERE dwtime.tm_month = 10
GROUP BY dwproduct.p_code
ORDER BY units_sold DESC;
```

```
 units_sold | category | product_code |         product_description
------------+----------+--------------+-------------------------------------
         17 | CAT3     | PVC23DRT     | PVC pipe, 3.5-in., 8-ft
          7 | CAT1     | 13-Q2/P2     | 7.25-in. pwr. saw blade
          4 | CAT4     | 23109-HB     | Claw hammer
          4 | CAT1     | 54778-2T     | Rat-tail file, 1/8-in. fine
          3 | CAT3     | WR3/TT3      | Steel matting, 4'x8'x1/6", .5" mesh
          3 | CAT4     | SM-18277     | 1.25-in. metal screw, 25
          1 | CAT2     | 2232/QTY     | B\&D jigsaw, 12-in. blade
          1 | CAT2     | 89-WRE-Q     | Hicut chain saw, 16 in.
(8 rows)
```

**Q10: List the number of product sales (number of rows) and total sales by month, product category, and product. Your
       output should be sorted by month, product category and product**

```
SELECT COUNT(dwdaysalesfact.sale_units) AS product_sales,
       SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwtime.tm_month AS month,
       dwproduct.p_category AS category,
       dwproduct.p_descript AS product
FROM dwdaysalesfact
JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
GROUP BY month, category, product
ORDER BY month, category, product;
```

```
 product_sales | total_sales | month | category |               product
---------------+-------------+-------+----------+-------------------------------------
             4 |           9 |     9 | CAT1     | 7.25-in. pwr. saw blade
             4 |           8 |     9 | CAT1     | Rat-tail file, 1/8-in. fine
             1 |           1 |     9 | CAT2     | B\&D jigsaw, 12-in. blade
             1 |           1 |     9 | CAT2     | Hicut chain saw, 16 in.
             2 |           2 |     9 | CAT2     | Hrd. cloth, 1/4-in., 2x50
             2 |           2 |     9 | CAT3     | B\&D cordless drill, 1/2-in.
             2 |          17 |     9 | CAT3     | PVC pipe, 3.5-in., 8-ft
             1 |           3 |     9 | CAT3     | Steel matting, 4'x8'x1/6", .5" mesh
             1 |           3 |     9 | CAT4     | 1.25-in. metal screw, 25
             5 |           6 |     9 | CAT4     | Claw hammer
             2 |           7 |    10 | CAT1     | 7.25-in. pwr. saw blade
             2 |           4 |    10 | CAT1     | Rat-tail file, 1/8-in. fine
             1 |           1 |    10 | CAT2     | B\&D jigsaw, 12-in. blade
             1 |           1 |    10 | CAT2     | Hicut chain saw, 16 in.
             2 |          17 |    10 | CAT3     | PVC pipe, 3.5-in., 8-ft
             1 |           3 |    10 | CAT3     | Steel matting, 4'x8'x1/6", .5" mesh
             1 |           3 |    10 | CAT4     | 1.25-in. metal screw, 25
             3 |           4 |    10 | CAT4     | Claw hammer
(18 rows)
```

**Q11: List the top 5 vendors based on the total sales of their products. Show both the vendors' names and the total
       sales of their product. Sort by total sales**

```
SELECT SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwvendor.v_name AS vendor_name
FROM dwdaysalesfact
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
JOIN dwvendor ON dwproduct.v_code = dwvendor.v_code
GROUP BY dwvendor.v_code
ORDER BY total_sales DESC;
```

```
 total_sales |   vendor_name
-------------+-----------------
          50 | Bryson, Inc.
          28 | Gomez Bros.
           8 | Rubicon Systems
           4 | ORDVA, Inc.
           2 | Randsets Ltd.
(5 rows)
```

Interestingly, the below query that substitutes `dwvendor.v_code` with `dwproduct.v_code` will throw an error.

```
SELECT SUM(dwdaysalesfact.sale_units) AS total_sales,
       dwvendor.v_name AS vendor_name
FROM dwdaysalesfact
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
JOIN dwvendor ON dwproduct.v_code = dwvendor.v_code
GROUP BY dwproduct.v_code
ORDER BY total_sales DESC;
```

```
ERROR:  column "dwvendor.v_name" must appear in the GROUP BY clause or be used in an aggregate function
LINE 2:        dwvendor.v_name AS vendor_name
```

**Q12: List the products that have not been sold in the year 2015. Show the product code, the product description, and
       the product category**

```
SELECT dwproduct.p_code AS product_code,
       dwproduct.p_descript AS product_description,
       dwproduct.p_category AS product_category
FROM dwproduct
LEFT JOIN dwdaysalesfact ON dwproduct.p_code = dwdaysalesfact.p_code
LEFT JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
WHERE dwdaysalesfact.p_code IS NULL
AND dwtime.tm_year != 2015 OR dwtime.tm_year IS NULL
ORDER BY dwproduct.p_category, dwproduct.p_code;
```

```
SELECT dwproduct.p_code AS product_code,
       dwproduct.p_descript AS product_description,
       dwproduct.p_category AS product_category
FROM dwdaysalesfact
JOIN dwtime ON dwdaysalesfact.tm_id = dwtime.tm_id
RIGHT JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
WHERE dwtime.tm_year != 2015 OR dwtime.tm_year IS NULL
ORDER BY dwproduct.p_category, dwproduct.p_code;
```

Both queries will produce this output
```
 product_code |       product_description        | product_category
--------------+----------------------------------+------------------
 11QER/31     | Power painter, 15 psi., 3-nozzle | CAT1
 14-Q1/L3     | 9.00-in. pwr. saw blade          | CAT1
 1558-QW1     | Hrd. cloth, 1/2-in., 3x50        | CAT2
 SW-23116     | 2.5-in. wd. screw, 50            | CAT2
 2232/QWE     | B\&D jigsaw, 8-in. blade         | CAT3
 23114-AA     | Sledge hammer, 12 lb.            | CAT4
(6 rows)
```

**Q13: Find the top-selling products in each region based on the number of units sold. Show the region names, product
       description sand total units sold. Order by region name and total units sold (from largest to smallest)**

This was the initial attempt, but it pulled more rows than I would like.
```
SELECT dwproduct.p_code AS product_code,
       dwproduct.p_descript AS product_description,
       dwregion.reg_name AS region_name,
       SUM(dwdaysalesfact.sale_units) AS units_sold
FROM dwdaysalesfact
JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
JOIN dwcustomer ON dwdaysalesfact.cus_code = dwcustomer.cus_code
JOIN dwregion ON dwcustomer.reg_id = dwregion.reg_id
GROUP BY dwregion.reg_id, dwproduct.p_code
ORDER BY units_sold DESC;
```

```
 product_code |         product_description         | region_name | units_sold
--------------+-------------------------------------+-------------+------------
 PVC23DRT     | PVC pipe, 3.5-in., 8-ft             | SE          |         17
 13-Q2/P2     | 7.25-in. pwr. saw blade             | SE          |         12
 PVC23DRT     | PVC pipe, 3.5-in., 8-ft             | SW          |         12
 54778-2T     | Rat-tail file, 1/8-in. fine         | SE          |          6
 54778-2T     | Rat-tail file, 1/8-in. fine         | SW          |          5
 PVC23DRT     | PVC pipe, 3.5-in., 8-ft             | NE          |          5
 23109-HB     | Claw hammer                         | SW          |          4
 23109-HB     | Claw hammer                         | SE          |          4
 SM-18277     | 1.25-in. metal screw, 25            | SE          |          3
 SM-18277     | 1.25-in. metal screw, 25            | NE          |          3
 WR3/TT3      | Steel matting, 4'x8'x1/6", .5" mesh | NW          |          3
 WR3/TT3      | Steel matting, 4'x8'x1/6", .5" mesh | SW          |          3
 13-Q2/P2     | 7.25-in. pwr. saw blade             | NE          |          2
 2232/QTY     | B\&D jigsaw, 12-in. blade           | SE          |          1
 2238/QPD     | B\&D cordless drill, 1/2-in.        | SE          |          1
 1546-QQ2     | Hrd. cloth, 1/4-in., 2x50           | SE          |          1
 23109-HB     | Claw hammer                         | NW          |          1
 89-WRE-Q     | Hicut chain saw, 16 in.             | SE          |          1
 2232/QTY     | B\&D jigsaw, 12-in. blade           | NW          |          1
 1546-QQ2     | Hrd. cloth, 1/4-in., 2x50           | NW          |          1
 13-Q2/P2     | 7.25-in. pwr. saw blade             | SW          |          1
 2238/QPD     | B\&D cordless drill, 1/2-in.        | SW          |          1
 13-Q2/P2     | 7.25-in. pwr. saw blade             | NW          |          1
 89-WRE-Q     | Hicut chain saw, 16 in.             | NE          |          1
 54778-2T     | Rat-tail file, 1/8-in. fine         | NE          |          1
 23109-HB     | Claw hammer                         | NE          |          1
```

I had a pretty hard time with this, but it seems like the proper approach is to use a subquery if you want to limit to
the top results only. In addition to the subquery, the ROW_NUMBER function is used to assign a number to the rows
returned by the subquery sorted by units sold descending. Because units sold is set in the same SELECT statement it can
not be used by the SUM within ROW_NUMBER() and so must be calculated twice.
```
WITH top_product_sold_by_region AS (
    SELECT dwproduct.p_code AS product_code,
           dwproduct.p_descript AS product_description,
           dwregion.reg_name AS region_name,
           SUM(dwdaysalesfact.sale_units) AS units_sold,
           ROW_NUMBER() OVER (
             PARTITION BY dwregion.reg_name
             ORDER BY SUM(dwdaysalesfact.sale_units) DESC
           ) AS row_num
    FROM dwdaysalesfact
    JOIN dwproduct ON dwdaysalesfact.p_code = dwproduct.p_code
    JOIN dwcustomer ON dwdaysalesfact.cus_code = dwcustomer.cus_code
    JOIN dwregion ON dwcustomer.reg_id = dwregion.reg_id
    GROUP BY dwregion.reg_name, dwproduct.p_code
)
SELECT product_code, product_description, region_name, units_sold
FROM top_product_sold_by_region
WHERE row_num = 1
ORDER BY region_name, units_sold DESC;
```

```
 product_code |         product_description         | region_name | units_sold
--------------+-------------------------------------+-------------+------------
 PVC23DRT     | PVC pipe, 3.5-in., 8-ft             | NE          |          5
 WR3/TT3      | Steel matting, 4'x8'x1/6", .5" mesh | NW          |          3
 PVC23DRT     | PVC pipe, 3.5-in., 8-ft             | SE          |         17
 PVC23DRT     | PVC pipe, 3.5-in., 8-ft             | SW          |         12
(4 rows)
```
