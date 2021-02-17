import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"id": "searchCountPages"})
    jobs = pagination.text.split('of')[1]

    jobs_count = int(''.join(list(filter(str.isdigit, jobs))))

    max_page = int(jobs_count / 50)
    return max_page


def extract_title(html):
    return html.find("h2", {"class": "title"}).find("a")["title"]


def extract_company(html):
    company = html.find("span", {"class": "company"})

    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)

    return company.strip()


def extract_location(html):
    return html.find("span", {"class": "location"}).string


def extract_job_id(html):
    return html["data-jk"]


def extract_job(html):
    title = extract_title(html)
    company = extract_company(html)
    location = extract_location(html)
    job_id = extract_job_id(html)

    return {'title': title, 'company': company, 'location': location, 'link': f"https://www.indeed.com/viewjob?jk={job_id}"}


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page+1}")

        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_pages = extract_last_pages()
    last_pages = 10
    jobs = extract_indeed_jobs(last_pages)
    return jobs
