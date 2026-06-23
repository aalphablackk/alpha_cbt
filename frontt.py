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

        choice= input('Enter choice: ')
        if choice == '1':
            self.register()
        elif choice == '2':
            self.login()
        # elif choice == '3':
        #     self.view()
        elif choice == '###':
            self.admin_page()
        # elif choice == '3':
        #     self.reset_password_flow()
        elif choice == '3':
            exit()
        
        
            
        # ==============REGISTER DASHBOARD=============

    def register(self):
        email=input('Input your mail: ')
        fullname = input('Enter fullname: ').capitalize()
        role= input(
                    '''
                    Enter role(Student/ Staff):
                    ''').lower()
        department= input('What department are you? CSE/CVE/EEE: ').upper()
        password = getpass.getpass('Enter password: ')
        confirm_password = getpass.getpass('Enter confirm password: ')
        id= random.randint(111111,999999)
        link= self.register_user(email, fullname, password, confirm_password, role, id,department)
        if link['status']:
            if link['role'] == 'student':
                print (link['message_student'])
            elif link['role'] == 'staff':
                print(link['message_staff'])
        else:
            print(link['message'])
        self.home()

        # ==============LOGIN DASHBOARD=============


    def login(self):
        email=input('Input your mail: ')
        password = getpass.getpass('Enter password: ')
        link = self.login_user(email,password)
        try:
            if link['status']:
                user=link['data']
                print(link['message'])
                print(link['login_message'])
                if user['role']=='student':
                    self.student_dashboard(user)
                elif user['role']=='staff':
                    self.staff_dashboard(user)
            else:
                print(link['message'])
                # print(link['error'])
                self.home()
        except Exception as e:
            print(e)
            print('Kindly register before signing in if you are new')
            self.home()




        # ==============STUDENT DASHBOARD=============
    def student_dashboard(self,user):
        try:
            print(
                '''
                1.  Take Exam
                2.  View Result
                3.  View Details
                4.  Logout
                '''
            )
            choice=input('What do you wish to do: ')
            if choice == '1':
                self.take_exam(user)
            if choice == '2':
                # percent=0
                self.view_result(user)
            if choice == '3':
                self.view_details(user)
            if choice == '4':
                self.home()
        except Exception as e:
            print(e)
            print('An error occured')

    def take_exam(self, user):
        engine = pyttsx3.init(driverName='sapi5')  # Windows driver
        engine.setProperty('rate', 180)  # speaking speed
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # default voice
        # engine.say("Your exam starts now. Good luck!")
        # engine.runAndWait()
        deptque = input('Which departmental exam are you writing?: ').upper()
        score = 0
        link = self.load_questions(user, deptque)
        linkkk = self.checkexam(user, deptque)

        if not linkkk['status']:
            print(linkkk['message'])
            self.student_dashboard(user)


        durations = {'CSE': 120, 'CVE': 130, 'EEE': 150}
        exam_duration = durations.get(deptque, 120)

        if (deptque == 'CSE' and len(link['csebank']) == 0) or \
        (deptque == 'CVE' and len(link['cvebank']) == 0) or \
        (deptque == 'EEE' and len(link['eeebank']) == 0):
            print("-" * 60)
            print("There are no questions yet")
            print("-" * 60)
            self.student_dashboard(user)


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
        else:
            print("Invalid department")
            return

        print(f'{len(questions)} question(s) in total')
        engine.say("Your exam starts now. Good luck!")
        engine.runAndWait()

        for q in questions:
            elapsed = time.time() - start_time
            if elapsed >= exam_duration:
                print("\n Time is up! Auto-submitting your exam...")
                engine.say("Time is up. Auto-submitting your exam.")
                engine.runAndWait()
                break

            print(f"Q{q['display_number']}: {q['question']}")
            print(f"Option A: {q['option_a']}")
            print(f"Option B: {q['option_b']}")
            print(f"Option C: {q['option_c']}")
            print("=" * 80)

            remaining = exam_duration - elapsed
            if remaining <= 30:
                print(" 30 seconds left!")
                engine.say("Warning, only thirty seconds left")
                engine.runAndWait()

            print(f" Time left: {int(remaining)} seconds")
            response = input("Type your answer exactly as shown: ").strip().upper()
            if response == q['answer'].upper():
                score += 1

        percent = (score / len(questions)) * 100

        # Grading
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

        # engine.say(f"Well done {user['fullname']}, you {status} with {grade}")
        # engine.runAndWait()

        if 'results_history' not in user:
            user['results_history'] = []
        user['results_history'].append(user['last_score'])

        self.student_dashboard(user)

    # def take_exam(self, user):
    #     # deptque = user['department']
    #     deptque = input('Which departmental exam are you writing?: ').upper()
    #     score = 0
    #     link = self.load_questions(user,deptque)
    #     linkkk=self.checkexam(user,deptque)
    #     if not linkkk['status']:
    #         print(linkkk['message'])
    #         self.student_dashboard(user)
    #     # exam_duration =10
    #     durations = {'CSE': 40, 'CVE': 40, 'EEE': 40}  # seconds
    #     exam_duration = durations.get(deptque, 120)
        
    #     if (deptque == 'CSE' and len(link['csebank']) == 0) or (deptque == 'CVE' and len(link['cvebank']) == 0) or (deptque == 'EEE' and len(link['eeebank']) == 0):
    #             print("-" * 60)
    #             print("There are no questions yet")
    #             print("-" * 60)
    #             self.student_dashboard(user)
    #     # if deptque=='CSE' or deptque=='CVE' or deptque=='EEE':
    #     if deptque == 'CSE':
    #         engine = pyttsx3.init()
    #         engine.say("Your Exam starts now")
    #         engine.runAndWait()
    #         start_time =time.time()
    #         print(link['message_cse'])
    #         print(f'{len(link["csebank"])} question(s) in total')
    #         for q in link['csebank']:
    #             elapsed = time.time() - start_time
    #             if elapsed >= exam_duration:
    #                 print("\n Time is up!  Auto-submitting your exam...")
    #                 break
    #             print(f"Q{q['display_number']}: {q['question']}")
    #             print(f"Option A: {q['option_a']}")
    #             print(f"Option B: {q['option_b']}")
    #             print(f"Option C: {q['option_c']}")
    #             print("=" * 80)
    #             remaining = exam_duration - elapsed
    #             if remaining <= 30:
    #                 print("30 seconds left!")
    #             print(f" Time left: {int(remaining)} seconds")
    #             response = input("Type your answer exactly as shown: ").strip().upper()
    #             if response.strip().upper() == q['answer'].upper():
    #                 score += 1
    #         percent = (score / len(link["csebank"])) * 100
    #         # print(f"Your score: {score}/{len(link['csebank'])} ({percent:.2f}%)")
    #     elif deptque == 'CVE':
    #         engine = pyttsx3.init()
    #         engine.say("Your Exam starts now")
    #         engine.runAndWait()
    #         start_time =time.time()
    #         print(link['message_cve'])
    #         print(f'{len(link["cvebank"])} question(s) in total')
    #         for q in link['cvebank']:
    #             elapsed = time.time() - start_time
    #             if elapsed >= exam_duration:
    #                 print("\n Time is up!  Auto-submitting your exam...")
    #                 break
    #             print(f"Q{q['display_number']}: {q['question']}")
    #             print(f"Option A: {q['option_a']}")
    #             print(f"Option B: {q['option_b']}")
    #             print(f"Option C: {q['option_c']}")
    #             print("=" * 80)
    #             remaining = exam_duration - elapsed
    #             if remaining <= 30:
    #                 print("⚠️ 30 seconds left!")
    #             print(f" Time left: {int(remaining)} seconds")
    #             response = input("Type your answer exactly as shown: ").strip().upper()
    #             if response.strip().upper() == q['answer'].upper():
    #                 score += 1
    #         percent = (score / len(link["cvebank"])) * 100
    #         # print(percent)
    #         # print(f"Your score: {score}/{len(link['cvebank'])} ({percent:.2f}%)")
    #     elif deptque == 'EEE':
    #         engine = pyttsx3.init()
    #         engine.say("Your Exam starts now")
    #         engine.runAndWait()
    #         start_time =time.time()
    #         print(link['message_eee'])
    #         print(f'{len(link["eeebank"])} question(s) in total')
    #         for q in link['eeebank']:
    #             elapsed = time.time() - start_time
    #             if elapsed >= exam_duration:
    #                 print("\n Time is up!  Auto-submitting your exam...")
    #                 break
    #             print(f"Q{q['display_number']}: {q['question']}")
    #             print(f"Option A: {q['option_a']}")
    #             print(f"Option B: {q['option_b']}")
    #             print(f"Option C: {q['option_c']}")
    #             print("=" * 80)
    #             remaining = exam_duration - elapsed
    #             if remaining <= 30:
    #                 print("⚠️ 30 seconds left!")
    #             print(f" Time left: {int(remaining)} seconds")
    #             response = input("Type your answer exactly as shown: ").strip().upper()
    #             if response.strip().upper() == q['answer'].upper():
    #                 score += 1
    #         percent = (score / len(link["eeebank"])) * 100
    #         # print(percent)
    #         # print(f"Your score: {score}/{len(link['eeebank'])} ({percent:.2f}%)")
    #     else:
    #         print("Invalid department")
    #     if 70 <= percent <= 100:
    #         grade = "Grade A"
    #     elif 60 <= percent <= 69:
    #         grade = "Grade B"
    #     elif 50 <= percent <= 59:
    #         grade = "Grade C"
    #     elif 40 <= percent <= 49:
    #         grade = "Grade D"
    #     else:
    #         grade = "Grade E"
    #     status = "Passed" if percent >= 50 else "Failed"
    #     user['last_score'] = {
    #         'percent': percent,
    #         'status': status,
    #         'grade': grade
    #     }
    #     linkk=self.submit_exam(user,percent,deptque,grade,status)
    #     # linkk=self.submit_exam(user)
    #     print(linkk['message'])
    #     if 'results_history' not in user:
    #         user['results_history'] = []
    #     user['results_history'].append(user['last_score'])
    #     self.student_dashboard(user)
    def view_result(self, user):
            link=self.view_resultt(user)
            # print("=" * 80)
            # print(f"{'Full Name':<15} {'Student ID':<10} {'Dept':<6} {'Score':<8} {'Grade':<15} {'Status':<8} {'Submitted':<20}")
            # print("-" * 80)
            # for i in link['result']:
            #     print(f"{str(i['fullname']):<15} {i['student_id']:<10} {i['department']:<6} {str(i['score']):<8} {i['grade']:<15} {i['status']:<8} {i['time_submitted']}")
            # print("=" * 80)
            print("=" * 100)
            print(f"{'No.':<5} {'Full Name':<15} {'Student ID':<10} {'Dept':<6} {'Score':<8} {'Grade':<15} {'Status':<8} {'Submitted':<20}")
            print("-" * 100)
            for i in link['result']:
                status_color = "\033[92m" if i['status'].lower() == "passed" else "\033[91m"
                reset_color = "\033[0m"

                print(f"{i['display_number']:<5} {str(i['fullname']):<15} {i['student_id']:<10} {i['department']:<6} "
                f"{str(i['score']):<8} {i['grade']:<15} {status_color}{i['status']:<8}{reset_color} {i['time_submitted']}")
                # print(f"{i['display_number']:<5} {str(i['fullname']):<15} {i['student_id']:<10} {i['department']:<6} {str(i['score']):<8} {i['grade']:<15} {i['status']:<8} {i['time_submitted']}")
            print("=" * 100)

            self.student_dashboard(user)
    def view_details(self, user):
            link=self.view_detail(user)
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

            self.student_dashboard(user)



#         # ==============STAFF DASHBOARD=============

    def staff_dashboard(self,user):
        try:
            print(
                '''
                1. Manage Exams
                2. Manage Students
                3. Log out()
                '''
            )

            choice=input('What do you wish to do: ')
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
                choice=input('What do you wish to do: ')
                if choice=='1':
                    self.update_exam(user)
                if choice == '2':
                    self.view_question(user)
                if choice == '3':
                    self.edit_question(user)
                if choice == '4':
                    self.delete_exam(user) 
                if choice == '5':
                    self.staff_dashboard(user)
            if choice == '2':
                print(
                    '''
                    1. View student Profile
                    2. Search student profile
                    3. View student result
                    4. Search student result
                    5. Go back
                    '''
                )
                choice=input('What do you wish to do: ')
                if choice == '1':
                    self.view_studentprofile(user)
                if choice == '2':
                    self.view_studentprofilesearch(user)
                if choice == '3':
                    self.view_studentresult(user)
                if choice == '4':
                    self.view_studentresultsearch(user)
                if choice == '5':
                    self.staff_dashboard(user)

            if choice == '3':
                self.home()
        except Exception as e:
            print(e)
            print('An error occured')
            self.staff_dashboard(user)

    def view_studentprofile(self,user):
        try:
            link=self.view_studentuser(user)
            if link['status']:
                print(f"{'Id':<10}{'Email':<25}{'Fullname':<20}{'Role':<15}{'Department':<20}")
                print("-" * 90)
                for user in link['data']:
                    print(f"{user['id']:<10}{user['email']:<25}{user['fullname']:<20}{user['role']:<15}{user['department']:<20}")
            else:
                print('No registered Users yet')
        except Exception as e:
                print(e)
        self.staff_dashboard(user)


    def view_studentprofilesearch(self,user):
        search=input('Kindly input the student Matric No/fullname: ').capitalize()
        try:
            link=self.view_studentusersearch(user,search)
            if link['status']:
                print(f"{'Id':<10}{'Email':<25}{'Fullname':<20}{'Role':<15}{'Department':<20}")
                print("-" * 90)
                for user in link['data']:
                    if search==user['id'] or search ==user['fullname']:
                        print(f"{user['id']:<10}{user['email']:<25}{user['fullname']:<20}{user['role']:<15}{user['department']:<20}")
            else:
                print('No registered Users yet')
        except Exception as e:
                print(e)
        self.staff_dashboard(user)
        
    def view_studentresultsearch(self,user):
        search=input('Kindly input the student Matric No/fullname: ').capitalize()
        try:
            link=self.view_studentresultsearchh(user,search)
            if link['status']:
                print("=" * 120)
                print(f"{'ID':<5} {'Full Name':<15} {'Student ID':<10} {'Dept':<6} {'Student Dept':<15} {'Score':<8} {'Grade':<15} {'Status':<8} {'Submitted':<20}")
                print("-" * 120)
            for i in link['data']:
                if search==i['student_id'] or search ==i['fullname']:
                    if i['student_department']==user['department']:
                        print(f"{i['id']:<5} {str(i['fullname']):<15} {i['student_id']:<10} {i['department']:<6} {str(i['student_department']):<15} {str(i['score']):<8} {i['grade']:<15} {i['status']:<8} {i['time_submitted']}")
            print("=" * 120)
        except Exception as e:
                print(e)
        self.staff_dashboard(user)
    
    def view_studentresult(self,user):
        try:
            link=self.view_studentresultt(user)
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
                # print(f"{i['id']:<5} {str(i['fullname']):<15} {i['student_id']:<10} {i['department']:<6} {str(i['student_department']):<15} {str(i['score']):<8} {i['grade']:<15} {i['status']:<8} {i['time_submitted']}")
            print("=" * 120)
        except Exception as e:
                print(e)
        self.staff_dashboard(user)

    



    def update_exam(self,user):
            try:
                deptque= input('Which department question bank do you want to update CSE/CVE/EEE or input back to go back: ').upper()
                if deptque=='back'.upper():
                    self.staff_dashboard(user)
                # print(f'Welcome {user['fullname']}, Id: {user['id']}')
                question = input('Enter question: ')
                option_a = input('Enter option A: ')
                option_b = input('Enter option B: ')
                option_c = input('Enter option C: ')
                answer = input('Enter answer: ')

                link = self.create_questions(question, option_a, option_b,option_c, answer,deptque)

                if link['status']:
                    if deptque=='CSE':
                        print(link['message_cse'])
                        # print(link['csebank'])
                    elif deptque=='CVE':
                        print(link['message_cve'])
                        # print(link['cvebank'])
                    elif deptque=='EEE':
                        print(link['message_eee'])
                        # print(link['eeebank'])
                    
                    self.update_exam(user)
                else:
                    print(link['message'])
                    self.staff_dashboard(user)
            except Exception as e:
                print(e)
                self.staff_dashboard(user)
                

    def view_question(self,user):
        deptque= input('Which department questiobank do you want to view (CSE/CVE/EEE): ').upper()
        link = self.view_questions(deptque)
        print("=" * 100)
        print(f"{'No.':<5}{'ID':<5} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
        print("-" * 100)

        # Table rows depending on department
        if deptque == 'CSE':
            # print(link['message_cse'])
            for q in link['csebank']:
                print(f"{q['display_number']:<5}{q['user_id']:<5}{q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"CSE QUESTION BANK: {len(link['csebank'])} question(s) in total")

        elif deptque == 'CVE':
            # print(link['message_cve'])
            for q in link['cvebank']:
                print(f"{q['display_number']:<5}{q['user_id']:<5}{q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"CVE QUESTION BANK: {len(link['cvebank'])} question(s) in total")

        elif deptque == 'EEE':
            # print(link['message_eee'])
            for q in link['eeebank']:
                print(f"{q['display_number']:<5}{q['user_id']:<5}{q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"EEE QUESTION BANK: {len(link['eeebank'])} question(s) in total")

        else:
            print("Invalid department")

        self.staff_dashboard(user)

    def edit_question(self, user):
        deptque = input('Which department question bank do you want to edit (CSE/CVE/EEE): ').upper()
        link = self.view_questions(deptque)
        print("=" * 100)
        print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
        print("-" * 100)

        if deptque == 'CSE':
            for q in link['csebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"CSE QUESTION BANK: {len(link['csebank'])} question(s) in total")
            choice = int(input('Which Question would you like to edit: '))
            question = input('Enter new question: ')
            option_a = input('Enter option A: ')
            option_b = input('Enter option B: ')
            option_c = input('Enter option C: ')
            answer = input('Enter answer: ')
            linkedit = self.editted_question(question, option_a, option_b, option_c, answer, deptque, choice)
            print(linkedit['message'])
        elif deptque == 'CVE':
            for q in link['cvebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"CVE QUESTION BANK: {len(link['cvebank'])} question(s) in total")
            choice = int(input('Which Question would you like to edit: '))
            question = input('Enter new question: ')
            option_a = input('Enter option A: ')
            option_b = input('Enter option B: ')
            option_c = input('Enter option C: ')
            answer = input('Enter answer: ')
            linkedit = self.editted_question(question, option_a, option_b, option_c, answer, deptque, choice)
            print(linkedit['message'])
        elif deptque == 'EEE':
            for q in link['eeebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"EEE QUESTION BANK: {len(link['eeebank'])} question(s) in total")
            choice = int(input('Which Question would you like to edit: '))
            question = input('Enter new question: ')
            option_a = input('Enter option A: ')
            option_b = input('Enter option B: ')
            option_c = input('Enter option C: ')
            answer = input('Enter answer: ')
            linkedit = self.editted_question(question, option_a, option_b, option_c, answer, deptque, choice)
            print(linkedit['message'])
        else:
            print("Invalid department")
        self.staff_dashboard(user)


    def delete_exam(self, user):
        deptque = input('Which department question bank do you want to delete (CSE/CVE/EEE): ').upper()
        link = self.view_questions(deptque)
        print("=" * 100)
        print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
        print("-" * 100)
        if deptque == 'CSE':
            for q in link['csebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"CSE QUESTION BANK: {len(link['csebank'])} question(s) in total")
            choice = int(input('Which Question would you like to delete: '))
            linkedit = self.delete_question(deptque, choice)
            print(linkedit['message'])
        elif deptque == 'CVE':
            for q in link['cvebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"CVE QUESTION BANK: {len(link['cvebank'])} question(s) in total")
            choice = int(input('Which Question would you like to delete: '))
            linkedit = self.delete_question(deptque, choice)
            print(linkedit['message'])
        elif deptque == 'EEE':
            for q in link['eeebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
            print("=" * 100)
            print(f"EEE QUESTION BANK: {len(link['eeebank'])} question(s) in total")
            choice = int(input('Which Question would you like to delete: '))
            linkedit = self.delete_question(deptque, choice)
            print(linkedit['message'])
        else:
            print("Invalid department")
        self.staff_dashboard(user)




#         # ==============ADMIN DASHBOARD=============


    def admin_page(self):
            choice= getpass.getpass('Go back home: ')
            if choice=='###':
                self.admin_dashboard()
            else:
                self.home()

    def admin_dashboard(self):
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

        choice=input('What do you wish to do: ')
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
            choice=input('What do you wish to do: ')
            if choice == '1':
                self.add_user()
            if choice == '2':
                self.view()
            if choice == '3':
                self.edit_user()
            if choice == '4':
                self.delete_userr()
            if choice == '5':
                self.admin_dashboard()

        if choice == '2':
            print(
                '''
                1. Add exams
                2. View exams
                3. Edit exams
                4. Delete exams
                5. Go back
                '''
            )
            choice=input('What do you wish to do: ')
            if choice == '1':
                  self.update_examm()
            if choice == '2':
                self.view_questionn()
            if choice == '3':
                self.edit_questionn()
            if choice == '4':
                self.delete_examm()
            if choice == '5':
                self.admin_dashboard()

        if choice == '3':
            self.view_plain_password()
        if choice == '4':
            self.reset_password_flow()
        if choice == '5':
            self.home()
    def view_plain_password(self):
        data = self.view_plain_passwords()
        print("="*60)
        print(f"{'ID':<10}{'Email':<25}{'Password':<20}")
        print("-"*60)
        for u in data:
            print(f"{u['id']:<10}{u['email']:<25}{u['password']:<20}")
        print("="*60)
        self.admin_dashboard()
        # print("⚠️ This is for admin migration only. Remove after hashing.")

            # ====================MANAGE USER===================
    def add_user(self):
        email=input('Input your mail: ')
        fullname = input('Enter fullname: ').capitalize()
        role= input(
                    '''
                    Enter role(Student/ Staff):
                    ''').lower()
        department= input('What department are you? CSE/CVE/EEE: ').upper()
        password = input('Enter password: ')
        confirm_password = input('Enter confirm password: ')
        id= random.randint(111111,999999)
        link= self.register_user(email, fullname, password, confirm_password, role, id,department)
        if link['status']:
            if link['role'] == 'student':
                print (link['message_student'])
            elif link['role'] == 'staff':
                print(link['message_staff'])
        else:
            print(link['message'])
        self.admin_dashboard()
                

    def view(self):
        try:
            link=self.view_user()
            print(f"{'Id':<10}{'Email':<25}{'Fullname':<20}{'Role':<15}{'Department':<20}")
            print("-" * 90)
            # print(link['data'])
            for user in link['data']:
                print(f"{user['id']:<10}{user['email']:<25}{user['fullname']:<20}{user['role']:<15}{user['department']:<20}")
        except Exception as e:
            print('No registered Users yet')
            print(e)
        self.admin_dashboard()
        
    def edit_user(self):
        usertype = input('Which User role do you want to edit (student/staff): ').lower().strip()
        # usertype='student'
        link = self.view_userss(usertype)
        if link['status']:
            print("=" * 100)
            print(f"{'USER ID':<8} {'Full Name':<20} {'Email':<25} {'Role':<10} {'Dept':<10}")
            print("-" * 100)

            # if usertype == 'student':
            for q in link['userlist']:
                    print(f"{q['id']:<10}{q['fullname']:<20}{q['email']:<25}{q['role']:<15}{q['department']:<20}")

            print("=" * 100)
            print(f"User list: {len(link['userlist'])} user(s) in total")
            choice = int(input('Which user would you like to edit (enter ID): '))
            email = input('Input your mail: ')
            fullname = input('Enter fullname: ').capitalize()
            role = input('Enter role (student/staff): ').lower()
            department = input('What department are you? CSE/CVE/EEE: ').upper()
            password = input('Enter password: ')
            confirm_password = input('Enter confirm password: ')

            linkedit = self.editted_user(email, fullname, password,confirm_password, role, department,choice, usertype )
            print(linkedit['message'])
        else:
                print("Invalid user type")

        self.admin_dashboard()

    def delete_userr(self):
        usertype = input('Which User role do you want to edit (student/staff): ').lower().strip()
        # usertype='student'
        link = self.view_userss(usertype)
        if link['status']:
            print("=" * 100)
            print(f"{'USER ID':<8} {'Full Name':<20} {'Email':<25} {'Role':<10} {'Dept':<10}")
            print("-" * 100)

            # if usertype == 'student':
            for q in link['userlist']:
                    print(f"{q['id']:<10}{q['fullname']:<20}{q['email']:<25}{q['role']:<15}{q['department']:<20}")

            print("=" * 100)
            print(f"User list: {len(link['userlist'])} user(s) in total")
            choice = int(input('Which user would you like to edit (enter ID): '))

            linkedit = self.delete_user(choice,usertype)
            if linkedit['status']:
                print(linkedit['message'])
            else:
                print(linkedit['message'])
            self.admin_dashboard()


# 

            # =====================MANAGE EXAMS======================
    def update_examm(self):
                try:
                    deptque= input('Which department question bank do you want to update CSE/CVE/EEE or input back to go back: ').upper()
                    if deptque=='back'.upper():
                        self.admin_dashboard()
                    # print(f'Welcome {user['fullname']}, Id: {user['id']}')
                    question = input('Enter question: ')
                    option_a = input('Enter option A: ')
                    option_b = input('Enter option B: ')
                    option_c = input('Enter option C: ')
                    answer = input('Enter answer: ')

                    link = self.create_questions(question, option_a, option_b,option_c, answer,deptque)

                    if link['status']:
                        if deptque=='CSE':
                            print(link['message_cse'])
                            # print(link['csebank'])
                        elif deptque=='CVE':
                            print(link['message_cve'])
                            # print(link['cvebank'])
                        elif deptque=='EEE':
                            print(link['message_eee'])
                            # print(link['eeebank'])
                        
                        self.update_examm()
                    else:
                        print(link['message'])
                        self.admin_dashboard()
                except Exception as e:
                    print(e)
                    self.admin_dashboard()
                    

    def view_questionn(self):
            deptque= input('Which department questiobank do you want to view (CSE/CVE/EEE): ').upper()
            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)

            # Table rows depending on department
            if deptque == 'CSE':
                # print(link['message_cse'])
                for q in link['csebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"CSE QUESTION BANK: {len(link['csebank'])} question(s) in total")

            elif deptque == 'CVE':
                # print(link['message_cve'])
                for q in link['cvebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"CVE QUESTION BANK: {len(link['cvebank'])} question(s) in total")

            elif deptque == 'EEE':
                # print(link['message_eee'])
                for q in link['eeebank']:
                    print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"EEE QUESTION BANK: {len(link['eeebank'])} question(s) in total")

            else:
                print("Invalid department")

            self.admin_dashboard()
    def edit_questionn(self):
            deptque = input('Which department question bank do you want to edit (CSE/CVE/EEE): ').upper()
            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)

            if deptque == 'CSE':
                for q in link['csebank']:
                        print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"CSE QUESTION BANK: {len(link['csebank'])} question(s) in total")
                choice = int(input('Which Question would you like to edit: '))
                question = input('Enter new question: ')
                option_a = input('Enter option A: ')
                option_b = input('Enter option B: ')
                option_c = input('Enter option C: ')
                answer = input('Enter answer: ')
                linkedit = self.editted_question(question, option_a, option_b, option_c, answer, deptque, choice)
                print(linkedit['message'])
            elif deptque == 'CVE':
                for q in link['cvebank']:
                        print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"CVE QUESTION BANK: {len(link['cvebank'])} question(s) in total")
                choice = int(input('Which Question would you like to edit: '))
                question = input('Enter new question: ')
                option_a = input('Enter option A: ')
                option_b = input('Enter option B: ')
                option_c = input('Enter option C: ')
                answer = input('Enter answer: ')
                linkedit = self.editted_question(question, option_a, option_b, option_c, answer, deptque, choice)
                print(linkedit['message'])
            elif deptque == 'EEE':
                for q in link['eeebank']:
                        print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"EEE QUESTION BANK: {len(link['eeebank'])} question(s) in total")
                choice = int(input('Which Question would you like to edit: '))
                question = input('Enter new question: ')
                option_a = input('Enter option A: ')
                option_b = input('Enter option B: ')
                option_c = input('Enter option C: ')
                answer = input('Enter answer: ')
                linkedit = self.editted_question(question, option_a, option_b, option_c, answer, deptque, choice)
                print(linkedit['message'])
            else:
                print("Invalid department")
            self.admin_dashboard()
    def delete_examm(self):
            deptque = input('Which department question bank do you want to delete (CSE/CVE/EEE): ').upper()
            link = self.view_questions(deptque)
            print("=" * 100)
            print(f"{'Q-ID':<8} {'Question':<30} {'Option A':<15} {'Option B':<15} {'Option C':<15} {'Answer':<10}")
            print("-" * 100)
            if deptque == 'CSE':
                for q in link['csebank']:
                        print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"CSE QUESTION BANK: {len(link['csebank'])} question(s) in total")
                choice = int(input('Which Question would you like to delete: '))
                linkedit = self.delete_question(deptque, choice)
                print(linkedit['message'])
            elif deptque == 'CVE':
                for q in link['cvebank']:
                        print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"CVE QUESTION BANK: {len(link['cvebank'])} question(s) in total")
                choice = int(input('Which Question would you like to delete: '))
                linkedit = self.delete_question(deptque, choice)
                print(linkedit['message'])
            elif deptque == 'EEE':
                for q in link['eeebank']:
                        print(f"{q['user_id']:<8} {q['question']:<30} {q['option_a']:<15} {q['option_b']:<15} {q['option_c']:<15} {q['answer']:<10}")
                print("=" * 100)
                print(f"EEE QUESTION BANK: {len(link['eeebank'])} question(s) in total")
                choice = int(input('Which Question would you like to delete: '))
                linkedit = self.delete_question(deptque, choice)
                print(linkedit['message'])
            else:
                print("Invalid department")
            self.admin_dashboard()
    def reset_password_flow(self):
        email = input('Enter your registered email: ')
        new_password = getpass.getpass('Enter new password: ')
        confirm_password = getpass.getpass('Confirm new password: ')
        link = self.reset_password(email, new_password, confirm_password)

        if link['status']:
            print(link['message'])
        else:
            print(link['message'])

        self.admin_dashboard()


        

alpha = cbtfront('Alpha Academy')

