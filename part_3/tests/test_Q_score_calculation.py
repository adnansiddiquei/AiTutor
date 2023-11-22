import numpy as np
from main import cosine_distance, compute_Q_scores
def test_Q_score_calculation():
    """
    Test Q score calculation for a known simples case of a 3x3 embedding matrix with 1 unasked question
    """
    
    embeddings = np.array([[1, 2], [4, 5], [7, 8]])
    z_scores = np.array([1, 0.5, np.nan])
    Q_scores = compute_Q_scores(embeddings, z_scores)
    answers = np.asarray([0.006998255927016391, 0.013996511854032782, 0.4930017440729836])
    
    assert np.amax(np.abs(Q_scores - answers)) < 1e-3, 'test'