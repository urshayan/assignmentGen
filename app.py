import streamlit as st
from pdf_utils import create_assignment_pdf
import tempfile
from datetime import datetime

st.set_page_config(page_title="Assignment Generator", layout="wide")
st.title("🎓 Assignment Generator")

# ---------------- COVER PAGE INPUTS ----------------
st.sidebar.header("Cover Page Info")
university = st.sidebar.text_input("University Name")
logo = st.sidebar.file_uploader("University Logo", type=["png","jpg","jpeg"])
student_name = st.sidebar.text_input("Student Name")
roll_number = st.sidebar.text_input("Roll Number")
department = st.sidebar.text_input("Department")
course = st.sidebar.text_input("Course Name")
professor = st.sidebar.text_input("Professor Name")
assignment_title = st.sidebar.text_input("Assignment Title")
submission_date = st.sidebar.date_input("Submission Date", value=datetime.today())

cover_info = {
    "university": university,
    "logo": logo,
    "student_name": student_name,
    "roll_number": roll_number,
    "department": department,
    "course": course,
    "professor": professor,
    "assignment_title": assignment_title,
    "submission_date": submission_date.strftime("%d-%m-%Y")
}

# ---------------- CONTENT BLOCKS ----------------
if "blocks" not in st.session_state:
    st.session_state.blocks = []

def add_text_block():
    if st.session_state.new_text.strip():
        st.session_state.blocks.append({"type":"text","content":st.session_state.new_text})
        st.session_state.new_text = ""  # safe, text_area allows this

def add_code_block():
    if st.session_state.new_code.strip():
        st.session_state.blocks.append({"type":"code","content":st.session_state.new_code})
        st.session_state.new_code = ""  # safe

def add_image_block():
    if st.session_state.new_image:
        st.session_state.blocks.append({"type":"image","file":st.session_state.new_image})
        st.session_state.new_image = None

# --- Input UI ---
st.header("Add Content Blocks")

st.subheader("Text Block")
st.text_area("Text Content", key="new_text")
st.button("Add Text Block", on_click=add_text_block)

st.subheader("Code Block")
st.text_area("Code Content", key="new_code")
st.button("Add Code Block", on_click=add_code_block)

st.subheader("Image Block")
st.subheader("Image Block")
uploaded_image = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

if st.button("Add Image Block") and uploaded_image is not None:
    st.session_state.blocks.append({"type":"image", "file":uploaded_image})
    st.success("Image added successfully! ✅")

# Show current blocks
st.write("### Current Blocks")
for i, block in enumerate(st.session_state.blocks):
    st.write(f"{i+1}. {block['type']}")

# --- Generate PDF ---
if st.button("Generate Assignment PDF"):
    if not st.session_state.blocks:
        st.warning("Add at least one content block before generating PDF.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            create_assignment_pdf(tmp_file.name, cover_info, st.session_state.blocks)
            st.success("PDF Generated Successfully ✅")
            st.download_button("Download PDF", data=open(tmp_file.name,"rb"), file_name="assignment.pdf")

