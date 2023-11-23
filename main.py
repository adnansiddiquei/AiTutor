from flask import Flask, jsonify, request
from part_5.gpt_explainer import generate_explanation
import json
from ast import literal_eval
import numpy as np
from sklearn.manifold import TSNE
app = Flask(__name__)

@app.route('/lessonSummary', methods=['GET'])
def lesson_summary():
    # Extract parameters from request (if needed)
    lesson_id = request.args.get('lessonId', type=int)

    # Normally, here you'd fetch or compute the summary data
    response = {
        "summary": "Lorem ipsum dolor sit amet..."
    }
    return jsonify(response)

@app.route('/question', methods=['GET'])
def get_question():
    # Extract parameters
    lesson_id = request.args.get('lessonId', type=int)
    question_number = request.args.get('questionNumber', type=int)

    # Fetch or compute the question data
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
    # Extract parameters
    question_id = request.args.get('questionId', type=int)

    # Fetch or compute the explanation
    response = {
        "explanation": "Lorem ipsum dolor..."
    }
    return jsonify(response)

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

def prepare_data(data):
    matrix = np.array(data['embedding'].apply(json.dumps).apply(literal_eval).to_list())
    tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200)
    vis_dims = tsne.fit_transform(matrix)

    # Preparing the response data
    response_data = []
    for idx, (x_coord, y_coord) in enumerate(vis_dims):
        response_data.append({
            "x": x_coord,
            "y": y_coord,
            "zScore": data['z_scores'][idx][-1],  # Assuming the last entry in each array
            "category": data['_category'][idx]
        })

    return response_data

@app.route('/visualise', methods=['GET'])
def visualise():
    response_data = prepare_data(df)
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
