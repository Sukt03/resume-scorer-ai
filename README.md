# Resume Scorer AI

Resume Scorer AI is an intelligent resume analysis tool built with Streamlit and powered by the Gemini API. It evaluates resumes based on multiple criteria, identifies the best-suited role for the candidate, and provides actionable feedback. The app also generates a downloadable PDF report summarizing the analysis. I've done this in Collaboration with Subrahmanyam B H V S P [GitHub](https://github.com/dr-pandit-69)

## Features

- **Resume Validation**: Ensures that the uploaded file is a valid resume.
- **Comprehensive Scoring**: Assigns scores for different aspects of the resume:
  - **Overall CV Score**
  - **Uniqueness Score**
  - **Projects Score**
  - **Work Experience Score**
  - **Skills Score**
  - **Education Score**
- **Best Suited Role Prediction**: Recommends the most appropriate role based on resume content.
- **Detailed Summary & Suggestions**: Provides an insightful overview and practical improvement tips.
- **PDF Report Generation**: Creates a well-structured report for download.

## Installation

### Clone the Repository
```sh
git clone https://github.com/Sukt03/resume-scorer-ai.git
cd resume-scorer-ai
```

### Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file for sensitive API keys

#### Example `.env` file:
```ini
API_KEY=your_gemini_api_key_here
```



## Usage

### Start the Application
```sh
streamlit run app.py
```

### Interact with the App
- Enter your target role.
- Upload your resume in PDF format.
- Click **Analyze Resume** to process the document.
- View detailed scores, role recommendation, and suggestions.
- Download the analysis as a **PDF report**.
- Use the **Try Another Resume** button to restart.

## Folder Structure
```
resume-scorer-ai/
├── app.py                   # Main Streamlit application
├── utils.py                 # Utility functions for text extraction, validation, and analysis
├── config.py                # Handles configurations and environment variables
├── requirements.txt         # List of dependencies
├── README.md                # Project documentation
├── .env                     # Public environment config
```

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch.
3. Make improvements.
4. Submit a pull request.

Ensure that your changes follow coding standards and best practices.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Streamlit** for providing an easy-to-use web framework.
- **Gemini API** for resume analysis capabilities.
- **ReportLab** for PDF generation.
- **Subrahmanyam B H V S P** for helping me out with the overall project- [GitHub](https://github.com/dr-pandit-69)

