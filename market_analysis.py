import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from new import fetch_job_data  

# Load API keys
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Function to analyze job market data
def market_analysis_agent():
    llm = ChatGroq(model_name="mixtral-8x7b-32768", api_key=GROQ_API_KEY, temperature=0.5)

    prompt = PromptTemplate(
        input_variables=["data"],
        template=(
            "Analyze the following real-time job market data from Adzuna API. "
            "Identify high-demand job roles, salary trends, and emerging skills. "
            "Data: {data}"
        )
    )

    return LLMChain(llm=llm, prompt=prompt)

# Function to Run Market Analysis
def analyze_market():
    job_data = fetch_job_data()  # Fetch job data using the fetch_job_data function
    if isinstance(job_data, str) and job_data.startswith("Failed"):
        return job_data  # Return error message if failed to fetch data

    # Format job data for analysis
    formatted_jobs = [
        {"title": job["Position"], "salary": job["Salary"]} for job in job_data
    ]

    chain = market_analysis_agent()
    insights = chain.run({"data": formatted_jobs})
    return insights

# API endpoint (replace with the actual one)
api_url = os.getenv("API_URL")

# Function to fetch and return job data
def fetch_job_data():
    # Fetch data from API
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

# Streamlit User Interface
def main():
    st.title("Job Market Analysis Dashboard")
    st.markdown("This application provides insights into the job market by analyzing real-time job postings.")

    # Run the market analysis when button is pressed
    if st.button("Analyze Market Data"):
        with st.spinner("Fetching and analyzing job data..."):
            analysis_results = analyze_market()

            # Display the results
            if isinstance(analysis_results, str) and analysis_results.startswith("Failed"):
                st.error(analysis_results)  # Show error if fetching failed
            else:
                st.subheader("Market Analysis Insights:")
                st.write(analysis_results)  # Display the analysis results

if __name__ == '__main__':
    main()