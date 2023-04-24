Open Issues
=============

(1) Bugs     

   - Descrepancy in swagger UI response message to actual message
	   + Login 200 OK case -> Swagger says "Operation successful"  but actual is "Login succeeded."
	   + Register with already exisrting user =  for 409 swagger says "Duplicate Entry" but actual is "Username \"pavan\" already exists"
   - Register: Empty username gets accepted
	- Register: Empty password gets accepted
	- No login check while adding the product to the cart
	- Add_to_cart api is accepting invalid quantity values
	- Cart add with "" quantity, breaks with  invalid literal for int() with base 10. Should be handled in dev code
	- Add cart response message is wrong

   .. code-block::

      (asapp-challenge) pkgovindraj@T3XJ736KQT ASAPP_QA_Automation % curl -s -o -  -w "%{http_code}" -X POST -d  '{"quantity":2}' -H 'Content-Type: application/json' http://localhost:5000/pavan/products/ASAPP%20Pens/add
      "QTY \"4\" of product \"ASAPP Pens\" added to cart"
      200%
      (asapp-challenge) pkgovindraj@T3XJ736KQT ASAPP_QA_Automation %
      
   - Response message could be better 
      + EG "Product \"PP Pens\" does not exist." can be proper like "Product "PP Pens" does not exist."

(2) Improvement in framework
	- Test_login.py have 2 jsons(one for positive cases, one for negative cases) so we can have setup method to register user in login positive case
   - Factory pattern

(3) Improvement in product 
	- Implement "Remove specific quantity of a product from Cart" feature.

(4) HTTPS support