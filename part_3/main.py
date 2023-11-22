import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
np.random.seed(42)
"""
Script computes Q scores for each question in csv file using embedding matrix and latest column in z score matrix
For each question computes cosine distance of embedding from each other previously answered question (z score not np.nan)
Q_score_i = Sum over j=!i 1/embedding_cosine_dist_i_j * z_score_j 
"""


def cosine_distance(a, b):
    cosine_similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return 1 - cosine_similarity

def compute_Q_scores(embeddings, current_z_scores):
    # compute Q score for each question
        Q_scores = []
        # compute the cosine distance between embedding i and all others
        inv_cosine_similarities = np.zeros((embeddings.shape[0],embeddings.shape[0]))
        for i in range(embeddings.shape[0]):
            # TODO: Make this loop more efficient
            for j in range(0,embeddings.shape[0]):
                if j == i or np.isnan(current_z_scores[j]):
                    inv_cosine_similarities[i,j] = np.nan
                else:
                    d_i_j = cosine_distance(embeddings[i], embeddings[j])
                    inv_cosine_similarities[i,j] = 1/d_i_j
                    inv_cosine_similarities[j,i] = 1/d_i_j

        # normalise inv_cosine_similarities
        max_val = np.nanmax(inv_cosine_similarities)
        min_val = np.nanmin(inv_cosine_similarities)

        normalised_inv_cosine_similarities = (inv_cosine_similarities - min_val)/(max_val - min_val)
        print(normalised_inv_cosine_similarities)
        total_normalised_inv_cosine_similarities = np.nansum(normalised_inv_cosine_similarities)/2
        for i in range(embeddings.shape[0]):
            # compute Q score for question i
            Q_score_i = 0
            for j in range(embeddings.shape[0]):
                if j != i and not np.isnan(current_z_scores[j]):
                    Q_score_i += normalised_inv_cosine_similarities[i,j]/(total_normalised_inv_cosine_similarities) * current_z_scores[j]
            Q_scores.append(Q_score_i)

        return Q_scores

def main():
    parser = argparse.ArgumentParser(description='Process a CSV file.')
    parser.add_argument('--csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('--demo', action='store_true', help='Run the demo')

    args = parser.parse_args()
    if args.demo:
        print('Running the demo')
        # generate a random embeddings matrix and z score matrix
        embeddings = np.random.randn(100, 400)
        current_z_scores = np.random.randn(100)
        no_unasked_qs = 40
        indices = np.random.choice(range(100), no_unasked_qs, replace=False)

        # assign a random subset of current z scores to np.nan
        current_z_scores[indices] = np.nan

        Q_scores = compute_Q_scores(embeddings, current_z_scores)
        
        plt.hist(Q_scores)
        plt.show()

    else:
        # Read the CSV file
        df = pd.read_csv(args.csv_file)

        # Read the embeddings matrix

        # Read the z score matrix


if __name__ == '__main__':
    main()

