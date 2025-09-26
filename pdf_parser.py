"""
PDF Gradesheet Parser
Extracts academic data from university transcripts/gradesheets
"""

import fitz  # PyMuPDF
import re
from typing import Dict, List, Tuple, Optional
from course_utils import AcademicRecord, Course, Semester
from course_data import GRADE_POINTS, GRADES

class GradesheetParser:
    """Parser for university gradesheet PDFs"""
    
    def __init__(self):
        # Common patterns for university gradesheets
        self.semester_patterns = [
            r'SEMESTER:\s*(.+)',
            r'Term:\s*(.+)',
            r'(SPRING|SUMMER|FALL)\s+(\d{4})',
            r'Semester\s*:\s*(.+)'
        ]
        
        self.course_patterns = [
            r'([A-Z]{3}\d{3})\s+',  # Course code pattern like CSE110
            r'([A-Z]{2,4}\d{3})\s+',  # Flexible course pattern
            r'([A-Z]+\d+)\s+'  # General pattern
        ]
        
        self.grade_patterns = [
            r'\b([A-F][+-]?|[WIXS])\b',  # Standard grades
            r'\b(A\+|A|A-|B\+|B|B-|C\+|C|C-|D\+|D|F)\b'
        ]
        
        self.gpa_patterns = [
            r'(\d\.\d{1,2})',  # GPA pattern
            r'(\d\.\d+)'
        ]
        
        # Text to remove/ignore
        self.ignore_text = {
            'BRAC University', 'GRADE SHEET', 'UNOFFICIAL COPY', 'UNDERGRADUATE PROGRAM',
            'Page', 'of', 'Kha', 'Bir Uttam', 'Rafiqul Islam', 'Avenue', 'Merul Badda',
            'Dhaka', 'Credits Earned', 'Quality Points', 'GPA', 'CGPA', 'SEMESTER'
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract all text from PDF"""
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            
            for page in doc:
                # Get text blocks sorted by position
                blocks = page.get_text("blocks")
                blocks = sorted(blocks, key=lambda b: (b[1], b[0]))  # Sort by y, then x
                
                for block in blocks:
                    full_text += block[4] + "\n"
            
            doc.close()
            return full_text
        
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def clean_text(self, text: str) -> List[str]:
        """Clean and split text into lines"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not any(ignore in line for ignore in self.ignore_text):
                cleaned_lines.append(line)
        
        return cleaned_lines
    
    def extract_student_info(self, lines: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """Extract student name and ID"""
        name = None
        student_id = None
        
        for i, line in enumerate(lines):
            if 'Name' in line and i + 1 < len(lines):
                name = lines[i + 1].strip()
            elif 'Student ID' in line and i + 1 < len(lines):
                student_id = lines[i + 1].strip()
            elif 'ID' in line and not student_id and i + 1 < len(lines):
                potential_id = lines[i + 1].strip()
                if potential_id.isdigit() and len(potential_id) >= 8:
                    student_id = potential_id
        
        return name, student_id
    
    def extract_semesters_and_courses(self, lines: List[str]) -> Dict:
        """Extract semester and course information"""
        academic_data = {
            'semesters': {},
            'courses': {}
        }
        
        current_semester = None
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check for semester indicators
            semester_match = None
            for pattern in self.semester_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    if len(match.groups()) == 2:  # SPRING 2024 format
                        semester_match = f"{match.group(1)} {match.group(2)}"
                    else:
                        semester_match = match.group(1).strip()
                    break
            
            if semester_match:
                current_semester = semester_match.upper()
                if current_semester not in academic_data['semesters']:
                    academic_data['semesters'][current_semester] = []
                i += 1
                continue
            
            # Look for course codes
            course_match = None
            for pattern in self.course_patterns:
                match = re.search(pattern, line)
                if match:
                    course_match = match.group(1)
                    break
            
            if course_match and current_semester:
                course_info = self.extract_course_details(lines, i, course_match)
                if course_info:
                    academic_data['semesters'][current_semester].append(course_info)
                    academic_data['courses'][course_match] = course_info
            
            i += 1
        
        return academic_data
    
    def extract_course_details(self, lines: List[str], start_idx: int, course_code: str) -> Optional[Dict]:
        """Extract details for a specific course"""
        # Look in current line and next few lines for grade and GPA
        search_lines = lines[start_idx:min(start_idx + 5, len(lines))]
        
        grade = None
        gpa = None
        credits = 3  # Default
        
        for line in search_lines:
            # Look for grades
            if not grade:
                for grade_pattern in self.grade_patterns:
                    grade_match = re.search(grade_pattern, line)
                    if grade_match:
                        potential_grade = grade_match.group(1)
                        if potential_grade in GRADES:
                            grade = potential_grade
                            break
            
            # Look for GPA
            if not gpa:
                gpa_matches = re.findall(r'\b(\d\.\d{1,2})\b', line)
                for match in gpa_matches:
                    gpa_val = float(match)
                    if 0.0 <= gpa_val <= 4.0:
                        gpa = gpa_val
                        break
            
            # Look for credits
            credit_match = re.search(r'\b([1-6])\s*(?:credit|credits|cr)?\b', line, re.IGNORECASE)
            if credit_match:
                credits = int(credit_match.group(1))
        
        # If we found grade but not GPA, calculate GPA from grade
        if grade and gpa is None:
            gpa = GRADE_POINTS.get(grade, 0.0)
        
        # Skip courses with failing grades or no transfer
        if grade in ['F', 'W', 'I'] or '(NT)' in ' '.join(search_lines):
            return None
        
        if grade and gpa is not None:
            return {
                'course_code': course_code,
                'grade': grade,
                'gpa': gpa,
                'credits': credits
            }
        
        return None
    
    def parse_gradesheet(self, pdf_path: str) -> AcademicRecord:
        """Main method to parse gradesheet and return AcademicRecord"""
        try:
            # Extract text from PDF
            full_text = self.extract_text_from_pdf(pdf_path)
            
            # Clean and process text
            lines = self.clean_text(full_text)
            
            # Extract student information
            name, student_id = self.extract_student_info(lines)
            
            # Create academic record
            academic_record = AcademicRecord(name or "", student_id or "")
            
            # Extract academic data
            academic_data = self.extract_semesters_and_courses(lines)
            
            # Populate academic record
            for semester_name, courses in academic_data['semesters'].items():
                if courses:  # Only add semesters with courses
                    for course_info in courses:
                        course = Course(
                            course_code=course_info['course_code'],
                            course_name=course_info['course_code'],  # Will be updated from course_data
                            credit=course_info['credits'],
                            grade=course_info['grade'],
                            gpa=course_info['gpa']
                        )
                        academic_record.add_course_to_semester(semester_name, course)
            
            return academic_record
        
        except Exception as e:
            raise Exception(f"Error parsing gradesheet: {str(e)}")
    
    def validate_parsed_data(self, academic_record: AcademicRecord) -> Dict:
        """Validate the parsed data and return statistics"""
        stats = {
            'total_courses': len(academic_record.courses_taken),
            'total_credits': academic_record.get_total_credits(),
            'semesters': len(academic_record.semesters),
            'cgpa': academic_record.get_current_cgpa(),
            'issues': []
        }
        
        # Check for potential issues
        if stats['total_courses'] == 0:
            stats['issues'].append("No courses found in the gradesheet")
        
        if stats['total_credits'] == 0:
            stats['issues'].append("No credits found")
        
        if stats['cgpa'] == 0:
            stats['issues'].append("CGPA is 0.0 - check if grades were parsed correctly")
        
        # Check for courses with 0 GPA (might be parsing errors)
        zero_gpa_courses = [code for code, course in academic_record.courses_taken.items() if course.gpa == 0]
        if zero_gpa_courses:
            stats['issues'].append(f"Courses with 0.0 GPA: {', '.join(zero_gpa_courses)}")
        
        return stats


class SmartGradesheetParser(GradesheetParser):
    """Enhanced parser with better pattern recognition"""
    
    def __init__(self):
        super().__init__()
        
        # Enhanced patterns for different university formats
        self.enhanced_course_patterns = [
            r'([A-Z]{3}\d{3})\s+([A-F][+-]?|\w+)\s+(\d\.\d{2})',  # Course + Grade + GPA
            r'([A-Z]{2,4}\d{3})\s+.*?([A-F][+-]?)\s+(\d\.\d{2})',  # Flexible with grade and GPA
            r'([A-Z]+\d+)(?:\s+.*?)?\s+([A-F][+-]?|[WIXS])\s+(\d\.\d{1,2})'  # General pattern
        ]
    
    def smart_course_extraction(self, text: str) -> List[Dict]:
        """Use enhanced patterns for better course extraction"""
        courses = []
        
        for pattern in self.enhanced_course_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                try:
                    course_code = match.group(1)
                    grade = match.group(2) if len(match.groups()) > 1 else 'A'
                    gpa = float(match.group(3)) if len(match.groups()) > 2 else 4.0
                    
                    if grade in GRADES and 0.0 <= gpa <= 4.0:
                        courses.append({
                            'course_code': course_code,
                            'grade': grade,
                            'gpa': gpa,
                            'credits': 4 if course_code.endswith('400') else 3
                        })
                except (ValueError, IndexError):
                    continue
        
        return courses
    
    def parse_gradesheet_smart(self, pdf_path: str) -> AcademicRecord:
        """Smart parsing with fallback methods"""
        try:
            # First try the regular parsing
            return self.parse_gradesheet(pdf_path)
        except Exception as e:
            # Fallback to smart extraction
            try:
                full_text = self.extract_text_from_pdf(pdf_path)
                lines = self.clean_text(full_text)
                
                name, student_id = self.extract_student_info(lines)
                academic_record = AcademicRecord(name or "", student_id or "")
                
                # Use smart course extraction
                courses = self.smart_course_extraction(full_text)
                
                for course_info in courses:
                    course = Course(
                        course_code=course_info['course_code'],
                        course_name=course_info['course_code'],
                        credit=course_info['credits'],
                        grade=course_info['grade'],
                        gpa=course_info['gpa']
                    )
                    academic_record.add_course_to_semester("PARSED SEMESTER", course)
                
                return academic_record
            except Exception as fallback_error:
                raise Exception(f"Both parsing methods failed. Original: {str(e)}, Fallback: {str(fallback_error)}")


def create_parser() -> SmartGradesheetParser:
    """Factory function to create a parser instance"""
    return SmartGradesheetParser()