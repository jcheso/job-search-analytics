# TODO: Exception control
# TODO: Filter out empty listings in top companies
# TODO: Find a way to remove recruiting agencies from companies hiring?
# TODO: Add number of jobs next to companies in search results

import pandas as pd
from textblob import TextBlob

def get_job_analytics(jobs, job, location):
    #Tidy up search results
    job = job.capitalize()
    location = location.capitalize()
    
    jobs.drop_duplicates(inplace=True, ignore_index=True)

    # Convert salaries to numeric data format
    jobs['salary_max'] = pd.to_numeric(jobs['salary_max'])
    jobs['salary_min'] = pd.to_numeric(jobs['salary_min'])

    # Filter out jobs without yearly salary listed
    jobs_salary = jobs.loc[(jobs['salary_min'] > 0) & (jobs['salary_type'] == 'Y')]

    # Calculate job pay analytics
    currency = jobs_salary['salary_currency_code']. value_counts().idxmax()
    average_pay_min = int(jobs_salary['salary_min'].mean())
    average_pay_max = int(jobs_salary['salary_max'].mean())
    average_pay = int((average_pay_max + average_pay_min)/2)

    # Job location analytics
    most_frequent_location = jobs['locations']. value_counts().idxmax()

    # Job company analytics
    count_companies =  jobs['company'].value_counts()
    top_companies = count_companies.index.to_list()
    top_companies_no = count_companies.to_list()
    companies_df = pd.DataFrame()
    companies_df['companies'] = top_companies
    companies_df['no of jobs'] = top_companies_no
    companies_df = companies_df[companies_df.companies != '']

    # Highest occuring keywords
    def bag_of_words(column):
        rows = range(len(jobs.index))
        temp_bag = []
        new_bag = []
        for row in rows:
            temp_str = jobs[column][row]
            # for word in temp_str:
            #     temp_str = temp_str + word
            blob = TextBlob(temp_str)
            blob_parsed = blob.noun_phrases
            temp_bag.append(blob_parsed)

        # TODO: FIX THIS
        for list in temp_bag:
            if len(list)>1:
                for word in list:
                  new_bag.append(word)
            else:
                temp_str = str(list)
                temp_str.split(' ')
                for new_word in temp_str:
                    new_bag.append(new_word)
        return new_bag

    bag_of_words_title = bag_of_words('title')
    bag_of_words_descript = bag_of_words('description')

    df_of_words = pd.DataFrame(bag_of_words_title)
    df_of_words.append(bag_of_words_descript)
    df_of_words.columns = ['words']
    df_of_words = df_of_words[df_of_words.words != ' ']
    common_words = df_of_words.value_counts()

    return(average_pay, most_frequent_location, companies_df, currency)