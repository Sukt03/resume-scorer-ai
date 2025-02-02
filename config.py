import os
from dotenv import load_dotenv

if os.path.exists('.env.development'):
    load_dotenv('.env.development')
    
else:
    
    load_dotenv('.env')

API_KEY = os.getenv("API_KEY")

STYLES="""
    <style>
    /* Button hover styling */
    div.stButton > button:hover {
         background-color: green;
         color: white;
    }
    /* Link hover styling */
    a:hover {
         color: green;
         text-decoration: underline;
    }
    
    div.stButton > button[type="submit"] {
    border: 2px solid green;
    border-radius: 4px;
    background-color: white; /* or any background color you prefer */
    color: green;
}

div.stFormSubmitButton > button[type="submit"]:hover {
    background-color: green;
    color: white;
}
    </style>

    """

STYLE_SUBMIT_BUTTON="""
<style>
div.stFormSubmitButton > button {
    border: 2px solid green;
    border-radius: 4px;
  
    color: green;
    padding: 0.5rem 1rem;
    font-weight: bold;
}
div.stFormSubmitButton > button:hover {
    background-color: green;
    color: white;
}
</style>
"""

FOOTER_STYLE="""
<div style='text-align: center; color: #888888; font-size: 12px;'>
    &copy; 2025 Resume Scorer AI. Built by Sukriti Tiwari &amp; Subrahmanyam B H V S P. All rights reserved.
</div>
"""



