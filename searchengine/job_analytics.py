# TODO: Exception control
# TODO: Filter out empty listings in top companies
# TODO: Find a way to remove recruiting agencies from companies hiring?
# TODO: Capitalise the search terms in search results
# TODO: Add number of jobs next to companies in search results

import pandas as pd

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
    companies_dict = dict(zip(top_companies, top_companies_no)) 
    companies_dict.pop('')




    return(average_pay, most_frequent_location, top_companies, currency)