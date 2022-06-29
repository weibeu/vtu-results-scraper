from concurrent.futures import ThreadPoolExecutor
from vtu_results.scraper import VTUResultScraper


MAX_WORKERS = 100


def get_bulk_results(usns):
    all_results = []
    with ThreadPoolExecutor(MAX_WORKERS) as executor:
        [
            executor.submit(lambda u: all_results.append(VTUResultScraper.get_results_from_usn(u)), usn)
            for usn in usns
        ]
    return all_results
