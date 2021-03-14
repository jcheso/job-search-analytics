from careerjet_api import CareerjetAPIClient
import concurrent.futures
import socket
import pandas as pd
import time

def get_job_data(job, location):
      # Set locale for job search - full list of locale available here https://pypi.org/project/careerjet-api/#description
      cj = CareerjetAPIClient("en_GB")

      # Get user IP
      hostname = socket.gethostname()
      ip_address = socket.gethostbyname(hostname)

      # Initialise DataFrame to store job data
      jobs = pd.DataFrame()

      # Initial search to return number of pages to search
      def get_job_details(page):
            result_json = cj.search({
                  'location': location,
                  'keywords': job,
                  'affid': '99e2f6a324cd6491b8124db8f1eeb3e5',
                  'user_ip': ip_address,
                  'url': 'http://www.example.com/jobsearch?q=python&l=london',
                  'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
                  'page': page,
                  'pagesize': 99
                  })
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
            'pagesize': 99
            })
            no_pages = result_json['pages']
            pages = list(range(1,no_pages))
            return pages

      pages = get_no_pages(job, location)

      tic = time.time()
      with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
            result = executor.map(get_job_details, pages)
      toc = time.time()
      print('Time taken: ', toc-tic)


      futures = result.gi_frame.f_locals['fs']

      jobs = pd.DataFrame()
      
      for future in futures:
            result = future._result
            jobs_temp = pd.DataFrame(data=result)
            jobs = jobs.append(jobs_temp, ignore_index=True)
      
      return jobs