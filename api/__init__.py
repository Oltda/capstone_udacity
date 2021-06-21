from flask import Flask, request, abort, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database import setup_db, Warehouse, StockItems, ProductCodes
from auth import AuthError, requires_auth

from authlib.integrations.flask_client import OAuth





def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)
    oauth = OAuth(app)
    app.secret_key = 'jgjhghg323jhg3j2hg3j2hg32jhg32jhg'

    AUTH0_DOMAIN = 'dev-j1fpxr2o.eu.auth0.com'
    AUTH0_JWT_API_AUDIENCE = 'warehouse'
    AUTH0_CLIENT_ID = 'OKLQ4Z8FAnpNsf8KhIQPdKd61DXucXiO'
    #AUTH0_CALLBACK_URL = 'http://localhost:3000'
    AUTH0_CALLBACK_URL = 'http://localhost:5000/result'


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response




    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={AUTH0_JWT_API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'

        return render_template('login.html', url=url)


    @app.route('/result', methods=['GET', 'POST'])
    def callbackpage():

        return render_template('result.html')




    @app.route('/warehouse', methods=['GET'])
    @requires_auth('get:warehouse')
    def show_warehouses(payload):

        warehouse_collection = Warehouse.query.all()
        warehouse_list = []

        for i in warehouse_collection:
            warehouse_list.append({"id": i.id, "name": i.name, "address": i.address})

        stock = StockItems.query.all()

        stock_array = []

        for i in stock:
            code = ProductCodes.query.filter_by(product_code=i.product_code).first()

            stock_item = {'id':i.id, 'name': i.product_name, 'quantity': i.quantity,
                          'expiration_date': i.expiration_date.strftime('%d-%b-%Y'), 'warehouse_id': i.warehouse_id, 'product_code': i.product_code, 'unit': code.unit}
            stock_array.append(stock_item)


        return jsonify({
            'success': True,
            'warehouse_list': warehouse_list,
            'stock_array': stock_array
        })


    @app.route('/warehouse', methods=['POST'])
    @requires_auth('post:warehouse')
    def post_warehouse(payload):
        try:
            body = request.get_json()

            new_warehouse_name = body.get('name', None)
            new_warehouse_address = body.get('address', None)

            warehouse = Warehouse(name=new_warehouse_name, address=new_warehouse_address)

            warehouse.insert()

            warehouse_collection = Warehouse.query.all()
            warehouse_list = []


            for i in warehouse_collection:
                warehouse_list.append({"id": i.id, "name": i.name, "address": i.address})

            return jsonify({
                'success': True,
                'new_warehouse_id':warehouse.id
            })
        except:
            abort(422)


    @app.route('/warehouse/<int:warehouse_id>', methods=['PATCH'])
    @requires_auth('patch:warehouse')
    def edit_warehouse(payload, warehouse_id):

        body = request.get_json()

        try:
            edited_name = body.get('name', None)
            edited_address = body.get('address', None)

            warehouse_patch = Warehouse.query.filter(Warehouse.id == warehouse_id).one_or_none()

            warehouse_patch.name = edited_name
            warehouse_patch.address = edited_address


            warehouse_patch.update()

            warehouse_collection = Warehouse.query.all()
            warehouse_list = []

            for i in warehouse_collection:
                warehouse_list.append({"id": i.id, "name": i.name, "address": i.address})

            return jsonify({
                'success': True,
                'warehouse_list': warehouse_list,
                'edited_warehouse_id': warehouse_patch.id
            })


        except:
            abort(422)



    @app.route('/warehouse/<int:warehouse_id>', methods=['DELETE'])
    @requires_auth('delete:warehouse')
    def delete_warehouse(payload, warehouse_id):
        try:
            warehouse_to_delete = Warehouse.query.filter(Warehouse.id == warehouse_id).one_or_none()

            if warehouse_to_delete is None:
                abort(404)


            stock_to_delete = StockItems.query.filter(StockItems.warehouse_id == warehouse_id).all()

            for i in stock_to_delete:
                i.delete()

            warehouse_to_delete.delete()

            return jsonify({
                'success': True,
                'deleted_warehouse':warehouse_id

            })
        except:
            abort(422)







    @app.route('/product-code', methods=['GET'])
    @requires_auth('get:product-code')
    def show_product_codes(payload):

        codes_collection = ProductCodes.query.all()
        codes_list = []

        for i in codes_collection:
            codes_list.append(i.product_code)


        return jsonify({
            'success': True,
            'codes_list': codes_list
        })




    @app.route('/product-code', methods=['POST'])
    @requires_auth('post:product-code')
    def post_product_code(payload):
        try:
            body = request.get_json()

            new_code = body.get('product_code', None)
            new_description = body.get('description', None)
            new_unit = body.get('unit', None)

            code = ProductCodes(product_code=new_code, description=new_description, unit=new_unit)

            code.insert()

            codes_collection = ProductCodes.query.all()
            codes_list = []

            for i in codes_collection:
                codes_list.append(i.product_code)

            return jsonify({
                'success': True,
                'codes_list': codes_list,
                'new_code_id': code.id
            })


        except:
            abort(422)




    @app.route('/product-code/<int:code_id>', methods=['DELETE'])
    @requires_auth('delete:product-code')
    def delete_product_code(payload, code_id):
        try:
            code_to_delete = ProductCodes.query.filter(ProductCodes.id == code_id).one_or_none()

            if code_to_delete is None:
                abort(404)


            stock_to_delete = StockItems.query.filter(StockItems.product_code == code_to_delete.product_code).all()

            for i in stock_to_delete:
                i.delete()


            code_to_delete.delete()

            return jsonify({
                'success': True,
                'deleted_code':code_id

            })
        except:
            abort(422)







    @app.route('/stock-items', methods=['GET'])
    @requires_auth('get:stock-items')
    def show_stock_items(payload):

        stock_items_collection = StockItems.query.all()
        items_list = []

        for i in stock_items_collection:
            items_list.append({"id": i.id, "product_name": i.product_name,
                               "quantity": i.quantity, "expiration_date": i.expiration_date.strftime('%d-%b-%Y'),
                               "warehouse_id": i.warehouse_id, "product_code": i.product_code})


        product_codes_collection = ProductCodes.query.all()
        product_code_list = []

        for i in product_codes_collection:
            product_code_list.append(i.product_code)


        return jsonify({
            'success': True,
            'items_list': items_list,
            'codes': product_code_list
        })



    @app.route('/stock-items/<int:warehouse_id>', methods=['GET'])
    @requires_auth('get:stock-items')
    def show_warehouse_stock(payload, warehouse_id):

        warehouse = Warehouse.query.get(warehouse_id)

        stock = StockItems.query.filter_by(warehouse_id=warehouse_id).all()
        stock_array = []

        for i in stock:

            code = ProductCodes.query.filter_by(product_code=i.product_code).first()
            stock_item = {'id':i.id, 'name': i.product_name, 'quantity': i.quantity,
                              'expiration_date': i.expiration_date.strftime('%d-%b-%Y'), 'warehouse_id': i.warehouse_id, 'product_code': i.product_code, 'unit': code.unit}
            stock_array.append(stock_item)




        warehouse_collection = Warehouse.query.all()
        warehouse_list = []

        for i in warehouse_collection:
            warehouse_list.append({"id": i.id, "name": i.name, "address": i.address})


        return jsonify({
            'success': True,
            'stock_array': stock_array,
            'warehouse_list': warehouse_list,
        })


    @app.route('/stock-items', methods=['POST'])
    @requires_auth('post:stock-items')
    def post_item(payload):
        try:
            body = request.get_json()

            new_product_name = body.get('product_name', None)
            new_quantity = int(body.get('quantity', None))
            new_expiration_date = body.get('expiration_date', None)
            warehouse_id = int(body.get('warehouse_id', None))
            product_code = body.get('product_code', None)



            item = StockItems(product_name=new_product_name, quantity=new_quantity,
                              expiration_date=new_expiration_date, warehouse_id=warehouse_id,
                              product_code=product_code)

            item.insert()

            stock_items_collection = StockItems.query.all()
            items_list = []

            for i in stock_items_collection:
                items_list.append({"id": i.id, "product_name": i.product_name,
                                   "quantity": i.quantity, "expiration_date": i.expiration_date.strftime('%d-%b-%Y'),
                                   "warehouse_id": i.warehouse_id, "product_code": i.product_code})

            product_codes_collection = ProductCodes.query.all()
            product_code_list = []

            for i in product_codes_collection:
                product_code_list.append(i.product_code)



            return jsonify({
                'success': True,
                'items_list': items_list,
                'codes': product_code_list,
                'new_stock_id': item.id
            })
        except:
            abort(422)





    @app.route('/stock-items/<int:stock_id>', methods=['PATCH'])
    @requires_auth('patch:stock-items')
    def edit_stock(payload, stock_id):

        body = request.get_json()

        try:
            edit_product_name = body.get('product_name', None)
            edit_quantity = int(body.get('quantity', None))
            edit_expiration_date = body.get('expiration_date', None)
            edit_warehouse_id = int(body.get('warehouse_id', None))
            edit_product_code = body.get('product_code', None)

            stock_patch = StockItems.query.filter(StockItems.id == stock_id).one_or_none()



            stock_patch.product_name = edit_product_name
            stock_patch.quantity = edit_quantity
            stock_patch.expiration_date = edit_expiration_date
            stock_patch.warehouse_id = edit_warehouse_id
            stock_patch.product_code = edit_product_code

            stock_patch.update()




            warehouse_collection = Warehouse.query.all()
            warehouse_list = []

            for i in warehouse_collection:
                warehouse_list.append({"id": i.id, "name": i.name, "address": i.address})


            stock_items_collection = StockItems.query.all()
            items_list = []

            for i in stock_items_collection:
                items_list.append({"id": i.id, "product_name": i.product_name,
                                   "quantity": i.quantity, "expiration_date": i.expiration_date.strftime('%d-%b-%Y'),
                                   "warehouse_id": i.warehouse_id, "product_code": i.product_code})

            product_codes_collection = ProductCodes.query.all()
            product_code_list = []

            for i in product_codes_collection:
                product_code_list.append(i.product_code)

            return jsonify({
                'success': True,
                'warehouse_list': warehouse_list,
                'items_list': items_list,
                'codes': product_code_list
            })


        except:
            abort(422)

    @app.route('/stock-items/<int:stock_id>', methods=['DELETE'])
    @requires_auth('delete:stock-items')
    def delete_warehouse_stock(payload, stock_id):
        try:
            stock_to_delete = StockItems.query.filter(StockItems.id == stock_id).one_or_none()

            if stock_to_delete is None:
                abort(404)



            stock_to_delete.delete()

            return jsonify({
                'success': True,
                'deleted_stock': stock_id

            })
        except:
            abort(422)


    @app.errorhandler(AuthError)
    def authentification_error(error):

        status_code = error.status_code
        msg = jsonify(error.error)
        return msg, status_code

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app

app = create_app()

if __name__ == '__main__':
    app.run()