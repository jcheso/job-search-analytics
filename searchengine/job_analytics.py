# TODO: Exception control
# TODO: Find a way to remove recruiting agencies from companies hiring?
# TODO: Add number of jobs next to companies in search results

from os import terminal_size
import pandas as pd
from textblob import TextBlob


def get_job_analytics(jobs, job, location):

    # Capitalise search results
    job = job.capitalize()
    location = location.capitalize()

    # Drop duplicate job listings
    jobs.drop_duplicates(inplace=True, ignore_index=True)

    # Convert salaries to numeric data format
    jobs['salary_max'] = pd.to_numeric(jobs['salary_max'])
    jobs['salary_min'] = pd.to_numeric(jobs['salary_min'])

    # Filter out jobs without yearly salary listed
    jobs_salary = jobs.loc[(jobs['salary_min'] > 0) &
                           (jobs['salary_type'] == 'Y')]

    # Set currency and calculate average salary
    currency = jobs_salary['salary_currency_code']. value_counts().idxmax()
    average_pay_min = int(jobs_salary['salary_min'].mean())
    average_pay_max = int(jobs_salary['salary_max'].mean())

    # Calculate the most frequent job location
    number_of_jobs = len(jobs['title'])
    most_frequent_location = jobs['locations'].value_counts().idxmax()

    # Calculate the companies with the most job listings
    count_companies = jobs['company'].value_counts()
    top_companies_list = count_companies.index.to_list()
    top_companies_no = count_companies.to_list()
    companies_df = pd.DataFrame()
    companies_df['name'] = top_companies_list
    companies_df['jobs'] = top_companies_no
    top_companies = companies_df[companies_df.name != '']
    top_companies = top_companies.values.tolist()

    # Calculate the highest occuring key words in the job title and description
    def bag_of_words(column):
        rows = range(len(jobs.index))
        temp_bag = []
        new_bag = []
        for row in rows:
            temp_str = jobs[column][row]
            blob = TextBlob(temp_str)
            blob_parsed = blob.noun_phrases
            temp_bag.append(blob_parsed)

        for list in temp_bag:
            if len(list) > 1:
                for word in list:
                    new_words = word.split(" ")
                    for new_word in new_words:
                        new_bag.append(new_word)
            elif len(list) == 1:
                list_blob = TextBlob(str(list))
                words = list_blob.words
                for new_word in words:
                    new_word = new_word.strip("'")
                    new_bag.append(new_word)
        return new_bag

    bag_of_words_title = bag_of_words('title')
    bag_of_words_descript = bag_of_words('description')
    df_of_words = pd.DataFrame(bag_of_words_title)
    df_of_words.append(bag_of_words_descript)
    df_of_words.columns = ['words']

    search_terms = job.split() +location.split()
    for term in search_terms:
        df_of_words = df_of_words[df_of_words.words != term.lower()]
    df_of_words = df_of_words[df_of_words.words != '']
    word_count = df_of_words.value_counts()
    top_word_count = word_count.to_list()
    top_words = word_count.index.to_list()
    words_df = pd.DataFrame()
    words_df['word'] = top_words
    words_df['count'] = top_word_count
    top_words = words_df.values.tolist()

    return(number_of_jobs, average_pay_min, average_pay_max, most_frequent_location, top_companies, currency, top_words, job, location)
