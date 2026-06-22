
 Alpha Academy CBT System


Alpha Academy CBT (Computer-Based Test) System is a Python application designed to manage digital examinations across multiple departments. It integrates with MySQL for persistent storage, uses `bcrypt` for secure password hashing, and provides voice feedback via `pyttsx3`. The system supports role-based access for students, staff, and administrators, enabling exam creation, randomized question delivery, timed assessments, and automated grading. Students benefit from real-time alerts and immediate results, while staff and admins can manage users, monitor performance, and analyze outcomes.  


- Language: Python
- Database: MySQL
- Libraries:  
  - `mysql-connector-python`  
  - `bcrypt`  
  - `pyttsx3`  
  - `getpass`



 Features
- Secure user registration and login with hashed passwords
- Password reset functionality
- Role-based dashboards:
  - Student: 
            take exams, 
            view results, 
            view details
  - Staff:  
            manage exams
                (Update Exam questions,View Exam questions,Edit Exam questions,Delete Exam questions), 
            manage students
                (View student Profile,Search student profile,View student result,Search student result)
  - Admin:  
            manage exams 
                (Update Exam questions,View Exam questions,Edit Exam questions,Delete Exam questions), 
            manage users
                (Add users,View users,Edit users,Delete users), 
            reset passwords, 
            view old passwords (migration only)

- Department-specific exam banks (CSE, CVE, EEE)
- Randomized question order and timed exams
- Voice prompts during exams (start, warnings, time up)


   
- Install dependencies:
   bash
   pip install mysql-connector-python bcrypt pyttsx3

   



 Notes
- Ensure the `user.password` column is `VARCHAR(255)` to store full bcrypt hashes.
- Remove the plain password viewer after migration for security.
- Voice feedback requires Windows SAPI voices (e.g., Microsoft David, Zira).