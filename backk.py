import mysql.connector as sql
try:
    conn = sql.connect(
        host = '127.0.0.1',
        port = '3306',
        user = 'root',
        database = 'alpha_cbt',
        password = ''
    )

    conn.autocommit = True
    mycursor = conn.cursor(dictionary=True)
except Exception as e:
    print(e)
else:
    print('Database connection successful')

import json
import random
import datetime
import re
import time
import bcrypt


class cbtback():
    __school_name = None
    def __init__(self, school_name):
        self.__school_name = school_name
        self.user=[]
        self.questioncse=[]
        self.questioncve=[]
        self.questioneee=[]
        self.result=[]
        self.exam=[]

    def create_questions(self, question, option_a, option_b, option_c, answer,deptque):
        new_question = {
            'question': question,
            'option': [
                option_a,
                option_b,
                option_c
            ],
            'answer': answer,
        }
        if deptque=='CSE':
            # self.questioncse.append(new_question)
            query = 'INSERT INTO questioncse(question, option_a,option_b,option_c,answer) VALUES(%s,%s,%s,%s,%s)'
            value = (question, option_a, option_b,option_c, answer)
            mycursor.execute(query,value)
            return{
                    'status':True,
                    'message_cse':'Question successfully added to CSE question bank',
                    'csebank':self.questioncse,
                }
        if deptque=='CVE':
            # self.questioncve.append(new_question)
            query = 'INSERT INTO questioncve(question, option_a,option_b,option_c,answer) VALUES(%s,%s,%s,%s,%s)'
            value = (question, option_a, option_b,option_c, answer)
            mycursor.execute(query,value)
            return{
                    'status':True,
                    'cvebank':self.questioncve,
                    'message_cve':'Question successfully added to CVE question bank',
                }
        if deptque=='EEE':
            # self.questioneee.append(new_question)
            query = 'INSERT INTO questioneee(question, option_a,option_b,option_c,answer) VALUES(%s,%s,%s,%s,%s)'
            value = (question, option_a, option_b,option_c, answer)
            mycursor.execute(query,value)
            return{
                    'status':True,
                    'eeebank':self.questioneee,
                    'message_eee':'Question successfully added to EEE question bank'
                }
        return{
            'status':False,
            'message': 'There are only CSE,CVE and EEE department at the moment, Kindly try again'
        }
    

    def view_questions(self, deptque):
        if deptque == 'CSE':
            query = 'SELECT * FROM questioncse'
            mycursor.execute(query)
            csebank = mycursor.fetchall()
            for i, row in enumerate(csebank, start=1):
                row['display_number'] = i

            return {
                'status': True,
                'message_cse': 'Here is your CSE Question Bank',
                'csebank': csebank
            }

        if deptque == 'CVE':
            query = 'SELECT * FROM questioncve'
            mycursor.execute(query)
            cvebank = mycursor.fetchall()
            for i, row in enumerate(cvebank, start=1):
                row['display_number'] = i

            return {
                'status': True,
                'message_cve': 'Here is your CVE Question Bank',
                'cvebank': cvebank
            }

        if deptque == 'EEE':
            query = 'SELECT * FROM questioneee'
            mycursor.execute(query)
            eeebank = mycursor.fetchall()
            for i, row in enumerate(eeebank, start=1):
                row['display_number'] = i

            return {
                'status': True,
                'message_eee': 'Here is your EEE Question Bank',
                'eeebank': eeebank
            }

        return {
            'status': False,
            'message': 'There are only CSE, CVE and EEE departments at the moment, Kindly try again'
        }

    def checkexam(self,user,deptque):
        query = 'SELECT *FROM result where student_id=%s and department=%s'
        value = (user['id'],deptque)
        mycursor.execute(query,value)
        resul= mycursor.fetchall()
        if len(resul)<1:
             return{
                'status': True,
                'message': 'Wishing you success'
            }
        return{
             'status': False,
             'message': 'You only have one attempt for each departmental exam'
        }
         

    def submit_exam(self,user,percent,deptque,grade,status):
            query = 'INSERT INTO result(fullname,student_id,department,student_department,score,grade,status) VALUES(%s,%s,%s,%s,%s,%s,%s)'
            value = (user['fullname'],user['id'],deptque,user['department'],percent,grade,status)
            mycursor.execute(query,value)
            return{
                'status': True,
                'message': 'Exam Submitted successfully'
            }
    def view_resultt(self,user):
        query='SELECT *FROM result where student_id=%s'
        value=(user['id'],)
        mycursor.execute(query,value)
        resul=mycursor.fetchall()
        # mycursor.execute("SET @count = 0")
        # mycursor.execute("UPDATE result SET id = @count:=@count+1")
        # mycursor.execute("ALTER TABLE result AUTO_INCREMENT = 1")
        for i, row in enumerate(resul, start=1):
            row['display_number'] = i
        return{
             'result':resul
        }
    def view_detail(self,user):
        query='SELECT *FROM user where id=%s'
        value=(user['id'],)
        mycursor.execute(query,value)
        resul=mycursor.fetchall()
        return{
             'result':resul
        }
    def load_questions(self,user,deptque):
        if deptque=='CSE':
            query = 'SELECT *FROM questioncse'
            mycursor.execute(query)
            csebank = mycursor.fetchall()
            random.shuffle(csebank)
            for i, row in enumerate(csebank, start=1):
                    row['display_number'] = i
            
            return{
                    'status':True,
                    'message_cse':'Here is your CSE Exam question, Answer all',
                    'csebank':csebank,
                    # 'percentcse':percentcse
                }
        if deptque=='CVE':
            query = 'SELECT *FROM questioncve'
            mycursor.execute(query)
            cvebank = mycursor.fetchall()
            # cvebank= random.shuffle(cveban)
            random.shuffle(cvebank)
            for i, row in enumerate(cvebank, start=1):
                    row['display_number'] = i
            return{
                    'status':True,
                    'cvebank': cvebank,
                    'message_cve':'Here is your CVE Exam question, Answer all',
                    # 'percentcve':percentcve
                }
        if deptque=='EEE':
            query = 'SELECT *FROM questioneee'
            mycursor.execute(query)
            eeebank = mycursor.fetchall()
            # eeebank= random.shuffle(eeeban)
            random.shuffle(eeebank)
            for i, row in enumerate(eeebank, start=1):
                    row['display_number'] = i
            return{
                    'status':True,
                    'eeebank': eeebank,
                    'message_eee':'Here is your EEE Exam question, Answer all',
                    # 'percenteee':percenteee
                }
        return{
            'status':False,
            'message': 'There are only CSE,CVE and EEE department at the moment, Kindly try again'
        }
    def editted_question(self,question, option_a, option_b,option_c, answer,deptque, choice):
        if deptque=='CSE':
                query = 'UPDATE  questioncse SET question=%s,option_a=%s,option_b=%s,option_c=%s,answer=%s where user_id=%s'
                values = (question,option_a,option_b,option_c,answer, choice)
                mycursor.execute(query, values)
                return {
                # 'csebank': csebank,
                'status': True,
                'message': 'Question editted successfully'
            }
        if deptque=='CVE':
                # self.questioncve[choice-1] = new_question
                query = 'UPDATE  questioncve SET question=%s,option_a=%s,option_b=%s,option_c=%s,answer=%s where user_id=%s'
                values = (question,option_a,option_b,option_c,answer, choice)
                mycursor.execute(query, values)
                return {
                # 'cvebank':self.questioncve,
                'status': True,
                'message': 'Question editted successfully'
            }
        if deptque=='EEE':
                query = 'UPDATE  questioneee SET question=%s,option_a=%s,option_b=%s,option_c=%s,answer=%s where user_id=%s'
                values = (question,option_a,option_b,option_c,answer, choice)
                mycursor.execute(query, values)
                return {
                'status': True,
                'message': 'Question editted successfully'
            }
        return{
            'status':False,
            'message': 'An error occured. There are only CSE,CVE and EEE department at the moment, Kindly try again'
        }
    def delete_question(self,deptque, choice):
        if deptque=='CSE':
                # self.questioncse.pop(choice-1)
                query = 'DELETE FROM questioncse where user_id=%s'
                value=(choice,)
                mycursor.execute(query,value)
                # mycursor.execute("SET @count = 0")
                # mycursor.execute("UPDATE questioncse SET user_id = @count:=@count+1")
                # mycursor.execute("ALTER TABLE questioncse AUTO_INCREMENT = 1")
                return {
                # 'csebank':self.questioncse,
                'status': True,
                'message': 'Question deleted successfully'
            }
        if deptque=='CVE':
                # self.questioncve.pop(choice-1)
                query = 'DELETE FROM questioncve where user_id=%s'
                value=(choice,)
                mycursor.execute(query,value)
                # mycursor.execute("SET @count = 0")
                # mycursor.execute("UPDATE questioncve SET user_id = @count:=@count+1")
                # mycursor.execute("ALTER TABLE questioncve AUTO_INCREMENT = 1")
                return {
                # 'cvebank':self.questioncve,
                'status': True,
                'message': 'Question deleted successfully'
            }
        if deptque=='EEE':
                # self.questioneee.pop(choice-1)
                query = 'DELETE FROM questioneee where user_id=%s'
                value=(choice,)
                mycursor.execute(query,value)
                # mycursor.execute("SET @count = 0")
                # mycursor.execute("UPDATE questioneee SET user_id = @count:=@count+1")
                # mycursor.execute("ALTER TABLE questioneee AUTO_INCREMENT = 1")
                return {
                # 'eeebank':self.questioneee,
                'status': True,
                'message': 'Question deleted successfully'
            }
        return{
            'status':False,
            'message': 'An error occured. There are only CSE,CVE and EEE department at the moment, Kindly try again'
        }

    def get_school_name(self):
        return self.__school_name
    def reset_password(self, email, new_password, confirm_password):
        # First check if passwords match
        if new_password != confirm_password:
            return {
                'status': False,
                'message': 'Passwords do not match'
            }

        try:
            # Check if user exists
            query = 'SELECT * FROM user WHERE email=%s'
            values = (email,)
            mycursor.execute(query, values)
            resul = mycursor.fetchone()

            if not resul:
                return {
                    'status': False,
                    'message': 'Email not found'
                }

            # Hash new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query = 'UPDATE user SET password=%s WHERE email=%s'
            values = (hashed_password, email)
            mycursor.execute(query, values)

            return {
                'status': True,
                'message': 'Password reset successful'
            }

        except Exception as e:
            return {
                'status': False,
                'message': f'Error: {str(e)}'
            }

    def register_user(self, email, fullname, password, confirm_password, role, id,department):
        if password != confirm_password:
            return {
                'status': False,
                'message': 'Password not match'
            }
        try:
            # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            if not re.match(r"^[\w.]+@[\w.]+\.com$", email):
                return {
                'status': False,
                'message': 'Invalid email format'
            }
            if len(fullname.strip().split()) != 2:
                return {
                'status': False,
                'message': 'Fullname must contain exactly two names'
            }
            if role!='student' and role!='staff' and role!='admin':
                return {
                    'status': False,
                    'message': 'Role can only be student/staff'
                }
            if department!='CSE' and department!='CVE' and department!='EEE':
                return {
                    'status': False,
                    'message': 'Only CSE/CVE/EEE departments exist at the moment'
                }
            if len(password) < 6:
                return {
                'status': False,
                'message': 'Password must be at least 6 characters long'
            }
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query = 'INSERT INTO user(email,fullname,password,role,id,department) VALUES(%s,%s,%s,%s,%s,%s)'
            value = (email,fullname,hashed_password,role,id,department)
            mycursor.execute(query,value)
        except sql.errors.IntegrityError as e:
            return{
                'status': False,
                'message':'email already exist'
            }
        except Exception as e:
            return{
                'status': False,
                'message': str(e)

            }




        for user in self.user:
            if user['email'] == email:
                return {
                'status': False,
                'message': 'Email already exist'
                }
        # new_user = {
        #     'id': id,
        #     'email' : email,
        #     'fullname': fullname,
        #     'password' : password,
        #     'role' : role.lower(),
        #     'department'  : department.upper()
        # }
        # self.user.append(new_user)
        return{
                'status': True,
                'role': role,
                'message_student': f'Account created successfully, Your matric number is  {id}',
                'message_staff': f'Account created successfully, Your staff id is  {id}'
        }
    def login_user(self,email,password):
        try:
            query= 'SELECT *FROM user where email=%s'
            values = (email,)
            mycursor.execute(query,values)
            resul= mycursor.fetchone()
            # print(resul)
            # if resul and bcrypt.checkpw(password.encode('utf-8'), resul['password'].encode('utf-8')):
            if resul:
                stored_password = resul['password']
                # print("Entered password:", password)
                # print("Stored hash:", stored_password)
                # print("Entered password:", password.encode('utf-8'))
                # print("Stored hash:", stored_password.encode('utf-8'))
                # If stored password is bcrypt hash
                if stored_password.startswith("$2b$"):
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        return{
                            'status': True,
                            'message': 'Login Successful',
                            'data':resul,
                            'login_message': f'Welcome here, {resul["fullname"]}, Your Id number is {resul["id"]}'
                        }
                else:
                # Fallback for old plain text passwords
                    if password == stored_password:
                        return {
                            'status': True,
                            'message': 'Login Successful (plain password)',
                            'data': resul,
                            'login_message': f'Welcome here, {resul["fullname"]}, Your Id number is {resul["id"]}'
                        }
            return{
                'status': False,
                'message': 'Invalid Credentials',
            }

        except Exception as e:
            return{
                'status': False,
                'message': str(e),
                # 'error': 'An error occured'
            }

        # for user in self.user:
        #     if user['email']==email and user['password']==password:
        #         return{
        #             'status': True,
        #             'data': user,
        #             'message': 'Login successful',
        #             'login_message': f'Welcome here, {fullname}, Your Id number is {user['id']}'}
        # else:
        #     return{
        #         'status': False,
        #         'message': 'Invalid credentials'
        #         }
    def view_studentuser(self,user):
                # i='student'
                # query = 'SELECT *FROM user where role=%s and department=%s'
                query = 'SELECT *FROM user where role=%s'
                # value = ('student', user['department'])
                value = ('student',)
                mycursor.execute(query,value)
                resul= mycursor.fetchall()
                if len(resul)>0:
                        return{
                        'status': True,
                        'data':resul
                    }
                return{
                   'status' : False,
                   'message': 'No registered student yet'
                }
    def view_studentusersearch(self,user,search):
                query = 'SELECT *FROM user where role=%s'
                # value = ('student', user['department'])
                value = ('student',)
                mycursor.execute(query,value)
                resul= mycursor.fetchall()
                if len(resul)>0:
                            return{
                            'status': True,
                            'data':resul
                        }
                return{
                'status' : False,
                'message': 'No student found'
                }
    def view_studentresultsearchh(self,user,search):
                query = 'SELECT *FROM result'
                # value = ('student', user['department'])
                # value = ('student',)
                mycursor.execute(query)
                resul= mycursor.fetchall()
                if len(resul)>0:
                            return{
                            'status': True,
                            'data':resul
                        }
                return{
                'status' : False,
                'message': 'No result yet'
                }
    def view_studentresultt(self,user):
                # i='student'
                query = 'SELECT *FROM result where department=%s'
                value = (user['department'],)
                mycursor.execute(query,value)
                resul= mycursor.fetchall()
                for i, row in enumerate(resul, start=1):
                    row['display_number'] = i
                if len(resul)>0:
                    return{
                        'status': True,
                        'data':resul
                    }
                return{
                    'status' : False,
                    'message': 'No result yet'
                    }
    def view_user(self):
                query = 'SELECT *FROM user'
                mycursor.execute(query)
                resul= mycursor.fetchall()
                return{
                    'data':resul
                }
    # def add_userr(self, email, fullname, password, confirm_password, role, id,department):
    #         query = 'INSERT INTO user(email,fullname,password,role,id,department) VALUES(%s,%s,%s,%s,%s,%s)'
    #         value = (email,fullname,password,role,id,department)
    #         mycursor.execute(query,value)

    def load_users(self):
            query = 'SELECT *FROM user'
            mycursor.execute(query)
            userx = mycursor.fetchall()
            return{
                    'status':True,
                    'message':'Here are the user available',
                    'userx':userx,
                    # 'percentcse':percentcse
                }
    
    def view_userss(self,usertype):
        # if usertype=='student' or usertype=='staff':
            query = 'SELECT *FROM user where role=%s'
            value=(usertype,)
            mycursor.execute(query,value)
            studentlist = mycursor.fetchall()
            return{
                    'status':True,
                    'message':'Here is your Registered Student list',
                    'userlist':studentlist
                }

    def editted_user(self,email, fullname, password,confirm_password, role,department,choice,usertype):
        # if choice==qq['user_id']:
        if password==confirm_password:
                query = 'UPDATE  user SET email=%s,fullname=%s,password=%s,role=%s,department=%s where id=%s'
                values = (email, fullname, password , role,department, choice)
                mycursor.execute(query, values)
                queryy = 'UPDATE result SET fullname=%s,student_department=%s where student_id=%s'
                valuee = (fullname,department,choice)
                mycursor.execute(queryy,valuee)
                return {
                # 'csebank': csebank,
                'status': True,
                'message': 'User editted successfully'
            }
        return{
            'status':False,
            'message': 'An error occured.'
        }
    def delete_user(self,choice,usertype):
        # if choice==qq['user_id']:
        if usertype=='student':
                # query = 'UPDATE  user SET email=%s,fullname=%s,password=%s,role=%s,department=%s where user_id=%s'
                # values = (email, fullname, password , role,department, choice)
                # mycursor.execute(query, values)
                query = 'DELETE FROM user where id=%s'
                value=(choice,)
                mycursor.execute(query,value)
                # mycursor.execute("SET @count = 0")
                # mycursor.execute("UPDATE user SET user_id = @count:=@count+1")
                # mycursor.execute("ALTER TABLE user AUTO_INCREMENT = 1")
                queryy = 'DELETE FROM result where student_id=%s'
                valuee=(choice,)
                mycursor.execute(queryy,valuee)
                # mycursor.execute("SET @count = 0")
                # mycursor.execute("UPDATE result SET student_id = @count:=@count+1")
                # mycursor.execute("ALTER TABLE result AUTO_INCREMENT = 1")
                return {
                'status': True,
                'message': 'User Deleted successfully'
            }
        return{
            'status':False,
            'message': 'An error occured.'
        }
    def view_plain_passwords(self):
        query = 'SELECT id, email, password FROM user'
        mycursor.execute(query)
        users = mycursor.fetchall()
        return users
        