# 🎓 BRACU CGPA Projection & Academic Planning Tool

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

A comprehensive web-based academic planning tool specifically designed for BRAC University students to track progress, project CGPA, and make informed decisions about their academic journey.

## 🌟 Live Demo

**🚀 [Launch the App](https://your-app-url.streamlit.app)**

Upload your BRACU gradesheet and start planning your academic success!

## ✨ Key Features

### 📄 **Smart Gradesheet Analysis**
- **PDF Upload**: Upload your official BRACU gradesheet/transcript
- **Automatic Parsing**: Extracts all course data, grades, and semester information
- **Intelligent Recognition**: Supports official BRACU gradesheet format
- **Real-time Processing**: Instant analysis and data loading

### 🎯 **CGPA Calculation & Projection**
- **Current CGPA**: Real-time calculation from all completed courses
- **Maximum Achievable CGPA**: See your highest possible CGPA
- **Target CGPA Planning**: Calculate what grades you need for your goal
- **Semester-wise Planning**: Plan future semesters strategically

### 📊 **Advanced Analytics**
- **Performance Trends**: Visualize your GPA progression over time
- **Grade Distribution**: Analyze your grade patterns
- **Category Analysis**: Performance breakdown by course categories
- **Interactive Charts**: Beautiful Plotly visualizations

### 🔮 **What-If Analysis**
- **Course Retake Simulation**: See how retaking courses affects CGPA
- **New Course Impact**: Analyze adding new courses to your record
- **Grade Improvement**: Calculate benefits of improving specific grades
- **Scenario Planning**: Explore different academic paths

### 📋 **Academic Management**
- **Course Management**: Add, edit, and remove courses easily
- **Semester Organization**: Organize courses by academic terms
- **Progress Tracking**: Monitor degree completion progress
- **Requirement Planning**: Track CSE/CS program requirements

## 🚀 Quick Start

### Option 1: Use Online (Recommended)
1. **Visit**: [Live App Link](https://your-app-url.streamlit.app)
2. **Upload**: Your BRACU gradesheet PDF
3. **Analyze**: Explore your academic data and projections
4. **Plan**: Use planning tools for future semesters

### Option 2: Run Locally
1. **Clone the repository**:
   ```bash
   git clone https://github.com/tah10mid/bracu-cgpa.git
   cd bracu-cgpa
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open browser**: Go to `http://localhost:8501`

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28.0+
- PyMuPDF 1.23.0+ (for PDF processing)
- Plotly 5.17.0+ (for visualizations)
- Pandas 2.0.0+ (for data handling)

## 📖 How to Use

### 📄 **Step 1: Upload Your Gradesheet**
- Click "Browse files" in the sidebar
- Select your official BRACU gradesheet PDF
- Click "Parse Gradesheet" to analyze

### 🎯 **Step 2: Review Your Data**
- Check the parsed courses and grades
- Verify your current CGPA calculation
- Explore the semester breakdown

### 📊 **Step 3: Analyze Performance**
- Visit "Analytics & Trends" tab
- Review grade distributions and trends
- Understand your academic patterns

### 🔮 **Step 4: Plan Your Future**
- Use "CGPA Planning" for target setting
- Try "What-If Analysis" for scenarios
- Plan future courses strategically

## 🎓 Supported Programs

- **CSE (Computer Science & Engineering)**: 136 credits
- **CS (Computer Science)**: 124 credits

### Course Categories
- **Core Courses**: Major requirement courses
- **General Education**: Math, Physics, English, etc.
- **Electives**: Specialized courses in your field
- **Stream Courses**: Arts, Social Science, Science, CST

## 📊 Technical Features

### 🔧 **PDF Processing**
- Advanced text extraction using PyMuPDF
- Pattern recognition for course codes and grades
- Semester-wise organization
- Error handling and validation

### 🎨 **User Interface**
- Clean, professional Streamlit interface
- Responsive design for all devices
- Interactive charts and visualizations
- Intuitive navigation with tabs

### 📈 **Calculations**
- Accurate CGPA computation
- Quality points calculation
- Credit-weighted averages
- Projection algorithms

## 🌐 Deployment on Streamlit Cloud

### For Developers
1. **Fork this repository**
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Choose `app.py` as main file
3. **Deploy**: Your app will be live in minutes!

### Configuration
- All dependencies are in `requirements.txt`
- Streamlit configuration in `.streamlit/config.toml`
- No additional setup needed

## 🔒 Privacy & Security

- **Local Processing**: All data processed locally in your browser
- **No Data Storage**: Personal information not stored on servers
- **Secure Upload**: Files processed temporarily and discarded
- **Privacy First**: Your academic data stays private

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? Report it in Issues
2. **Suggest Features**: Ideas for improvement? Let us know
3. **Submit PRs**: Code improvements are welcome
4. **Update Course Data**: Help maintain accurate course information

## 📞 Support & Feedback

- **Issues**: [GitHub Issues](https://github.com/tah10mid/bracu-cgpa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tah10mid/bracu-cgpa/discussions)
- **Email**: For private concerns

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **BRAC University** for the academic structure and grading system
- **Streamlit** for the amazing web app framework
- **The Academic Community** for inspiration and feedback

## 📋 Changelog

### Version 1.0.0 (September 2025)
- ✅ Initial release
- ✅ PDF gradesheet parsing
- ✅ CGPA calculation and projection
- ✅ Advanced analytics and visualization
- ✅ What-if analysis tools
- ✅ Academic planning features

---

**Made with ❤️ for BRACU students**

*Plan Smart • Study Hard • Achieve More* 🎓
