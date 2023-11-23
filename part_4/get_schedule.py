import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler
from fsrs_optimizer import lineToTensor, FSRS
import torch
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
# Necessary Input:
# z_score - only for questions that have been asked
# asked questions to put into scheduler

# parameters for FSRS
w = [1.1008, 1.2746, 5.7619, 10.5114, 5.3148, 1.5796, 1.244, 0.003, 1.5741, 0.1741, 1.0137, 2.7279, 0.0114, 0.3071, 0.3981, 0.0, 1.9569]
requestRetention = 0.82  # recommended setting: 0.8 ~ 0.9

# parameters for Anki
graduatingInterval = 1
easyInterval = 4
easyBonus = 1.3
hardInterval = 1.2
intervalModifier = 1
newInterval = 0
minimumInterval = 1
leechThreshold = 8
leechSuspend = False

# common parameters
maximumInterval = 36500
new_cards_limits = 20
review_limits = 400
max_time_limts = 10000
learn_days = 50

# smooth curves
moving_average_period = 14

# Set it to True if you don't want the optimizer to use the review logs from suspended cards.
filter_out_suspended_cards = False

# Red: 1, Orange: 2, Green: 3, Blue: 4, Pink: 5, Turquoise: 6, Purple: 7
# Set it to [1, 2] if you don't want the optimizer to use the review logs from cards with red or orange flag.
filter_out_flags = []


def get_schedule_scores(df, date):
    deck_size = len(df)
    def calculate_review_duration(states, times):
        if states[-1] != 2:
            return 5
        else:
            # Find the most recent transition to state 2 from either 1 or 3
            for i in range(len(states) - 1, 0, -1):
                if states[i] == 2 and (states[i - 1] == 1 or states[i - 1] == 3):
                    return times[i] - times[i - 1]
            return 5  # Default value if no valid transition is found

    # Apply the function to each row
    df['review_duration'] = [calculate_review_duration(s, t) for s, t in zip(df['review_state'], df['review_time'])]

    # Define the bins for the intervals
    bins = [0.25, 0.5, 0.75]

    # Use numpy's digitize method to convert z_scores to review_rating
    df['review_rating'] = np.digitize(df['z_scores'], bins) + 1
    df['review_rating'] = 5 - df['review_rating']
    df['review_time_curr'] = df['review_time'].apply(lambda x: x[-1])
    df['review_state_curr'] = df['review_state'].apply(lambda x: x[-1])
    New = 0
    Learning = 1
    Review = 2
    Relearning = 3

    df.sort_values(by=["id", "review_time_curr"], inplace=True, ignore_index=True)


    recall_card_revlog = df[
        (df["review_state_curr"] == Review) & (df["review_rating"].isin([2, 3, 4]))
    ]
    review_rating_prob = np.zeros(3)
    review_rating_prob[recall_card_revlog["review_rating"].value_counts().index - 2] = (
        recall_card_revlog["review_rating"].value_counts()
        / recall_card_revlog["review_rating"].count()
    )
    random_array = np.random.rand(4)
    random_array /= random_array.sum()
    first_rating_prob = random_array


    df["review_state_curr"] = df["review_state_curr"].map(
        lambda x: x if x != New else Learning)

    recall_costs = np.zeros(3)
    recall_costs_df = recall_card_revlog.groupby(by="review_rating")[
        "review_duration"
    ].mean()
    recall_costs[recall_costs_df.index - 2] = recall_costs_df / 1000

    state_sequence = np.array(df["review_state_curr"])
    duration_sequence = np.array(df["review_duration"])
    learn_cost = round(
        df[df["review_state_curr"] == Learning]["review_duration"].sum()
        / len(df["id"].unique())
        / 1000,
        1,
    )

    state_block = dict()
    state_count = dict()
    state_duration = dict()
    last_state = state_sequence[0]
    state_block[last_state] = 1
    state_count[last_state] = 1
    state_duration[last_state] = duration_sequence[0]
    for i, state in enumerate(state_sequence[1:]):
        state_count[state] = state_count.setdefault(state, 0) + 1
        state_duration[state] = state_duration.setdefault(
            state, 0) + duration_sequence[i]
        if state != last_state:
            state_block[state] = state_block.setdefault(state, 0) + 1
        last_state = state

    recall_cost = round(state_duration[Review] / state_count[Review] / 1000, 1)

    if Relearning in state_count and Relearning in state_block:
        forget_cost = round(
            state_duration[Relearning] /
            state_block[Relearning] / 1000 + recall_cost,
            1,
        )

    def generate_rating(review_type):
        if review_type == "new":
            return np.random.choice([1, 2, 3, 4], p=first_rating_prob)
        elif review_type == "recall":
            return np.random.choice([2, 3, 4], p=review_rating_prob)

    class Collection:
        def __init__(self):
            self.model = FSRS(w)
            self.model.eval()

        def states(self, t_history, r_history):
            with torch.no_grad():
                line_tensor = lineToTensor(
                    list(zip([str(t_history)], [str(r_history)]))[0]
                ).unsqueeze(1)
                output_t = self.model(line_tensor)
                return output_t[-1][0]

        def next_states(self, states, t, r):
            with torch.no_grad():
                return self.model.step(torch.FloatTensor([[t, r]]), states.unsqueeze(0))[0]

        def init(self, idx):
            t = df["review_time_curr"][idx]
            r = df["review_rating"][idx]
            p = round(first_rating_prob[r - 1], 2)
            new_states = self.states(t, r)
            return r, t, p, new_states


    feature_list = [
        "id",
        "difficulty",
        "stability",
        "retrievability",
        "delta_t",
        "reps",
        "lapses",
        "last_date",
        "due",
        "r_history",
        "t_history",
        "p_history",
        "states",
        "time",
        "factor",
    ]
    field_map = {key: i for i, key in enumerate(feature_list)}


    def fsrs4anki_scheduler(stability):
        def constrain_interval(stability):
            if stability > 0:
                return min(
                    max(1, round(9 * stability * (1 / requestRetention - 1))),
                    maximumInterval,
                )
            else:
                return 1

        interval = constrain_interval(stability)
        return interval


    def scheduler(fsrs_inputs):
            return fsrs4anki_scheduler(fsrs_inputs), 2.5

    #for scheduler_name in ("anki", "fsrs"):
    for scheduler_name in ["fsrs"]:
        new_card_per_day = np.array([0] * learn_days)
        new_card_per_day_average_per_period = np.array([0.0] * learn_days)
        review_card_per_day = np.array([0.0] * learn_days)
        review_card_per_day_average_per_period = np.array([0.0] * learn_days)
        time_per_day = np.array([0.0] * learn_days)
        time_per_day_average_per_period = np.array([0.0] * learn_days)
        learned_per_day = np.array([0.0] * learn_days)
        retention_per_day = np.array([0.0] * learn_days)
        expected_memorization_per_day = np.array([0.0] * learn_days)

        card = pd.DataFrame(
            np.zeros((deck_size, len(feature_list))),
            index=range(deck_size),
            columns=feature_list,
        )
        card["id"] = df["id"]
        card["states"] = card["states"].astype(object)
        card['reps'] = df['review_state'].apply(lambda x: len(x))
        card["lapses"] = 0
        card["due"] = learn_days
        card["last_date"] = df["review_time"].apply(lambda x: x[-1])
        
        student = Collection()
        random.seed(2022)
        # do 1 step:
        day = date
        reviewed = 0
        learned = 0
        review_time_today = 0
        learn_time_today = 0

        card["delta_t"] = day - card["last_date"]
        card["retrievability"] = np.power(
            1 + card["delta_t"] / (9 * card["stability"]), -1
        )
        need_learn = card[card["stability"] == 0]

        for idx in need_learn.index:
            if (
                learned >= new_cards_limits
                or review_time_today + learn_time_today >= max_time_limts
            ):
                break
            learned += 1
            learn_time_today += learn_cost
            #card.iat[idx, field_map["last_date"]] = day

            #card.iat[idx, field_map["reps"]] = 1
            #card.iat[idx, field_map["lapses"]] = 0

            r, t, p, new_states = student.init(idx)
            new_stability = float(new_states[0])
            new_difficulty = float(new_states[1])
            card['r_history'] = card['r_history'].astype(object)
            card['t_history'] = card['t_history'].astype(object)
            card['p_history'] = card['p_history'].astype(object)
            card.iat[idx, field_map["r_history"]] = str(r)
            card.iat[idx, field_map["t_history"]] = str(t)
            card.iat[idx, field_map["p_history"]] = str(p)
            card.iat[idx, field_map["stability"]] = new_stability
            card.iat[idx, field_map["difficulty"]] = new_difficulty
            card.iat[idx, field_map["states"]] = new_states

            delta_t, factor = scheduler(new_stability)
            card.iat[idx, field_map["due"]] = day + delta_t
            #card.iat[idx, field_map["due"]] = day + delta_t
            card.iat[idx, field_map["factor"]] = factor

            card.iat[idx, field_map["time"]] = learn_cost


        new_card_per_day[day] = learned
        review_card_per_day[day] = reviewed
        learned_per_day[day] = learned_per_day[day - 1] + learned
        time_per_day[day] = review_time_today + learn_time_today
        expected_memorization_per_day[day] = sum(
            card[card["retrievability"] > 0]["retrievability"]
        )

        if day >= moving_average_period:
            new_card_per_day_average_per_period[day] = np.true_divide(
                new_card_per_day[day - moving_average_period: day].sum(),
                moving_average_period,
            )
            review_card_per_day_average_per_period[day] = np.true_divide(
                review_card_per_day[day - moving_average_period: day].sum(),
                moving_average_period,
            )
            time_per_day_average_per_period[day] = np.true_divide(
                time_per_day[day - moving_average_period: day].sum(),
                moving_average_period,
            )
        else:
            new_card_per_day_average_per_period[day] = np.true_divide(
                new_card_per_day[: day + 1].sum(), day + 1
            )
            review_card_per_day_average_per_period[day] = np.true_divide(
                review_card_per_day[: day + 1].sum(), day + 1
            )
            time_per_day_average_per_period[day] = np.true_divide(
                time_per_day[: day + 1].sum(), day + 1
            )
    scaler = MinMaxScaler(feature_range=(0, 1))
    card['schedule_score'] = scaler.fit_transform(card[['due']])

    # Inverting the values so that lower 'due' values are closer to 1
    card['schedule_score'] = 1 - card['schedule_score']

    # Returning the DataFrame with 'id' and 'schedule_score'
    result = card[['id', 'schedule_score']]
    return result