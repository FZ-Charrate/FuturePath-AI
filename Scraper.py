# Import necessary modules from Selenium and others for data handling and timing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import time
import csv 



# Keywords to search for on LinkedIn job search
keywords = [    
    # Software / IT
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Engineer",
    "DevOps Engineer",
    "AI Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Embedded Systems Engineer",
    "Cybersecurity Engineer",

    # Core Engineering
    "Mechanical Engineer",
    "Electrical Engineer",
    "Civil Engineer",
    "Industrial Engineer",
    "Chemical Engineer",
    "Structural Engineer",
    "Petroleum Engineer",

    # Specialized / Modern Fields
    "Systems Engineer",
    "Robotics Engineer",
    "Hardware Engineer",
    "Telecommunications Engineer",
    "Mechatronics Engineer",
    "Renewable Energy Engineer",
    "Environmental Engineer",
    "Aerospace Engineer"
]

# This block is commented out but was intended to create the CSV header row.
### TODO: ##THis line will be executed only one time !!!!##
# with open("job_links.csv",mode= "w", newline="", encoding="utf-8") as file:
#     job_writer=csv.writer(file)
#     job_writer.writerow(["Job Title", "Company", "Location", "Link" ,"num_applicants" ,"description" ,"seniority_level", "employment_type", "job_function", "industries"])

# Load previously collected job links from CSV to avoid duplicates
df = pd.read_csv("job_links.csv")

# Helper function to wrap expressions in try/except and return "N/A" if they fail
def tryexcept(expression):
     try:
         return expression
     except Exception:
         return "N/A"

# Main loop for each keyword
for keyword in keywords:
    # Set up the Chrome driver
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # Open LinkedIn
    driver.get("https://www.linkedin.com/")
    wait = WebDriverWait(driver, 20)

    # Click on the 'Jobs' section
    jobs_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Jobs")))
    jobs_button.click()

    # Close any popup if it appears
    try:
        dismiss_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modal__dismiss")))
        dismiss_button.click()
    except Exception:
        pass

    # Set the job location to "Worldwide"
    search_bar_location = wait.until(EC.element_to_be_clickable((By.ID, "job-search-bar-location")))
    search_bar_location.click()
    search_bar_location.clear()
    search_bar_location.send_keys("Worldwide")

    # Search for the current keyword
    search_bar = wait.until(EC.element_to_be_clickable((By.ID, "job-search-bar-keywords")))
    search_bar.click()
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.ENTER)

    # Set of already collected job URLs to avoid duplicates
    already_existing_links = set(df["Link"])
    job_links = []
    job_urls = []
    previous_len = -1

    # Scroll and load more job links until no new links are found
    while len(job_urls) != previous_len:
        previous_len = len(job_urls)
        new_job_links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "base-card__full-link")))
        for new_job_link in new_job_links:
            if (new_job_link.get_attribute("href") not in job_urls and 
                new_job_link.get_attribute("href") not in already_existing_links):
                job_links.append(new_job_link)
                job_urls.append(new_job_link.get_attribute("href"))
        print("total job links found for now: ", len(job_links))
        
        # Scroll to load more jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 100);")
        time.sleep(2)

        # Close any additional modal if it appears
        try:
            dismiss_button2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modal__dismiss")))
            dismiss_button2.click()
        except Exception:
            pass

        # Click on 'See more jobs' if available
        try:
            see_more_jobs = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "infinite-scroller__show-more-button")))
            see_more_jobs.click()
            time.sleep(2)
        except Exception:
            pass

    print("total job links found: ", len(job_links))

    # New browser instance for scraping job details
    job_driver = webdriver.Chrome(service=service)
    for job_url in job_urls:
        try:
            job_driver.get(job_url)
            job_wait = WebDriverWait(job_driver, 10)
            time.sleep(2)

            # Close modal if it appears
            try:
                dismiss_button = job_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "modal__dismiss")))
                dismiss_button.click()
            except Exception:
                pass

            # Extract job details
            job_title = tryexcept(job_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "top-card-layout__title"))).text.strip())
            job_company = tryexcept(job_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "topcard__org-name-link"))).text.strip())
            job_location = tryexcept(job_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]' ))).text.strip())
            job_num_applicants = tryexcept(job_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "num-applicants__caption"))).text.strip())
            job_description = tryexcept(job_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup"))).text.strip())

            # Extract extra job info like seniority level, type, function, industry
            job_description_list = job_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "description__job-criteria-text")))
            job_seniority_level = tryexcept(job_description_list[0].text.strip()) if len(job_description_list) > 0 else "N/A"
            job_employment_type = tryexcept(job_description_list[1].text.strip()) if len(job_description_list) > 1 else "N/A"
            job_function = tryexcept(job_description_list[2].text.strip()) if len(job_description_list) >  2 else "N/A"
            job_industries = tryexcept(job_description_list[3].text.strip()) if len(job_description_list) > 3 else "N/A"

            # Append extracted job data to the CSV file
            with open("job_links.csv", mode="a", newline="", encoding="utf-8") as file:
                job_writer = csv.writer(file)
                job_writer.writerow([
                    job_title, job_company, job_location, job_url,
                    job_num_applicants, job_description, job_seniority_level,
                    job_employment_type, job_function, job_industries
                ])
            
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Skipped job due to error: {e}")
            continue

    # Close job detail browser instance
    job_driver.quit()

    # Close main browser instance
    driver.quit()

