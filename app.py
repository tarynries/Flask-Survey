from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)


RESPONSES_KEY = "responses"

#app.debug = True 
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TO_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []

@app.route('/')
def home_page():
    """Shows home page"""
    return render_template('survey_start.html', survey=survey)

@app.route('/begin', methods=['POST'])
def begin_survey():
    session[RESPONSES_KEY] = []
    return redirect ('/questions/0')


@app.route('/questions/<int:qid>')
def get_questions(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]

    return render_template('question.html', question_num=qid, question=question)

@app.route('/answer', methods=["POST"])
def get_answer():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')

    else: 
        return redirect(f"/questions/{len(responses)}")

@app.route('/complete')
def complete():
    return render_template('comeplete.html')


