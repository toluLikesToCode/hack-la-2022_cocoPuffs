import csv
import pandas as pd
from difflib import SequenceMatcher
import matplotlib as plt
import numpy as np
import sys
import argparse
import overall_engagement

# Get timestamp deadlines as thresholds
# Get the student's engagement score at each threshold (before this assignment due date and after previous assignment due date)
# Plot against their grade on this assignment

def convert_timestamp_to_integer(time):
    """
    Converts a timestamp to an integer value for comparison.

    Returns an integer value representing a timestamp.
    """
    time_stamp = pd.Timestamp(time)
    return int(round(time_stamp.timestamp()))

# Takes in an array of assignment names (same timestamps)
# Output the common longest substring
def get_common_assignment_name(assignments):
    """
    Gets the common assignment name for a list of similarly-named assignments.

    Takes in a list of assignment names.
    Returns a string representing the common assignment name.
    """
    l = len(assignments)
    if l == 0:
        return ""
    first_assignment = assignments[0]
    if l == 1:
        return first_assignment

    for i in range(0, l - 1):
        match = SequenceMatcher(None, assignments[i], assignments[i+1]).find_longest_match()

    return first_assignment[match.a:match.a + match.size]
        
# convert timestamps into integer values for comparisons
def get_time_thresholds():
    """
    Gets the assignment due date timestamps and associated assignments.

    Returns a dict with key = timestamps, and val = assignment name. 
    """
    deadlines = {}

    with open("data/additional/assignments.csv") as csv_file:
        reader = csv.DictReader

        for row in reader:
            time = convert_timestamp_to_integer(row["Due_at"])
            name = row["Name"]
            if time in deadlines:
                if type(deadlines[time]) == list:
                    deadlines[time].append(name)
                else:
                    deadlines[time] = [deadlines[time], name]
            else:
                deadlines[time] = name
        
    for key in deadlines:
        if type(deadlines[key]) == list:
            deadlines[key] = get_common_assignment_name(deadlines[key])

    return deadlines

def get_threshold_scores(actor_id, threshold_timestamps):
    """
    Params: actor_id is a string
            threshold_timestamps is a dict, key = timestamps, value = assignment name

    WE ASSUME THAT threshold_timestamps HAS TIMESTAMP KEYS IN ASCENDING ORDER, I.E., 1, 2, 3 ...
    For the student passed in, compute their engagement score between two successive timestamp keys in
    threshold_timestamps
    Then we get their assignment score at the recent timestamp, match it against assignment name

    Returns a dictionary of key: timestamp threshold, value: (engagement score, assignment score)
    """
    engagement_scores = []
    assignment_scores = []

    discussions_df = pd.read_csv('data/additional/discussions.csv')
    gradebook_df = pd.read_csv('data/additional/gradebook.csv')
    for key in threshold_timestamps:
        index = list(threshold_timestamps).index(key)
        if (index == 0):
            # discussions before first assignment
            key = convert_timestamp_to_integer(key)
            starting_discussions = discussions_df[convert_timestamp_to_integer(discussions_df['timestamp']) <= key]
            engagement_score = overall_engagement.get_engagement(actor_id, starting_discussions)
        else:
            # compute engagement score for the relevant discussions between this key and the last
            # store the engagement scores in an intermediate list
            # discussions between nth assignment and (n+1)th assignment
            before_key = list(threshold_timestamps)[index - 1]
            before_key = convert_timestamp_to_integer(before_key)
            discussions = discussions_df[convert_timestamp_to_integer(discussions_df['timestamp']) <= key and convert_timestamp_to_integer(discussions_df['timestamp']) >= before_key]
            engagement_score = overall_engagement.get_engagement(actor_id, discussions)

        engagement_scores.append(engagement_score)
        # now, get the assignment using the key
        # match the assignment against the first assignment for the actor_id with a non-empty score
        # place the score in intermediate list
        assignment_name: str = threshold_timestamps[key]
        assignments = gradebook_df['actor_id', assignment_name]
        assignment_score = assignments[actor_id]
        assignment_scores.append(assignment_score)
        print("not implemented")
    

    return dict(zip(engagement_scores, assignment_scores))

def plot(threshold_timestamps, score_timestamps):
    """
    Plot engagement score vs grade at certain timestamps.
    """
    labels = []
    engagement_scores = []
    grade_scores = []

    # labels = ['Assignment 1', 'Assignment 2', 'Assignment 3']
    for timestamp in threshold_timestamps:
        labels.append(threshold_timestamps[timestamp])
        engagement_scores.append(score_timestamps[timestamp][0])
        grade_scores.append(score_timestamps[timestamp][1])

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, engagement_scores, width, label='Men')
    rects2 = ax.bar(x + width/2, grade_scores, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Engagement and grade scores')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("student", 
                        help="The id of the student",
                        type=str)
    args = parser.parse_args()

    deadlines = get_time_thresholds()
    scores = get_threshold_scores(args.student, deadlines)
    plot(deadlines, scores)

if __name__ == "__main__":
    main()