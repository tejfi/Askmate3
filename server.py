from flask import Flask, render_template, request, redirect, session, escape, url_for, flash
from flask_bootstrap import Bootstrap
import data_handler, os, bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(16)
Bootstrap(app)
app.config['DEBUG'] = True


@app.route('/logout', methods=['GET'])
def logout():
    if request.method == "GET":
        session.pop('user_name', None)
        return redirect(url_for('index'))


def logged_user_info():
    if 'user_name' in session:
        logged_in = 'Logged in as %s' % escape(session['user_name'])
        return logged_in


@app.route('/logged_in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_name'] = request.form.get('user_name')
        plain_text_password = request.form.get("password")
        questions = data_handler.get_latest_questions()
        hashed_password = data_handler.get_password_by_user(session['user_name'])
        verify = data_handler.verify_password(plain_text_password, hashed_password["password"])
        if 'user_name' in session and verify:
            logged_in = 'Logged in as %s' % escape(session['user_name'])
            flash("Successful Login")
            return render_template("index.html", logged_in=logged_in, questions=questions, verify=verify)

        else:
            flash("Invalid Password or Username")
            return render_template("index.html", questions=questions, verify=verify)


@app.route('/', methods=['POST', 'GET'])
def index():
    logged_in=logged_user_info()
    questions = data_handler.get_latest_questions()
    header = data_handler.get_header()
    if logged_in is None:
        return render_template("index.html", questions=questions, header=header)
    return render_template("index.html", questions=questions, header=header, logged_in=logged_in)



@app.route('/list')
def list():
    logged_in = logged_user_info()
    questions = data_handler.get_questions()
    header = data_handler.get_header()
    return render_template("list.html", questions=questions, header=header, logged_in=logged_in)


@app.route("/search", methods=["GET"])
def search():
    if request.method == "GET":
        post_request = request.args.get('search')
        search = ('%' + post_request + '%')

    questions = data_handler.get_result_by_search(search)
    answer = data_handler.get_answer_by_search(search)
    header = data_handler.get_header()
    if answer == []:
        return render_template("search.html", questions=questions, header=header)
    return render_template("search.html", questions=answer, header=header)


@app.route('/ask-question', methods=['POST', 'GET'])
def ask_question():
    if request.method == 'POST':
        title = request.form.get('title')
        view_number = request.form.get("view_number")
        vote_number = request.form.get("vote_number", type=int)
        message = request.form.get("message")
        image = request.form.get("image")
        user_id = data_handler.get_user_id_by_user_name(session["user_name"])
        data_handler.insert_question_table(view_number, vote_number, title, message, image, user_id['id'])
        return redirect('/')

    questions = data_handler.get_questions()
    header = data_handler.get_header()
    return render_template('add.html', questions=questions, header=header)


@app.route('/question/<id>', methods=['GET', 'POST'])
def display_question(id):
    comments = []
    logged_in=logged_user_info()
    answers = data_handler.get_all_answer(id)
    questions = data_handler.get_all_question(id)
    header = data_handler.get_header()
    answers_header = data_handler.get_answer_header()
    comment_to_question = data_handler.get_comment_by_question_id(id)
    for answer in answers:
        comments.append(data_handler.get_comments_by_answer_id(answer["id"]))
    return render_template('display.html', questions=questions, answers=answers,
                           comment_to_question=comment_to_question, comments=comments,logged_in=logged_in)


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == 'POST':
        vote_number = request.form["vote_number"]
        message = request.form["message"]
        image = request.form["image"]
        data_handler.insert_answer_table(vote_number, question_id, message, image)
        return redirect(url_for("display_question", id=question_id))

    question = data_handler.get_all_question(question_id)
    # for num in question_container:
    #     if num["id"] == int(question_id):
    #         question_number = num
    #         print(num)
    return render_template('add_answer.html', question=question, question_id=question_id)


@app.route('/update/<int:id>/edit', methods=['POST', 'GET'])
def update_answer(id):
    if request.method == "POST":
        message = request.form.get('message')
        image = request.form.get('image')
        question_id = request.form.get('question_id')
        data_handler.update_answer(id, message, image)
        return redirect(url_for('display_question', id=question_id))

    answer = data_handler.get_all_answer_by_id(id)
    return render_template('update.html', id=id, answer=answer)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        message_data = request.form.to_dict()
        message = message_data['message']
        data_handler.add_comment_to_question(question_id, message)
        return redirect(url_for('display_question', id=question_id))

    return render_template('add_comment_to_question.html', question_id=question_id)


@app.route('/comment/<question_id>/delete', methods=['POST'])
def delete_comment(question_id):
    if request.method == 'POST':
        data_handler.delete_comment(question_id)
        return redirect(url_for("display_question", id=question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def comments_on_answers(answer_id):
    answer = data_handler.get_all_answer_by_id(answer_id)
    comments = data_handler.get_comments_by_answer_id(answer_id)
    comments_header = ['Comments:']

    if request.method == 'POST':
        question_id = request.form.get('question_id')
        message = request.form["message"]
        data_handler.insert_comment_table(question_id, answer_id, message)
        return redirect(url_for("display_question", id=question_id, comments=comments))

    return render_template('answer_comments.html', id=answer_id, answer=answer, comments=comments,
                           comments_header=comments_header)


@app.route('/comments/<comment_id>/edit', methods=['GET', 'POST'])
def edit_answer_comment(comment_id):
    if request.method == 'POST':
        question_id = request.form.get('question_id')
        message = request.form.get('message')
        data_handler.edit_answer_comment(message, comment_id)
        return redirect(url_for('display_question', id=question_id))

    question_id = request.form.get('question_id')
    comment = data_handler.get_comment_by_id(comment_id)
    return render_template('edit_answer_comments.html', id=question_id, comment=comment)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        hashed_password = data_handler.hash_password(password)
        existing_user_names = data_handler.get_all_user_names()
        data_handler.add_new_user(user_name, hashed_password)

        return redirect(url_for('index'))

    return render_template('registration.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
