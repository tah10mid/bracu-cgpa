"""
BRACU Gradesheet Parser
Specialized parser for BRAC University gradesheet format
Based on the official BRACU Gradesheet Analyzer implementation
"""

import fitz  # PyMuPDF
import re
import logging
import tempfile
import os
from typing import Dict, List, Tuple, Optional
from course_utils import Course, Semester, AcademicRecord

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BRACUParser:
    """
    BRACU-specific gradesheet parser that follows the official transcript format
    """
    
    def __init__(self):
        # BRACU-specific filtering sets
        self.to_remove = {
            'BRAC University', '', 'Kha 224, Bir Uttam Rafiqul Islam Avenue ', 
            'Merul Badda, Dhaka 1212.', '', 'Page 1 of 2', '', ' ', '', 
            'GRADE SHEET', '', 'UNOFFICIAL COPY', '', 'UNDERGRADUATE PROGRAM ', '',
        }
        
        self.valid_grades = [
            "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "W", "I"
        ]
        
        # Course code pattern for validation
        self.course_pattern = re.compile(r'^[A-Z]{3}\d{3}$')
        
        # Course prerequisites from BRACU data
        self.course_codes = {
            "STA201", "HUM103", "BNG103", "EMB101", "MAT110", "MAT120", "MAT215", "MAT216", 
            "PHY111", "PHY112", "ENG101", "ENG102", "ENG103", "CSE110", "CSE111", "CSE220", 
            "CSE221", "CSE230", "CSE250", "CSE251", "CSE260", "CSE320", "CSE321", "CSE330", 
            "CSE331", "CSE340", "CSE341", "CSE350", "CSE360", "CSE370", "CSE420", "CSE421", 
            "CSE422", "CSE423", "CSE460", "CSE461", "CSE470", "CSE471", "CSE400", "CHE101", 
            "BIO101", "ENV103", "PSY101", "SOC101", "ANT101", "POL101", "BUS201", "ECO101", 
            "ECO102", "HUM101", "HUM102", "HST102", "HST104", "HUM207", "ENG113", "ENG114", 
            "ENG115", "ENG333", "CST301", "CST302", "CST303", "CST304", "CST305", "CST306", 
            "CST307", "CST308", "CST309", "CST310"
        }
    
    def extract_gradesheet(self, pdf_path: str) -> Tuple[Optional[str], Optional[str], Dict, Dict]:
        """
        Extract gradesheet data using BRACU-specific parsing logic
        Returns: (name, student_id, courses_done, semesters_done)
        """
        courses_done = {}
        semesters_done = {}
        name, student_id = None, None
        
        try:
            # Open PDF document
            doc = fitz.open(pdf_path)
            full_text = ""
            
            # Extract text from all pages
            for page in doc:
                blocks = page.get_text("blocks")
                # Sort blocks by position (top to bottom, left to right)
                blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
                for block in blocks:
                    full_text += block[4] + "\n"
            
            doc.close()
            
            # Split into lines and clean
            lines = full_text.splitlines()
            
            # Remove unwanted lines
            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if line and line not in self.to_remove:
                    cleaned_lines.append(line)
            
            # Parse the content using BRACU format
            name, student_id, courses_done, semesters_done = self._parse_bracu_format(cleaned_lines)
            
            logger.info(f"Successfully parsed BRACU gradesheet for {name} ({student_id})")
            logger.info(f"Found {len(courses_done)} courses across {len(semesters_done)} semesters")
            
            return name, student_id, courses_done, semesters_done
            
        except Exception as e:
            logger.error(f"Error parsing BRACU gradesheet: {str(e)}")
            raise Exception(f"Failed to parse gradesheet: {str(e)}")
    
    def _parse_bracu_format(self, lines: List[str]) -> Tuple[Optional[str], Optional[str], Dict, Dict]:
        """Parse lines following exact BRACU gradesheet format"""
        courses_done = {}
        semesters_done = {}
        name, student_id = None, None
        
        i = 0
        while i < len(lines):
            try:
                line = lines[i]
                
                # Extract student name
                if line == "Name" and name is None:
                    i += 1
                    if i < len(lines) and lines[i].strip():
                        i += 1
                        if i < len(lines):
                            name = lines[i]
                            logger.info(f"Found student name: {name}")
                
                # Extract student ID
                elif line == "Student ID" and student_id is None:
                    i += 1
                    if i < len(lines) and lines[i].strip():
                        i += 1
                        if i < len(lines):
                            student_id = lines[i]
                            logger.info(f"Found student ID: {student_id}")
                
                # Parse semester data
                elif line == "SEMESTER:":
                    i += 1
                    if i < len(lines):
                        current_semester = lines[i]
                        logger.info(f"Processing semester: {current_semester}")
                        
                        # Create semester object
                        semester_obj = Semester(current_semester)
                        semesters_done[current_semester] = semester_obj
                        
                        # Parse courses in this semester
                        i = self._parse_semester_courses(lines, i, current_semester, courses_done, semester_obj)
                
                i += 1
                
            except Exception as e:
                logger.warning(f"Error parsing line {i}: {line} - {str(e)}")
                i += 1
        
        return name, student_id, courses_done, semesters_done
    
    def _parse_semester_courses(self, lines: List[str], start_idx: int, semester: str, 
                               courses_done: Dict, semester_obj: Semester) -> int:
        """Parse courses within a semester following BRACU format"""
        i = start_idx + 1
        
        logger.debug(f"Starting course parsing for {semester} at line {i}")
        
        while i < len(lines) and lines[i] != "CGPA":
            try:
                line = lines[i]
                logger.debug(f"Examining line {i}: '{line}'")
                
                # Check if this is a valid BRACU course code
                if line in self.course_codes or self.course_pattern.match(line):
                    course_code = line
                    logger.debug(f"Found potential course: {course_code}")
                    
                    # Look ahead for grade information
                    j = i + 1
                    is_nt = False  # No Transfer
                    is_repeat = False
                    
                    logger.debug(f"Looking for grade starting at line {j}")
                    
                    # Check for special markers and find grade
                    while j < len(lines) and lines[j] not in self.valid_grades:
                        logger.debug(f"Checking line {j}: '{lines[j]}'")
                        if "(NT)" in lines[j]:
                            is_nt = True
                            logger.debug("Found NT marker")
                            break
                        elif "(RP)" in lines[j] or "(RT)" in lines[j]:
                            # Handle repeat courses
                            hold = lines[j].split()
                            if hold:
                                lines[j] = hold[0]
                            is_repeat = True
                            logger.debug("Found repeat marker")
                            break
                        j += 1
                        
                        # Safety check to avoid infinite loop
                        if j - i > 10:
                            logger.debug("Breaking search - too many lines ahead")
                            break
                    
                    # Skip NT (No Transfer) courses
                    if is_nt:
                        logger.debug(f"Skipping NT course: {course_code}")
                        i = j + 1
                        continue
                    
                    # Check if we found a valid grade
                    if j < len(lines) and lines[j] in self.valid_grades:
                        grade = lines[j]
                        logger.debug(f"Found grade: {grade}")
                        
                        # Skip failed/incomplete courses (as per BRACU analyzer)
                        if grade in {"F", "I", "W"}:
                            logger.debug(f"Skipping failed/incomplete course: {course_code} ({grade})")
                            i = j + 1
                            continue
                        
                        try:
                            # Look for credit value (should be before the grade)
                            credit = 3.0  # Default credit
                            if j > 0 and self._is_number(lines[j - 1]):
                                credit = float(lines[j - 1])
                                logger.debug(f"Found credit from previous line: {credit}")
                            elif course_code == "CSE400":
                                credit = 4.0  # CSE400 is typically 4 credits
                                logger.debug("Using CSE400 special credit: 4.0")
                            
                            # Look for GPA value (should be after the grade)
                            gpa = 0.0
                            if j + 1 < len(lines) and self._is_gpa_value(lines[j + 1]):
                                gpa = float(lines[j + 1])
                                logger.debug(f"Found GPA from next line: {gpa}")
                            else:
                                # Calculate GPA from grade
                                gpa = self._grade_to_gpa(grade)
                                logger.debug(f"Calculated GPA from grade: {gpa}")
                            
                            # Create course object
                            course = Course(
                                course_code=course_code,
                                course_name=course_code,  # Use code as name
                                credit=credit,
                                grade=grade,
                                gpa=gpa
                            )
                            
                            courses_done[course_code] = course
                            semester_obj.add_course(course)
                            
                            logger.info(f"✅ Successfully added course: {course_code} - {grade} ({gpa}) - {credit} credits")
                            
                            i = j + 2  # Move past the GPA value
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Error parsing course {course_code}: {str(e)}")
                            i += 1
                    else:
                        logger.debug(f"No valid grade found for {course_code} at line {j}")
                        i += 1
                else:
                    i += 1
                    
            except Exception as e:
                logger.warning(f"Error in semester course parsing at line {i}: {str(e)}")
                i += 1
        
        logger.debug(f"Finished parsing {semester} with {len(semester_obj.courses)} courses")
        
        # Parse semester GPA and CGPA
        if i < len(lines) and lines[i] == "CGPA":
            try:
                # Look for semester GPA (usually appears before CGPA)
                gpa_idx = i - 1
                while gpa_idx > start_idx and not self._is_gpa_value(lines[gpa_idx]):
                    gpa_idx -= 1
                
                if gpa_idx > start_idx and self._is_gpa_value(lines[gpa_idx]):
                    semester_gpa = float(lines[gpa_idx])
                    semester_obj.gpa = semester_gpa
                    logger.debug(f"Set semester GPA: {semester_gpa}")
                
                # Get CGPA
                if i + 1 < len(lines) and self._is_gpa_value(lines[i + 1]):
                    cgpa = float(lines[i + 1])
                    logger.debug(f"Found CGPA: {cgpa}")
                    
            except (ValueError, IndexError) as e:
                logger.warning(f"Error parsing semester GPA/CGPA: {str(e)}")
        
        return i
    
    def _is_gpa_value(self, text: str) -> bool:
        """Check if text looks like a GPA value (0.00 to 4.00)"""
        try:
            val = float(text)
            return 0.0 <= val <= 4.0 and '.' in text
        except:
            return False
    
    def _is_number(self, text: str) -> bool:
        """Check if text is a number"""
        try:
            float(text)
            return True
        except:
            return False
    
    def _grade_to_gpa(self, grade: str) -> float:
        """Convert letter grade to GPA"""
        grade_mapping = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0,
            'W': 0.0, 'I': 0.0
        }
        return grade_mapping.get(grade, 0.0)
    
    def parse_gradesheet_smart(self, pdf_path: str) -> Optional[AcademicRecord]:
        """
        Smart parsing that creates an AcademicRecord object
        """
        try:
            name, student_id, courses_done, semesters_done = self.extract_gradesheet(pdf_path)
            
            if not name or not student_id:
                raise Exception("Could not extract student name or ID from gradesheet")
            
            # Create academic record
            record = AcademicRecord(student_id, name)
            
            # Add semesters and courses
            for semester_name, semester_obj in semesters_done.items():
                if semester_name and semester_obj.courses:  # Skip empty semesters
                    record.add_semester(semester_obj)
            
            # Validate the record
            if not record.semesters:
                raise Exception("No valid semesters found in gradesheet")
            
            logger.info(f"Successfully created academic record with {len(record.get_completed_courses())} courses")
            return record
            
        except Exception as e:
            logger.error(f"BRACU parsing failed: {str(e)}")
            return None


def create_parser() -> BRACUParser:
    """Factory function to create a BRACU gradesheet parser"""
    return BRACUParser()