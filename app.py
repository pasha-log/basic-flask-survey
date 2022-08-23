from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__) 
app.config['SECRET_KEY'] = "something_secret" 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug= DebugToolbarExtension(app) 

responses = []

@app.route('/')
def home_page():
    """Return homepage""" 
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions 
    return render_template('homepage.html', title=title, instructions=instructions) 

@app.route('/questions/<int:quest_index>') 
def show_question(quest_index): 
    """Show yes or no question""" 

    if responses is None:
        # They are trying to skip ahead? I don't think so.
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != quest_index): 
        # Trying to access a question out of order.
        flash(f"Invalid question number: {quest_index}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[quest_index].question
    choice_1 = satisfaction_survey.questions[quest_index].choices[0]
    choice_2 = satisfaction_survey.questions[quest_index].choices[1] 
    return render_template('question.html', question=question, choice_1=choice_1, choice_2=choice_2)

@app.route('/answer', methods=["POST"])
def collect_answer(): 
    """As soon as an answer is submitted, this route is fired off to append to responses"""
    option = request.form['option']      
    responses.append(option) 
    
    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}") 
    
@app.route('/complete')
def completed_survey():
    """This is the page for the end of the survey""" 
    return render_template('completion.html')