"""
Takes in a list of features and computes z score to quantify difficulty of question
"""

def calc_z_score(question, answer, response, response_time, is_fact):
    """
    Calculate the z-score for a given question and response.

    Idea is that if fact based the logic is binary - either you know the answer or you don't.
    If you know set a low z score of 0.1 - answer memorised
    If you don't know set a neutral z score of 0.5 - answer guessed

    If reasoning based, the z score is calculated based on proportion of time spent thinking about the question out of total time taken to answer.
    regardless of true or false. Idea is that if it takes a long time to answer, even if you are correct it was hard for you.


    Over several askings of a question should trigger the memorisation loop where 

    Parameters:
    question (str): The question asked.
    answer (str): The correct answer to the question.
    response (str): The response given by the student.
    response_time (float): The time taken by the student to respond in seconds.
    is_fact (bool): Fact based True or False.

    Returns:
    float: The z-score calculated based on the response time.
    """
    # count number of words in question and adjust response time
    question_length = len(question.split())

    # use an avg reading rate of 200 words per minute
    reading_time = 60 * (question_length / 200)
    understanding_time = response_time - reading_time
    
    # if negative understanding time, question was answered without much thought - answer known or guessed
    if understanding_time < 0:
        understanding_time = 0
        # if wrong, assume answer was guessed and set a neutral z score
        if response != answer:
            return 0.5
        # if correct, assume answer was memorised and set a z score of 0.1
        if response == answer:
            return 0.1

    # if fact_based question and correct answer, assume answer was known and set a neutral z score
    if is_fact:
        if response == answer:
            # add logic here to think about how many times person has seen this
            # rn will just run this till answer is memorised and prev loop is run so z score is 0.1
            return 0.1
        else:
            return 0.5
    
    else:
        # reasoning based question, calculate z score based on time taken to answer
        # if thinking proportion high - question was challenging, not punished for very long vs slightly long
        return understanding_time/response_time


        
    




    
        
    

    

        






