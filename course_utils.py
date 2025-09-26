"""
Course and Semester Management Utilities
"""

class Course:
    """Represents a single course with its academic details"""
    
    def __init__(self, course_code, course_name="", credit=3, grade="", gpa=0.0):
        self.course_code = course_code
        self.course_name = course_name
        self.credit = credit
        self.grade = grade
        self.gpa = gpa
        
    def __repr__(self):
        return f"Course({self.course_code}, {self.grade}, {self.gpa}, {self.credit})"
    
    def get_quality_points(self):
        """Calculate quality points for this course"""
        return self.gpa * self.credit
    
    def update_grade(self, grade, gpa):
        """Update course grade and GPA"""
        self.grade = grade
        self.gpa = gpa


class Semester:
    """Represents a semester with multiple courses"""
    
    def __init__(self, semester_name):
        self.semester_name = semester_name
        self.courses = []
        self.gpa = 0.0
        self.credit = 0
        self.cgpa = 0.0
        
    def add_course(self, course):
        """Add a course to this semester"""
        self.courses.append(course)
        self._calculate_stats()
        
    def remove_course(self, course_code):
        """Remove a course from this semester"""
        self.courses = [c for c in self.courses if c.course_code != course_code]
        self._calculate_stats()
        
    def _calculate_stats(self):
        """Calculate semester GPA and total credits"""
        if not self.courses:
            self.gpa = 0.0
            self.credit = 0
            return
            
        total_quality_points = sum(course.get_quality_points() for course in self.courses)
        total_credits = sum(course.credit for course in self.courses)
        
        self.gpa = round(total_quality_points / total_credits, 2) if total_credits > 0 else 0.0
        self.credit = total_credits
        
    def get_courses_list(self):
        """Get list of course codes in this semester"""
        return [course.course_code for course in self.courses]


class AcademicRecord:
    """Manages all academic records across semesters"""
    
    def __init__(self, student_name="", student_id=""):
        self.student_name = student_name
        self.student_id = student_id
        self.semesters = {}
        self.courses_taken = {}  # course_code -> Course object
        
    def add_semester(self, semester_name):
        """Add a new semester"""
        if semester_name not in self.semesters:
            self.semesters[semester_name] = Semester(semester_name)
    
    def add_course_to_semester(self, semester_name, course):
        """Add a course to a specific semester"""
        if semester_name not in self.semesters:
            self.add_semester(semester_name)
            
        self.semesters[semester_name].add_course(course)
        self.courses_taken[course.course_code] = course
        self._update_cgpa()
    
    def remove_course(self, course_code):
        """Remove a course from all records"""
        # Remove from courses_taken
        if course_code in self.courses_taken:
            del self.courses_taken[course_code]
        
        # Remove from all semesters
        for semester in self.semesters.values():
            semester.remove_course(course_code)
        
        self._update_cgpa()
    
    def update_course_grade(self, course_code, grade, gpa):
        """Update grade for an existing course"""
        if course_code in self.courses_taken:
            self.courses_taken[course_code].update_grade(grade, gpa)
            
            # Update in semester as well
            for semester in self.semesters.values():
                for course in semester.courses:
                    if course.course_code == course_code:
                        course.update_grade(grade, gpa)
                        break
                semester._calculate_stats()
            
            self._update_cgpa()
    
    def _update_cgpa(self):
        """Update CGPA for all semesters"""
        if not self.courses_taken:
            return
            
        total_quality_points = 0
        total_credits = 0
        
        # Calculate cumulative stats for each semester
        semester_names = sorted(self.semesters.keys())
        
        for semester_name in semester_names:
            semester = self.semesters[semester_name]
            
            # Add current semester's contribution
            for course in semester.courses:
                total_quality_points += course.get_quality_points()
                total_credits += course.credit
            
            # Update CGPA for this semester
            semester.cgpa = round(total_quality_points / total_credits, 2) if total_credits > 0 else 0.0
    
    def get_current_cgpa(self):
        """Get current overall CGPA"""
        if not self.courses_taken:
            return 0.0
            
        total_quality_points = sum(course.get_quality_points() for course in self.courses_taken.values())
        total_credits = sum(course.credit for course in self.courses_taken.values())
        
        return round(total_quality_points / total_credits, 2) if total_credits > 0 else 0.0
    
    def get_total_credits(self):
        """Get total credits earned"""
        return sum(course.credit for course in self.courses_taken.values())
    
    def get_semester_data(self):
        """Get semester data sorted by semester order"""
        semester_order = {
            'SPRING': 1, 'SUMMER': 2, 'FALL': 3, 'VIRTUAL': 99
        }
        
        def sort_key(sem_name):
            if sem_name == "VIRTUAL SEMESTER":
                return (9999, 99)
            try:
                parts = sem_name.split()
                season = parts[0].upper()
                year = int(parts[1]) if len(parts) > 1 else 0
                return (year, semester_order.get(season, 99))
            except:
                return (9999, 99)
        
        sorted_semesters = sorted(self.semesters.keys(), key=sort_key)
        return [(name, self.semesters[name]) for name in sorted_semesters]


def calculate_grade_points(grade):
    """Convert letter grade to GPA points"""
    grade_points = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'F': 0.0
    }
    return grade_points.get(grade.upper(), 0.0)


def get_letter_grade(gpa):
    """Convert GPA to letter grade"""
    if gpa >= 4.0:
        return 'A+'
    elif gpa >= 3.7:
        return 'A-'
    elif gpa >= 3.3:
        return 'B+'
    elif gpa >= 3.0:
        return 'B'
    elif gpa >= 2.7:
        return 'B-'
    elif gpa >= 2.3:
        return 'C+'
    elif gpa >= 2.0:
        return 'C'
    elif gpa >= 1.7:
        return 'C-'
    elif gpa >= 1.3:
        return 'D+'
    elif gpa >= 1.0:
        return 'D'
    else:
        return 'F'