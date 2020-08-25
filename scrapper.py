import requests
from bs4 import BeautifulSoup


def get_so_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).findAll("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(job_html):
    title = (
        job_html.find("h2").find("a")["title"]
    )
    company, lcoation = job_html.find("h3").findAll("span", recursive=False)
    company = company.get_text(strip=True)
    location = lcoation.get_text(strip=True)
    location = location.strip("-").strip(" \r").strip("\n")
    job_id = job_html['data-jobid']
    job = {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": f"https://stackoverflow.com/jobs/{job_id}",
    }
    return job


def scrape_jobs(max_pages, url):
    jobs = []

    for page in range(max_pages):
        print(f"Scrapping SO Page: {page}")
        response = requests.get(f"{url}&pg={page + 1}")
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.findAll("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_so_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    pages = get_so_pages(url)
    print(url, pages)
    jobs = scrape_jobs(pages, url)
    return jobs
