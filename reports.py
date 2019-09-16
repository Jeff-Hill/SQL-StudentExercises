import sqlite3

class Student():
    # Since the data you are retrieving from the database represents students, the next step in the process
    #  is to create a Python class named Student so that there is context for the data in your code.
    # For example, with the code you have now, every time you wanted to access the last name of the student, you would have to use the student[5] syntax.

    def __init__(self, id, first, last, handle, cohort):
        self.id = id
        self.first_name = first
        self.last_name = last
        self.slack_handle = handle
        self.cohort = cohort

    # Now you can use the __repr__ dunder method to provide a default string representation of a student.
    def __repr__(self):
        return f'{self.first_name} {self.last_name} is in {self.cohort}'

class Cohort():
    def __init__(self, id, name):
        self.id = id
        self.Name = name

    def __repr__(self):
        return f'Id {self.id} represents {self.Name}'

class Exercise():
    def __init__(self, id, name, language):
        self.id = id
        self.exercise = name
        self.language = language

    def __repr__(self):
        return f'Id {self.id} is the exercise {self.exercise} using the {self.language} language'

class Instructor():
    def __init__(self, id, first, last, handle, specialty, cohort):
        self.id = id
        self.first_name = first
        self.last_name = last
        self.slack_handle = handle
        self.specialty = specialty
        self.cohort = cohort

    def __repr__(self):
        return f'The instructor {self.first_name} {self.last_name} has the talent of {self.specialty} and teaches {self.cohort}'

class StudentExerciseReports():

    """Methods for reports on the Student Exercises database"""
    # The function assigned to the row_factory property must take two arguments - the cursor, and the current row of data.
    # It must return something. In your case, it will return a new instance of student. Add the create_student() method below to your report class.
    # def create_student(self, cursor, row):
    #     return Student(row[1], row[2], row[3], row[5])

    def __init__(self):
        self.db_path = "/Users/jeffh/workspace/python/StudentExercises/studex.db"


    def all_students(self):

        """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            # Then assign the create_student function to the row_factory method of the database connection.
            # conn.row_factory = self.create_student

            # You can delete the create_student() function and define it as a lambda instead.

            conn.row_factory = lambda cursor, row: Student(
                row[0], row[1], row[2], row[3], row[5]
            )

            db_cursor = conn.cursor()

            db_cursor.execute("""
            select s.Id,
                s.FirstName,
                s.LastName,
                s.SlackHandle,
                s.CohortId,
                c.Name
            from Student s
            join Cohort c on s.CohortId = c.Id
            order by s.CohortId
            """)

            all_students = db_cursor.fetchall()
            # Use the following code to just display the first name (second column), last name (third column), and cohort name (sixth column).
            # for student in all_students:
            #     print(f'{student[1]} {student[2]} is in {student[5]}. {student[1]}s slackhandle is {student[3]}')

            # Now when you run the fetchall() method, you will end up with a list of Student objects instead of a list of tuples.
            # This means that you can access those properties when displaying them.
            # for student in all_students:
            #     print(f'{student.first_name} {student.last_name} is in {student.cohort}')

            # Since that is how you were printing out the student information when looping over the database results, you can replace the loop above
            # With this straightforward loop...
            for student in all_students:
                print(student)


    def all_cohorts(self):

        with sqlite3.connect(self.db_path) as conn:

            conn.row_factory = lambda cursor, row: Cohort(
                row[0], row[1]
            )

            db_cursor = conn.cursor()

            db_cursor.execute("""
            select c.Id,
                c.Name
            from Cohort c
            """)

            all_cohorts = db_cursor.fetchall()

            for cohort in all_cohorts:
                print(cohort)

    def all_exercises(self):

        with sqlite3.connect(self.db_path) as conn:

            conn.row_factory = lambda cursor, row: Exercise(
                row[0], row[1], row[2]
            )

            db_cursor = conn.cursor()

            db_cursor.execute("""
            select e.id,
                e.ExerciseName,
                e.ExerciseLanguage
            from Exercise e
            where e.ExerciseLanguage = "React"

            """)

            all_exercises = db_cursor.fetchall()

            for exercise in all_exercises:
                print(exercise)

    def all_instructors(self):

        with sqlite3.connect(self.db_path) as conn:

            conn.row_factory = lambda cursor, row: Instructor(
                row[0], row[1], row[2], row[3], row[4], row[6],
            )

            db_cursor = conn.cursor()

            db_cursor.execute("""
            select i.id,
                i.FirstName,
                i.LastName,
                i.SlackHandle,
                i.Specialty,
                i.CohortId,
                c.Name

            from Instructor i
            join Cohort c on i.CohortId = c.Id
            order by i.CohortId

            """)

            all_instructors = db_cursor.fetchall()

            for instructor in all_instructors:
                print(instructor)

    def student_exercises(self):

        exercises = dict()

        with sqlite3.connect(self.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
                select
                    e.Id ExerciseId,
                    e.ExerciseName,
                    s.Id,
                    s.FirstName,
                    s.LastName
                from Exercise e
                join StudentExercise se on se.ExerciseId = e.Id
                join Student s on s.Id = se.StudentId
            """)

            dataset = db_cursor.fetchall()
        # Then start iterating over the rows in the data set, and assign all rows to a variable.

        for row in dataset:
            exercise_id = row[0]
            exercise_name = row[1]
            student_id = row[2]
            student_name = f'{row[3]} {row[4]}'

        # Then you start using the dictionary. For each row, you are going to determine if the dictionary has the
        # current exercise's name as a key. If it doesn't have the key yet, you will create it and put the student's
        # name in a list. If it already has the key, you will append to the list of students.

            if exercise_name not in exercises:
                exercises[exercise_name] = [student_name]
            else:
                exercises[exercise_name].append(student_name)
        print(exercises)

        # Once the dictionary is built, then you can iterate all of the items in it.
        # When you access the items() in a dictionary, you have to define a variable to hold the key, and
        # one to hold the value in the for loop.
        for exercise_name, students in exercises.items():
            print(exercise_name)
            for student in students:
                print(f'\t* {student}')

    def student_workload(self):

        workload = dict()

        with sqlite3.connect(self.db_path) as conn:
            db_cursor = conn.cursor()


            db_cursor.execute("""
                    select
                        s.Id StudentId,
                        s.FirstName,
                        s.LastName,
                        e.Id,
                        e.ExerciseName
                    from Student s
                    join StudentExercise se on se.StudentId = s.Id
                    join Exercise e on e.Id = se.ExerciseId
                    """)

            dataset = db_cursor.fetchall()

    # Then start iterating over the rows in the data set, and assign all rows to a variable.

        for row in dataset:
            student_id = row[0]
            student_name = f'{row[1]} {row[2]}'
            student_exercise_id = row[3]
            exercise_name = row[4]

        # Then you start using the dictionary. For each row, you are going to determine if the dictionary has the
        # current exercise's name as a key. If it doesn't have the key yet, you will create it and put the student's
        # name in a list. If it already has the key, you will append to the list of students.

            if student_name not in workload:
                workload[student_name] = [exercise_name]
            else:
                workload[student_name].append(exercise_name)
        print(workload)

        for student_name, exercises in workload.items():
            print(student_name)
            for exercise in exercises:
                print(f'\t* {exercise}')

reports = StudentExerciseReports()
# reports.all_students()
# reports.all_cohorts()
# reports.all_exercises()
# reports.all_instructors()
reports.student_exercises()
reports.student_workload()

# Now you have a Student class that you can use to generate a new object, with contextual properties,
# for interacting with student data. You would create a new instance like so.
# student = Student(1, 'Bart', 'Simpson', '@bart', 'Cohort 8')
# print(f'{student.first_name} {student.last_name} is in {student.cohort}')