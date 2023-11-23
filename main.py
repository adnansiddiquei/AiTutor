from flask import Flask, jsonify, request
from utils import *

df = pd.read_pickle('data_full.pkl')
# compute Q scores
embeddings = np.asarray(df['embedding']).reshape(len(df), -1)
# Assuming df['z_scores'] is a column of lists or similar structures
z_scores_list = df['z_scores'].tolist()
max_length = 11
padded_z_scores = []

# Padding each z_score sequence to ensure all are of the same length
for z_score in z_scores_list:
    if len(z_score) < max_length:
        pad_len = max_length - len(z_score)
        padded_z_score = [np.nan]*pad_len + z_score
    else:
        padded_z_score = z_score
    padded_z_scores.append(padded_z_score)

# Converting the list of lists into a 2D numpy array
z_scores_array = np.array(padded_z_scores)
get_schedule_scores(df,z_scores_array,0)


# app = Flask(__name__)

# @app.route('/lessonSummary', methods=['GET'])
# def lesson_summary():
#     # Extract parameters from request (if needed)
#     lesson_id = request.args.get('lessonId', type=int)

#     # Normally, here you'd fetch or compute the summary data
#     response = {
#         "summary": "Lorem ipsum dolor sit amet..."
#     }
#     return jsonify(response)

# @app.route('/question', methods=['GET'])
# def get_question():
#     # Extract parameters
#     lesson_id = request.args.get('lessonId', type=int)
#     question_number = request.args.get('questionNumber', type=int)

#     # Fetch or compute the question data
#     response = {
#         "id": "17",
#         "question": "Which of the following is not a requirement of GIPS for composite construction?",
#         "answers": [
#             "one or more portfolios.",
#             "portfolios selected on an ex-post basis.",
#             "portfolios managed according to a similar investment strategy."
#         ],
#         "correctAnswer": 0,
#         "lessonFinished": True
#     }
#     return jsonify(response)

# @app.route('/question', methods=['POST'])
# def post_question():
#     # Extract data from request
#     data = request.json
#     question_id = data.get('id')
#     answer = data.get('answer')
#     time_taken = data.get('timeTaken')

#     # Process the posted data (e.g., record the answer and time taken)
#     # For this example, we'll just send back a confirmation
#     return jsonify({"message": "Response recorded"})

# @app.route('/explain', methods=['GET'])
# def explain():
#     # Extract parameters
#     question_id = request.args.get('questionId', type=int)

#     # Fetch or compute the explanation
#     response = {
#         "explanation": "Lorem ipsum dolor..."
#     }
#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True)
