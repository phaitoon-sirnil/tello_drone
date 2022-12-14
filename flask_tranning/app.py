from flask import Flask, render_template,request,redirect,url_for
import pymysql

app = Flask(__name__)
def connect_db():    
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = '',
        db='fruits',
        )
    return conn

@app.route('/')
def index():
    # return "hello flask..."
    return render_template("index.html")
@app.route('/about')
def about():
    #return "about page1"
    return render_template("about.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/user/<name>/<surname>')
def member(name,surname):
    return "<h1>สวัสดี : {} {} </h1>".format(name,surname)

@app.route('/showData')
def showData():
    print('show data..')
    # return render_template("profile.html")
    conn = connect_db()
    with conn:
        cur = conn.cursor()
        cur.execute("select * from fruits")
        rows = cur.fetchall()
        conn.commit()
        
        return render_template('index.html',data_rows = rows)

@app.route('/showform')
def showForm():
    print('show form')
    return render_template('inputform.html')


@app.route('/insert',methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        conn = connect_db()
        with conn.cursor() as cursor:
            sql = "insert into `fruits` (`name`,`price`) values (%s,%s)"
            cursor.execute(sql, (temp,humid))
        conn.commit()
        return redirect(url_for('showData'))


@app.route('/update',methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form['Id']
        name = request.form['Name']
        price = request.form['Price']

        conn = connect_db()
        with conn.cursor() as cursor:
            sql = "update `fruits` set `name`=%s,`price`=%s where `id`=%s"
            cursor.execute(sql, (temp,humid,id))
        conn.commit()
        return redirect(url_for('showData'))


@app.route('/delete/<string:id>',methods=['GET'])
def delete(id):
    sql = "delete from `fruits` where `id`=%s"
    conn = connect_db()
    with conn.cursor() as cur:        
        cur.execute(sql,id)
    
    conn.commit()
    return redirect(url_for('showData'))

if __name__ == "__main__":
    app.run(debug=True)
