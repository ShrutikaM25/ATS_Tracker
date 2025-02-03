import requests
import os
from dotenv import load_dotenv
load_dotenv()

# API endpoint (replace with the actual one)
api_url = os.getenv("API_URL")

# Function to fetch and return job data
def fetch_job_data():
    # Fetch data
    response = requests.get(api_url)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        
        job_details_list = []  # List to store all job details
        
        # Example: Extract relevant fields for each job post
        for job in data:
            job_details = {
                "Position": job.get("positionName"),
                "Company": job.get("company"),
                "Location": job.get("location"),
                "Job Type": job.get("jobType"),
                "Salary": job.get("salary"),
                "Rating": job.get("rating"),
                "Reviews": job.get("reviewsCount"),
                "Posted At": job.get("postedAt"),
                "Job URL": job.get("url"),
                "Description": job.get("description"),
                "Scraped At": job.get("scrapedAt"),
            }
            job_details_list.append(job_details)  # Add each job's details to the list
        
        return job_details_list  # Return the list of job details
    
    else:
        return f"Failed to fetch data. Status code: {response.status_code}"  # Return error message if request fails

# Example: Call the function and get the data
job_data = fetch_job_data()

# Print or use the returned data as needed
print(job_data)
