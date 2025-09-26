"""
CGPA Projection Website
A comprehensive academic planning tool for university students
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime
import random
from typing import Dict, List

# Import our custom modules
import sys
import os
import tempfile
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_utils import AcademicRecord, Course, calculate_grade_points, get_letter_grade
from cgpa_calculator import CGPACalculator, WhatIfAnalyzer
from course_data import (
    GRADES, GRADE_POINTS, get_all_courses, get_unlocked_courses, 
    categorize_course, get_program_requirements, plan_general_education_courses,
    COURSE_NAMES, get_course_credit
)

# Try to import PDF parsing functionality
try:
    from bracu_parser import create_parser
    PDF_PARSING_AVAILABLE = True
except ImportError as e:
    PDF_PARSING_AVAILABLE = False
    st.error(f"PDF parsing not available: {str(e)}")

# Page configuration
st.set_page_config(
    page_title="CGPA Projection Tool",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
/* Main theme */
.main {
    padding-top: 2rem;
}

/* Header styling */
h1 {
    color: #1f77b4;
    text-align: center;
    font-size: 2.5rem !important;
    margin-bottom: 1rem;
}

/* Metric styling */
[data-testid="metric-container"] {
    background-color: #f0f2f6;
    border: 1px solid #e0e0e0;
    padding: 0.5rem;
    border-radius: 0.5rem;
    margin: 0.25rem 0;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
}

/* Info box styling */
.info-box {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}

/* Success box styling */
.success-box {
    background-color: #e8f5e8;
    border-left: 4px solid #4caf50;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}

/* Warning box styling */
.warning-box {
    background-color: #fff3e0;
    border-left: 4px solid #ff9800;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'academic_record' not in st.session_state:
    st.session_state.academic_record = AcademicRecord()
    st.session_state.calculator = CGPACalculator(st.session_state.academic_record)
    st.session_state.analyzer = WhatIfAnalyzer(st.session_state.calculator)

if 'program' not in st.session_state:
    st.session_state.program = "CSE"

# BRACU-specific session state
if 'uploaded_gradesheet' not in st.session_state:
    st.session_state.uploaded_gradesheet = False
    st.session_state.name = ""
    st.session_state.student_id = ""
    st.session_state.courses_done = {}
    st.session_state.semesters_done = {}

# Title and description
st.title("🎓 CGPA Projection & Academic Planning Tool")
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem; color: #666;">
Plan your academic journey • Track your progress • Achieve your goals
</div>
""", unsafe_allow_html=True)

# Instructions banner
if not st.session_state.academic_record.courses_taken:
    st.info("""
    🚀 **Get Started:**
    1. **Upload Gradesheet**: Use the sidebar to upload your official PDF gradesheet for automatic parsing
    2. **Manual Entry**: Or manually add your courses in the Course Management tab
    3. **Explore**: Use the analytics and planning tools to optimize your academic journey
    """)

# Display gradesheet upload status
if st.session_state.uploaded_gradesheet:
    st.success(f"📄 **Gradesheet Loaded**: {st.session_state.name} ({st.session_state.student_id}) - {len(st.session_state.courses_done)} courses from {len(st.session_state.semesters_done)} semesters")
    
    # Debug information
    if st.session_state.academic_record:
        courses_in_record = len(st.session_state.academic_record.courses_taken)
        st.info(f"🔍 **Debug**: Academic record has {courses_in_record} courses loaded")
        if courses_in_record == 0:
            st.warning("⚠️ **Issue**: Courses were parsed but not loaded into academic record. Conversion issue detected.")

# Show current status if data exists
if st.session_state.academic_record.courses_taken:
    col1, col2, col3, col4 = st.columns(4)
    
    current_cgpa = st.session_state.calculator.academic_record.get_current_cgpa()
    current_credits = st.session_state.calculator.academic_record.get_total_credits()
    requirements = get_program_requirements(st.session_state.program)
    
    with col1:
        st.metric("👤 Student", 
                 st.session_state.academic_record.student_name or "Not Set",
                 help="Student name from gradesheet or manual entry")
    
    with col2:
        st.metric("🎯 Current CGPA", f"{current_cgpa:.2f}",
                 help="Calculated from all completed courses")
    
    with col3:
        st.metric("📚 Credits Earned", f"{current_credits}",
                 help=f"Out of {requirements['total_credits']} required credits")
    
    with col4:
        progress = (current_credits / requirements['total_credits']) * 100
        st.metric("📊 Progress", f"{progress:.1f}%",
                 help="Degree completion progress")

# Sidebar for student information and program selection
st.sidebar.header("📚 Gradesheet Upload")

# Program selection
program = st.sidebar.selectbox(
    "Select Program:",
    ["CSE", "CS"],
    index=0 if st.session_state.program == "CSE" else 1
)

if program != st.session_state.program:
    st.session_state.program = program
    st.rerun()

# Gradesheet upload section
st.sidebar.markdown("---")
st.sidebar.subheader("📄 Upload Your Gradesheet")

if PDF_PARSING_AVAILABLE:
    uploaded_file = st.sidebar.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your official university gradesheet/transcript"
    )

    if uploaded_file is not None:
        if st.sidebar.button("🔍 Parse Gradesheet", type="primary"):
            try:
                try:
                with st.spinner("Parsing gradesheet..."):
                    # Save uploaded file as temp.pdf (BRACU analyzer style)
                    with open("temp.pdf", "wb") as f:
                        f.write(uploaded_file.read())
                    
                    # Parse the gradesheet using BRACU-specific parser
                    parser = create_parser()
                    name, student_id, courses_done, semesters_done = parser.extract_gradesheet("temp.pdf")
                    
                    # Update session state with parsed data
                    if name and student_id and courses_done:
                        # Store in BRACU analyzer compatible format
                        st.session_state.name = name
                        st.session_state.student_id = student_id
                        st.session_state.courses_done = courses_done
                        st.session_state.semesters_done = semesters_done
                        st.session_state.uploaded_gradesheet = True
                        
                        # Update calculator - always create new record
                        # Convert parsed data to our AcademicRecord format
                        record = AcademicRecord(name, student_id)
                        
                        # Add all courses to the record
                        for course_code, course in courses_done.items():
                            # Find which semester this course belongs to
                            semester_name = "IMPORTED COURSES"
                            for sem_name, sem_obj in semesters_done.items():
                                if hasattr(sem_obj, 'courses'):
                                    for sem_course in sem_obj.courses:
                                        if sem_course.course_code == course_code:
                                            semester_name = sem_name
                                            break
                            
                            # Add course to the record
                            record.add_course_to_semester(semester_name, course)
                        
                        st.session_state.academic_record = record
                        st.session_state.calculator = CGPACalculator(record)
                        st.session_state.analyzer = WhatIfAnalyzer(st.session_state.calculator)
                        
                        # Clean up temp file
                        if os.path.exists("temp.pdf"):
                            os.unlink("temp.pdf")
                        
                        # Show success message
                        st.sidebar.success("✅ Gradesheet parsed successfully!")
                        st.sidebar.write(f"👤 **Student:** {name}")
                        st.sidebar.write(f"🆔 **ID:** {student_id}")
                        st.sidebar.write(f"📚 **Courses:** {len(courses_done)}")
                        st.sidebar.write(f"📖 **Semesters:** {len(semesters_done)}")
                        
                        current_cgpa = st.session_state.academic_record.get_current_cgpa() if st.session_state.academic_record else 0.0
                        st.sidebar.write(f"🎯 **CGPA:** {current_cgpa:.2f}")
                        
                        st.rerun()
                    else:
                        st.sidebar.error("❌ Could not extract complete data from gradesheet")
                        st.sidebar.write("Please check:")
                        st.sidebar.write("- Gradesheet format is supported")
                        st.sidebar.write("- Student info is clearly visible")
                        st.sidebar.write("- Course data is readable")
                    
            except Exception as e:
                st.sidebar.error(f"❌ Error parsing gradesheet: {str(e)}")
                st.sidebar.write("Please ensure:")
                st.sidebar.write("- File is a valid PDF")
                st.sidebar.write("- Gradesheet contains course codes and grades")
                st.sidebar.write("- Text is readable (not scanned image)")
                
                # Clean up temp file on error
                if os.path.exists("temp.pdf"):
                    os.unlink("temp.pdf")
else:
    st.sidebar.warning("📄 PDF parsing is currently unavailable. Please add courses manually below.")
                # Save uploaded file as temp.pdf (BRACU analyzer style)
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.read())
                
                # Parse the gradesheet using BRACU-specific parser
                parser = create_parser()
                name, student_id, courses_done, semesters_done = parser.extract_gradesheet("temp.pdf")
                
                # Update session state with parsed data
                if name and student_id and courses_done:
                    # Store in BRACU analyzer compatible format
                    st.session_state.name = name
                    st.session_state.student_id = student_id
                    st.session_state.courses_done = courses_done
                    st.session_state.semesters_done = semesters_done
                    st.session_state.uploaded_gradesheet = True
                    
                    # Update calculator - always create new record
                    # Convert parsed data to our AcademicRecord format
                    record = AcademicRecord(name, student_id)
                    
                    # Add all courses to the record
                    for course_code, course in courses_done.items():
                        # Find which semester this course belongs to
                        semester_name = "IMPORTED COURSES"
                        for sem_name, sem_obj in semesters_done.items():
                            if hasattr(sem_obj, 'courses'):
                                for sem_course in sem_obj.courses:
                                    if sem_course.course_code == course_code:
                                        semester_name = sem_name
                                        break
                        
                        # Add course to the record
                        record.add_course_to_semester(semester_name, course)
                    
                    st.session_state.academic_record = record
                    st.session_state.calculator = CGPACalculator(record)
                    st.session_state.analyzer = WhatIfAnalyzer(st.session_state.calculator)
                    
                    # Clean up temp file
                    if os.path.exists("temp.pdf"):
                        os.unlink("temp.pdf")
                    
                    # Show success message
                    st.sidebar.success("✅ Gradesheet parsed successfully!")
                    st.sidebar.write(f"� **Student:** {name}")
                    st.sidebar.write(f"🆔 **ID:** {student_id}")
                    st.sidebar.write(f"📚 **Courses:** {len(courses_done)}")
                    st.sidebar.write(f"📖 **Semesters:** {len(semesters_done)}")
                    
                    current_cgpa = st.session_state.academic_record.get_current_cgpa() if st.session_state.academic_record else 0.0
                    st.sidebar.write(f"🎯 **CGPA:** {current_cgpa:.2f}")
                    
                    st.rerun()
                else:
                    st.sidebar.error("❌ Could not extract complete data from gradesheet")
                    st.sidebar.write("Please check:")
                    st.sidebar.write("- Gradesheet format is supported")
                    st.sidebar.write("- Student info is clearly visible")
                    st.sidebar.write("- Course data is readable")
                
        except Exception as e:
            st.sidebar.error(f"❌ Error parsing gradesheet: {str(e)}")
            st.sidebar.write("Please ensure:")
            st.sidebar.write("- File is a valid PDF")
            st.sidebar.write("- Gradesheet contains course codes and grades")
            st.sidebar.write("- Text is readable (not scanned image)")
            
            # Clean up temp file on error
            if os.path.exists("temp.pdf"):
                os.unlink("temp.pdf")

# Manual entry section
st.sidebar.markdown("---")
st.sidebar.subheader("📝 Or Enter Manually")

# Student details
student_name = st.sidebar.text_input("Student Name (Optional)", 
                                    value=st.session_state.academic_record.student_name)
student_id = st.sidebar.text_input("Student ID (Optional)", 
                                  value=st.session_state.academic_record.student_id)

if student_name != st.session_state.academic_record.student_name:
    st.session_state.academic_record.student_name = student_name

if student_id != st.session_state.academic_record.student_id:
    st.session_state.academic_record.student_id = student_id

# Clear/Reset functionality
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear All Data", help="Reset and start fresh"):
    st.session_state.academic_record = AcademicRecord()
    st.session_state.calculator = CGPACalculator(st.session_state.academic_record)
    st.session_state.analyzer = WhatIfAnalyzer(st.session_state.calculator)
    st.success("✅ All data cleared!")
    st.rerun()

# Program requirements
requirements = get_program_requirements(st.session_state.program)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Program Requirements")
st.sidebar.metric("Total Credits Required", requirements["total_credits"])

current_cgpa = st.session_state.calculator.academic_record.get_current_cgpa()
current_credits = st.session_state.calculator.academic_record.get_total_credits()

st.sidebar.metric("Current CGPA", f"{current_cgpa:.2f}")
st.sidebar.metric("Credits Completed", f"{current_credits}/{requirements['total_credits']}")

progress_percentage = (current_credits / requirements['total_credits']) * 100
st.sidebar.progress(progress_percentage / 100)
st.sidebar.caption(f"Progress: {progress_percentage:.1f}%")

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Course Management", "📈 CGPA Planning", "📊 Analytics & Trends", 
    "🔮 What-If Analysis", "📋 Academic Summary"
])

# Tab 1: Course Management
with tab1:
    st.header("🎯 Course Management")
    
    col1, col2 = st.columns(2)
    
    # Add Course Section
    with col1:
        st.subheader("➕ Add Course")
        
        with st.form("add_course_form"):
            all_courses = get_all_courses()
            completed_courses = list(st.session_state.academic_record.courses_taken.keys())
            available_courses = [c for c in all_courses if c not in completed_courses]
            
            course_code = st.selectbox(
                "Select Course:",
                [""] + available_courses,
                format_func=lambda x: f"{x} - {COURSE_NAMES.get(x, 'Course')}" if x else "Select a course"
            )
            
            col_grade, col_gpa = st.columns(2)
            with col_grade:
                grade = st.selectbox("Grade:", [""] + GRADES)
            
            with col_gpa:
                if grade and grade in GRADE_POINTS:
                    gpa = st.number_input("GPA:", value=GRADE_POINTS[grade], min_value=0.0, max_value=4.0, step=0.01)
                else:
                    gpa = st.number_input("GPA:", value=0.0, min_value=0.0, max_value=4.0, step=0.01)
            
            semester = st.selectbox(
                "Semester:",
                ["VIRTUAL SEMESTER", "SPRING 2024", "SUMMER 2024", "FALL 2024", "SPRING 2025", "SUMMER 2025", "FALL 2025"]
            )
            
            credit = st.number_input("Credits:", value=get_course_credit(course_code) if course_code else 3, min_value=1, max_value=6)
            
            add_course_btn = st.form_submit_button("Add Course", type="primary")
            
            if add_course_btn and course_code and grade:
                try:
                    course = Course(course_code, COURSE_NAMES.get(course_code, course_code), credit, grade, gpa)
                    st.session_state.academic_record.add_course_to_semester(semester, course)
                    st.success(f"✅ Added {course_code} successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding course: {str(e)}")
    
    # Remove/Edit Course Section
    with col2:
        st.subheader("✏️ Manage Existing Courses")
        
        if st.session_state.academic_record.courses_taken:
            course_to_manage = st.selectbox(
                "Select Course to Manage:",
                [""] + list(st.session_state.academic_record.courses_taken.keys()),
                format_func=lambda x: f"{x} - {COURSE_NAMES.get(x, 'Course')}" if x else "Select a course"
            )
            
            if course_to_manage:
                current_course = st.session_state.academic_record.courses_taken[course_to_manage]
                
                st.write(f"**Current Details:**")
                st.write(f"- Grade: {current_course.grade}")
                st.write(f"- GPA: {current_course.gpa}")
                st.write(f"- Credits: {current_course.credit}")
                
                # Edit course
                with st.expander("📝 Edit Course"):
                    with st.form(f"edit_course_{course_to_manage}"):
                        new_grade = st.selectbox("New Grade:", GRADES, 
                                               index=GRADES.index(current_course.grade) if current_course.grade in GRADES else 0)
                        new_gpa = st.number_input("New GPA:", value=float(current_course.gpa), min_value=0.0, max_value=4.0, step=0.01)
                        
                        edit_btn = st.form_submit_button("Update Course")
                        
                        if edit_btn:
                            st.session_state.academic_record.update_course_grade(course_to_manage, new_grade, new_gpa)
                            st.success(f"✅ Updated {course_to_manage}!")
                            st.rerun()
                
                # Remove course
                if st.button(f"🗑️ Remove {course_to_manage}", key=f"remove_{course_to_manage}"):
                    st.session_state.academic_record.remove_course(course_to_manage)
                    st.success(f"✅ Removed {course_to_manage}!")
                    st.rerun()
        else:
            st.info("No courses added yet. Add your first course above!")
    
    # Display current courses
    st.markdown("---")
    st.subheader("📚 Current Courses")
    
    if st.session_state.academic_record.courses_taken:
        courses_data = []
        for course_code, course in st.session_state.academic_record.courses_taken.items():
            courses_data.append({
                "Course Code": course_code,
                "Course Name": COURSE_NAMES.get(course_code, "Unknown"),
                "Grade": course.grade,
                "GPA": f"{course.gpa:.2f}",
                "Credits": course.credit,
                "Category": categorize_course(course_code, st.session_state.program),
                "Quality Points": f"{course.get_quality_points():.2f}"
            })
        
        df = pd.DataFrame(courses_data)
        st.dataframe(df, use_container_width=True)
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Courses", len(courses_data))
        with col2:
            st.metric("Total Credits", sum(course.credit for course in st.session_state.academic_record.courses_taken.values()))
        with col3:
            total_qp = sum(course.get_quality_points() for course in st.session_state.academic_record.courses_taken.values())
            st.metric("Quality Points", f"{total_qp:.2f}")
        with col4:
            st.metric("Current CGPA", f"{current_cgpa:.2f}")
    else:
        st.info("No courses added yet.")

# Tab 2: CGPA Planning
with tab2:
    st.header("📈 CGPA Planning & Projection")
    
    # Max CGPA Projection Section (prominent display)
    st.subheader("🔮 Maximum Achievable CGPA")
    max_projection = st.session_state.calculator.calculate_cgpa_projection(
        total_required_credits=requirements["total_credits"]
    )
    
    col_max1, col_max2, col_max3, col_max4 = st.columns(4)
    with col_max1:
        st.metric("Current CGPA", f"{max_projection['current_cgpa']:.2f}")
    with col_max2:
        st.metric("Credits Completed", f"{max_projection['current_credits']}")
    with col_max3:
        st.metric("Remaining Credits", f"{max_projection['remaining_credits']}")
    with col_max4:
        st.metric("**MAX Possible CGPA**", f"{max_projection['max_possible_cgpa']:.2f}", 
                 delta=f"+{max_projection['max_possible_cgpa'] - max_projection['current_cgpa']:.2f}")
    
    if max_projection['remaining_credits'] > 0:
        st.info(f"🎯 **To achieve maximum CGPA:** You need to maintain a **4.0 GPA** in all remaining {max_projection['remaining_credits']} credits.")
    else:
        st.success("🎉 **Congratulations!** You have completed all required credits!")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Target CGPA Calculator")
        
        target_cgpa = st.number_input("Enter Target CGPA:", min_value=0.0, max_value=4.0, value=3.5, step=0.01)
        
        if st.button("Calculate Requirements", type="primary"):
            projection = st.session_state.calculator.calculate_cgpa_projection(
                target_cgpa=target_cgpa, 
                total_required_credits=requirements["total_credits"]
            )
            
            st.markdown("### 📊 Projection Results")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Current CGPA", f"{projection['current_cgpa']:.2f}")
            with col_b:
                st.metric("Max Possible CGPA", f"{projection['max_possible_cgpa']:.2f}")
            with col_c:
                if 'required_avg_gpa' in projection:
                    st.metric("Required Average GPA", f"{projection['required_avg_gpa']:.2f}")
            
            if 'message' in projection:
                if projection['max_possible_cgpa'] < target_cgpa:
                    st.error(projection['message'])
                elif 'required_avg_gpa' in projection and projection['required_avg_gpa'] <= 4.0:
                    st.success(projection['message'])
                else:
                    st.warning(projection['message'])
    
    with col2:
        st.subheader("📅 Semester Planning")
        
        with st.form("semester_planning"):
            num_semesters = st.number_input("Number of Future Semesters:", min_value=1, max_value=10, value=4)
            courses_per_semester = st.number_input("Courses per Semester:", min_value=1, max_value=6, value=4)
            planning_target = st.number_input("Target CGPA for Planning:", min_value=0.0, max_value=4.0, value=3.5, step=0.01)
            
            plan_btn = st.form_submit_button("Generate Plan")
            
            if plan_btn:
                plan = st.session_state.calculator.calculate_semester_planning(
                    target_cgpa=planning_target,
                    num_semesters=num_semesters,
                    courses_per_semester=courses_per_semester,
                    total_required_credits=requirements["total_credits"]
                )
                
                st.markdown("### 📋 Semester Plan")
                
                col_x, col_y, col_z = st.columns(3)
                with col_x:
                    st.metric("Planned Courses", plan['planned_courses'])
                with col_y:
                    st.metric("Planned Credits", plan['planned_credits'])
                with col_z:
                    st.metric("Max Achievable CGPA", f"{plan['max_cgpa']:.2f}")
                
                if 'message' in plan:
                    if 'not achievable' in plan['message'].lower():
                        st.error(plan['message'])
                    else:
                        st.info(plan['message'])
    
    # Course recommendations
    st.markdown("---")
    st.subheader("🔓 Unlocked Courses")
    
    completed_courses = list(st.session_state.academic_record.courses_taken.keys())
    unlocked = get_unlocked_courses(completed_courses)
    
    if unlocked:
        st.success(f"You have {len(unlocked)} courses available to take:")
        
        # Categorize unlocked courses
        unlocked_by_category = {}
        for course in unlocked:
            category = categorize_course(course, st.session_state.program)
            if category not in unlocked_by_category:
                unlocked_by_category[category] = []
            unlocked_by_category[category].append(course)
        
        for category, courses in unlocked_by_category.items():
            with st.expander(f"{category} ({len(courses)} courses)"):
                for course in courses:
                    st.write(f"• **{course}** - {COURSE_NAMES.get(course, 'Course')}")
    else:
        st.info("No new courses are unlocked at this time. Complete prerequisite courses to unlock more options.")

# Tab 3: Analytics & Trends
with tab3:
    st.header("📊 Academic Analytics & Trends")
    
    if not st.session_state.academic_record.courses_taken:
        st.info("Add some courses to see analytics and trends!")
    else:
        # Performance overview
        stats = st.session_state.calculator.get_performance_stats()
        
        st.subheader("📈 Performance Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Courses", stats['total_courses'])
        with col2:
            st.metric("Total Credits", stats['total_credits'])
        with col3:
            st.metric("Current CGPA", f"{stats['current_cgpa']:.2f}")
        with col4:
            st.metric("Highest GPA", f"{stats['highest_gpa']:.2f}")
        with col5:
            st.metric("Average GPA", f"{stats['average_gpa']:.2f}")
        
        # Progress visualization
        st.subheader("🎯 Degree Progress")
        
        completed_credits = stats['total_credits']
        total_required = requirements['total_credits']
        remaining_credits = total_required - completed_credits
        
        # Progress pie chart
        fig_progress = go.Figure(data=[go.Pie(
            labels=['Completed', 'Remaining'],
            values=[completed_credits, remaining_credits],
            hole=0.4,
            marker_colors=['#2E8B57', '#FF6B6B']
        )])
        
        fig_progress.update_traces(textposition='inside', textinfo='percent+label')
        fig_progress.update_layout(
            title=f"Degree Progress ({completed_credits}/{total_required} credits)",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # Grade distribution
        st.subheader("📊 Grade Distribution")
        
        grade_dist = st.session_state.calculator.get_grade_distribution()
        if grade_dist:
            grades = list(grade_dist.keys())
            counts = list(grade_dist.values())
            
            fig_grades = px.bar(
                x=grades, y=counts,
                title="Distribution of Grades",
                labels={'x': 'Grade', 'y': 'Number of Courses'},
                color=counts,
                color_continuous_scale='viridis'
            )
            
            st.plotly_chart(fig_grades, use_container_width=True)
        
        # Semester trends
        trends = st.session_state.calculator.get_semester_trends()
        
        if len(trends['semesters']) > 1:
            st.subheader("📈 Semester Trends")
            
            fig_trends = go.Figure()
            
            fig_trends.add_trace(go.Scatter(
                x=trends['semesters'],
                y=trends['gpas'],
                mode='lines+markers',
                name='Semester GPA',
                line=dict(color='blue'),
                marker=dict(size=8)
            ))
            
            fig_trends.add_trace(go.Scatter(
                x=trends['semesters'],
                y=trends['cgpas'],
                mode='lines+markers',
                name='Cumulative CGPA',
                line=dict(color='red'),
                marker=dict(size=8)
            ))
            
            fig_trends.update_layout(
                title="GPA Trends Over Time",
                xaxis_title="Semester",
                yaxis_title="GPA",
                yaxis=dict(range=[0, 4.1]),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trends, use_container_width=True)
        
        # Course performance by category
        st.subheader("📚 Performance by Course Category")
        
        category_performance = {}
        for course_code, course in st.session_state.academic_record.courses_taken.items():
            category = categorize_course(course_code, st.session_state.program)
            if category not in category_performance:
                category_performance[category] = {'gpas': [], 'credits': 0}
            category_performance[category]['gpas'].append(course.gpa)
            category_performance[category]['credits'] += course.credit
        
        if category_performance:
            categories = []
            avg_gpas = []
            total_credits = []
            
            for category, data in category_performance.items():
                categories.append(category)
                avg_gpas.append(sum(data['gpas']) / len(data['gpas']))
                total_credits.append(data['credits'])
            
            fig_category = go.Figure()
            
            fig_category.add_trace(go.Bar(
                x=categories,
                y=avg_gpas,
                name='Average GPA',
                marker_color='lightblue',
                text=[f"{gpa:.2f}" for gpa in avg_gpas],
                textposition='auto'
            ))
            
            fig_category.update_layout(
                title="Average GPA by Course Category",
                xaxis_title="Course Category",
                yaxis_title="Average GPA",
                yaxis=dict(range=[0, 4.1])
            )
            
            st.plotly_chart(fig_category, use_container_width=True)

# Tab 4: What-If Analysis
with tab4:
    st.header("🔮 What-If Analysis")
    
    st.markdown("""
    Explore how different scenarios would affect your CGPA. Use this tool to make informed decisions about retakes, future courses, and academic planning.
    """)
    
    analysis_type = st.radio(
        "Choose Analysis Type:",
        ["🔄 Course Retake Simulation", "➕ New Course Impact", "📈 Grade Improvement Analysis"]
    )
    
    if analysis_type == "🔄 Course Retake Simulation":
        st.subheader("Course Retake Simulation")
        
        if not st.session_state.academic_record.courses_taken:
            st.info("Add courses first to simulate retakes.")
        else:
            completed_courses = list(st.session_state.academic_record.courses_taken.keys())
            
            with st.form("retake_simulation"):
                st.write("Select courses to retake and their new expected GPAs:")
                
                retake_courses = {}
                
                for i, course_code in enumerate(completed_courses[:5]):  # Limit to first 5 courses for UI
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        retake = st.checkbox(f"Retake {course_code}", key=f"retake_{course_code}")
                    
                    with col2:
                        if retake:
                            current_gpa = st.session_state.academic_record.courses_taken[course_code].gpa
                            new_gpa = st.number_input(
                                f"New GPA for {course_code}:",
                                min_value=0.0, max_value=4.0, value=min(4.0, current_gpa + 1.0),
                                step=0.01, key=f"new_gpa_{course_code}"
                            )
                            retake_courses[course_code] = new_gpa
                    
                    with col3:
                        if course_code in st.session_state.academic_record.courses_taken:
                            current = st.session_state.academic_record.courses_taken[course_code].gpa
                            st.caption(f"Current: {current:.2f}")
                
                simulate_btn = st.form_submit_button("Simulate Retakes")
                
                if simulate_btn and retake_courses:
                    result = st.session_state.calculator.simulate_retakes(retake_courses)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Current CGPA", f"{current_cgpa:.2f}")
                    with col2:
                        st.metric("Projected CGPA", f"{result['simulated_cgpa']:.2f}")
                    with col3:
                        improvement = result['improvement']
                        st.metric("Improvement", f"{improvement:+.2f}", delta=improvement)
                    
                    if improvement > 0:
                        st.success(result['message'])
                    elif improvement < 0:
                        st.warning("This would decrease your CGPA.")
                    else:
                        st.info("No change in CGPA.")
    
    elif analysis_type == "➕ New Course Impact":
        st.subheader("New Course Impact Analysis")
        
        with st.form("new_course_impact"):
            all_courses = get_all_courses()
            completed = list(st.session_state.academic_record.courses_taken.keys())
            available = [c for c in all_courses if c not in completed]
            
            course_to_add = st.selectbox(
                "Course to analyze:",
                [""] + available,
                format_func=lambda x: f"{x} - {COURSE_NAMES.get(x, 'Course')}" if x else "Select a course"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                expected_gpa = st.number_input("Expected GPA:", min_value=0.0, max_value=4.0, value=3.5, step=0.01)
            with col2:
                credits = st.number_input("Credits:", min_value=1, max_value=6, value=get_course_credit(course_to_add) if course_to_add else 3)
            
            analyze_btn = st.form_submit_button("Analyze Impact")
            
            if analyze_btn and course_to_add:
                result = st.session_state.analyzer.analyze_course_addition(course_to_add, expected_gpa, credits)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current CGPA", f"{result['current_cgpa']:.2f}")
                with col2:
                    st.metric("Projected CGPA", f"{result['projected_cgpa']:.2f}")
                with col3:
                    change = result['cgpa_change']
                    st.metric("CGPA Change", f"{change:+.3f}", delta=change)
                
                st.info(result['message'])
    
    elif analysis_type == "📈 Grade Improvement Analysis":
        st.subheader("Grade Improvement Analysis")
        
        if not st.session_state.academic_record.courses_taken:
            st.info("Add courses first to analyze grade improvements.")
        else:
            with st.form("grade_improvement"):
                completed_courses = list(st.session_state.academic_record.courses_taken.keys())
                
                course_to_improve = st.selectbox(
                    "Select course to improve:",
                    [""] + completed_courses,
                    format_func=lambda x: f"{x} - {COURSE_NAMES.get(x, 'Course')}" if x else "Select a course"
                )
                
                if course_to_improve:
                    current_gpa = st.session_state.academic_record.courses_taken[course_to_improve].gpa
                    st.write(f"Current GPA: **{current_gpa:.2f}**")
                    
                    new_gpa = st.number_input("New GPA:", min_value=0.0, max_value=4.0, value=min(4.0, current_gpa + 0.5), step=0.01)
                
                improve_btn = st.form_submit_button("Analyze Improvement")
                
                if improve_btn and course_to_improve:
                    result = st.session_state.analyzer.analyze_grade_improvement(course_to_improve, new_gpa)
                    
                    if 'error' not in result:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Current CGPA", f"{result['current_cgpa']:.2f}")
                        with col2:
                            st.metric("Projected CGPA", f"{result['projected_cgpa']:.2f}")
                        with col3:
                            change = result['cgpa_change']
                            st.metric("CGPA Change", f"{change:+.3f}", delta=change)
                        
                        st.info(result['message'])
                    else:
                        st.error(result['error'])

# Tab 5: Academic Summary
with tab5:
    st.header("📋 Academic Summary")
    
    # Student information
    if student_name or student_id:
        st.subheader("👤 Student Information")
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            if student_name:
                st.write(f"**Name:** {student_name}")
        with info_col2:
            if student_id:
                st.write(f"**Student ID:** {student_id}")
        
        st.markdown("---")
    
    # Academic overview
    st.subheader("📊 Academic Overview")
    
    overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
    
    with overview_col1:
        st.metric("Program", st.session_state.program)
    
    with overview_col2:
        st.metric("Current CGPA", f"{current_cgpa:.2f}")
    
    with overview_col3:
        st.metric("Credits Completed", f"{current_credits}")
    
    with overview_col4:
        remaining = requirements['total_credits'] - current_credits
        st.metric("Credits Remaining", f"{remaining}")
    
    # Course breakdown by category
    if st.session_state.academic_record.courses_taken:
        st.subheader("📚 Course Breakdown by Category")
        
        category_data = {}
        for course_code, course in st.session_state.academic_record.courses_taken.items():
            category = categorize_course(course_code, st.session_state.program)
            if category not in category_data:
                category_data[category] = {'courses': [], 'credits': 0, 'total_qp': 0}
            
            category_data[category]['courses'].append({
                'code': course_code,
                'name': COURSE_NAMES.get(course_code, 'Unknown'),
                'grade': course.grade,
                'gpa': course.gpa,
                'credits': course.credit
            })
            category_data[category]['credits'] += course.credit
            category_data[category]['total_qp'] += course.get_quality_points()
        
        for category, data in category_data.items():
            with st.expander(f"{category} ({len(data['courses'])} courses, {data['credits']} credits)"):
                avg_gpa = data['total_qp'] / data['credits'] if data['credits'] > 0 else 0
                st.write(f"**Average GPA:** {avg_gpa:.2f}")
                
                course_df = pd.DataFrame(data['courses'])
                course_df.columns = ['Course Code', 'Course Name', 'Grade', 'GPA', 'Credits']
                st.dataframe(course_df, use_container_width=True, hide_index=True)
    
    # General education planning
    st.subheader("🎓 General Education Planning")
    
    completed_courses = list(st.session_state.academic_record.courses_taken.keys())
    ge_plan = plan_general_education_courses(completed_courses)
    
    ge_col1, ge_col2, ge_col3, ge_col4, ge_col5 = st.columns(5)
    
    with ge_col1:
        st.metric("Arts", ge_plan['arts_completed'])
    with ge_col2:
        st.metric("Social Science", ge_plan['social_science_completed'])
    with ge_col3:
        st.metric("CST", ge_plan['cst_completed'])
    with ge_col4:
        st.metric("Science", ge_plan['science_completed'])
    with ge_col5:
        st.metric("Total Streams", ge_plan['total_completed'])
    
    if ge_plan['plan']:
        st.write("**Recommended next courses:**")
        for stream, course in ge_plan['plan']:
            st.write(f"- **{course}** ({stream} stream) - {COURSE_NAMES.get(course, 'Course')}")
    
    # Degree completion projection
    st.subheader("🎯 Degree Completion Projection")
    
    if current_credits > 0:
        remaining_credits = requirements['total_credits'] - current_credits
        
        if remaining_credits <= 0:
            st.success("🎉 Congratulations! You have completed all required credits!")
        else:
            avg_credits_per_semester = 12  # Assume 4 courses * 3 credits
            estimated_semesters = (remaining_credits + avg_credits_per_semester - 1) // avg_credits_per_semester
            
            proj_col1, proj_col2 = st.columns(2)
            with proj_col1:
                st.metric("Estimated Semesters to Graduate", estimated_semesters)
            with proj_col2:
                st.metric("Credits Remaining", remaining_credits)
            
            # Calculate what CGPA is needed for different targets
            st.write("**CGPA Requirements for Target CGPAs:**")
            
            target_cgpas = [3.0, 3.25, 3.5, 3.75]
            target_df = []
            
            for target in target_cgpas:
                projection = st.session_state.calculator.calculate_cgpa_projection(
                    target_cgpa=target, 
                    total_required_credits=requirements["total_credits"]
                )
                
                if 'required_avg_gpa' in projection:
                    required_gpa = projection['required_avg_gpa']
                    achievable = "✅" if required_gpa <= 4.0 else "❌"
                    target_df.append({
                        'Target CGPA': target,
                        'Required Average GPA': f"{required_gpa:.2f}",
                        'Achievable': achievable
                    })
            
            if target_df:
                st.dataframe(pd.DataFrame(target_df), use_container_width=True, hide_index=True)
    else:
        st.info("Add some courses to see degree completion projections!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
<p>🎓 CGPA Projection Tool | Plan Smart • Study Hard • Achieve More</p>
<p><small>Built for academic success</small></p>
</div>
""", unsafe_allow_html=True)