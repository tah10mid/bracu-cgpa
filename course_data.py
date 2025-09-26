"""
Course Data and University Configuration
Contains course prerequisites, categories, and grading systems
"""

# Grading system
GRADES = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "W", "I"]

GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "F": 0.0,
    "W": 0.0, "I": 0.0
}

# Course Prerequisites (course -> list of courses it unlocks)
COURSE_PREREQUISITES = {
    # Math courses
    "MAT110": ["MAT120"], 
    "MAT120": ["MAT215", "MAT216"], 
    "MAT215": [], 
    "MAT216": ["CSE330", "CSE423"],
    
    # Physics
    "PHY111": ["PHY112"], 
    "PHY112": ["CSE250"],
    
    # English
    "ENG101": ["ENG102"], 
    "ENG102": ["ENG103"], 
    "ENG103": [],
    
    # Core CSE courses
    "CSE110": ["CSE111"], 
    "CSE111": ["CSE220"], 
    "CSE220": ["CSE221"],
    "CSE221": ["CSE321", "CSE331", "CSE370", "CSE422"],
    "CSE230": [], 
    "CSE250": ["CSE251"], 
    "CSE251": ["CSE260", "CSE350"],
    "CSE260": ["CSE340", "CSE341", "CSE460", "CSE461"],
    "CSE340": ["CSE341", "CSE420"], 
    "CSE341": ["CSE360", "CSE461"],
    "CSE320": ["CSE421"], 
    "CSE350": [], 
    "CSE360": ["CSE461"],
    "CSE370": ["CSE470", "CSE471"], 
    "CSE420": [], 
    "CSE421": ["CSE400"], 
    "CSE422": ["CSE400"],
    "CSE423": [], 
    "CSE460": [], 
    "CSE461": [], 
    "CSE470": ["CSE400"], 
    "CSE471": [],
    "CSE321": ["CSE420"], 
    "CSE331": ["CSE420"], 
    "CSE400": [], 
    "CSE330": [],
    
    # Elective courses
    "CSE310": [], "CSE342": [], "CSE371": [], "CSE390": [],
    "CSE391": [], "CSE392": [], "CSE410": [], "CSE419": [], 
    "CSE424": [], "CSE425": [], "CSE426": [], "CSE427": [], 
    "CSE428": [], "CSE429": [], "CSE430": [], "CSE431": [], 
    "CSE432": [], "CSE462": [], "CSE472": [], "CSE473": [], 
    "CSE474": [], "CSE490": [], "CSE491": [],
    
    # General education courses
    "HUM101": [], "HUM102": [], "HUM103": [], "HST102": [], 
    "HST104": [], "HUM207": [], "BNG103": [], "EMB101": [],
    "ENG113": [], "ENG114": [], "ENG115": [], "ENG333": [],
    "STA201": [],
    
    # Science courses
    "CHE101": [], "BIO101": [], "ENV103": [],
    
    # Social Science courses
    "PSY101": [], "SOC101": [], "ANT101": [], "POL101": [], 
    "BUS201": [], "ECO101": [], "ECO102": [], "ECO105": [], 
    "BUS102": [], "POL102": [], "DEV104": [], "POL201": [], 
    "SOC201": [], "ANT342": [], "ANT351": [], "BUS333": [],
    
    # CST courses
    "CST301": [], "CST302": [], "CST303": [], "CST304": [], "CST305": [],
    "CST306": [], "CST307": [], "CST308": [], "CST309": [], "CST310": [],
}

# Course Categories
CORE_CSE_COURSES = {
    "CSE110", "CSE111", "CSE220", "CSE221", "CSE230", "CSE250", 
    "CSE251", "CSE260", "CSE320", "CSE321", "CSE330", "CSE331", 
    "CSE340", "CSE341", "CSE350", "CSE360", "CSE370", "CSE420", 
    "CSE421", "CSE422", "CSE423", "CSE460", "CSE461", "CSE470", "CSE471"
}

CORE_CS_COURSES = CORE_CSE_COURSES - {"CSE250", "CSE251", "CSE320", "CSE341", "CSE350", "CSE360"}

CSE_ELECTIVES = {
    "CSE310", "CSE342", "CSE371", "CSE390", "CSE391", "CSE392", 
    "CSE410", "CSE419", "CSE424", "CSE425", "CSE426", "CSE427", 
    "CSE428", "CSE429", "CSE430", "CSE431", "CSE432", "CSE462", 
    "CSE472", "CSE473", "CSE474", "CSE490", "CSE491"
}

# Compulsory General Education courses
COMPULSORY_GENERAL_ED = {
    "PHY111", "PHY112", "ENG101", "ENG102", "MAT110", "MAT120", 
    "MAT215", "MAT216", "STA201", "HUM103", "BNG103", "EMB101"
}

# TARC courses (Transfer And Readmission Credit)
TARC_COURSES = {"HUM103", "BNG103", "EMB101", "ENG102"}

# Science stream courses
SCIENCE_STREAM = {"CHE101", "BIO101", "ENV103"}

# Arts stream courses  
ARTS_STREAM = {
    "HUM101", "HUM102", "HST102", "HST104", "HUM207",
    "ENG113", "ENG114", "ENG115", "ENG333", "ENG103"
}

# Social Science stream courses
SOCIAL_SCIENCE_STREAM = {
    "PSY101", "SOC101", "ANT101", "POL101", "BUS201", 
    "ECO101", "ECO102", "ECO105", "BUS102", "POL102", 
    "DEV104", "POL201", "SOC201", "ANT342", "ANT351", "BUS333"
}

# CST stream courses
CST_STREAM = {
    "CST301", "CST302", "CST303", "CST304", "CST305",
    "CST306", "CST307", "CST308", "CST309", "CST310"
}

# Lab courses (typically 1 credit)
LAB_COURSES = {
    "CSE110", "CSE111", "CSE220", "CSE221", "CSE230", "CSE250", 
    "CSE251", "CSE260", "CSE321", "CSE330", "CSE341", "CSE350", 
    "CSE360", "CSE370", "CSE420", "CSE421", "CSE422", "CSE423", 
    "CSE460", "CSE461", "CSE471", "PHY111", "PHY112", "MAT120"
}

# Course names mapping
COURSE_NAMES = {
    # Math
    "MAT110": "Mathematics I",
    "MAT120": "Mathematics II", 
    "MAT215": "Statistics and Probability",
    "MAT216": "Discrete Mathematics",
    
    # Physics
    "PHY111": "Physics I",
    "PHY112": "Physics II",
    
    # English
    "ENG101": "English Composition I",
    "ENG102": "English Composition II",
    "ENG103": "Report Writing",
    
    # Core CSE
    "CSE110": "Programming Language I",
    "CSE111": "Programming Language II", 
    "CSE220": "Data Structures",
    "CSE221": "Algorithms",
    "CSE230": "Digital Logic Design",
    "CSE250": "Circuits and Electronics",
    "CSE251": "Electronic Devices and Circuits",
    "CSE260": "Digital Electronics and Pulse Techniques",
    "CSE320": "Data Communication",
    "CSE321": "Computer Networks",
    "CSE330": "Numerical Methods",
    "CSE331": "Microprocessor Interfacing & Embedded System",
    "CSE340": "Computer Architecture",
    "CSE341": "Microprocessors",
    "CSE350": "Software Engineering",
    "CSE360": "Database Management System",
    "CSE370": "Operating System",
    "CSE400": "Project/Thesis",
    "CSE420": "Compiler",
    "CSE421": "Computer Networks",
    "CSE422": "Artificial Intelligence",
    "CSE423": "Computer Graphics",
    "CSE460": "Algorithm Engineering",
    "CSE461": "Database Management System II",
    "CSE470": "Software Engineering",
    "CSE471": "System Analysis and Design",
    
    # General Education
    "HUM103": "Bangladesh Studies",
    "BNG103": "Bangla",
    "EMB101": "Microbiology",
    "STA201": "Business Statistics",
    
    # Science
    "CHE101": "General Chemistry",
    "BIO101": "General Biology", 
    "ENV103": "Environmental Science",
}

# Default credit values
DEFAULT_CREDITS = {
    "CSE400": 4,  # Project/Thesis is 4 credits
    # Most other courses are 3 credits by default
}

def get_course_credit(course_code):
    """Get credit value for a course"""
    return DEFAULT_CREDITS.get(course_code, 3)

def get_unlocked_courses(completed_courses):
    """Get list of courses that are now unlocked based on completed courses"""
    completed_set = set(completed_courses)
    unlocked = set()
    
    # Build prerequisite map (what each course requires)
    prereq_map = {}
    for course, unlocks_list in COURSE_PREREQUISITES.items():
        for unlocked_course in unlocks_list:
            if unlocked_course not in prereq_map:
                prereq_map[unlocked_course] = []
            prereq_map[unlocked_course].append(course)
    
    # Check which courses are unlocked
    for course in COURSE_PREREQUISITES.keys():
        if course in completed_set:
            continue  # Already completed
            
        prereqs = prereq_map.get(course, [])
        if all(prereq in completed_set for prereq in prereqs):
            unlocked.add(course)
    
    return sorted(unlocked)

def get_all_courses():
    """Get all available courses"""
    all_courses = set(COURSE_PREREQUISITES.keys())
    
    # Add courses from all categories
    all_courses.update(CORE_CSE_COURSES)
    all_courses.update(CSE_ELECTIVES)
    all_courses.update(COMPULSORY_GENERAL_ED)
    all_courses.update(SCIENCE_STREAM)
    all_courses.update(ARTS_STREAM)
    all_courses.update(SOCIAL_SCIENCE_STREAM)
    all_courses.update(CST_STREAM)
    
    return sorted(all_courses)

def categorize_course(course_code, program="CSE"):
    """Categorize a course based on program"""
    if program == "CSE":
        core_courses = CORE_CSE_COURSES
    else:
        core_courses = CORE_CS_COURSES
    
    if course_code in core_courses:
        return "Core"
    elif course_code in COMPULSORY_GENERAL_ED:
        return "Compulsory General Education"
    elif course_code in CSE_ELECTIVES:
        return "CSE Elective"
    elif course_code in SCIENCE_STREAM:
        return "Science Stream"
    elif course_code in ARTS_STREAM:
        return "Arts Stream"
    elif course_code in SOCIAL_SCIENCE_STREAM:
        return "Social Science Stream"
    elif course_code in CST_STREAM:
        return "CST Stream"
    else:
        return "Other"

def get_program_requirements(program="CSE"):
    """Get credit requirements for a program"""
    if program == "CSE":
        return {
            "total_credits": 136,
            "core_credits": len(CORE_CSE_COURSES) * 3 + 4,  # +4 for CSE400
            "general_ed_credits": 36,
            "elective_credits": 18
        }
    else:  # CS
        return {
            "total_credits": 124,
            "core_credits": len(CORE_CS_COURSES) * 3 + 4,  # +4 for CSE400
            "general_ed_credits": 36,
            "elective_credits": 12
        }

def plan_general_education_courses(completed_courses, max_courses=5):
    """Plan general education courses based on completion status"""
    completed_set = set(completed_courses)
    
    # Count courses in each stream
    arts_completed = len([c for c in completed_courses if c in ARTS_STREAM])
    social_science_completed = len([c for c in completed_courses if c in SOCIAL_SCIENCE_STREAM])  
    cst_completed = len([c for c in completed_courses if c in CST_STREAM])
    science_completed = len([c for c in completed_courses if c in SCIENCE_STREAM])
    
    total_stream_courses = arts_completed + social_science_completed + cst_completed + science_completed
    remaining = max_courses - total_stream_courses
    
    plan = []
    
    # Priority: Arts (required), Social Science (required), then others
    if arts_completed == 0 and remaining > 0:
        available_arts = [c for c in ARTS_STREAM if c not in completed_set]
        if available_arts:
            plan.append(("Arts", available_arts[0]))
            remaining -= 1
    
    if social_science_completed == 0 and remaining > 0:
        available_ss = [c for c in SOCIAL_SCIENCE_STREAM if c not in completed_set]
        if available_ss:
            plan.append(("Social Science", available_ss[0]))
            remaining -= 1
    
    if cst_completed == 0 and remaining > 0:
        available_cst = [c for c in CST_STREAM if c not in completed_set]
        if available_cst:
            plan.append(("CST", available_cst[0]))
            remaining -= 1
    
    if science_completed == 0 and remaining > 0:
        available_science = [c for c in SCIENCE_STREAM if c not in completed_set]
        if available_science:
            plan.append(("Science", available_science[0]))
            remaining -= 1
    
    return {
        "plan": plan,
        "arts_completed": arts_completed,
        "social_science_completed": social_science_completed,
        "cst_completed": cst_completed,
        "science_completed": science_completed,
        "total_completed": total_stream_courses,
        "remaining_slots": remaining
    }