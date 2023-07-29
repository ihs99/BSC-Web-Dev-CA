# Imprting required librarues of flask and MYSQL for connection of MYSQL with external db
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL



# Creating app names "inigo_huidobro"
inigo_huidobro = Flask(__name__)
inigo_huidobro.secret_key = 'many random bytes'


# Configuration of ZAMPP that I'm using as my localhost.
inigo_huidobro.config['MYSQL_HOST'] = 'localhost'
# My username is root
inigo_huidobro.config['MYSQL_USER'] = 'root'
# By default no password in config file, so setting password as empty here
inigo_huidobro.config['MYSQL_PASSWORD'] = ''
# Locating the created MySQL databae, that is crud
# database is crud and table that I've inserted in students
inigo_huidobro.config['MYSQL_DB'] = 'crud'

# Creating a MySQL object to interact with the database
mysql = MySQL(inigo_huidobro)



                            ###         CRUD Operations        ###
         # Read all students already present in students table of crud database
@inigo_huidobro.route('/')
def Index():
    # Establishing the mySQL connction
    cur = mysql.connection.cursor()
    # Selecting all students from stundets table by SQL query
    cur.execute("SELECT * FROM students")
    # Fetching all students
    data = cur.fetchall()
    # After fetching, closing the connection
    cur.close()
    # Showing those students on web page
    return render_template('index.html', students=data)



                   # Add a new students, C in CRUD
@inigo_huidobro.route('/insert', methods = ['POST'])
def insert():
    # Adding student by POST method
    if request.method == "POST":
        flash("Data Inserted Successfully")
        # Getting the name, email, and phone of students to add in students table
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        # Inserting provided info in students table
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        # Commiting the changes
        mysql.connection.commit()
        # Showing newly added students on web page
        return redirect(url_for('Index'))



                      # Update a student, U in CRUD
@inigo_huidobro.route('/update', methods= ['POST', 'GET'])
def update():
    # Updating student record using POST and taking new value of name, email, phone
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        # Updating student data by SQL query on the basis of id
        cur.execute("""
        UPDATE students SET name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id_data))
        mysql.connection.commit()
        flash("Data Updated Successfully")
        # Showing updated students on web page
        return redirect(url_for('Index'))



                         # Delete a student, D in CRUD
@inigo_huidobro.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    # Deleting students from students table on the values of id using SQL query
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    # Commiting the changes
    mysql.connection.commit()
    # Showing students on web page
    return redirect(url_for('Index'))



# Running the app
if __name__ == "__main__":
    inigo_huidobro.run(debug=True)
