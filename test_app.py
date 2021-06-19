import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app

from api.models.database import setup_db

from dotenv import load_dotenv

load_dotenv()

manager_token = os.environ.get('warehousemanager_token')
employee_token = os.environ.get('employee_token')

def get_headers(token):
    return {'Authorization': f'Bearer {token}'}





class WarehouseTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "stock_test"
        self.database_name = "stock_database"
        self.database_path = "postgresql://{}:{}@{}/{}".format('oltda', 'janaoltova', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_warehouse = {
            'name': 'BIG WAREHOUSE',
            'address': 'Karel Platz'

        }

        self.new_product_code = {
            'product_code': 'VV2',
            'description': 'vegetable',
            'unit': 'kg'
        }



        self.new_stock_item = {
            'product_name': 'carrot',
            'quantity': '234',
            'expiration_date': '2021-06-21',
            'warehouse_id': '1',
            'product_code': 'BB1'
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()



    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.


    """
    def test_get_warehouses(self):
        res = self.client().get('/warehouse', headers=get_headers(manager_token))
        data = json.loads(res.data)


        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['warehouse_list']))
        self.assertTrue(len(data['stock_array']))




    def test_get_warehouses_without_token(self):
        res = self.client().get('/warehouse')
        data = json.loads(res.data)


        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 'invalid_header')

    # def test_post_warehouse(self):
    #     res = self.client().post('/warehouse', json=self.new_warehouse, headers=get_headers(manager_token))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['new_warehouse_id'])


    def test_405_post_warehouse(self):

        res = self.client().post('/warehouse/2', json=self.new_warehouse, headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')


    def test_patch_warehouse(self):
        res = self.client().patch('/warehouse/2', json={'name': 'altered name', 'address':'altered address'}, headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['edited_warehouse_id'])





    def test_422_patch_warehouse(self):
        res = self.client().patch('/warehouse/554', json={'name': 'altered name', 'address':'altered address'}, headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # def test_delete_warehouse(self):
    #     res = self.client().delete('/warehouse/3', headers=get_headers(manager_token))
    #     warehouse = Warehouse.query.filter(Warehouse.id == 3).one_or_none()
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted_warehouse'], 3)


    def test_422_warehouse_does_not_exist(self):
        res = self.client().delete('/warehouse/11111', headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_get_product_codes(self):
        res = self.client().get('/product-code', headers=get_headers(manager_token))
        data = json.loads(res.data)


        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['codes_list']))


    def test_get_product_codes_without_token(self):
        res = self.client().get('/product-code')
        data = json.loads(res.data)


        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 'invalid_header')


    # def test_post_code(self):
    #     res = self.client().post('/product-code', json=self.new_product_code, headers=get_headers(manager_token))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['codes_list']))
    #     self.assertTrue(data['new_code_id'])



    def test_405_post_product_code(self):

        res = self.client().post('/product-code/2', json=self.new_product_code, headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')








    def test_get_stock_items(self):
        res = self.client().get('/stock-items', headers=get_headers(manager_token))
        data = json.loads(res.data)


        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['items_list']))
        self.assertTrue(len(data['codes']))


    def test_get_stock_items_without_token(self):
        res = self.client().get('/stock-items')
        data = json.loads(res.data)


        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 'invalid_header')


    # def test_post_stock_items(self):
    #     res = self.client().post('/stock-items', json=self.new_stock_item, headers=get_headers(manager_token))
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['items_list']))
    #     self.assertTrue(len(data['codes']))
    #     self.assertTrue(data['new_stock_id'])


    def test_405_post_stock_items(self):

        res = self.client().post('/stock-items/2', json=self.new_stock_item, headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')




    def test_patch_stock_item(self):
        res = self.client().patch('/stock-items/3', json={
            'product_name': 'chips',
            'quantity': '213',
            'expiration_date': '2021-07-21',
            'warehouse_id': '1',
            'product_code': 'BB1'
            }, headers=get_headers(manager_token))

        data = json.loads(res.data)


        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['items_list']))
        self.assertTrue(len(data['codes']))


    def test_422_patch_stock_item(self):
        res = self.client().patch('/stock-items/37676', json={
            'product_name': 'chips',
            'quantity': '213',
            'expiration_date': '2021-07-21',
            'warehouse_id': '1',
            'product_code': 'BB1'
            }, headers=get_headers(manager_token))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')




    # def test_delete_stock_item(self):
    #     res = self.client().delete('/stock-items/4', headers=get_headers(manager_token))
    #     stock_to_delete = StockItems.query.filter(StockItems.id == 4).one_or_none()
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted_stock'], 4)



    def test_422_stock_item_does_not_exist(self):
        res = self.client().delete('/stock-items/11111', headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')



    def test_delete_product_code(self):
        res = self.client().delete('/product-code/11', headers=get_headers(manager_token))

        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_code'], 11)



    def test_422_product_code_does_not_exist(self):
        res = self.client().delete('/product-code/11111', headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # ROLE AND PERMISSION TEST

    def test_RBAC_patch_warehouse_employee(self):
        res = self.client().patch('/warehouse/2', json={'name': 'employee changes', 'address':'employee address'}, headers=get_headers(employee_token))
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 'missing_permission')
        self.assertEqual(res.status_code, 401)


    def test_RBAC_patch_warehouse_manager(self):
        res = self.client().patch('/warehouse/2', json={'name': 'manager changes', 'address':'manager address'}, headers=get_headers(manager_token))
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['edited_warehouse_id'])
        self.assertEqual(res.status_code, 200)






    #--------------------------------------------------------------------------------
    # def test_404_sent_request_when_not_valid_page(self):
    #     res = self.client().get('/questions?page=1000')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    #
    # def test_get_question_by_category(self):
    #     res = self.client().get('/categories/2/questions')
    #
    #     data =json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['questions']))
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(data['current_category'], 'Art')
    #
    # def test_404_for_category_out_of_range(self):
    #     res = self.client().get('/categories/212/questions')
    #
    #     data =json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    #
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/17')
    #     data = json.loads(res.data)
    #     question = Question.query.filter(Question.id == 17).one_or_none()
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'], 17)
    #     self.assertEqual(question, None)
    #
    #
    # def test_422_question_does_not_exist(self):
    #     res = self.client().delete('/questions/2212')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    #
    # def test_post_question(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #
    #
    #
    # def test_405_for_posting_question(self):
    #
    #     res = self.client().post('/questions/10', json=self.new_question)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'method not allowed')
    #
    #
    #
    # def test_422_posting_question_empty_string(self):
    #     new_question = {'question': '',
    #                     'answer': "Prague",
    #                     "difficulty": 3,
    #                     "category": 3}
    #     res = self.client().post('/questions', json = new_question)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    #
    # def test_search_question(self):
    #     res = self.client().post('/questions/search', json={'searchTerm': "who"})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #
    # def test_no_result_search(self):
    #     res = self.client().post('/questions/search', json={'searchTerm': "xsxsxf"})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(len(data['questions']), 0)
    #     self.assertEqual(data['total_questions'], 0)
    #
    # def test_get_categories(self):
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['categories'])
    #
    # def test_get_questions_for_quizzes(self):
    #     res = self.client().post('/quizzes', json={'quiz_category':{'type': 'Art', 'id': '2'},
    #                                                "previous_questions": ["17"]})
    #     data = json.loads(res.data)
    #
    #
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['question'])






if __name__ == "__main__":
    unittest.main()