
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from core.models.base import ChapterData
from core.models.parts import PartManager
from generators.docx.base import DocumentGenerator

def test_generation():
    print("--- Starting Test Generation ---")
    
    # Create dummy data with markdown
    data = ChapterData()
    data.chapter_title = "Test Chapter"
    data.learning_objectives = "**Bold Objective**\n*Italic Objective*"
    data.syllabus_alert_enabled = True
    data.syllabus_alert_text = "Alert: **This should be bold**"
    
    # Create manager
    pm = PartManager()
    
    # Init generator
    generator = DocumentGenerator(data, pm)
    
    # Generate Cover Page (this triggers the code in question)
    print("Generating Cover Page...")
    doc = generator.generate_cover_only()
    
    print("Generation Complete.")

if __name__ == "__main__":
    test_generation()
