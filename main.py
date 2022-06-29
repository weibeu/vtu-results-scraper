from vtu_results.bulks import get_bulk_results
from vtu_results.scraper import VTUResultScraper

if __name__ == "__main__":
    # batch_results = get_bulk_results(f"1SG19CS{str(rn).zfill(3)}" for rn in range(1, 121))
    # print(batch_results)
    results = VTUResultScraper.get_results_from_usn("1SG19CS026")
    print(reversed)
