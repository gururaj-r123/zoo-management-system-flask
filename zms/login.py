from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_mysqldb import MySQL
# creating a new flask application
app=Flask(__name__)
app.secret_key='gururaj'
#connecting to mysql database
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1605'
app.config['MYSQL_DB']='zoo'
mysql=MySQL(app)
#this is home page
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/animals')
def an():
    return render_template('animals.html')
@app.route('/info')
def info():
    return render_template('info.html')
#this is login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        id=request.form['user_id']
        passwd=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute('select *from admin where user_id=%s and password=%s',(id,passwd))
        account=cur.fetchone()
        if account:
            session['id']=id
            flash('you are succesfully logged in')
            return render_template('content.html')            
        else:
            flash('invalid username or password')
            return redirect(url_for('login'))
    else:
        if 'id' in session:
            return render_template('content.html')
        else:
            return render_template('login.html')
#this is logout page
@app.route('/logout')
def logout():
   session.pop('id',None)
   flash('Logged out')
   return redirect(url_for('login'))
#this is adding admin
@app.route('/addadmin',methods=['GET','POST'])
def addadmin():
    if 'id' in session:
        if request.method=='POST':
            id=request.form['user_id']
            password=request.form['password']
            name=request.form['name']
            phone=request.form['phone']
            gender=request.form['gender']
            cur=mysql.connection.cursor()
            cur.execute('select *from admin where user_id=%s',(id,))
            account=cur.fetchone()
            if account:
                flash('ADMIN ID ALREADY EXISTS PLEASE USE NEW ID')
                return redirect(url_for('addadmin'))
            else:
                cur=mysql.connection.cursor()
                cur.execute('insert into admin(user_id,name,password,phone_num,gender) values(%s,%s,%s,%s,%s)',(id,name,password,phone,gender))
                mysql.connection.commit()
                flash('SUCCESFULLY ADDED')
                return redirect(url_for('addadmin'))
        else:
          return render_template('add_to_zoo.html',name='admin')
            
    return redirect(url_for('login'))
#this is adding animals
@app.route('/addanimals',methods=['GET','POST'])
def addanimals():
    if 'id' in session:
        if request.method=='POST':
            id=request.form['unq_id']
            cur=mysql.connection.cursor()
            cur.execute('select *from animals where animal_id=%s',(id,))
            account=cur.fetchone()
            if account:
                flash('ANIMAL ID ALREADY EXISTS PLEASE USE NEW ID')
                return redirect(url_for('addanimals'))
            else:
                name=request.form['name']
                gender=request.form['gender']
                date=request.form['date']
                block=request.form['block']
                cur=mysql.connection.cursor()
                cur.execute('insert into animals(animal_id,name,gender,date_of_join,b_id) values(%s,%s,%s,%s,%s)',(id,name,gender,date,block))
                mysql.connection.commit()
                return redirect(url_for('addanimals'))
        else:
            
            return render_template('add_to_zoo.html',name='animals')
            
    return redirect(url_for('login'))
#this is adding visitor
@app.route('/addvisitor',methods=['GET','POST'])
def addvisitor():
    if 'id' in session:
        if request.method=='POST':
            name=request.form['name']
            gender=request.form['gender']
            age=request.form['age']
            phone=request.form['phone']
            date=request.form['date']
            amount=request.form['amount']
            cur=mysql.connection.cursor()
            cur.execute('insert into visitor(name,gender,age,phone_num,date_of_visit,paid) values(%s,%s,%s,%s,%s,%s)',(name,gender,age,phone,date,amount))
            mysql.connection.commit()
            flash('Succesfully added')
            return redirect(url_for('addvisitor'))
        else:  
            return render_template('add_to_zoo.html',name='visitor')
            
    return redirect(url_for('login'))

#this is adding adoptee
@app.route('/addadoptee',methods=['GET','POST'])
def addadoptee():
      if 'id' in session:
        if request.method=='POST':
            name=request.form['name']
            amount=request.form['amount']
            date=request.form['date']
            phone=request.form['phone']
            animal_id=request.form['unq_id']
            cur=mysql.connection.cursor()
            cur.execute(f'select * from animals where animal_id=%s',(animal_id,))
            a=cur.fetchone()
            if a:
              cur=mysql.connection.cursor()
              cur.execute('insert into adoption(name,amount,date_of_adoption,phone_num,an_id) values(%s,%s,%s,%s,%s)',(name,amount,date,phone,animal_id))
              mysql.connection.commit()
              flash('Succesfully added')
              return redirect(url_for('addadoptee'))
            else:
                flash('THE ANIMAL ID U ENTERED DOES NOT EXISTS')
                return render_template('add_to_zoo.html',name='adoptee')           
        else: 
            return render_template('add_to_zoo.html',name='adoptee')      
      return redirect(url_for('login'))

#this is adding employee
@app.route('/addemployee',methods=['GET','POST'])
def addemployee():
     if 'id' in session:
        if request.method=='POST':
            name=request.form['name']
            salary=request.form['amount']
            age=request.form['age']
            block=request.form['block']
            date=request.form['date']
            cur=mysql.connection.cursor()
            cur.execute('insert into employee(name,salary,age,b_id,d_of_join) values(%s,%s,%s,%s,%s)',(name,salary,age,block,date))
            mysql.connection.commit()
            flash('Succesfully added')
            return redirect(url_for('addemployee'))
        else:
            return render_template('add_to_zoo.html',name='employee')        
     return redirect(url_for('login'))

#this is to view admin
@app.route('/dis_admin')
def dis_admin():
    cur=mysql.connection.cursor()
    cur.execute('Select *from admin')
    details=cur.fetchall()
    
    if details:
        return render_template('display.html',details=details,name='admin')  
    else:
        return redirect(url_for('login'))

#this is to view animals
@app.route('/dis_animals')
def dis_animals():
    cur=mysql.connection.cursor()
    cur.execute('Select *from animals')
    details=cur.fetchall()
    cur.execute('Select COUNT(*)from animals')
    total=cur.fetchone()

    if details:
        return render_template('display.html',details=details,name='animals',total=total)
    else:
        return redirect(url_for('login'))

#this is to view block animals seperately
@app.route('/dis_block/<string:block>')
def dis_birds(block):  
    cur=mysql.connection.cursor()
    cur.execute('Select *from animals where b_id=%s',(block,))
    details=cur.fetchall()
    cur.execute('Select COUNT(*)from animals where b_id=%s',(block,))
    total=cur.fetchone()
   
    if details:
        return render_template('display.html',details=details,name=block,total=total) 
    else:
        return redirect(url_for('login'))
    
#this is to view visitors
@app.route('/dis_visitors')
def dis_visitors():
    cur=mysql.connection.cursor()
    cur.execute('Select *from visitor')
    details=cur.fetchall()
    cur.execute('Select SUM(paid),COUNT(name)from visitor')
    total=cur.fetchone()
   
    if details:
        return render_template('display.html',details=details,name='visitor',total=total) 
    else:
        return redirect(url_for('login'))

    
#this is to view adoptee
@app.route('/dis_adoptee')
def dis_adoptee():
    cur=mysql.connection.cursor()
    cur.execute('Select ad.a_id,ad.name,ad.amount,ad.date_of_adoption,ad.phone_num,ad.an_id,a.name from adoption as ad,animals as a where a.animal_id=ad.an_id')
    details=cur.fetchall() 
    if details:
        
        return render_template('display.html',details=details,name='adoptee')  
    else:
        return redirect(url_for('login'))


#this is to view admin
@app.route('/dis_employee')
def dis_employee():
    cur=mysql.connection.cursor()
    cur.execute('Select *from employee')
    details=cur.fetchall()
    if details:
        
        cur.execute('Select COUNT(*)from employee')
        total=cur.fetchone()
        return render_template('display.html',details=details,name='employee',total=total)
    else:
        return redirect(url_for('login'))

#this is to view block employees seperately
@app.route('/dis_blockemp/<string:block>')
def dis_emp(block):  
    cur=mysql.connection.cursor()
    cur.execute('Select *from employee where b_id=%s',(block,))
    details=cur.fetchall()
    print(details)
    cur.execute('Select COUNT(*)from employee where b_id=%s',(block,))
    total=cur.fetchone()
    
    if details:
        return render_template('display.html',details=details,name='employee',total=total,b=block)
    else:
        return redirect(url_for('dis_employee'))
    
@app.route('/update_admin/<string:id_data>',methods=['GET','POST'])
def update_admin(id_data):
    if 'id' in session:
        if request.method=='POST':
            id=request.form['user_id']
            password=request.form['password']
            name=request.form['name']
            phone=request.form['phone']
            gender=request.form['gender']
            cur=mysql.connection.cursor()
            cur.execute('update admin  set user_id=%s,name=%s,password=%s,phone_num=%s,gender=%s where id=%s',(id,name,password,phone,gender,id_data))
            mysql.connection.commit()
            return redirect('/dis_admin')

        else:
            cur=mysql.connection.cursor()
            cur.execute('Select *from admin where id=%s',id_data)
            details=cur.fetchall()
            print(details);
            return render_template('update.html',name='admin',row=details[0])         
    return redirect(url_for('login'))
    
@app.route('/update_animals/<string:id_data>',methods=['GET','POST'])
def update_animals(id_data):
    
    if 'id' in session:
        if request.method=='POST':
            id=request.form['unq_id']
            name=request.form['name']
            gender=request.form['gender']
            date=request.form['date']
            block=request.form['block']
            cur=mysql.connection.cursor()
            cur.execute('update  animals set  animal_id=%s,name=%s,gender=%s,date_of_join=%s,b_id=%s where id=%s',(id,name,gender,date,block,id_data))
            mysql.connection.commit()
            flash('SUCCESFULLY UPDATED ANIMAL')
            return redirect('/dis_animals')
          
        else:
            cur=mysql.connection.cursor()
            cur.execute('Select *from animals where id=%s',(id_data,))
            details=cur.fetchall()
            print(details)
            return render_template('update.html',name='animals',row=details[0])
    return redirect(url_for('login'))  
    
@app.route('/update_visitor/<string:id_data>',methods=['GET','POST'])
def update_visitor(id_data): 
    if 'id' in session:
        if request.method=='POST':
            name=request.form['name']
            gender=request.form['gender']
            age=request.form['age']
            phone=request.form['phone']
            date=request.form['date']
            amount=request.form['amount']
            cur=mysql.connection.cursor()
            cur.execute('update visitor set name=%s,gender=%s,age=%s,phone_num=%s,date_of_visit=%s,paid=%s where id=%s',(name,gender,age,phone,date,amount,id_data))
            mysql.connection.commit()
            return redirect('/dis_visitors')
        else:
            cur=mysql.connection.cursor()
            cur.execute('Select *from visitor where id=%s',(id_data,))
            details=cur.fetchall()
            return render_template('update.html',name='visitor',row=details[0])
            
    return redirect(url_for('login'))  

@app.route('/update_adoptee/<string:id_data>',methods=['GET','POST'])
def update_adoptee(id_data):
    if 'id' in session:
        if request.method=='POST':
            name=request.form['name']
            amount=request.form['amount']
            date=request.form['date']
            phone=request.form['phone']
            animal_id=request.form['unq_id']
            cur=mysql.connection.cursor()
            cur.execute(f'select * from animals where animal_id=%s',(animal_id,))
            a=cur.fetchone()
            if a:
                cur=mysql.connection.cursor()
                cur.execute('update adoption set name=%s,amount=%s,date_of_adoption=%s,phone_num=%s,an_id=%s where a_id=%s',(name,amount,date,phone,animal_id,id_data))
                mysql.connection.commit()
                return redirect('/dis_adoptee') 
            else:
                flash('THE ANIMAL ID U ENTERED DOES NOT EXISTS')
                cur=mysql.connection.cursor()
                cur.execute('Select *from adoption where a_id=%s',(id_data,))
                details=cur.fetchall()
                print(details)
                return render_template('update.html',name='adoptee',row=details[0])        
        else:
            cur=mysql.connection.cursor()
            cur.execute('Select *from adoption where a_id=%s',(id_data,))
            details=cur.fetchall()
            print(details)
            return render_template('update.html',name='adoptee',row=details[0])
            
    return redirect(url_for('login'))  

@app.route('/update_employee/<string:id_data>',methods=['GET','POST'])
def update_employee(id_data):
    if 'id' in session:
        if request.method=='POST': 
            name=request.form['name']
            salary=request.form['amount']
            age=request.form['age']
            block=request.form['block']
            date=request.form['date']
            cur=mysql.connection.cursor()
            cur.execute('update employee set name=%s,salary=%s,age=%s,b_id=%s,d_of_join=%s where e_id=%s',(name,salary,age,block,date,id_data))
            mysql.connection.commit()
            return redirect('/dis_employee')
        
        else:
            cur=mysql.connection.cursor()
            cur.execute('Select *from employee where e_id=%s',(id_data,))
            details=cur.fetchall()
            print(details);
            return render_template('update.html',name='employee',row=details[0])        
    return redirect(url_for('login'))

@app.route('/delete/<string:id_data>')
def delete(id_data):
    cur=mysql.connection.cursor()
    cur.execute('delete from admin where id=%s',(id_data))
    print(cur.fetchone())
    mysql.connection.commit()
    return redirect('/dis_admin')

@app.route('/animals_delete/<string:id_data>')
def an_delete(id_data):
    cur=mysql.connection.cursor()
    print('this is delting')
    cur.execute('delete from animals where id=%s',(id_data,))
    print(cur.fetchone())
    
    mysql.connection.commit()
    return redirect('/dis_animals')

@app.route('/vi_delete/<string:id_data>')
def vi_delete(id_data):
    cur=mysql.connection.cursor()
    print('this is delting')
    cur.execute('delete from visitor where id=%s',(id_data,))
    mysql.connection.commit()
    return redirect('/dis_visitors')

@app.route('/adoptee_delete/<string:id_data>')
def addop_delete(id_data):
    cur=mysql.connection.cursor()
    cur.execute('delete from adoption where a_id=%s',(id_data,))
    mysql.connection.commit()
    return redirect('/dis_adoptee')

@app.route('/emp_delete/<string:id_data>')
def emp_delete(id_data):
    cur=mysql.connection.cursor()
    cur.execute('delete from employee where e_id=%s',(id_data,))
    mysql.connection.commit()
    return redirect('/dis_employee')

if __name__=='__main__':
  app.run(debug=True)
