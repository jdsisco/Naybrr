import io
import pymysql
from app import app
from db_config import mysql
from tables import Results
from flask import Flask, Response, render_template
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/new_user')
def add_user_view():
	return render_template('add.html')

"""@app.route('/add', methods=['POST'])
def new_user():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		
		cursor.execute("SELECT emp_id, emp_first_name, emp_last_name, emp_designation FROM employee")
		result = cursor.fetchall()

		output = io.StringIO()
		writer = csv.writer(output)
		
		line = ['Emp Id, Emp First Name, Emp Last Name, Emp Designation']
		writer.writerow(line)

		for row in result:
			line = [str(row['emp_id']) + ',' + row['emp_first_name'] + ',' + row['emp_last_name'] + ',' + row['emp_designation']]
			writer.writerow(line)

		output.seek(0)
		
		return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
"""

@app.route('/add', methods=['POST'])
def add_user():
    conn = None
    cursor = None
    try: 
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
    # validate the received values
        if _name and _email and _password and request.method == 'POST':
        #do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
        # save edits
            sql = "INSERT INTO Naybrr.Account(Username, Email, HashPass) VALUES(%s, %s, %s)" 
            data = (_name, _email, _hashed_password,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('User added successfully!')
            return redirect('/')
        else:
            return 'Error while adding user'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/table')
def users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Naybrr.Account")
        rows = cursor.fetchall()
        table = Results(rows)
        table.border = True
        return render_template('users.html', table=table)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
"""
@app.route('/edit/<int:id>')
def edit_view(id):
conn = None
cursor = None
try:
conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
row = cursor.fetchone()
if row:
return render_template('edit.html', row=row)
else:
return 'Error loading #{id}'.format(id=id)
except Exception as e:
print(e)
finally:
cursor.close()
conn.close()

@app.route('/update', methods=['POST'])
def update_user():
conn = None
cursor = None
try: 
_name = request.form['inputName']
_email = request.form['inputEmail']
_password = request.form['inputPassword']
_id = request.form['id']
# validate the received values
if _name and _email and _password and _id and request.method == 'POST':
#do not save password as a plain text
_hashed_password = generate_password_hash(_password)
print(_hashed_password)
# save edits
sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s
                                                       WHERE user_id=%s"
data = (_name, _email, _hashed_password, _id,)
conn = mysql.connect()
cursor = conn.cursor()
cursor.execute(sql, data)
conn.commit()
flash('User updated successfully!')
return redirect('/')
else:
return 'Error while updating user'
except Exception as e:
print(e)
finally:
cursor.close() 
conn.close()

@app.route('/delete/<int:id>')
def delete_user(id):
conn = None
cursor = None
try:
conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
conn.commit()
flash('User deleted successfully!')
return redirect('/')
except Exception as e:
print(e)
finally:
cursor.close() 
conn.close() """

if __name__ == "__main__":
app.run(threaded=True)
