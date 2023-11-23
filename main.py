from flask import Flask, jsonify, request
from utils import *

# Load the dataframe
df = pd.read_pickle('data_full.pkl')

app = Flask(__name__)


@app.route('/question', methods=['GET'])
def get_question():
    # Extract parameters
    lesson_id = request.args.get('lessonId', type=int)
    question_number = request.args.get('questionNumber', type=int)
    
    question = df.loc[question_number] 
    response = {
        "id": "17",
        "question": "Which of the following is not a requirement of GIPS for composite construction?",
        "answers": [
            "one or more portfolios.",
            "portfolios selected on an ex-post basis.",
            "portfolios managed according to a similar investment strategy."
        ],
        "correctAnswer": 0,
        "lessonFinished": True
    }

    return jsonify(response)

@app.route('/question', methods=['POST'])
def post_question():
    # Extract data from request
    data = request.json
    question_id = data.get('id')
    answer = data.get('answer')
    time_taken = data.get('timeTaken')

    # Process the posted data (e.g., record the answer and time taken)
    # For this example, we'll just send back a confirmation
    return jsonify({"message": "Response recorded"})


@app.route('/explain', methods=['GET'])
def explain():
    try:
        # Extract questionId from query parameters
        question_id = request.args.get('questionId', type=int)

        # Retrieve the question from the dataframe
        if question_id in df.index:
            question = df.loc[question_id, 'question']
        else:
            return jsonify({'error': 'Question ID not found'}), 404

        # Generate the explanation
        explanation = generate_explanation(question)

        # Return the explanation in the response
        return jsonify({'explanation': explanation})
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({'error': str(e)}), 500

@app.route('/lessonSummary', methods=['GET'])
def lesson_summary():
    try:
        # Extract lessonId from query parameters
        lesson_id = request.args.get('lessonId', type=int)

        # Retrieve the list of question IDs for the given lesson ID
        question_ids = lesson_questions.get(lesson_id)
        if question_ids is None:
            return jsonify({'error': 'Lesson ID not found'}), 404

        # Retrieve the questions from the dataframe and concatenate them
        questions = df[df['id'].isin(question_ids)]['question'].tolist()
        questions_str = " ".join(questions)

        # Generate the summary
        summary = generate_summary(questions_str)

        # Return the summary in the response
        return jsonify({'summary': summary})
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
