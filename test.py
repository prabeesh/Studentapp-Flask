from flask import render_template
from flask import Flask
import sqlite3
from flask import request,url_for
from flask import redirect,Response

app = Flask(__name__)




@app.route("/")
def mainpage():
	resp = Response("""<html><body>
					<p><a href="/details"> Add a student details</a></p>
					<p><a href="/sort1"> Details of All students sorted by age </a></p>
					<p><a href="/sort2"> Details of All students sorted by mark</a></p>
					<p><a href="/remove"> Remove details of a student </a></p>
					<p><a href="/search"> Search details of a student </a></p>
					<body></html>""", status=200, mimetype='html')
	return resp	

@app.route('/details', methods=['POST', 'GET'])
def details():
  if request.method == 'GET':
	return render_template('test.html')
	
  if request.method == 'POST':
    	name=request.form['student_name']
	sex=request.form['sex']
	age=request.form['age']
	mark=request.form['mark']

	data=(name, sex, age, mark)

	con = sqlite3.connect("student.db")
	cur=con.cursor()
   	cur.execute("CREATE TABLE IF NOT EXISTS student(name text, sex text, age text, mark text)")
    	cur.execute("INSERT INTO student VALUES(?, ?, ?, ?)", data)
	con.commit()
	con.close()
		
	return redirect(url_for('mainpage'))		
	
@app.route('/sort1', methods=['POST', 'GET'])
def sort1():
 if request.method == 'GET':
	con = sqlite3.connect('student.db')    
    
    	cur = con.cursor()    
    	cur.execute("SELECT * FROM student ORDER BY age ASC")

    	rows = cur.fetchall()
	entries = [dict(name=row[0], age=row[1], sex=row[2], mark=row[3]) for row in rows]
	return render_template('show_entries.html', entries=entries)
        
    

	
@app.route('/sort2', methods=['POST', 'GET'])
def sort2():
  if request.method == 'GET':
	con = sqlite3.connect('student.db')    
    
    	cur = con.cursor()    
    	cur.execute("SELECT * FROM student ORDER BY mark DESC")
	
	rows = cur.fetchall()
	entries = [dict(name=row[0], age=row[1], sex=row[2], mark=row[3]) for row in rows]
	return render_template('show_entries.html', entries=entries)
        

    	
@app.route('/remove', methods=['POST', 'GET'])
def remove():
  if request.method == 'GET':
	resp = Response("""<html><body>
					<form action='/remove' method="post">	
					<div> Student Name <input type="text" name = "remove" ></input></div>
					<div><input type="submit" value="submit"></div>
					</form>		
					</body></html>""", status=200, mimetype='html')
	return resp	

  if request.method == 'POST':
	remove=request.form['remove']
	con = sqlite3.connect('student.db')
	cur = con.cursor()
	cur.execute("DELETE FROM student WHERE name=:name", {"name": remove})
	con.commit()
	con.close()
	resp = Response("""<html><body>
					<div>"""+remove+"""'s details removed</div>
					<p><a href="/">Home</a></p>
					</body></html>""",mimetype='html')
	return resp 

@app.route('/search', methods=['POST', 'GET'])
def search():
  if request.method == 'GET':
	resp = Response("""<html><body>
					<form action='/search' method="post">	
					<div> Student Name <input type="text" name = "search" ></input></div>
					<div><input type="submit" value="submit"></div>
					</form>		
					</body></html>""", status=200, mimetype='html')
	return resp

  if request.method == 'POST':
	search=request.form['search']
	con = sqlite3.connect('student.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM student WHERE name=:name", {"name": search})
	
	rows = cur.fetchall()
	entries = [dict(name=row[0], age=row[1], sex=row[2], mark=row[3]) for row in rows]
	return render_template('show_entries.html', entries=entries)
    	
		
if __name__ == '__main__':
    app.debug = True
    app.run()
