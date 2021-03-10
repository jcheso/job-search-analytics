import socket
import pandas as pd
import requests
import json
import aiohttp
import asyncio
import json
import os
import time
from careerjet_api import CareerjetAPIClient

cj = CareerjetAPIClient("en_AU")

# Get user IP
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Initialise DataFrame to store job data
jobs = pd.DataFrame()
job = 'mechanical engineer'
location = 'london'

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

def extract_fields_from_response(jobs, response):
        temp = response['jobs']
        jobs_temp = pd.DataFrame(data=temp)
        # jobs = jobs.append(jobs_temp, ignore_index=True)
        return jobs_temp

async def get_job_details (page, job, location):
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
    return result_json      

async def run_program(page):
    """Wrapper for running program in an asynchronous manner"""
    parsed_response = pd.DataFrame()
    try:
        response = await get_job_details(page, job, location)
        parsed_response = extract_fields_from_response(jobs, response)
    except Exception as err:
        print(f"Exception occured: {err}")
        pass
    return parsed_response

pages = get_no_pages(job, location)

async def gather_data():
    results = await asyncio.gather(*[run_program(page) for page in pages])   
    print(results)

# jobs = jobs.append(jobs_temp, ignore_index=True)
tic = time.perf_counter()
asyncio.run(gather_data())
toc = time.perf_counter()
print(toc-tic)


