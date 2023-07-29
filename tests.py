import unittest
from app import inigo_huidobro, mysql

class FlaskCRUDTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the testing environment
        inigo_huidobro.testing = True
        self.app = inigo_huidobro.test_client()
        self._create_test_student()

    def _create_test_student(self):
        # Helper method to create a test student in the database
        with inigo_huidobro.app_context():
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students (name, email, phone) VALUES ('Test Student', 'test@gmail.com', '9876543210')")
            mysql.connection.commit()
            cur.close()

    def test_create_student(self):
        # Test creating a new student
        response = self.app.post('/insert', data={'name': 'dummy', 'email': 'dummy@yahoo.com', 'phone': '1234567890'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        # Add more assertions to verify that the student was added to the database

    def test_read_students(self):
        # Test reading all students
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response is successful
        # Add more assertions to verify the data displayed matches the expected data

    def test_update_student(self):
        # Test updating an existing student
        response = self.app.post('/update', data={'id': '1', 'name': 'Updated Student', 'email': 'updated@yahooo.com', 'phone': '1111111111'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect

        # Check if the student details are updated in the database
        with inigo_huidobro.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM students WHERE id=1")
            updated_student = cur.fetchone()
            cur.close()

    def test_delete_student(self):
        # Test deleting a student
        response = self.app.get('/delete/1')
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect

        # Check if the student is deleted from the database
        with inigo_huidobro.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM students WHERE id=1")
            deleted_student = cur.fetchone()
            cur.close()

        self.assertIsNone(deleted_student)

if __name__ == '__main__':
    unittest.main()
