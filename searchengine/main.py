import pandas as pd
from . import job_data
from . import job_analytics

# import job_data
# import job_analytics

# TODO: Create a page that displays the job adverts
# TODO: Exception control for null searches


def get_analytics(job, location):

    jobs = job_data.get_job_data(job, location)
    number_of_jobs, average_pay_min, average_pay_max, most_frequent_location, top_companies, currency, top_words, job, location = job_analytics.get_job_analytics(
        jobs, job, location)

    return(number_of_jobs, average_pay_min, average_pay_max, most_frequent_location, top_companies, currency, top_words, job, location)

# get_analytics('finance analyst', 'australia')
