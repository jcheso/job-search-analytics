from careerjet_api import CareerjetAPIClient
import concurrent.futures
import socket
import pandas as pd
import time

# TODO: Capitalise the search terms in search results
# TODO: Add number of jobs next to companies in search results
# TODO: Create a page that displays the job adverts
# TODO: Filter out empty listings in top companies
# TODO: Find a way to remove recruiting agencies from companies hiring?
# TODO: Refactor this code
# TODO: Add loading bar while scraping text

def get_analytics(job, location):
      # Set locale for job search - full list of locale available here https://pypi.org/project/careerjet-api/#description
      cj = CareerjetAPIClient("en_GB")

      # Get user IP
      hostname = socket.gethostname()
      ip_address = socket.gethostbyname(hostname)

      # Initialise DataFrame to store job data
      jobs = pd.DataFrame()

      # Initial search to return number of pages to search
      def get_job_details(page):
            print('Scraping page', page)
            result_json = cj.search({
                  'location': location,
                  'keywords': job,
                  'affid': '99e2f6a324cd6491b8124db8f1eeb3e5',
                  'user_ip': ip_address,
                  'url': 'http://www.example.com/jobsearch?q=python&l=london',
                  'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
                  'page': page
                  })
            print('Completed scraping page:', page)
            temp = result_json['jobs']
            return temp

      def get_no_pages(job, location):
            result_json = cj.search({
            'location': location,
            'keywords': job,
            'affid': '99e2f6a324cd6491b8124db8f1eeb3e5',
            'user_ip': ip_address,
            'url': 'http://www.example.com/jobsearch?q=python&l=london',
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
            })
            no_pages = result_json['pages']
            pages = list(range(1,no_pages))
            return pages

      pages = get_no_pages(job, location)

      with concurrent.futures.ThreadPoolExecutor(max_workers = 128) as executor:
            futures = []
            jobs = pd.DataFrame()
            for page_no in pages:
                  futures.append(executor.submit(get_job_details, page=page_no))
            for future in concurrent.futures.as_completed(futures):
                  result = future._result
                  jobs_temp = pd.DataFrame(data=result)
                  jobs = jobs.append(jobs_temp, ignore_index=True)

      # Convert salaries to numeric data format
      jobs['salary_max'] = pd.to_numeric(jobs['salary_max'])
      jobs['salary_min'] = pd.to_numeric(jobs['salary_min'])

      # Filter out jobs without yearly salary listed
      jobs_salary = jobs.loc[(jobs['salary_min'] > 0) &
                        (jobs['salary_type'] == 'Y')]

      # Calculate job pay analytics
      currency = jobs_salary['salary_currency_code']. value_counts().idxmax()
      average_pay_min = int(jobs_salary['salary_min'].mean())
      average_pay_max = int(jobs_salary['salary_max'].mean())
      average_pay = int((average_pay_max + average_pay_min)/2)

      # Print pay analytics
      print('---- You\'re searching for' + job + 'in' + location + '-----')
      print('The average minimum pay for this job is',
            average_pay_min, currency, 'per year')
      print('The average pay for this job is', average_pay, currency, 'per year')
      print('The average maximum pay for this job is',
            average_pay_max, currency, 'per year')

      # Job location analytics
      most_frequent_location = jobs['locations']. value_counts().idxmax()
      print('The most common location for this job in ' +
            location + 'is ' + most_frequent_location)

      # Job company analytics
      count_companies =  jobs['company'].value_counts()
      print('----The most common employers and number of ads----')
      print(count_companies[:10])
      top_companies = count_companies[1:11].index.to_list

      return(average_pay, most_frequent_location, top_companies, currency)

# st = time.time()  
# get_analytics('software engineer', 'london')
# ft = time.time()
# print(ft-st)