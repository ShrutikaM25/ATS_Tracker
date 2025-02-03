import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from dotenv import load_dotenv


# Load API key from environment variable
def main():
    # Load API key from environment variable
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Please add it to your environment variables.")

    # Initialize LLM model with API key
    llm = ChatGroq(model_name="mixtral-8x7b-32768", groq_api_key=GROQ_API_KEY, temperature=0.5)

    # Define a function to generate a career roadmap
    def generate_roadmap(user_input):
        prompt = f"""
        Based on the following user details:
        {user_input}
        
        Provide a detailed career roadmap including:
        
        Career Roadmap:
        
        Suitable Career Paths:
        - List career options
        
        Necessary Skills to Develop:
        - List required skills
        
        Recommended Certifications or Courses:
        - Course Name 1 (Course Link 1)
        - Course Name 2 (Course Link 2)
        - Course Name 3 (Course Link 3)
        
        Potential Job Roles and Industries:
        - Job role 1
        - Job role 2
        - Industry 1
        - Industry 2
        
        Short-term and Long-term Goals:
        - Short-term goal example
        - Long-term goal example
        
        Ensure the response is in simple text without markdown.
        """
        return llm.invoke(prompt)

    # Define a tool for career roadmap generation
    tools = [
        Tool(
            name="Career Roadmap Generator",
            func=generate_roadmap,
            description="Generates a career roadmap based on user skills, interests, and goals."
        )
    ]

    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Streamlit UI
    col1, col2 = st.columns([8, 1]) 
    with col2:
        if st.button("🔙 Back to Dashboard", key="back_to_dashboard"):
            st.session_state.page = "features"
    
    st.title("🚀 Career Roadmap Generator")

    st.write("Enter your details below to get a personalized career roadmap.")

    skills = st.text_area("Current Skills (comma-separated)")
    interests = st.text_area("Interests (comma-separated)")
    education = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "PhD"])
    industries = st.multiselect("Preferred Industries", ["Tech", "Finance", "Healthcare", "Education", "Marketing", "Other"])

    if st.button("Generate Roadmap"):
        user_input = {
            "current_skills": skills.split(","),
            "interests": interests.split(","),
            "education_level": education,
            "preferred_industries": industries
        }

        response = agent.run(str(user_input))
        
        # Splitting response into sections based on predefined headings
        sections = {}
        current_section = None
        for line in response.split("\n"):
            line = line.strip()
            if line.endswith(":"):
                current_section = line.replace(":", "")
                sections[current_section] = []
            elif current_section and line:
                sections[current_section].append(line)

        # Display formatted response in Streamlit
        st.markdown("### Career Roadmap")

        if "Suitable Career Paths" in sections:
            st.markdown("#### Suitable Career Paths")
            st.write("\n".join(sections["Suitable Career Paths"]))

        if "Necessary Skills to Develop" in sections:
            st.markdown("#### Necessary Skills to Develop")
            st.write("\n".join(sections["Necessary Skills to Develop"]))

        if "Recommended Certifications or Courses" in sections:
            st.markdown("#### Recommended Certifications or Courses")
            st.write("\n".join(sections["Recommended Certifications or Courses"]))

        if "Potential Job Roles and Industries" in sections:
            st.markdown("#### Potential Job Roles and Industries")
            st.write("\n".join(sections["Potential Job Roles and Industries"]))

        if "Short-term and Long-term Goals" in sections:
            st.markdown("#### Short-term and Long-term Goals")
            st.write("\n".join(sections["Short-term and Long-term Goals"]))

if __name__ == "__main__":
    main()
