"""
CGPA Calculator and Projection Utilities
"""

from course_utils import Course, AcademicRecord, calculate_grade_points


class CGPACalculator:
    """Main class for CGPA calculations and projections"""
    
    def __init__(self, academic_record):
        self.academic_record = academic_record
        
    def add_course(self, course_code, semester="VIRTUAL SEMESTER", credit=3, grade="", gpa=0.0):
        """Add a new course to academic record"""
        course = Course(course_code, credit=credit, grade=grade, gpa=gpa)
        self.academic_record.add_course_to_semester(semester, course)
        
    def retake_course(self, course_code, new_grade, new_gpa):
        """Retake an existing course with new grade"""
        self.academic_record.update_course_grade(course_code, new_grade, new_gpa)
        
    def remove_course(self, course_code):
        """Remove a course from academic record"""
        self.academic_record.remove_course(course_code)
        
    def calculate_cgpa_projection(self, target_cgpa=None, total_required_credits=136):
        """Calculate maximum possible CGPA and projection to target"""
        current_credits = self.academic_record.get_total_credits()
        current_quality_points = sum(
            course.get_quality_points() 
            for course in self.academic_record.courses_taken.values()
        )
        
        remaining_credits = max(total_required_credits - current_credits, 0)
        total_credits = current_credits + remaining_credits
        
        # Maximum possible CGPA (assuming 4.0 in all remaining courses)
        max_possible_quality_points = current_quality_points + (remaining_credits * 4.0)
        max_possible_cgpa = max_possible_quality_points / total_credits if total_credits > 0 else 0.0
        
        result = {
            'current_cgpa': self.academic_record.get_current_cgpa(),
            'current_credits': current_credits,
            'remaining_credits': remaining_credits,
            'max_possible_cgpa': round(max_possible_cgpa, 2)
        }
        
        # Calculate requirements for target CGPA
        if target_cgpa is not None:
            target_cgpa = round(target_cgpa, 2)
            required_total_quality_points = target_cgpa * total_credits
            needed_quality_points = required_total_quality_points - current_quality_points
            
            if remaining_credits <= 0:
                result['message'] = "All credits completed. Cannot improve CGPA further."
            elif max_possible_cgpa <= target_cgpa:
                result['required_avg_gpa'] = 4.0
                result['message'] = f"To reach CGPA {target_cgpa}, you must get 4.00 GPA in all remaining courses."
            elif max_possible_cgpa < target_cgpa:
                result['message'] = f"Target CGPA of {target_cgpa} is not achievable. Max possible CGPA is {round(max_possible_cgpa, 2)}."
            else:
                required_avg_gpa = needed_quality_points / remaining_credits
                result['required_avg_gpa'] = round(required_avg_gpa, 2)
                result['message'] = f"To reach CGPA {target_cgpa}, you need to average {round(required_avg_gpa, 2)} GPA over the remaining {remaining_credits} credits."
        
        return result
    
    def calculate_semester_planning(self, target_cgpa=None, num_semesters=0, courses_per_semester=0, total_required_credits=136):
        """Calculate CGPA planning for future semesters"""
        current_credits = self.academic_record.get_total_credits()
        current_quality_points = sum(
            course.get_quality_points() 
            for course in self.academic_record.courses_taken.values()
        )
        
        remaining_credits = total_required_credits - current_credits
        planned_courses = num_semesters * courses_per_semester
        
        # Limit planned courses to available credits
        max_possible_courses = (remaining_credits + 2) // 3  # Assuming 3 credits per course
        planned_courses = min(planned_courses, max_possible_courses)
        planned_credits = min(planned_courses * 3, remaining_credits)
        
        # Calculate max possible CGPA with planned courses
        total_quality_points_max = current_quality_points + (planned_credits * 4.0)
        total_credits = current_credits + planned_credits
        max_possible_cgpa = round(total_quality_points_max / total_credits, 2) if total_credits > 0 else 0.0
        
        result = {
            'planned_courses': planned_courses,
            'planned_credits': planned_credits,
            'max_cgpa': max_possible_cgpa
        }
        
        # Calculate requirements for target CGPA
        if target_cgpa is not None and planned_credits > 0:
            target_cgpa = round(target_cgpa, 2)
            required_total_quality_points = target_cgpa * total_credits
            needed_quality_points = required_total_quality_points - current_quality_points
            
            if max_possible_cgpa < target_cgpa:
                result['required_avg_gpa'] = round(needed_quality_points / planned_credits, 2)
                result['message'] = f"Target CGPA of {target_cgpa} is not achievable with current plan. Required GPA: {result['required_avg_gpa']}."
            elif max_possible_cgpa == target_cgpa:
                result['required_avg_gpa'] = 4.0
                result['message'] = f"To reach CGPA {target_cgpa}, you must get 4.00 GPA in all planned courses."
            else:
                required_avg_gpa = needed_quality_points / planned_credits
                result['required_avg_gpa'] = round(required_avg_gpa, 2)
                result['message'] = f"To reach CGPA {target_cgpa}, you must average {round(required_avg_gpa, 2)} GPA in the next {planned_courses} courses ({planned_credits} credits)."
        elif planned_credits <= 0:
            result['message'] = "No valid credits planned. Cannot calculate required GPA."
        
        return result
    
    def simulate_retakes(self, retake_grades):
        """Simulate the effect of retaking courses with new grades"""
        total_quality_points = 0
        total_credits = 0
        
        for course_code, course in self.academic_record.courses_taken.items():
            if course_code in retake_grades:
                simulated_gpa = retake_grades[course_code]
                total_quality_points += simulated_gpa * course.credit
            else:
                total_quality_points += course.get_quality_points()
            total_credits += course.credit
        
        new_cgpa = round(total_quality_points / total_credits, 2) if total_credits > 0 else 0.0
        return {
            'simulated_cgpa': new_cgpa,
            'improvement': round(new_cgpa - self.academic_record.get_current_cgpa(), 2),
            'message': f"After retaking specified courses, your projected CGPA would be {new_cgpa}."
        }
    
    def get_semester_trends(self):
        """Get GPA and CGPA trends across semesters"""
        semester_data = self.academic_record.get_semester_data()
        trends = {
            'semesters': [],
            'gpas': [],
            'cgpas': [],
            'credits': [],
            'courses_count': []
        }
        
        for semester_name, semester in semester_data:
            if semester.courses:  # Only include semesters with courses
                trends['semesters'].append(semester_name)
                trends['gpas'].append(semester.gpa)
                trends['cgpas'].append(semester.cgpa)
                trends['credits'].append(semester.credit)
                trends['courses_count'].append(len(semester.courses))
        
        return trends
    
    def get_grade_distribution(self):
        """Get distribution of grades"""
        grade_counts = {}
        for course in self.academic_record.courses_taken.values():
            if course.grade:
                grade_counts[course.grade] = grade_counts.get(course.grade, 0) + 1
        
        return grade_counts
    
    def get_performance_stats(self):
        """Get comprehensive performance statistics"""
        courses = list(self.academic_record.courses_taken.values())
        if not courses:
            return {}
        
        gpas = [course.gpa for course in courses if course.gpa > 0]
        
        stats = {
            'total_courses': len(courses),
            'total_credits': sum(course.credit for course in courses),
            'current_cgpa': self.academic_record.get_current_cgpa(),
            'highest_gpa': max(gpas) if gpas else 0,
            'lowest_gpa': min(gpas) if gpas else 0,
            'average_gpa': round(sum(gpas) / len(gpas), 2) if gpas else 0,
            'courses_above_3_5': len([gpa for gpa in gpas if gpa >= 3.5]),
            'courses_below_2_0': len([gpa for gpa in gpas if gpa < 2.0])
        }
        
        return stats


class WhatIfAnalyzer:
    """Analyze what-if scenarios for academic planning"""
    
    def __init__(self, cgpa_calculator):
        self.calculator = cgpa_calculator
    
    def analyze_course_addition(self, course_code, gpa, credit=3):
        """Analyze impact of adding a new course"""
        current_cgpa = self.calculator.academic_record.get_current_cgpa()
        current_credits = self.calculator.academic_record.get_total_credits()
        
        # Calculate new CGPA with added course
        current_quality_points = sum(
            course.get_quality_points() 
            for course in self.calculator.academic_record.courses_taken.values()
        )
        
        new_quality_points = current_quality_points + (gpa * credit)
        new_total_credits = current_credits + credit
        new_cgpa = round(new_quality_points / new_total_credits, 2) if new_total_credits > 0 else 0.0
        
        return {
            'current_cgpa': current_cgpa,
            'projected_cgpa': new_cgpa,
            'cgpa_change': round(new_cgpa - current_cgpa, 3),
            'message': f"Adding {course_code} with GPA {gpa} would change your CGPA from {current_cgpa} to {new_cgpa}"
        }
    
    def analyze_grade_improvement(self, course_code, new_gpa):
        """Analyze impact of improving a course grade"""
        if course_code not in self.calculator.academic_record.courses_taken:
            return {'error': f'Course {course_code} not found in academic record'}
        
        original_course = self.calculator.academic_record.courses_taken[course_code]
        original_gpa = original_course.gpa
        credit = original_course.credit
        
        current_cgpa = self.calculator.academic_record.get_current_cgpa()
        
        # Calculate CGPA with improved grade
        current_quality_points = sum(
            course.get_quality_points() 
            for course in self.calculator.academic_record.courses_taken.values()
        )
        current_credits = self.calculator.academic_record.get_total_credits()
        
        # Remove original contribution and add new
        adjusted_quality_points = current_quality_points - (original_gpa * credit) + (new_gpa * credit)
        new_cgpa = round(adjusted_quality_points / current_credits, 2) if current_credits > 0 else 0.0
        
        return {
            'course_code': course_code,
            'original_gpa': original_gpa,
            'new_gpa': new_gpa,
            'current_cgpa': current_cgpa,
            'projected_cgpa': new_cgpa,
            'cgpa_change': round(new_cgpa - current_cgpa, 3),
            'message': f"Improving {course_code} from {original_gpa} to {new_gpa} would change your CGPA from {current_cgpa} to {new_cgpa}"
        }