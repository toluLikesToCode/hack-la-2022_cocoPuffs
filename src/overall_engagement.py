import pandas as pd
    
def get_engagement(actor_id: str, data_frame) -> float:
    """
    param actor_id {str} the student id
    
    param data_frame {DataFrame} the data frame to perform the opperations on

    returns {float} the engagemnent score of a specified student
    """
    discussions_df = data_frame
    
    # filtering the df by the relivent actor_id
    filtered_discussions_actor_id = discussions_df[discussions_df['actor_id'] == actor_id ]
    
    #incuding only the discussion topics that have "Assignment" or "Discussion" in the title
    relvant_discussions = filtered_discussions_actor_id[filtered_discussions_actor_id['discussion_topic_title'].str.contains('Assignment|Discussion')]
    
    number_of_posts = len(relvant_discussions.index)
    avg_post_length = relvant_discussions['post_message_length'].mean()
    
    post_weight = 0.7
    len_weight = 0.3
    
    score = (post_weight * number_of_posts) + (len_weight * avg_post_length)
    
    if (type(score) is float):
        return 0
    
    return score

def get_engagement_dict(df):
    """
    returns a dictionary of with scheme {id: str, score: foat}
    """
    student_ids = pd.read_csv('data/additional/gradebook.csv')['Student'][2:]
    result = {}
    for id in student_ids:
        val = get_engagement(id,df)
        result[id] = val
    return result


