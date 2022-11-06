import csv
import overall_engagement
import pandas as pd
import matplotlib.pyplot as plt

# engagements gets discussion data
# engagements predicts an engagement score for each student
# get_engagement_csv cross-checks grades and id with engagement score and id ad puts into csv
# plot will plot the csv data

def obtain_student_grades():
    """
    Obtains grade scorings for each student.

    Returns a dict containing student id and current score.
    """
    students = {}

    with open('data/additional/gradebook.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # All student scores will have LEARNER in the student id
            if "LEARNER" in row['Student']:
                students[row["Student"]] = row["Current Score"]
    
    return students

def obtain_scores():
    """
    Obtains engagement scoring and grade scoring for each student.

    Returns an array of tuples containing engagement and grade scores.
    """
    student_grade_dict = obtain_student_grades()
    student_engagement_dict = overall_engagement.get_engagement_dict(pd.read_csv('data/additional/discussions.csv')) # Subject to change

    scores = []
    
    for student in student_engagement_dict:
        if student in student_grade_dict:
            scores.append((student_engagement_dict[student], student_grade_dict[student]))

    return scores

def write_scores_csv(data):
    """
    Writes engagement and grade scores into a csv file.
    """ 
    with open('src/data/engagement.csv', 'w', newline='') as csv_file:
        fieldnames = ['Engagement Score', 'Grade']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for score in data:
            writer.writerow({'Engagement Score': score[0], 'Grade': score[1] })

def plot_data():
    # """
    # Plots the engagement scores from the data/engagements.csv against overall average grade scores.
    # """
    # engagement_scores = []
    # grades = []
    # # read engagement.csv which will give us Discussion Engagement Score and Grade
    # with open('src/data/engagement.csv', 'r') as csv_file:
    #         plots = csv.reader(csv_file, delimiter = ',')
    #         for row in plots:
    #             engagement_scores.append([0])
    #             grades.append(row[0])
    # plt.scatter(engagement_scores, grades, color = 'g')
    # plt.xlabel('Engagement Score')
    # plt.ylabel('Ages')
    # plt.title('Effectiveness of Canvas Discussion')
    # plt.show()
    df = pd.read_csv("src/data/engagement.csv")
    df.plot(kind='scatter', x='Engagement Score', y='Grade')
    plt.show()

def main():
    data = obtain_scores()
    write_scores_csv(data)
    plot_data()

if __name__ == "__main__":
    main()

