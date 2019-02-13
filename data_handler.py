import os, datetime
import database_common
import bcrypt
from datetime import datetime

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_answer = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
header = {'Title': 'Title', 'Message': 'Message', 'Image': 'Image'}
# 'ID': 'ID', 'Submission Time': 'Submission Time', 'View Number': 'View Number', 'Vote Number': 'Vote Number',
DATA_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answers_header = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
DATA_HEADER_ANSWER = ['ID', 'Submission Time', 'Question ID', 'Message', 'Image']


@database_common.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
    """)
    answers = cursor.fetchall()

    return answers


@database_common.connection_handler
def insert_question_table(cursor, view_number, vote_number, title, message, image):
    submission_time = datetime.now()
    cursor.execute("""INSERT INTO question(submission_time,view_number,vote_number, title,message,image)
    VALUES(%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s);
    
    """,
                   {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number,
                    'title': title, 'message': message, 'image': image})


@database_common.connection_handler
def insert_answer_table(cursor, vote_number, question_id, message, image):
    submission_time = datetime.now()
    cursor.execute("""INSERT INTO answer(submission_time,vote_number, question_id,message,image)
       VALUES(%(submission_time)s,%(vote_number)s,%(question_id)s, %(message)s,%(image)s);

       """,
                   {'submission_time': submission_time, 'vote_number': vote_number, 'question_id': question_id,
                    'message': message, 'image': image})


@database_common.connection_handler
def get_result_by_search(cursor, title):
    cursor.execute("""
                            SELECT id,submission_time, view_number, vote_number,title,message FROM question
                            WHERE title LIKE  %(title)s
                             OR message LIKE %(title)s ;
                           """,
                   {'title': title})
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def get_answer_by_search(cursor, title):
    cursor.execute("""
                                SELECT * FROM answer
                                WHERE message LIKE  %(title)s;
                               """,
                   {'title': title})
    result = cursor.fetchall()
    return result


def get_header():
    return header


def get_answer_header():
    return DATA_HEADER_ANSWER


@database_common.connection_handler
def get_latest_questions(cursor):
    cursor.execute("""
                                SELECT * FROM question
                                ORDER BY id DESC 
                                LIMIT 5;
                               """)
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def update_answer(cursor, id, message, image):
    submission_time = datetime.now()
    cursor.execute("""
    UPDATE answer set submission_time=%(submission_time)s, message=%(message)s,image=%(image)s
    WHERE id = %(id)s;
    """, {'id': id, 'submission_time': submission_time, 'message': message, 'image': image})


@database_common.connection_handler
def get_all_question(cursor, id):
    cursor.execute("""
        SELECT * FROM question
        WHERE  id = %(id)s;
        
    """, {'id': id})
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_all_answer(cursor, question_id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE question_id = %(question_id)s;
    
    """, {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def add_comment_to_question(cursor, question_id, message):
    submission_time = datetime.now().isoformat(timespec='seconds')
    edited_count = 0
    cursor.execute("""
                      INSERT INTO comment (question_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s); """,
                   {'question_id': question_id, 'message': message, 'submission_time': submission_time,
                    'edited_count': edited_count})


@database_common.connection_handler
def get_comment_by_question_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id=%(question_id)s;
                    """, {'question_id': id})
    comment = cursor.fetchall()
    return comment


@database_common.connection_handler
def delete_comment(cursor, question_id):
    cursor.execute("""
    DELETE FROM comment WHERE question_id=%(question_id)s;

    """, {'question_id': question_id})


@database_common.connection_handler
def get_all_answer_by_id(cursor, id):
    cursor.execute("""
    SELECT * FROM answer
    WHERE id = %(id)s;
    """, {'id': id})
    answers = cursor.fetchall()

    return answers


@database_common.connection_handler
def get_comments_by_answer_id(cursor, answer_id):
    cursor.execute("""
    SELECT message, answer_id, id,question_id FROM comment
    WHERE answer_id=%(answer_id)s;
    """, {'answer_id': answer_id})
    comments = cursor.fetchall()

    return comments


@database_common.connection_handler
def insert_comment_table(cursor, question_id, answer_id, message):
    submission_time = datetime.now()
    cursor.execute("""INSERT INTO comment(submission_time, question_id, answer_id, message)
       VALUES (%(submission_time)s, %(question_id)s, %(answer_id)s, %(message)s);
       """, {'submission_time': submission_time, 'question_id': question_id, 'answer_id': answer_id,
             'message': message})


@database_common.connection_handler
def edit_answer_comment(cursor, message, id):
    submission_time = datetime.now()
    cursor.execute("""
            UPDATE comment SET message=%(message)s, submission_time=%(submission_time)s
            WHERE id=%(id)s;
        """, {'message': message, 'submission_time': submission_time, 'id': id})


@database_common.connection_handler
def get_comment_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id=%(id)s;
    """, {'id': id})
    comment = cursor.fetchone()
    return comment


@database_common.connection_handler
def add_new_user(cursor, user_name, password):
    registration_date = datetime.now().isoformat(timespec='seconds')
    reputation = 0
    cursor.execute("""
                    INSERT INTO users(user_name, password, registration_date, reputation)
                    VALUES (%(user_name)s, %(password)s, %(registration_date)s, %(reputation)s);
                    """, {'user_name': user_name, 'password': password,
                          'registration_date': registration_date, 'reputation': reputation})


@database_common.connection_handler
def get_all_user_names(cursor):
    cursor.execute("""
                    SELECT user_name FROM users;
                    """)
    user_names = cursor.fetchall()
    return user_names


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)



@database_common.connection_handler
def get_password_by_user(cursor,user_name):
    cursor.execute("""
    SELECT password FROM users
    WHERE user_name = %(user_name)s;
    
    """, {"user_name":user_name})
    password = cursor.fetchone()
    print(password)
    return password
