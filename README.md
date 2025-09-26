# 🎓 BRACU CGPA Projection & Academic Planning Tool

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bracu-cgpa.streamlit.app)

A comprehensive web-based academic planning tool specifically designed for BRAC University students to track progress, project CGPA, and make informed decisions about their academic journey.

## 🚀 **[Launch the Live App](https://bracu-cgpa.streamlit.app)**

*Ready to deploy on Streamlit Cloud!*

## ✨ Features

### 🎯 Course Management
- **Add/Remove Courses**: Easily manage your academic record
- **Grade Updates**: Update grades for retaken courses
- **Multi-Semester Support**: Organize courses by semester
- **Course Categories**: Automatic categorization (Core, Electives, General Education)

### 📈 CGPA Planning & Projection
- **Target CGPA Calculator**: See what grades you need to reach your goal
- **Semester Planning**: Plan future semesters with course load optimization
- **Maximum CGPA Projection**: Know your highest achievable CGPA
- **Credit Requirements**: Track progress toward degree completion

### 📊 Analytics & Trends
- **Performance Overview**: Comprehensive academic statistics
- **Semester Trends**: Visualize GPA progression over time
- **Grade Distribution**: See your grade patterns
- **Category Performance**: Analyze performance by course type
- **Progress Visualization**: Interactive charts and graphs

### 🔮 What-If Analysis
- **Course Retake Simulation**: See how retaking courses affects your CGPA
- **New Course Impact**: Analyze the effect of adding new courses
- **Grade Improvement Analysis**: Understand the impact of grade changes

### 📋 Academic Summary
- **Complete Academic Record**: Detailed breakdown by category
- **General Education Planning**: Strategic course selection guidance
- **Degree Completion Projection**: Estimate graduation timeline
- **Requirement Tracking**: Monitor progress toward program requirements

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd cgpa-projection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   The application will automatically open in your default browser at `http://localhost:8501`

## 🎮 How to Use

### Getting Started
1. **Select Your Program**: Choose between CSE or CS in the sidebar
2. **Enter Student Info**: Optionally add your name and student ID
3. **Add Courses**: Start adding your completed courses with grades

### Adding Courses
1. Go to the **Course Management** tab
2. Select a course from the dropdown menu
3. Enter your grade and GPA
4. Choose the semester
5. Click "Add Course"

### Planning Your Future
1. Navigate to the **CGPA Planning** tab
2. Set your target CGPA
3. Use the semester planner to see course requirements
4. Check unlocked courses based on prerequisites

### Analyzing Performance
1. Visit the **Analytics & Trends** tab
2. View your performance metrics
3. Explore interactive charts and visualizations
4. Analyze performance by course category

### What-If Scenarios
1. Go to the **What-If Analysis** tab
2. Simulate retaking courses with better grades
3. Analyze the impact of new courses
4. Explore different academic scenarios

## 📚 Supported Programs

### CSE (Computer Science & Engineering)
- **Total Credits**: 136
- **Core Courses**: 25+ courses
- **Electives**: 6 courses
- **General Education**: 12+ courses

### CS (Computer Science)
- **Total Credits**: 124
- **Core Courses**: 22+ courses
- **Electives**: 4 courses
- **General Education**: 12+ courses

## 🎯 Key Features in Detail

### Intelligent Course Prerequisites
The system understands course prerequisites and automatically shows you which courses you can take next based on your completed courses.

### Comprehensive CGPA Calculations
- Real-time CGPA updates
- Quality points tracking
- Credit-weighted averages
- Semester-wise GPA calculations

### Visual Analytics
- Interactive Plotly charts
- Semester trend analysis
- Grade distribution visualization
- Progress tracking pie charts

### Academic Planning Tools
- Target CGPA requirements calculator
- Semester course load planning
- General education stream planning
- Degree completion timeline estimation

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualization
- **Pandas**: Data manipulation and analysis
- **Python**: Core programming language

### Architecture
```
cgpa-projection/
├── app.py                 # Main Streamlit application
├── course_utils.py        # Course and semester management classes
├── cgpa_calculator.py     # CGPA calculation and projection logic
├── course_data.py         # Course data, prerequisites, and categories
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── data/                 # Data storage directory
```

## 📖 Course Categories

### Core Courses
Essential courses required for your major (CSE110, CSE111, CSE220, etc.)

### General Education
- **Compulsory**: Math, Physics, English, Bengali studies
- **Arts Stream**: Humanities and literature courses
- **Social Science Stream**: Psychology, sociology, economics
- **Science Stream**: Chemistry, biology, environmental science
- **CST Stream**: Computer studies and technology courses

### Electives
Specialized courses in your field of interest

## 🎨 User Interface

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Clean, intuitive interface
- Professional color scheme

### Interactive Elements
- Real-time calculations
- Dynamic charts and graphs
- Form-based data entry
- Tabbed navigation

## 🔧 Customization

### Adding New Courses
1. Edit `course_data.py`
2. Add course codes to appropriate categories
3. Update prerequisites mapping
4. Add course names to `COURSE_NAMES` dictionary

### Modifying Program Requirements
1. Update `get_program_requirements()` function in `course_data.py`
2. Adjust credit requirements and course counts

## 📱 Usage Tips

### Best Practices
1. **Start with completed courses**: Add all your finished courses first
2. **Keep grades updated**: Update grades for retaken courses
3. **Use what-if analysis**: Explore different scenarios before making decisions
4. **Plan ahead**: Use the semester planner for future course selection
5. **Check prerequisites**: Always verify course prerequisites before enrolling

### Data Management
- Your data is stored locally in your browser session
- No personal information is transmitted or stored externally
- Refresh the page to start with a clean slate

## 🔮 Future Enhancements

### Planned Features
- **Data Import/Export**: Save and load academic records
- **Course Recommendations**: AI-powered course suggestions
- **Scholarship Tracking**: Monitor scholarship GPA requirements
- **Comparative Analysis**: Compare with program averages
- **Academic Calendar Integration**: Semester and deadline tracking

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Use the issue tracker to report problems
2. **Suggest Features**: Share ideas for new functionality
3. **Submit Pull Requests**: Contribute code improvements
4. **Update Course Data**: Help maintain accurate course information

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by the BRACU Gradesheet Analyzer project
- Built for students, by students
- Special thanks to the academic planning community

## 📞 Support

If you encounter any issues or have questions:

1. Check the documentation above
2. Look for similar issues in the project repository
3. Create a new issue with detailed information
4. Include screenshots if reporting UI problems

---

**Happy Academic Planning! 🎓📚**

*Plan Smart • Study Hard • Achieve More*