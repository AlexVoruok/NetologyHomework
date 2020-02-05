import psycopg2
from psycopg2 import sql
from pprint import pprint


# Student:
#  id     | integer                  | not null
#  name   | character varying(100)   | not null
#  gpa    | numeric(10,2)            |
#  birth  | timestamp with time zone |
#
# Course:
#  id     | integer                  | not null
#  name   | character varying(100)   | not null

student_fields = {'id': 'integer, primary key, not null',
                  'name': 'character, varying(100), not null',
                  'gpa':  'numeric(10,2)',
                  'birth': 'timestamp with time zone'}

course_fields = ['id integer primary key not null',
                 'name character varying(100) not null']


def create_db():  # создает таблицы

    with psycopg2.connect(dbname='test_db', user='test', password='12345') as conn:
        with conn.cursor() as curs:

            # Student
            curs.execute('''create table Student (id integer primary key not null,
                                        name character varying(100) not null,
                                        gpa numeric(10,2),
                                        birth timestamp with time zone)''')
            print('Таблица Student создана')

            # Course
            curs.execute('''create table Course (id serial primary key not null, 
                            name character varying(100) not null)''')
            print('Таблица Course создана')

            # Student_Course
            curs.execute('''create table Student_Course 
                            (st_id integer REFERENCES Student(id), 
                             course_id integer REFERENCES Course(id),
                             Primary key(st_id, course_id))''')
            print('Таблица Student_Course создана')

    conn.close()


def del_table(*table_name):  # Удаляет таблицы
    with psycopg2.connect(dbname='test_db', user='test', password='12345') as conn:
        with conn.cursor() as curs:
            for table in table_name:
                curs.execute(f"drop table {table} cascade;")
                print(f'таблица {table} удалена')
    conn.close()


def get_students(course_id):  # возвращает студентов определенного курса
    with psycopg2.connect(dbname='test_db', user='test', password='12345') as conn:
        with conn.cursor() as curs:
            curs.execute("""select s.name from Student s join Student_course sc on 
                            s.id = sc.st_id where sc.course_id = %s""", (course_id, ))
            course_students = (curs.fetchall())

            curs.execute("""select name from Course where id = %s""", (course_id, ))
            course_name = curs.fetchall()[0][0]
            print(f'Перечень студентов курса {course_id} {course_name}: ')
            print(course_students, '\n')
    conn.close()


def add_students(course_id, *students):  # создает студентов и записывает их на курс
    for st in students:
        add_student(st)

        with psycopg2.connect(dbname='test_db', user='test', password='12345') as conn:
            with conn.cursor() as curs:

                # проверим не записан ли этот студент уже на этот курс
                curs.execute("SELECT (st_id, course_id) from Student_Course where st_id = %s and course_id = %s",
                             (st['id'], course_id))
                found = curs.fetchall()

                if not found:
                    curs.execute("""insert into Student_Course (st_id, course_id) values(%s, %s)""",
                                 (st['id'], course_id))
                    print(f"Студент {st['name']} записан на курс {course_id}")
                else:
                    print(f"Студент {st['name']} уже ранее был записан на курс {course_id}")


def add_student(student):  # просто создает студента
    with psycopg2.connect(dbname='test_db', user='test', password='12345') as conn:
        with conn.cursor() as curs:

            # проверим нет ли этого студента уже в нашей таблице
            curs.execute("SELECT id from student where id = %s", (student['id'], ))
            found = curs.fetchall()

            if not found:
                curs.execute("""insert into Student (id, name, gpa, birth) values(%s, %s, %s, %s)""",
                             (student['id'], student['name'], student['gpa'], student['birth']))

                print(f"запись о студенте {student['name']} создана")

            else:
                print(f"запись о студенте {student['name']} была создана ранее")


def check_tables():  # Показывает текущий список таблиц
    with psycopg2.connect(dbname='test_db', user='test', password='12345') as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN "
                         "('information_schema','pg_catalog');")
            pprint(curs.fetchall())
    conn.close()


def get_student(student_id):  # Выводит данные о студенте по его D
    with psycopg2.connect(dbname='test_db', user='test', password='12345') as conn:
        with conn.cursor() as curs:
            curs.execute(
                """SELECT (id, name, gpa, birth) FROM student WHERE (id = %s);""", (student_id, ))
            output = curs.fetchall()[0][0]
            pprint(output)
    conn.close()


def add_course(name):  # ДОбавляет курс
    with psycopg2.connect(dbname='test_db', user='test', password='12345') as conn:
        with conn.cursor() as curs:
            curs.execute("""insert into Course (name) values(%s)""", (name, ))

            print(f"Курс {name} создан")


if __name__ == '__main__':
    check_tables()
    create_db()
    # del_table('Student', 'Course', 'Student_Course')
    check_tables()
    print()

    student = {'id': '1',
               'name': 'Виталий',
               'gpa': '4.5',
               'birth': '2000-07-15 08:15:23.5+01'}

    student2 = {'id': '2',
               'name': 'Антон',
               'gpa': '3.5',
               'birth': '2010-04-16 18:14:20.3+01'}

    student3 = {'id': '3',
               'name': 'Миша',
               'gpa': '2',
               'birth': '1960-04-16 18:14:20.8+01'}

    add_course('математика')
    add_course('программирование')
    add_course('кулинария')
    print()

    add_student(student)
    print()

    get_student(1)
    print()

    add_students(1, student, student2)
    print()
    add_students(2, student2, student3)
    print()
    add_students(3, student2)
    print()
    add_students(2, student2)
    print()

    get_students(1)
    get_students(2)
    get_students(3)

