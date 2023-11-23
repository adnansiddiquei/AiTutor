from flask import Flask, jsonify, request
from utils import *
import json
from ast import literal_eval
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd

# Load the dataframe
df = pd.read_pickle('data_full.pkl')
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/question', methods=['GET'])
def get_question():
    # Extract parameters
    df = pd.read_pickle('data_full.pkl')
    lesson_id = request.args.get('lessonId', type=int)
    question_number = request.args.get('questionNumber', type=int)
    
    if lesson_id == 0:
        # Retrieve 10 random questions from the dataframe
        question_ids = df.sample(10)['id'].tolist()

    else:
        df = pd.read_pickle('data_full.pkl')

        # count number of nans in the z score column 
        no_unasked_qs = df['z_scores'].isna().sum()
        prop_answered = no_unasked_qs/len(df)
        prop_answered = np.ceil(prop_answered)
       
        df['final_score'] = df['Q_scores'] * df['s_scores']
        question_ids = df.nlargest(prop_answered, 'final_score')['id'].tolist()

        for i in range(10-prop_answered):
            # select questions from the rows with nan for z score
            question_ids.append(df[df['z_scores'].isna()].sample(1)['id'].tolist()[0])


    for idx,question_id in enumerate(question_ids):
        question_row = df.loc[question_id]
        question = question_row['question']
        answers = question_row['answers']
        correct_answer = 0
        lesson_finished = False

        response = {
            "id": question_id,
            "question": question,
            "answers": answers,
            "correctAnswer": correct_answer,
            "lessonFinished": True if idx==9 else False
    }

    return jsonify(response)

@app.route('/question', methods=['POST'])
def post_question():
    df = pd.read_pickle('data_full.pkl')
    
    # Extract data from request
    data = request.json
    question_id = [entry.get('id') for entry in data]
    answer = [entry.get('answer') for entry in data]
    response_times = [entry.get('responseTime') for entry in data]
    lesson_id = [entry.get('lessonId') for entry in data]


    df = pd.read_pickle(f'data_full_{lesson_id[0]}.pkl')
    df['fact_bool'] = np.random.choice([True, False], df.shape[0], p=[0.2, 0.8])

    
    df = pd.read_pickle(f'data_full_{lesson_id[0]}.pkl')
    df['fact_bool'] = np.random.choice([True, False], df.shape[0], p=[0.2, 0.8])

    # Compute z scores
    current_z_scores = []
    for idx,id_ in enumerate(question_id):
        question_row = df.loc[id_]
        question = question_row['question']
        response = answer[idx]
        response_time = response_times[idx]

        # generate a random column of boolean value for the fact_bool column
        df['fact_bool'] = np.random.choice([True, False], df.shape[0], p=[0.2, 0.8])
        is_fact = bool(question_row['fact_bool']) 
        question_z_scores = question_row['z_scores']
        z_score_new = calc_z_score(question, answer, response, response_time, is_fact)
        question_z_scores.append(z_score_new)
        
        current_z_scores.append(question_z_scores)
    
    # Compute Q scores
    embeddings = df.loc[question_id, 'embedding']
    Q_scores = compute_Q_scores(embeddings, current_z_scores)
    S_scores = get_schedule_scores(df,lesson_id)

    # save Q and S scores
    df.loc[question_id, 'Q_scores'] = Q_scores
    df.loc[question_id, 's_scores'] = S_scores
        
    # save to pickle
    df.to_pickle(f'data_full_{lesson_id[0] + 1}.pkl')

    question_ids = question_id.tolist()
    if question_ids is None:
        return jsonify({'error': 'Lesson ID not found'}), 404

    # Retrieve the questions from the dataframe and concatenate them
    questions = df[df['id'].isin(question_ids)]['question'].tolist()
    questions_str = " ".join(questions)

    # Generate the summary
    summary = generate_summary(questions_str)

    # Generate the summary
    summary = generate_summary(questions_str)

    # save summary as summary txt file
    with open('summary.txt', 'w') as f:
        f.write(summary)
        
    
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
        # read summary from txt file
        with open('summary.txt', 'r') as f:
            summary = f.read()

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
            "x": float(x_coord),  # Convert to native Python float
            "y": float(y_coord),  
            "zScore": float(data['z_scores'][idx][-1]),  
            "category": data['_category'][idx]
        })

    return response_data

@app.route('/visualise', methods=['GET'])
def visualise():
    response_data = prepare_data(df)
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
