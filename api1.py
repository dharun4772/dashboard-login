from flask import Flask,jsonify,request,render_template
from flask_restful import Resource,Api
import pymysql
import takeimg
import trainmodel
import pickle


app=Flask(__name__)
api=Api(app)


#http://127.0.0.1:5000/api/takeimg/?class_=5&section=A&firstname=abi&lastname=harri&rollno=5&phoneno=3442653
@app.route("/api/takeimg/")
def call_take_img():
    class_=request.args.get('class_')
    section=request.args.get('section')
    rollno=request.args.get('rollno')
    firstname=request.args.get('firstname')
    lastname=request.args.get('lastname')
    phno=request.args.get('phoneno')
    
    
    takeimg.take_img(class_,section,rollno,firstname,lastname,phno)
    return "Successfully Created"

@app.route("/api/trainimg/")
def trainimg():
    class_name=request.args.get('class_')
    section=request.args.get('section')
    model=trainmodel.train_model(class_name,section)
    filename='model'+class_name+section+'.pk'
    with open('C:/Users/Dell/python/'+class_name+'/'+section+'/'+filename,'wb') as file:
        pickle.dump(model,file)
    return "Dataset trained"

@app.route("/api/addstudent/")
def add_student():
    class_=request.args.get('class_')
    section=request.args.get('section')
    rollno=request.args.get('rollno')
    firstname=request.args.get('firstname')
    lastname=request.args.get('lastname')
    phno=request.args.get('phoneno')
    try:
        db = pymysql.connect(
        "Aparajithashri.mysql.pythonanywhere-services.com",
        "Aparajithashri",
        "Shinchan",
        "Aparajithashri$ATTENDANCE"
        )
        cursor=db.cursor()
        sql="INSERT INTO Attendance (CLASS,SECTION,ROLLNO,FIRSTNAME,LASTNAME,PHONENO) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,[class_,section,rollno,firstname,lastname,phno])
        db.commit()
        return "Student Added Successfully!"
    except Exception as e:
        return "Student already exists"
    finally:
        cursor.close()
        db.close()

@app.route("/api/deletestudent/")
def delete_student():
    class_=request.args.get('class_')
    section=request.args.get('section')
    rollno=request.args.get('rollno')
    firstname=request.args.get('firstname')
    lastname=request.args.get('lastname')
    try:
        db = pymysql.connect(
        "Aparajithashri.mysql.pythonanywhere-services.com",
        "Aparajithashri",
        "Shinchan",
        "Aparajithashri$ATTENDANCE"
        )
        cursor=db.cursor()
        sql="DELETE FROM Attendance WHERE CLASS=%s AND SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s"
        cursor.execute(sql,[class_,section,rollno,firstname,lastname])
        db.commit()
        return "Student Deleted Successfully!"
    except Exception as e:
        return "Student data not deleted"
    finally:
        cursor.close()
        db.close()

@app.route("/api/search/",methods=['POST'])
def search_attendance():
    date=request.args.get('date')
    class_=request.args.get('class_')
    section=request.args.get('section')
    rollno=request.args.get('rollno')
    firstname=request.args.get('firstname')
    lastname=request.args.get('lastname')
    lst=[]
    count=dat=0
    lst.append(class_)
    lst.append(section)
    lst.append(rollno)
    lst.append(firstname)
    lst.append(lastname)
    for i in lst:
        if i:
            count+=1
    if date:
        dat+=1
    try:
        db = pymysql.connect(
        "Aparajithashri.mysql.pythonanywhere-services.com",
        "Aparajithashri",
        "Shinchan",
        "Aparajithashri$ATTENDANCE"
        )
        cursor=db.cursor()
        #query
        if int(count==1) & int(dat==0):
            sql="SELECT CLASS,SECTION,ROLLNO,FIRSTNAME,LASTNAME,`%s` FROM Attendance WHERE CLASS=%s OR SECTION=%s OR ROLLNO=%s OR FIRSTNAME=%s OR LASTNAME=%s"
            cursor.execute(sql,[date,class_,section,rollno,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==1) & int(dat==1):
            sql="SELECT * FROM Attendance WHERE CLASS=%s OR SECTION=%s OR ROLLNO=%s OR FIRSTNAME=%s OR LASTNAME=%s"
            cursor.execute(sql,[class_,section,rollno,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==2) & int(dat==0):
            sql="SELECT CLASS,SECTION,ROLLNO,FIRSTNAME,LASTNAME,`%s` FROM Attendance WHERE (CLASS=%s AND SECTION=%s) OR (CLASS=%s AND ROLLNO=%s) OR (CLASS=%s AND FIRSTNAME=%s) OR (CLASS=%s AND LASTNAME=%s) OR (SECTION=%s AND ROLLNO=%s) OR (SECTION=%s AND FIRSTNAME=%s) OR (SECTION=%s AND LASTNAME=%s) OR (ROLLNO=%s AND FIRSTNAME=%s) OR (ROLLNO=%s AND LASTNAME=%s) OR (FIRSTNAME=%s AND LASTNAME=%s)"
            cursor.execute(sql,[date,class_,section,class_,rollno,class_,firstname,class_,lastname,section,rollno,section,firstname,section,lastname,rollno,firstname,rollno,lastname,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==2) & int(dat==1):
            sql="SELECT * FROM Attendance WHERE (CLASS=%s AND SECTION=%s) OR (CLASS=%s AND ROLLNO=%s) OR (CLASS=%s AND FIRSTNAME=%s) OR (CLASS=%s AND LASTNAME=%s) OR (SECTION=%s AND ROLLNO=%s) OR (SECTION=%s AND FIRSTNAME=%s) OR (SECTION=%s AND LASTNAME=%s) OR (ROLLNO=%s AND FIRSTNAME=%s) OR (ROLLNO=%s AND LASTNAME=%s) OR (FIRSTNAME=%s AND LASTNAME=%s)"
            cursor.execute(sql,[class_,section,class_,rollno,class_,firstname,class_,lastname,section,rollno,section,firstname,section,lastname,rollno,firstname,rollno,lastname,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==3) & int(dat==0):
            sql="SELECT CLASS,SECTION,ROLLNO,FIRSTNAME,LASTNAME,`%s` FROM Attendance WHERE (CLASS=%s AND SECTION=%s AND ROLLNO=%s) OR (CLASS=%s AND SECTION=%s AND FIRSTNAME=%s) OR (CLASS=%s AND SECTION=%s AND LASTNAME=%s) OR (CLASS=%s AND ROLLNO=%s AND FIRSTNAME=%s) OR (CLASS=%s AND ROLLNO=%s AND LASTNAME=%s) OR (CLASS=%s AND FIRSTNAME=%s AND LASTNAME=%s) OR (SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s) OR (SECTION=%s AND ROLLNO=%s AND LASTNAME=%s) OR (SECTION=%s AND FIRSTNAME=%s AND LASTNAME=%s) OR (ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s)"
            cursor.execute(sql,[date,class_,section,rollno,class_,section,firstname,class_,section,lastname,class_,rollno,firstname,class_,rollno,lastname,class_,firstname,lastname,section,rollno,firstname,section,rollno,lastname,section,firstname,lastname,rollno,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==3) & int(dat==1):
            sql="SELECT * FROM Attendance WHERE (CLASS=%s AND SECTION=%s AND ROLLNO=%s) OR (CLASS=%s AND SECTION=%s AND FIRSTNAME=%s) OR (CLASS=%s AND SECTION=%s AND LASTNAME=%s) OR (CLASS=%s AND ROLLNO=%s AND FIRSTNAME=%s) OR (CLASS=%s AND ROLLNO=%s AND LASTNAME=%s) OR (CLASS=%s AND FIRSTNAME=%s AND LASTNAME=%s) OR (SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s) OR (SECTION=%s AND ROLLNO=%s AND LASTNAME=%s) OR (SECTION=%s AND FIRSTNAME=%s AND LASTNAME=%s) OR (ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s)"
            cursor.execute(sql,[class_,section,rollno,class_,section,firstname,class_,section,lastname,class_,rollno,firstname,class_,rollno,lastname,class_,firstname,lastname,section,rollno,firstname,section,rollno,lastname,section,firstname,lastname,rollno,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==4) & int(dat==0):
            sql="SELECT CLASS,SECTION,ROLLNO,FIRSTNAME,LASTNAME,`%s` FROM Attendance WHERE (CLASS=%s AND SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s) OR (CLASS=%s AND SECTION=%s AND FIRSTNAME=%s AND LASTNAME=%s) OR (CLASS=%s AND SECTION=%s AND ROLLNO=%s AND LASTNAME=%s) OR (CLASS=%s AND ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s) OR (SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s)"
            cursor.execute(sql,[date,class_,section,rollno,firstname,class_,section,firstname,lastname,class_,section,rollno,lastname,class_,rollno,firstname,lastname,section,rollno,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==4) & int(dat==1):
            sql="SELECT * FROM Attendance WHERE (CLASS=%s AND SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s) OR (CLASS=%s AND SECTION=%s AND FIRSTNAME=%s AND LASTNAME=%s) OR (CLASS=%s AND SECTION=%s AND ROLLNO=%s AND LASTNAME=%s) OR (CLASS=%s AND ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s) OR (SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s)"
            cursor.execute(sql,[class_,section,rollno,firstname,class_,section,firstname,lastname,class_,section,rollno,lastname,class_,rollno,firstname,lastname,section,rollno,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==5) & int(dat==0):
            sql="SELECT CLASS,SECTION,ROLLNO,FIRSTNAME,LASTNAME,`%s` FROM Attendance WHERE (CLASS=%s AND SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s)"
            cursor.execute(sql,[date,class_,section,rollno,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        elif int(count==5) & int(dat==1):
            sql="SELECT * FROM Attendance WHERE (CLASS=%s AND SECTION=%s AND ROLLNO=%s AND FIRSTNAME=%s AND LASTNAME=%s)"
            cursor.execute(sql,[class_,section,rollno,firstname,lastname])
            data=cursor.fetchall()
            return jsonify(data)
        else:
            return "Result Not Found"
    except Exception as e:
        return "Result Not Found"
    finally:
        db.commit()
        cursor.close()
        db.close()


@app.route("/")
def root():
    sql.createdb()
    return "Attendance system"

if __name__=='__main__':
    app.run(debug=False)
    
