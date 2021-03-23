import pandas as pd
# from . import job_data 
# from . import job_analytics

import job_data
import job_analytics

# TODO: Create a page that displays the job adverts

def get_analytics(job, location):

      jobs = job_data.get_job_data(job, location)
      average_pay, most_frequent_location, top_companies, currency = job_analytics.get_job_analytics(jobs, job, location)

      return(average_pay, most_frequent_location, top_companies, currency)

get_analytics('software engineer', 'london')
