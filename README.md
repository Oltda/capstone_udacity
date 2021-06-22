                                
                                            WAREHOUSE APP
_________________________________________________________________________________________________________________________


This is an API for a warehouse application that allows its users to add, delete, and update warehouse information,
stock items and product codes.

Frontend has not yet been implemented.

My motivation for this project was the fact that I wanted to consolidate the knowledge that I have gained in 
Udacity Full-Stack Developer Nanodegree.

Another motivation was the fact that a friend of mine has recently started his own business and expressed his need of 
a stock management app that would help him to keep track of his items and their expiration dates 

Access Token
_________________________________________________________________________________________________________________________

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

heroku link: https://dans-warehouse-app.herokuapp.com
to run on local machine: http://127.0.0.1:5000



## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 



## Running the server

After activating virtual environment: 


To create the database with psql, execute:

```
createdb capstone_database

```

To run the server, execute:

```bash
export FLASK_APP=api
export FLASK_ENV=development
flask run
```










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

example response:

            {
                "new_warehouse_id": 11,
                "success": true
            }
            
********posting new product code********
----------------------------------------- 
endpoint:
    https://dans-warehouse-app.herokuapp.com/product-code
    
body:

      {
       "product_code" : "TTTY5",
       "description" : "frozen meat",
       "unit": "5 kg boxes"
      }    
    
NOTE (each product code must have a unique name)

example response:

        {
            "codes_list": [
                "AAA",
                "BB9",
                "TYHY",
                "AQ1",
                "AAA2134"
            ],
            "new_code_id": 6,
            "success": true
        }
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

example response:

        {
            "codes": [
                "AAA",
                "BB9",
                "TYHY",
                "AQ1"
            ],
            "items_list": [
                {
                    "expiration_date": "25-Jan-2052",
                    "id": 1,
                    "product_code": "AAA",
                    "product_name": "tomatoes",
                    "quantity": 123,
                    "warehouse_id": 1
                },
                {
                    "expiration_date": "25-Jan-3002",
                    "id": 2,
                    "product_code": "AAA",
                    "product_name": "cucumbers",
                    "quantity": 2145,
                    "warehouse_id": 1
                }
            ],
            "new_stock_id": 9,
            "success": true
        }

********View warehouses********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/warehouse


example response:

    {
        "stock_array": [
            {
                "expiration_date": "25-Jan-2052",
                "id": 1,
                "name": "tomatoes",
                "product_code": "AAA",
                "quantity": 123,
                "unit": "kg",
                "warehouse_id": 1
            },
            {
                "expiration_date": "25-Jan-3002",
                "id": 2,
                "name": "cucumbers",
                "product_code": "AAA",
                "quantity": 2145,
                "unit": "kg",
                "warehouse_id": 1
            },

        ],
        "success": true,
        "warehouse_list": [
            {
                "address": "City6",
                "id": 2,
                "name": "Warehouse6"
            },
            {
                "address": "trial3 address",
                "id": 1,
                "name": "trial3 name"
            }
        ]
    }

********View Stock********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/stock-items

Example response:
        
        {
            "codes": [
                "AAA",
                "BB9",
                "TYHY",
                "AQ1"
            ],
            "items_list": [
                {
                    "expiration_date": "25-Jan-2052",
                    "id": 1,
                    "product_code": "AAA",
                    "product_name": "tomatoes",
                    "quantity": 123,
                    "warehouse_id": 1
                },
                {
                    "expiration_date": "25-Jan-2062",
                    "id": 4,
                    "product_code": "BB9",
                    "product_name": "becherovka",
                    "quantity": 10000,
                    "warehouse_id": 1
                }
            ],
            "success": true
        }

********View Product Codes********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/product-code

example response:

        {
            "codes_list": [
                "AAA",
                "BB9",
                "TYHY"
            ],
            "success": true
        }

********Patch warehouses********
----------------------------------------- 
Endpoint:
https://dans-warehouse-app.herokuapp.com/warehouse/1


body:

    {
     "name" : "trial3 name",
     "address" : "trial3 address"
    }
example response:

        {
            "edited_warehouse_id": 3,
            "success": true,
            "warehouse_list": [
                {
                    "address": "City6",
                    "id": 2,
                    "name": "Warehouse6"
                },
                {
                    "address": "trial3 address",
                    "id": 1,
                    "name": "trial3 name"
                },
                {
                    "address": "City10",
                    "id": 4,
                    "name": "Warehouse10"
                }
            ]
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

example response:

        {
            "codes": [
                "AAA",
                "BB9",
                "TYHY",
                "AQ1",
                "AAA2134"
            ],
            "items_list": [
                {
                    "expiration_date": "25-Jan-3002",
                    "id": 2,
                    "product_code": "AAA",
                    "product_name": "cucumbers",
                    "quantity": 2145,
                    "warehouse_id": 1
                },
                {
                    "expiration_date": "25-Jan-2062",
                    "id": 3,
                    "product_code": "BB9",
                    "product_name": "vodka",
                    "quantity": 10000,
                    "warehouse_id": 2
                },
                {
                    "expiration_date": "25-Jan-2062",
                    "id": 4,
                    "product_code": "BB9",
                    "product_name": "becherovka",
                    "quantity": 10000,
                    "warehouse_id": 1
                },
                {
                    "expiration_date": "23-Jan-2024",
                    "id": 1,
                    "product_code": "AAA",
                    "product_name": "Ham",
                    "quantity": 32,
                    "warehouse_id": 1
                }
            ],
            "success": true,
            "warehouse_list": [
                {
                    "address": "City6",
                    "id": 2,
                    "name": "Warehouse6"
                },
                {
                    "address": "trial3 address",
                    "id": 1,
                    "name": "trial3 name"
                }

            ]
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
 
         
        
     

