                                
                                            WAREHOUSE APP
_________________________________________________________________________________________________________________________


This is an API for a warehouse application that allows its users to add, delete, and update warehouse information,
stock items and product codes.

Frontend has not yet been implemented.

To obtain an access token to test the application in Postman please visit the following url: 

https://dans-warehouse-app.herokuapp.com/authorization/url

and click on the link provided which will either redirect you to Auth0 Login 
where you can enter the following credentials for two different roles:


CREDENTIALS
---------------------------------------

To test the application you can log in with the following credentials


username: manager@manager.com
password: Password1

permissions: Can only view warehouses, stock and product codes 


username: employee@employee.com
password: Password2

permissions: Can view, post, delete, patch warehouses, stock and view post, delete product codes
NOTE: (patch was not implemented for product codes) 




POSTMAN EXAMPLES

********posting new warehouse********
-----------------------------------------
endpoint:
    https://dans-warehouse-app.herokuapp.com/warehouse

body:

      {
       "name" : "Warehouse6",
       "address" : "City6"
      }
   
********posting new product code********
----------------------------------------- 
endpoint:
    https://dans-warehouse-app.herokuapp.com/product-code
    
body:
    {
     "product_code" : "TY5",
     "description" : "frozen meat",
     "unit": "5 kg boxes"
    }    
    
NOTE (each product code must have a unique name)
  
********posting new stock item********
----------------------------------------- 
endpoint:
    https://dans-warehouse-app.herokuapp.com/stock-items

body:

    {
     "product_name" : "Rum",
     "quantity" : "4300",
     "expiration_date": "2062-01-25",
     "warehouse_id": "2",
     "product_code": "BB9"
    }
NOTE1 (date must be in the following format yyyy-mm-dd)
NOTE2 (warehouse and product code are foreign keys)
  

********View warehouses********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/warehouse


********View Stock********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/stock-items



********View Product Codes********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/product-code



********Patch warehouses********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/warehouse/1


body:

    {
     "name" : "trial3 name",
     "address" : "trial3 address"
    }


********Patch Stock********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/stock-items/1



body:

    {
     "product_name" : "tequila",
     "quantity" : "322",
     "expiration_date": "2024-01-23",
     "warehouse_id": "1",
     "product_code": "BB9"
    }

    
********Delete Warehouses********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/warehouse/3


********Delete Stock********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/stock-items/2


********Delete Product Codes********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/product-code/3
 
         
        
     

