
import fitz  
import requests
import os
import re
import json
import logging
import google.generativeai as genai
from config import API_KEY
import time
  

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file using PyMuPDF.

    Parameters:
        uploaded_file (file-like object): The uploaded PDF file.

    Returns:
        str: Extracted text from the PDF.
    
    Raises:
        ValueError: If text extraction fails.
    """
    try:
        logging.info("Starting text extraction from PDF.")
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page_num, page in enumerate(doc, start=1):
                page_text = page.get_text()
                logging.debug(f"Extracted text from page {page_num}.")
                text += page_text
        logging.info("Successfully extracted text from PDF.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise ValueError(f"Failed to extract text from PDF: {e}")


def clean_text(text):
    """
    Cleans the extracted text by removing extra whitespace and unwanted characters.

    Parameters:
        text (str): The raw extracted text.

    Returns:
        str: Cleaned text.
    """
    logging.info("Starting text cleaning.")
    # Remove multiple spaces, newlines, and tabs
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ASCII characters (optional)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    cleaned_text = text.strip()
    logging.info("Text cleaning completed.")
    return cleaned_text


def analyze_resume_with_gemini(resume_text, api_key, api_url):
    """
    Sends the resume text to the Gemini API for analysis.

    Parameters:
        resume_text (str): The cleaned resume text.
        api_key (str): Your Gemini API key.
        api_url (str): The Gemini API endpoint URL.

    Returns:
        dict: The analysis results from Gemini API.
    
    Raises:
        SystemError: If the API request fails.
    """
    logging.info("Starting resume analysis with Gemini API.")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "resume_text": resume_text
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()  
        logging.info("Successfully received response from Gemini API.")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise SystemError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
        raise SystemError(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
        raise SystemError(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request exception: {req_err}")
        raise SystemError(f"An error occurred while requesting the Gemini API: {req_err}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise SystemError(f"An unexpected error occurred: {e}")


def ensure_output_directory():
    """
    Ensures that the output directory exists. Creates it if it doesn't.
    """
    output_dir = os.path.join("data", "outputs")
    try:
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Ensured that the output directory '{output_dir}' exists.")
    except Exception as e:
        logging.error(f"Failed to create output directory '{output_dir}': {e}")
        raise SystemError(f"Failed to create output directory '{output_dir}': {e}")

def clean_and_parse_json(text):
    """
    Removes Markdown code block markers from a JSON string and returns a parsed dictionary.
    
    Parameters:
        text (str): The JSON string possibly wrapped in Markdown code block markers.
    
    Returns:
        dict: The parsed JSON content.
    """
    
    cleaned = re.sub(r'^```(?:json)?\s*', '', text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r'\s*```$', '', cleaned, flags=re.MULTILINE)

    return json.loads(cleaned)


def validate_resume(resume_text,API_KEY=API_KEY):
    """
    Validates whether the provided resume text is a valid resume using the Gemini API.
    
    Parameters:
        resume_text (str): The text extracted from the resume PDF.
    
    Returns:
        tuple: (is_valid, comments) where is_valid is a boolean indicating if the resume is valid,
               and comments is a string containing the evaluation feedback.
    """
   


    genai.configure(api_key=API_KEY)


    model = genai.GenerativeModel("gemini-1.5-flash")

   
    prompt = (
        "You are an expert in evaluating resumes. Determine if the following text is a valid resume, do not worry about the layout or formatting or structuring, just check if the given text is a resume or not "
        "Respond strictly in JSON format with two keys: \"valid\" (a boolean) and \"comments\" (a brief explanation). "
        "Here is the resume text: " + resume_text
    )

   
    response = model.generate_content(prompt)

    
    try:

       
        result = clean_and_parse_json(response.text)
        is_valid = result.get("valid", False)
        comments = result.get("comments", "")
        return is_valid, comments
    except json.JSONDecodeError as e:
   
        return False, f"Error parsing API response: {e} - Raw response: {response.text}"
  


def analyze_resume_dashboard(resume_text, role, API_KEY=API_KEY):
    """
    Uses the Gemini API to analyze a resume and produce a JSON response with multiple score metrics,
    the best suited role, an overall summary, and suggestions.
    
    Parameters:
        resume_text (str): The cleaned text extracted from the resume.
        role (str): The ideal role that the candidate is targeting.
        
    Returns:
        dict: A dictionary containing keys:
            - overall_cv_score (numeric 0-100)
            - uniqueness_score (numeric 0-100)
            - projects_score (numeric 0-100)
            - work_experience_score (numeric 0-100)
            - skills_score (numeric 0-100)
            - education_score (numeric 0-100)
            - best_suited_role (str)
            - overall_summary (str)
            - suggestions (list of str)
    """



    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
   
    prompt = f"""
You are an expert resume analyzer. Act like a realistic hiring manager. 
Analyze the following resume text for a candidate applying for the role "{role}". You can be as critical as needed.
Return a JSON response with the following keys:
- "overall_cv_score": numeric score between 0 and 100.
- "uniqueness_score": numeric score between 0 and 100.
- "projects_score": numeric score between 0 and 100.
- "work_experience_score": numeric score between 0 and 100.
- "skills_score": numeric score between 0 and 100.
- "education_score": numeric score between 0 and 100.
- "best_suited_role": the best suited elaborate niche role for the candidate.
- "overall_summary": a detailed, crisp, to-the-point, actionable summary of the resume.
- "suggestions": a list of actionable, implementable, realistic suggestions for improvement.
Respond strictly in JSON format.
Resume text: {resume_text}
Ideal role: {role}
"""
    response = model.generate_content(prompt)
    
    try:
 
        result = clean_and_parse_json(response.text)
        

        if "suggestions" in result:
            suggestions = result["suggestions"]
            if isinstance(suggestions, str):
  
                suggestions_list = [s.strip() for s in suggestions.split('\n') if s.strip()]
                if not suggestions_list:
                    suggestions_list = [s.strip() for s in suggestions.split(',') if s.strip()]
                result["suggestions"] = suggestions_list
    except Exception as e:
        result = {"error": f"Error parsing response: {e}"}
        
    return result


def colored_metric(label, score):
    try:
        numeric_score = float(score)
    except:
        numeric_score = None

    if numeric_score is None:
        color = "gray"
        display_value = "N/A"
    elif numeric_score >= 80:
        color = "green"
        display_value = f"{numeric_score:.0f}"
    elif numeric_score >= 60:
        color = "orange"
        display_value = f"{numeric_score:.0f}"
    else:
        color = "red"
        display_value = f"{numeric_score:.0f}"
    
    html = f"""
    <div style="border: 2px solid {color}; border-radius: 5px; padding: 10px; margin: 5px; text-align: center;">
        <div style="font-weight: bold; margin-bottom: 4px;">{label}</div>
        <div style="font-size: 24px; color: {color};">{display_value}</div>
    </div>
    """
    return html