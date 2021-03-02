import socket
import pandas as pd
from careerjet_api import CareerjetAPIClient

# Set locale for job search - full list of locale available here https://pypi.org/project/careerjet-api/#description
cj = CareerjetAPIClient("en_AU")

# Get user IP
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Define the job search parameters
job = 'mechanical engineer'
location = 'london '

# Initialise DataFrame to store job data
jobs = pd.DataFrame()

# Initial search to return number of pages to search
result_json = cj.search({
    'location': location,
    'keywords': job,
    'affid': '99e2f6a324cd6491b8124db8f1eeb3e5',
    'user_ip': ip_address,
    'url': 'http://www.example.com/jobsearch?q=python&l=london',
    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
})

pages = result_json['pages']

# Iterate through all pages and save job data to DataFrame
for page in range(pages+1):
    print('Scraping page:', page)
    result_json = cj.search({
                            'location': location,
                            'keywords': job,
                            'affid': '99e2f6a324cd6491b8124db8f1eeb3e5',
                            'user_ip': ip_address,
                            'url': 'http://www.example.com/jobsearch?q=python&l=london',
                            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
                            'page': page
                            })
    temp = result_json['jobs']
    jobs_temp = pd.DataFrame(data=temp)
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
