from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    questions = data_handler.get_latest_questions()
    header = data_handler.get_header()
    return render_template("index.html", questions=questions, header=header)


@app.route('/list')
def list():
    questions = data_handler.get_questions()
    header = data_handler.get_header()
    return render_template("list.html", questions=questions, header=header)


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
        data_handler.insert_question_table(view_number, vote_number, title, message, image)
        return redirect('/')

    questions = data_handler.get_questions()
    header = data_handler.get_header()
    return render_template('add.html', questions=questions, header=header)


@app.route('/question/<id>', methods=['GET', 'POST'])
def display_question(id):
    comments = []
    answers = data_handler.get_all_answer(id)
    questions = data_handler.get_all_question(id)
    header = data_handler.get_header()
    answers_header = data_handler.get_answer_header()
    comment_to_question = data_handler.get_comment_by_question_id(id)
    for answer in answers:
        comments.append(data_handler.get_comments_by_answer_id(answer["id"]))
        print(comments)
    return render_template('display.html', questions=questions, answers=answers,comment_to_question=comment_to_question, comments=comments)


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
    if request.method=="POST":
        message=request.form.get('message')
        image=request.form.get('image')
        question_id = request.form.get('question_id')
        data_handler.update_answer(id,message,image)
        return redirect(url_for('display_question', id=question_id))

    answer = data_handler.get_all_answer_by_id(id)
    # for line in answer_container:
    #     if line["id"]==int(id):
    #         answer=line
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
        return redirect(url_for("display_question",id=question_id))


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
    print(comment)
    return render_template('edit_answer_comments.html', id=question_id, comment=comment)




if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
