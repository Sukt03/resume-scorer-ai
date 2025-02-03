import streamlit as st
from utils import (
    extract_text_from_pdf,
    clean_text,
    validate_resume,
    ensure_output_directory,
    analyze_resume_dashboard
)
from config import STYLES,FOOTER_STYLE, STYLE_SUBMIT_BUTTON
from utils import colored_metric


if "valid" not in st.session_state:
    st.session_state["valid"] = True

if "done" not in st.session_state:
    st.session_state["done"] = False


if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = {}

if "comments" not in st.session_state:
    st.session_state["comments"] = ""

st.set_page_config(
    page_title="Resume Scorer AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="auto"
)


st.markdown(STYLES, unsafe_allow_html=True)


st.title(" Resume Scorer AI ")
st.markdown("### An intelligent Resume Assistance Tool using Gemini API")
st.markdown(
        """##### Built by <a href="https://www.linkedin.com/in/sukriti-tiwari3/" target="_blank">Sukriti Tiwari</a> &amp; <a href="https://www.linkedin.com/in/drpandit69/" target="_blank">B H V S P Subrahmanyam</a> #####""",
        unsafe_allow_html=True
    )
st.markdown("---")
x=st.empty()
main_container=x.form("main_form",enter_to_submit=False,clear_on_submit=True)

def check_data():
    
    role = st.session_state["role"]
    if(st.session_state["file"]==None):
        st.error("Please upload a valid resume to proceed.")
        return



    clean_text_val = clean_text(extract_text_from_pdf(st.session_state['file']))

    ensure_output_directory()



    is_valid, comments = validate_resume(clean_text_val)
  
  

    if not is_valid:
        st.session_state['comments'] = comments
        st.session_state['valid'] = False
    else:
  
        analysis_result = analyze_resume_dashboard(clean_text_val, role)
     
        st.session_state["analysis_result"] = analysis_result
        st.session_state['valid'] = True
        st.session_state['done'] = True
        

def back_to_main():
    st.session_state["valid"]=True
    st.session_state["done"]=False

    st.session_state["comments"]=""
    st.session_state["analysis_result"]={}
    st.session_state["clean_text"]=""
    x.empty()

def download_pdf():
    import io
    import base64
    import re
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors


    analysis = st.session_state.get("analysis_result", {})


    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []


    story.append(Paragraph("Resume Analysis", styles["Title"]))
    story.append(Spacer(1, 12))


    score_data = [
        ["Metric", "Score"],
        ["Overall CV Score", analysis.get("overall_cv_score", "N/A")],
        ["Projects Score", analysis.get("projects_score", "N/A")],
        ["Uniqueness Score", analysis.get("uniqueness_score", "N/A")],
        ["Work Experience Score", analysis.get("work_experience_score", "N/A")],
        ["Skills Score", analysis.get("skills_score", "N/A")],
        ["Education Score", analysis.get("education_score", "N/A")]
    ]
    table = Table(score_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.green),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Your Best Suited Role is:", styles["Heading2"]))
    story.append(Paragraph(str(analysis.get("best_suited_role", "N/A")), styles["Normal"]))
    story.append(Spacer(1, 12))


    story.append(Paragraph("Overall Summary:", styles["Heading2"]))
    story.append(Paragraph(str(analysis.get("overall_summary", "N/A")), styles["Normal"]))
    story.append(Spacer(1, 12))

  
    def convert_md_to_xml(text):
        return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

   
    story.append(Paragraph("Suggestions:", styles["Heading2"]))
    suggestions = analysis.get("suggestions", [])
    if isinstance(suggestions, list):
        for s in suggestions:
            formatted_s = convert_md_to_xml(s)
            story.append(Paragraph(f"- {formatted_s}", styles["Normal"]))
    else:
        story.append(Paragraph(convert_md_to_xml(str(suggestions)), styles["Normal"]))

 
    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()


    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    

    html = f"""
    <html>
      <body>
        <a id="download_link" href="data:application/pdf;base64,{b64_pdf}" download="analysis_report.pdf" style="display:none">Download PDF</a>
        <script>
            document.getElementById("download_link").click();
        </script>
      </body>
    </html>
    """
  
    st.components.v1.html(html, height=0, width=0)




if(st.session_state["valid"] and not st.session_state["done"]):
        

    st.markdown(STYLE_SUBMIT_BUTTON, unsafe_allow_html=True)
    with main_container:
 
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 🎯 Target Role")
            role = st.text_input("Enter the role you are applying for:", value="Software Engineer", key="role")
      
        with col2:
            st.markdown("### 📂 Upload Your Resume")
            uploaded_file = st.file_uploader("", type="pdf",key="file")

        col_left, col_right = st.columns([7, 1])
        with col_right:
                analyze_button = st.form_submit_button("🔍 Analyze Resume",on_click=check_data)


elif((st.session_state["valid"])==False):
        

    st.title(" Resume Scorer AI ")
    st.markdown("### An intelligent Resume Assistance Tool using Gemini API")
    st.markdown(
        """##### Built by <a href="https://www.linkedin.com/in/sukriti-tiwari3/" target="_blank">Sukriti Tiwari</a> &amp; <a href="https://www.linkedin.com/in/drpandit69/" target="_blank">B H V S P Subrahmanyam</a> #####""",
        unsafe_allow_html=True
    )
    st.markdown("---")

    x.empty()
    comments=st.session_state["comments"]
    st.write("# 🚫 Invalid Resume")
    st.error(f'{comments} Please upload a valid resume to proceed.')
    button = st.button("Back to main page",on_click=back_to_main)
                       

elif st.session_state["valid"] == True and st.session_state["done"]:

    x.empty()

    analysis = st.session_state.get("analysis_result", {})

    st.markdown("## Resume Analysis Dashboard")
    st.markdown("### Scores")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(colored_metric("Overall CV Score", analysis.get("overall_cv_score", "N/A")), unsafe_allow_html=True)
        st.markdown(colored_metric("Projects Score", analysis.get("projects_score", "N/A")), unsafe_allow_html=True)
    with col2:
        st.markdown(colored_metric("Uniqueness Score", analysis.get("uniqueness_score", "N/A")), unsafe_allow_html=True)
        st.markdown(colored_metric("Work Experience Score", analysis.get("work_experience_score", "N/A")), unsafe_allow_html=True)
    with col3:
        st.markdown(colored_metric("Skills Score", analysis.get("skills_score", "N/A")), unsafe_allow_html=True)
        st.markdown(colored_metric("Education Score", analysis.get("education_score", "N/A")), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Best Suited Role
    st.markdown("### Your Best Suited Role is:")
    st.write(analysis.get("best_suited_role", "N/A"))
    
    st.markdown("---")
    

    st.markdown("### Overall Summary:")
    st.write(analysis.get("overall_summary", "N/A"))
    
    st.markdown("---")

    st.markdown("### Suggestions:")
    suggestions = analysis.get("suggestions", [])
    if isinstance(suggestions, list):
       
        suggestions_text = "\n".join([f"- {s}" for s in suggestions])
    else:
        suggestions_text = suggestions
    st.markdown(suggestions_text)
    
   
    with st.container():

        col_space, col_buttons = st.columns([7, 2])
        with col_buttons:
            btn_cols = st.columns([1, 1])
            with btn_cols[0]:
                st.button("Try another resume", on_click=back_to_main)
            with btn_cols[1]:
                st.button("Download as PDF", on_click=download_pdf)



st.markdown("---")
st.markdown(FOOTER_STYLE, unsafe_allow_html=True)

