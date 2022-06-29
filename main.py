from vtu_results.scraper import VTUResultScraper


if __name__ == "__main__":
    batch_results = []
    for roll_no in range(1, 121):
        usn = f"1SG19CS{str(roll_no).zfill(3)}"
        scraper = VTUResultScraper(usn)
        results = scraper.get_results()
        batch_results.append(results)
        print(f"Fetched result of USN: {usn}.")
    print(batch_results)
