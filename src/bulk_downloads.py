import requests
import time
import os
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path
from urllib.parse import urlparse

# get_articles(None, 22)

def get_articles(journal_id, issue_id):
    if (journal_id):
        articles = requests.get(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?journalID={journal_id}&scraped=1"
        )
    
    else: 
        articles = requests.get(
            f"https://api-service-mrz6aygprq-oa.a.run.app/api/articles?issueID={issue_id}&scraped=1"
        )

    articles = articles.json()

    print(" got articles "+str(len(articles)))

    bulk_download(articles)

def bulk_download(articles):
    cpus = cpu_count()
    # print("cpu count "+str(cpus))

    results = ThreadPool(cpus - 1).imap_unordered(download_url, articles)
    for result in results:
        print('url:', result[0], 'time (s):', result[1])

def download_url(article):
    # print("article ", article["title"])

    path = os.path.join(str(Path.home() / "Downloads"), "AaronsKit_PDF_Downloads")
    if not os.path.exists(path):
        os.makedirs(path)

    bucket_url = article["bucketURL"]

    file_path = urlparse(bucket_url)
    download_url = path+"/"+os.path.basename(file_path.path)

    t0 = time.time()
    url, fn = bucket_url, download_url
    try:
        r = requests.get(url)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return(url, time.time() - t0)
    except Exception as e:
        print('Exception in download_url():', e)

# get_articles(None, 22)
