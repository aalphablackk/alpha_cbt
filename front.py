from back import cbtback
# import bcrypt
import random
import time
import pyttsx3
import getpass

class cbtfront(cbtback):
    def __init__(self, school_name):
        super().__init__(school_name)
        self.home()


    def home(self):
        try:
            engine = pyttsx3.init()
            print('Welcome to Alpha Academy')
            print(
                '''
                1. Register
                2. Login
                3. exit
                '''
            )
            engine.say("Welcome to Alpha Academy")
            engine.runAndWait()

            choice = input('Enter choice: ').strip()
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '###':
                self.admin_page()
            elif choice == '3':
                print('Goodbye!')
                exit()
            else:
                print('Invalid choice. Please enter 1, 2, or 3.')
                self.home()
        except KeyboardInterrupt:
            print('\nSession interrupted. Goodbye!')
            exit()
        except Exception as e:
            print(f'An unexpected error occurred at home: {e}')
            self.home()

            
        # ==============REGISTER DASHBOARD=============

    def register(self):
        try:
            email = input('Input your mail: ').strip()
            if not email:
                print('Email cannot be empty.')
                return self.home()

            fullname = input('Enter fullname: ').strip().capitalize()
            if not fullname:
                print('Fullname cannot be empty.')
                return self.home()

            role = input(
                        '''
                        Enter role(Student/ Staff):
                        ''').strip().lower()
            if not role:
                print('Role cannot be empty.')
                return self.home()

            department = input('What department are you? CSE/CVE/EEE: ').strip().upper()
            if not department:
                print('Department cannot be empty.')
                return self.home()

            password = getpass.getpass('Enter password: ')
            if not password:
                print('Password cannot be empty.')
                return self.home()

            confirm_password = getpass.getpass('Enter confirm password: ')
            if not confirm_password:
                print('Confirm password cannot be empty.')
                return self.home()

            id = random.randint(111111, 999999)
            link = self.register_user(email, fullname, password, confirm_password, role, id, department)

            if link['status']:
                if link['role'] == 'student':
                    print(link['message_student'])
                elif link['role'] == 'staff':
                    print(link['message_staff'])
            else:
                print(link['message'])

        except KeyboardInterrupt:
            print('\nRegistration cancelled.')
        except EOFError:
            print('Input ended unexpectedly during registration.')
        except Exception as e:
            print(f'An error occurred during registration: {e}')
        finally:
            self.home()

        # ==============LOGIN DASHBOARD=============


    def login(self):
        try:
            email = input('Input your mail: ').strip()
            if not email:
                print('Email cannot be empty.')
                return self.home()

            password = getpass.getpass('Enter password: ')
            if not password:
                print('Password cannot be empty.')
                return self.home()

            link = self.login_user(email, password)

            if link['status']:
                user = link['data']
                print(link['message'])
                print(link['login_message'])
                if user['role'] == 'student':
                    self.student_dashboard(user)
                elif user['role'] == 'staff':
                    self.staff_dashboard(user)
                else:
                    print('Unknown role. Please contact admin.')
                    self.home()
            else:
                print(link['message'])
                self.home()

        except KeyboardInterrupt:
            print('\nLogin cancelled.')
            self.home()
        except EOFError:
            print('Input ended unexpectedly during login.')
            self.home()
        except Exception as e:
            print(f'An error occurred during login: {e}')
            print('Kindly register before signing in if you are new')
            self.home()




        # ==============STUDENT DASHBOARD=============
    def student_dashboard(self, user):
        try:
            print(
                '''
                1.  Take Exam
                2.  View Result
                3.  View Details
                4.  Logout
                '''
            )
            choice = input('What do you wish to do: ').strip()
            if choice == '1':
                self.take_exam(user)
            elif choice == '2':
                self.view_result(user)
            elif choice == '3':
                self.view_details(user)
            elif choice == '4':
                self.home()
            else:
                print('Invalid option. Please enter 1, 2, 3, or 4.')
                self.student_dashboard(user)
        except KeyboardInterrupt:
            print('\nSession interrupted. Returning to home.')
            self.home()
        except Exception as e:
            print(f'An error occurred: {e}')
            self.student_dashboard(user)

    def take_exam(self, user):
        try:
            try:
                engine = pyttsx3.init(driverName='sapi5')  # Windows driver
                engine.setProperty('rate', 180)
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[1].id)
            except Exception:
                engine = None

            deptque = input('Which departmental exam are you writing?: ').strip().upper()
            if not deptque:
                print('Department cannot be empty.')
                return self.student_dashboard(user)

            score = 0
            link = self.load_questions(user, deptque)
            linkkk = self.checkexam(user, deptque)

            if not linkkk['status']:
                print(linkkk['message'])
                return self.student_dashboard(user)

            durations = {'CSE': 120, 'CVE': 130, 'EEE': 150}
            exam_duration = durations.get(deptque, 120)

            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Choose CSE, CVE, or EEE.')
                return self.student_dashboard(user)

            bank_key = f'{deptque.lower()}bank'
            if not link.get(bank_key) or len(link[bank_key]) == 0:
                print("-" * 60)
                print("There are no questions yet")
                print("-" * 60)
                return self.student_dashboard(user)

            start_time = time.time()

            if deptque == 'CSE':
                questions = link['csebank']
                print(link['message_cse'])
            elif deptque == 'CVE':
                questions = link['cvebank']
                print(link['message_cve'])
            elif deptque == 'EEE':
                questions = link['eeebank']
                print(link['message_eee'])

            print(f'{len(questions)} question(s) in total')

            try:
                if engine:
                    engine.say("Your exam starts now. Good luck!")
                    engine.runAndWait()
            except Exception:
                pass

            for q in questions:
                try:
                    elapsed = time.time() - start_time
                    if elapsed >= exam_duration:
                        print("\n Time is up! Auto-submitting your exam...")
                        try:
                            if engine:
                                engine.say("Time is up. Auto-submitting your exam.")
                                engine.runAndWait()
                        except Exception:
                            pass
                        break

                    print(f"Q{q['display_number']}: {q['question']}")
                    print(f"Option A: {q['option_a']}")
                    print(f"Option B: {q['option_b']}")
                    print(f"Option C: {q['option_c']}")
                    print("=" * 80)

                    remaining = exam_duration - elapsed
                    if remaining <= 30:
                        print(" 30 seconds left!")
                        try:
                            if engine:
                                engine.say("Warning, only thirty seconds left")
                                engine.runAndWait()
                        except Exception:
                            pass

                    print(f" Time left: {int(remaining)} seconds")
                    response = input("Type your answer exactly as shown: ").strip().upper()
                    if response == q['answer'].upper():
                        score += 1

                except KeyboardInterrupt:
                    print('\nExam interrupted. Auto-submitting...')
                    break
                except Exception as e:
                    print(f'Error on question: {e}. Skipping...')
                    continue

            if len(questions) == 0:
                print('No questions were answered.')
                return self.student_dashboard(user)

            percent = (score / len(questions)) * 100

            if 70 <= percent <= 100:
                grade = "Grade A"
            elif 60 <= percent <= 69:
                grade = "Grade B"
            elif 50 <= percent <= 59:
                grade = "Grade C"
            elif 40 <= percent <= 49:
                grade = "Grade D"
            else:
                grade = "Grade E"

            status = "Passed" if percent >= 50 else "Failed"

            user['last_score'] = {
                'percent': percent,
                'status': status,
                'grade': grade
            }

            linkk = self.submit_exam(user, percent, deptque, grade, status)
            print(linkk['message'])

            if 'results_history' not in user:
                user['results_history'] = []
            user['results_history'].append(user['last_score'])

        except KeyboardInterrupt:
            print('\nExam session interrupted.')
        except Exception as e:
            print(f'An error occurred during the exam: {e}')
        finally:
            self.student_dashboard(user)

    def view_result(self, user):
        try:
            link = self.view_resultt(user)
            if not link.get('result'):
                print('No results found yet.')
                return self.student_dashboard(user)

            print("=" * 100)
            print(f"{'No.':<5} {'Full Name':<15} {'Student ID':<10} {'Dept':<6} {'Score':<8} {'Grade':<15} {'Status':<8} {'Submitted':<20}")
            print("-" * 100)
            for i in link['result']:
                status_color = "\033[92m" if i['status'].lower() == "passed" else "\033[91m"
                reset_color = "\033[0m"
                print(f"{i['display_number']:<5} {str(i['fullname']):<15} {i['student_id']:<10} {i['department']:<6} "
                      f"{str(i['score']):<8} {i['grade']:<15} {status_color}{i['status']:<8}{reset_color} {i['time_submitted']}")
            print("=" * 100)

        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while viewing results: {e}')
        finally:
            self.student_dashboard(user)

    def view_details(self, user):
        try:
            link = self.view_detail(user)
            if not link.get('result'):
                print('No user details found.')
                return self.student_dashboard(user)

            for i in link['result']:
                print("=" * 50)
                print(" User Details")
                print("=" * 50)
                print(f"ID:          {i['id']}")
                print(f"Full Name:   {i['fullname']}")
                print(f"Email:       {i['email']}")
                print(f"Role:        {i['role'].capitalize()}")
                print(f"Department:  {i['department']}")
                print("=" * 50)

        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while viewing details: {e}')
        finally:
            self.student_dashboard(user)



#         # ==============STAFF DASHBOARD=============

    def staff_dashboard(self, user):
        try:
            print(
                '''
                1. Manage Exams
                2. Manage Students
                3. Log out()
                '''
            )

            choice = input('What do you wish to do: ').strip()
            if choice == '1':
                print(
                    '''
                    1. Update Exam questions
                    2. View Exam questions
                    3. Edit Exam questions
                    4. Delete Exam questions
                    5. Go back
                    '''
                )
                choice = input('What do you wish to do: ').strip()
                if choice == '1':
                    self.update_exam(user)
                elif choice == '2':
                    self.view_question(user)
                elif choice == '3':
                    self.edit_question(user)
                elif choice == '4':
                    self.delete_exam(user)
                elif choice == '5':
                    self.staff_dashboard(user)
                else:
                    print('Invalid option. Please enter 1-5.')
                    self.staff_dashboard(user)

            elif choice == '2':
                print(
                    '''
                    1. View student Profile
                    2. Search student profile
                    3. View student result
                    4. Search student result
                    5. Go back
                    '''
                )
                choice = input('What do you wish to do: ').strip()
                if choice == '1':
                    self.view_studentprofile(user)
                elif choice == '2':
                    self.view_studentprofilesearch(user)
                elif choice == '3':
                    self.view_studentresult(user)
                elif choice == '4':
                    self.view_studentresultsearch(user)
                elif choice == '5':
                    self.staff_dashboard(user)
                else:
                    print('Invalid option. Please enter 1-5.')
                    self.staff_dashboard(user)

            elif choice == '3':
                self.home()
            else:
                print('Invalid option. Please enter 1, 2, or 3.')
                self.staff_dashboard(user)

        except KeyboardInterrupt:
            print('\nSession interrupted. Returning to home.')
            self.home()
        except Exception as e:
            print(f'An error occurred: {e}')
            self.staff_dashboard(user)

    def view_studentprofile(self, user):
        try:
            link = self.view_studentuser(user)
            if link['status']:
                print(f"{'Id':<10}{'Email':<25}{'Fullname':<20}{'Role':<15}{'Department':<20}")
                print("-" * 90)
                for u in link['data']:
                    print(f"{u['id']:<10}{u['email']:<25}{u['fullname']:<20}{u['role']:<15}{u['department']:<20}")
            else:
                print(link.get('message', 'No registered students yet.'))
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            self.staff_dashboard(user)


    def view_studentprofilesearch(self, user):
        try:
            search = input('Kindly input the student Matric No/fullname: ').strip().capitalize()
            if not search:
                print('Search term cannot be empty.')
                return self.staff_dashboard(user)

            link = self.view_studentusersearch(user, search)
            if link['status']:
                print(f"{'Id':<10}{'Email':<25}{'Fullname':<20}{'Role':<15}{'Department':<20}")
                print("-" * 90)
                found = False
                for u in link['data']:
                    if search == str(u['id']) or search == u['fullname']:
                        print(f"{u['id']:<10}{u['email']:<25}{u['fullname']:<20}{u['role']:<15}{u['department']:<20}")
                        found = True
                if not found:
                    print('No matching student found.')
            else:
                print(link.get('message', 'No registered students yet.'))
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred during search: {e}')
        finally:
            self.staff_dashboard(user)
        
    def view_studentresultsearch(self, user):
        try:
            search = input('Kindly input the student Matric No/fullname: ').strip().capitalize()
            if not search:
                print('Search term cannot be empty.')
                return self.staff_dashboard(user)

            link = self.view_studentresultsearchh(user, search)
            if link['status']:
                print("=" * 120)
                print(f"{'ID':<5} {'Full Name':<15} {'Student ID':<10} {'Dept':<6} {'Student Dept':<15} {'Score':<8} {'Grade':<15} {'Status':<8} {'Submitted':<20}")
                print("-" * 120)
                found = False
                for i in link['data']:
                    if search == str(i['student_id']) or search == i['fullname']:
                        if i['student_department'] == user['department']:
                            print(f"{i['id']:<5} {str(i['fullname']):<15} {i['student_id']:<10} {i['department']:<6} {str(i['student_department']):<15} {str(i['score']):<8} {i['grade']:<15} {i['status']:<8} {i['time_submitted']}")
                            found = True
                if not found:
                    print('No matching result found.')
                print("=" * 120)
            else:
                print(link.get('message', 'No results yet.'))
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred during search: {e}')
        finally:
            self.staff_dashboard(user)
    
    def view_studentresult(self, user):
        try:
            link = self.view_studentresultt(user)
            if link['status']:
                print("=" * 120)
                print(f"{'ID':<5} {'Full Name':<15} {'Student ID':<10} {'Dept':<6} {'Student Dept':<15} {'Score':<8} {'Grade':<15} {'Status':<8} {'Submitted':<20}")
                print("-" * 120)
                for i in link['data']:
                    status_color = "\033[92m" if i['status'].lower() == "passed" else "\033[91m"
                    reset_color = "\033[0m"
                    print(f"{i['id']:<5} {str(i['fullname']):<15} {i['student_id']:<10} {i['department']:<6} "
                          f"{str(i['student_department']):<15} {str(i['score']):<8} {i['grade']:<15} "
                          f"{status_color}{i['status']:<8}{reset_color} {i['time_submitted']}")
                print("=" * 120)
            else:
                print(link.get('message', 'No results yet.'))
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while viewing results: {e}')
        finally:
            self.staff_dashboard(user)

    

    def update_exam(self, user):
        try:
            deptque = input('Which department question bank do you want to update CSE/CVE/EEE or input back to go back: ').strip().upper()
            if deptque == 'BACK':
                return self.staff_dashboard(user)

            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Only CSE, CVE, or EEE allowed.')
                return self.update_exam(user)

            question = input('Enter question: ').strip()
            if not question:
                print('Question cannot be empty.')
                return self.update_exam(user)

            option_a = input('Enter option A: ').strip()
            option_b = input('Enter option B: ').strip()
            option_c = input('Enter option C: ').strip()
            answer = input('Enter answer: ').strip()

            if not all([option_a, option_b, option_c, answer]):
                print('All options and the answer must be filled in.')
                return self.update_exam(user)

            link = self.create_questions(question, option_a, option_b, option_c, answer, deptque)

            if link['status']:
                if deptque == 'CSE':
                    print(link['message_cse'])
                elif deptque == 'CVE':
                    print(link['message_cve'])
                elif deptque == 'EEE':
                    print(link['message_eee'])
                self.update_exam(user)
            else:
                print(link['message'])
                self.staff_dashboard(user)

        except KeyboardInterrupt:
            print('\nUpdate cancelled.')
            self.staff_dashboard(user)
        except Exception as e:
            print(f'An error occurred while updating exam: {e}')
            self.staff_dashboard(user)
            

    def view_question(self, user):
        try:
            deptque = input('Which department question bank do you want to view (CSE/CVE/EEE): ').strip().upper()
            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Choose CSE, CVE, or EEE.')
                return self.staff_dashboard(user)

            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'No.':<5}{'ID':<5} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)

            if deptque == 'CSE':
                for q in link['csebank']:
                    print(f"{q['display_number']:<5}{q['user_id']:<5}{q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"CSE QUESTION BANK: {len(link['csebank'])} question(s) in total")
            elif deptque == 'CVE':
                for q in link['cvebank']:
                    print(f"{q['display_number']:<5}{q['user_id']:<5}{q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"CVE QUESTION BANK: {len(link['cvebank'])} question(s) in total")
            elif deptque == 'EEE':
                for q in link['eeebank']:
                    print(f"{q['display_number']:<5}{q['user_id']:<5}{q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"EEE QUESTION BANK: {len(link['eeebank'])} question(s) in total")

        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while viewing questions: {e}')
        finally:
            self.staff_dashboard(user)

    def edit_question(self, user):
        try:
            deptque = input('Which department question bank do you want to edit (CSE/CVE/EEE): ').strip().upper()
            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Choose CSE, CVE, or EEE.')
                return self.staff_dashboard(user)

            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)

            bank_key = f'{deptque.lower()}bank'
            for q in link[bank_key]:
                print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"{deptque} QUESTION BANK: {len(link[bank_key])} question(s) in total")

            try:
                choice = int(input('Which Question would you like to edit: ').strip())
            except ValueError:
                print('Invalid input. Please enter a valid question ID number.')
                return self.staff_dashboard(user)

            question = input('Enter new question: ').strip()
            option_a = input('Enter option A: ').strip()
            option_b = input('Enter option B: ').strip()
            option_c = input('Enter option C: ').strip()
            answer = input('Enter answer: ').strip()

            if not all([question, option_a, option_b, option_c, answer]):
                print('All fields must be filled in.')
                return self.staff_dashboard(user)

            linkedit = self.editted_question(question, option_a, option_b, option_c, answer, deptque, choice)
            print(linkedit['message'])

        except KeyboardInterrupt:
            print('\nEdit cancelled.')
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while editing question: {e}')
        finally:
            self.staff_dashboard(user)

    def delete_exam(self, user):
        try:
            deptque = input('Which department question bank do you want to delete (CSE/CVE/EEE): ').strip().upper()
            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Choose CSE, CVE, or EEE.')
                return self.staff_dashboard(user)

            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)

            bank_key = f'{deptque.lower()}bank'
            for q in link[bank_key]:
                print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"{deptque} QUESTION BANK: {len(link[bank_key])} question(s) in total")

            try:
                choice = int(input('Which Question would you like to delete: ').strip())
            except ValueError:
                print('Invalid input. Please enter a valid question ID number.')
                return self.staff_dashboard(user)

            linkedit = self.delete_question(deptque, choice)
            print(linkedit['message'])

        except KeyboardInterrupt:
            print('\nDelete cancelled.')
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while deleting question: {e}')
        finally:
            self.staff_dashboard(user)




#         # ==============ADMIN DASHBOARD=============


    def admin_page(self):
        try:
            choice = getpass.getpass('Go back home: ')
            if choice == '###':
                self.admin_dashboard()
            else:
                self.home()
        except KeyboardInterrupt:
            print('\nCancelled.')
            self.home()
        except Exception as e:
            print(f'An error occurred: {e}')
            self.home()

    def admin_dashboard(self):
        try:
            print('Welcome Admin page')
            print(
                '''
                1. Manage Users
                2. Manage Exams
                3. View Old plain passwords
                4. Reset password
                5. Exit()
                '''
            )

            choice = input('What do you wish to do: ').strip()
            if choice == '1':
                print(
                    '''
                    1. Add users
                    2. View users
                    3. Edit users
                    4. Delete users
                    5. Go back
                    '''
                )
                choice = input('What do you wish to do: ').strip()
                if choice == '1':
                    self.add_user()
                elif choice == '2':
                    self.view()
                elif choice == '3':
                    self.edit_user()
                elif choice == '4':
                    self.delete_userr()
                elif choice == '5':
                    self.admin_dashboard()
                else:
                    print('Invalid option. Please enter 1-5.')
                    self.admin_dashboard()

            elif choice == '2':
                print(
                    '''
                    1. Add exams
                    2. View exams
                    3. Edit exams
                    4. Delete exams
                    5. Go back
                    '''
                )
                choice = input('What do you wish to do: ').strip()
                if choice == '1':
                    self.update_examm()
                elif choice == '2':
                    self.view_questionn()
                elif choice == '3':
                    self.edit_questionn()
                elif choice == '4':
                    self.delete_examm()
                elif choice == '5':
                    self.admin_dashboard()
                else:
                    print('Invalid option. Please enter 1-5.')
                    self.admin_dashboard()

            elif choice == '3':
                self.view_plain_password()
            elif choice == '4':
                self.reset_password_flow()
            elif choice == '5':
                self.home()
            else:
                print('Invalid option. Please enter 1-5.')
                self.admin_dashboard()

        except KeyboardInterrupt:
            print('\nAdmin session interrupted.')
            self.home()
        except Exception as e:
            print(f'An error occurred in admin dashboard: {e}')
            self.admin_dashboard()

    def view_plain_password(self):
        try:
            data = self.view_plain_passwords()
            if not data:
                print('No users found.')
                return self.admin_dashboard()
            print("=" * 60)
            print(f"{'ID':<10}{'Email':<25}{'Password':<20}")
            print("-" * 60)
            for u in data:
                print(f"{u['id']:<10}{u['email']:<25}{u['password']:<20}")
            print("=" * 60)
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            self.admin_dashboard()

            # ====================MANAGE USER===================
    def add_user(self):
        try:
            email = input('Input your mail: ').strip()
            if not email:
                print('Email cannot be empty.')
                return self.admin_dashboard()

            fullname = input('Enter fullname: ').strip().capitalize()
            if not fullname:
                print('Fullname cannot be empty.')
                return self.admin_dashboard()

            role = input(
                        '''
                        Enter role(Student/ Staff):
                        ''').strip().lower()
            if not role:
                print('Role cannot be empty.')
                return self.admin_dashboard()

            department = input('What department are you? CSE/CVE/EEE: ').strip().upper()
            if not department:
                print('Department cannot be empty.')
                return self.admin_dashboard()

            password = input('Enter password: ')
            confirm_password = input('Enter confirm password: ')

            if not password or not confirm_password:
                print('Password fields cannot be empty.')
                return self.admin_dashboard()

            id = random.randint(111111, 999999)
            link = self.register_user(email, fullname, password, confirm_password, role, id, department)

            if link['status']:
                if link['role'] == 'student':
                    print(link['message_student'])
                elif link['role'] == 'staff':
                    print(link['message_staff'])
            else:
                print(link['message'])

        except KeyboardInterrupt:
            print('\nAdd user cancelled.')
        except Exception as e:
            print(f'An error occurred while adding user: {e}')
        finally:
            self.admin_dashboard()
                

    def view(self):
        try:
            link = self.view_user()
            print(f"{'Id':<10}{'Email':<25}{'Fullname':<20}{'Role':<15}{'Department':<20}")
            print("-" * 90)
            for user in link['data']:
                print(f"{user['id']:<10}{user['email']:<25}{user['fullname']:<20}{user['role']:<15}{user['department']:<20}")
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print('No registered Users yet')
            print(e)
        finally:
            self.admin_dashboard()
        
    def edit_user(self):
        try:
            usertype = input('Which User role do you want to edit (student/staff): ').strip().lower()
            if usertype not in ('student', 'staff'):
                print('Invalid user type. Choose student or staff.')
                return self.admin_dashboard()

            link = self.view_userss(usertype)
            if link['status']:
                print("=" * 100)
                print(f"{'USER ID':<8} {'Full Name':<20} {'Email':<25} {'Role':<10} {'Dept':<10}")
                print("-" * 100)
                for q in link['userlist']:
                    print(f"{q['id']:<10}{q['fullname']:<20}{q['email']:<25}{q['role']:<15}{q['department']:<20}")
                print("=" * 100)
                print(f"User list: {len(link['userlist'])} user(s) in total")

                try:
                    choice = int(input('Which user would you like to edit (enter ID): ').strip())
                except ValueError:
                    print('Invalid input. Please enter a valid user ID number.')
                    return self.admin_dashboard()

                email = input('Input your mail: ').strip()
                fullname = input('Enter fullname: ').strip().capitalize()
                role = input('Enter role (student/staff): ').strip().lower()
                department = input('What department are you? CSE/CVE/EEE: ').strip().upper()
                password = input('Enter password: ')
                confirm_password = input('Enter confirm password: ')

                if not all([email, fullname, role, department, password, confirm_password]):
                    print('All fields must be filled in.')
                    return self.admin_dashboard()

                linkedit = self.editted_user(email, fullname, password, confirm_password, role, department, choice, usertype)
                print(linkedit['message'])
            else:
                print('Invalid user type or no users found.')

        except KeyboardInterrupt:
            print('\nEdit user cancelled.')
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while editing user: {e}')
        finally:
            self.admin_dashboard()

    def delete_userr(self):
        try:
            usertype = input('Which User role do you want to delete (student/staff): ').strip().lower()
            if usertype not in ('student', 'staff'):
                print('Invalid user type. Choose student or staff.')
                return self.admin_dashboard()

            link = self.view_userss(usertype)
            if link['status']:
                print("=" * 100)
                print(f"{'USER ID':<8} {'Full Name':<20} {'Email':<25} {'Role':<10} {'Dept':<10}")
                print("-" * 100)
                for q in link['userlist']:
                    print(f"{q['id']:<10}{q['fullname']:<20}{q['email']:<25}{q['role']:<15}{q['department']:<20}")
                print("=" * 100)
                print(f"User list: {len(link['userlist'])} user(s) in total")

                try:
                    choice = int(input('Which user would you like to delete (enter ID): ').strip())
                except ValueError:
                    print('Invalid input. Please enter a valid user ID number.')
                    return self.admin_dashboard()

                linkedit = self.delete_user(choice, usertype)
                if linkedit['status']:
                    print(linkedit['message'])
                else:
                    print(linkedit['message'])
            else:
                print('No users found for that role.')

        except KeyboardInterrupt:
            print('\nDelete user cancelled.')
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while deleting user: {e}')
        finally:
            self.admin_dashboard()


#

            # =====================MANAGE EXAMS======================
    def update_examm(self):
        try:
            deptque = input('Which department question bank do you want to update CSE/CVE/EEE or input back to go back: ').strip().upper()
            if deptque == 'BACK':
                return self.admin_dashboard()

            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Only CSE, CVE, or EEE allowed.')
                return self.update_examm()

            question = input('Enter question: ').strip()
            if not question:
                print('Question cannot be empty.')
                return self.update_examm()

            option_a = input('Enter option A: ').strip()
            option_b = input('Enter option B: ').strip()
            option_c = input('Enter option C: ').strip()
            answer = input('Enter answer: ').strip()

            if not all([option_a, option_b, option_c, answer]):
                print('All options and the answer must be filled in.')
                return self.update_examm()

            link = self.create_questions(question, option_a, option_b, option_c, answer, deptque)

            if link['status']:
                if deptque == 'CSE':
                    print(link['message_cse'])
                elif deptque == 'CVE':
                    print(link['message_cve'])
                elif deptque == 'EEE':
                    print(link['message_eee'])
                self.update_examm()
            else:
                print(link['message'])
                self.admin_dashboard()

        except KeyboardInterrupt:
            print('\nUpdate cancelled.')
            self.admin_dashboard()
        except Exception as e:
            print(f'An error occurred while updating exam: {e}')
            self.admin_dashboard()
                

    def view_questionn(self):
        try:
            deptque = input('Which department question bank do you want to view (CSE/CVE/EEE): ').strip().upper()
            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Choose CSE, CVE, or EEE.')
                return self.admin_dashboard()

            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)

            bank_key = f'{deptque.lower()}bank'
            for q in link[bank_key]:
                print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"{deptque} QUESTION BANK: {len(link[bank_key])} question(s) in total")

        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while viewing questions: {e}')
        finally:
            self.admin_dashboard()

    def edit_questionn(self):
        try:
            deptque = input('Which department question bank do you want to edit (CSE/CVE/EEE): ').strip().upper()
            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Choose CSE, CVE, or EEE.')
                return self.admin_dashboard()

            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)

            bank_key = f'{deptque.lower()}bank'
            for q in link[bank_key]:
                print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"{deptque} QUESTION BANK: {len(link[bank_key])} question(s) in total")

            try:
                choice = int(input('Which Question would you like to edit: ').strip())
            except ValueError:
                print('Invalid input. Please enter a valid question ID number.')
                return self.admin_dashboard()

            question = input('Enter new question: ').strip()
            option_a = input('Enter option A: ').strip()
            option_b = input('Enter option B: ').strip()
            option_c = input('Enter option C: ').strip()
            answer = input('Enter answer: ').strip()

            if not all([question, option_a, option_b, option_c, answer]):
                print('All fields must be filled in.')
                return self.admin_dashboard()

            linkedit = self.editted_question(question, option_a, option_b, option_c, answer, deptque, choice)
            print(linkedit['message'])

        except KeyboardInterrupt:
            print('\nEdit cancelled.')
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while editing question: {e}')
        finally:
            self.admin_dashboard()

    def delete_examm(self):
        try:
            deptque = input('Which department question bank do you want to delete (CSE/CVE/EEE): ').strip().upper()
            if deptque not in ('CSE', 'CVE', 'EEE'):
                print('Invalid department. Choose CSE, CVE, or EEE.')
                return self.admin_dashboard()

            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)

            bank_key = f'{deptque.lower()}bank'
            for q in link[bank_key]:
                print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"{deptque} QUESTION BANK: {len(link[bank_key])} question(s) in total")

            try:
                choice = int(input('Which Question would you like to delete: ').strip())
            except ValueError:
                print('Invalid input. Please enter a valid question ID number.')
                return self.admin_dashboard()

            linkedit = self.delete_question(deptque, choice)
            print(linkedit['message'])

        except KeyboardInterrupt:
            print('\nDelete cancelled.')
        except KeyError as e:
            print(f'Missing data field: {e}')
        except Exception as e:
            print(f'An error occurred while deleting question: {e}')
        finally:
            self.admin_dashboard()

    def reset_password_flow(self):
        try:
            email = input('Enter your registered email: ').strip()
            if not email:
                print('Email cannot be empty.')
                return self.admin_dashboard()

            new_password = getpass.getpass('Enter new password: ')
            confirm_password = getpass.getpass('Confirm new password: ')

            if not new_password or not confirm_password:
                print('Password fields cannot be empty.')
                return self.admin_dashboard()

            link = self.reset_password(email, new_password, confirm_password)
            print(link['message'])

        except KeyboardInterrupt:
            print('\nPassword reset cancelled.')
        except Exception as e:
            print(f'An error occurred during password reset: {e}')
        finally:
            self.admin_dashboard()


try:
    alpha = cbtfront('Alpha Academy')
except KeyboardInterrupt:
    print('\nApplication closed.')
except Exception as e:
    print(f'Failed to start application: {e}')
