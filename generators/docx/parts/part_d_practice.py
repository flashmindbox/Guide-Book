"""
Part D: Practice Questions generator for Guide Book Generator.
Simplified design matching reference document style.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from core.models.base import ChapterData
from styles.theme import Colors, Fonts

from ..helpers import DocxHelpers


class PartDGenerator:
    """Generates Part D: Practice Questions with clean styling."""

    def __init__(self, document: Document, data: ChapterData):
        self.document = document
        self.data = data

    def generate(self):
        """Generate Part D: Practice Questions."""
        DocxHelpers.add_page_break(self.document)
        self._add_part_header()

        # MCQs
        if self.data.mcqs:
            self._add_mcq_section()

        # Assertion-Reason
        if self.data.assertion_reason:
            self._add_ar_section()

        # Source-Based Questions
        if self.data.source_based:
            self._add_source_based_section()

        # Case Study Questions
        if self.data.case_study:
            self._add_case_study_section()

        # Short Answer Questions
        if self.data.short_answer:
            self._add_short_answer_section()

        # Long Answer Questions
        if self.data.long_answer:
            self._add_long_answer_section()

        # HOTS Questions
        if self.data.hots:
            self._add_hots_section()

        # Competency-Based Questions
        if self.data.competency_based:
            self._add_cbq_section()

        # Value-Based Questions
        if self.data.value_based:
            self._add_value_based_section()

    def _add_part_header(self):
        """Add part header with light red background box."""
        table = self.document.add_table(rows=1, cols=1)
        table.alignment = 1
        table.columns[0].width = Inches(6.5)

        cell = table.cell(0, 0)
        DocxHelpers.set_cell_background(cell, Colors.BG_WARNING)  # Light red background
        DocxHelpers.set_cell_padding(cell, 100)

        para = cell.paragraphs[0]
        run = para.add_run("Part D: Practice Questions")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.YEAR_RED)  # Red text

        self.document.add_paragraph()

    def _add_section_title(self, title: str, count: int = None):
        """Add a section title with optional count."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(18)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run(title)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        if count:
            run = para.add_run(f" ({count})")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(12)
            run.font.color.rgb = Colors.hex_to_rgb(Colors.BODY_TEXT)

        # Difficulty legend for MCQ section
        if "MCQ" in title:
            para = self.document.add_paragraph()
            para.paragraph_format.space_after = Pt(6)

            run = para.add_run("[E]")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)
            run = para.add_run(" Easy  ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

            run = para.add_run("[M]")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb('#D97706')  # Orange
            run = para.add_run(" Medium  ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

            run = para.add_run("[H]")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)
            run = para.add_run(" Hard")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

    def _add_mcq_section(self):
        """Add MCQ section."""
        self._add_section_title("1. MCQs (Multiple Choice Questions)", len(self.data.mcqs))

        for idx, q in enumerate(self.data.mcqs, 1):
            self._add_mcq(idx, q)

        # Answer key
        self._add_mcq_answers()

    def _add_mcq(self, num: int, question):
        """Add a single MCQ."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(6)
        para.paragraph_format.space_after = Pt(3)

        # Difficulty tag
        diff = question.difficulty.upper()
        diff_colors = {
            'E': Colors.SUCCESS_GREEN,
            'M': '#D97706',
            'H': Colors.ACCENT_RED
        }
        diff_color = diff_colors.get(diff[0] if diff else 'M', '#D97706')

        run = para.add_run(f"[{diff[0] if diff else 'M'}] ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(diff_color)

        # Question number and text
        run = para.add_run(f"{num}. ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True

        DocxHelpers.add_formatted_text(para, question.question)

        # Options
        if question.options:
            for i, opt in enumerate(question.options):
                option_letter = chr(97 + i)  # a, b, c, d
                para = self.document.add_paragraph()
                para.paragraph_format.left_indent = Inches(0.5)
                para.paragraph_format.space_after = Pt(1)

                run = para.add_run(f"({option_letter}) {opt}")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(11)

    def _add_mcq_answers(self):
        """Add MCQ answer key."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run("✓ Answers (MCQs): ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        # Answer grid
        answers_text = "  ".join([
            f"{idx}({q.answer})" for idx, q in enumerate(self.data.mcqs, 1)
            if q.answer
        ])

        run = para.add_run(answers_text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)

    def _add_ar_section(self):
        """Add Assertion-Reason section."""
        self._add_section_title("2. Assertion-Reason Questions", len(self.data.assertion_reason))

        # AR instructions
        para = self.document.add_paragraph()
        para.paragraph_format.space_after = Pt(6)
        run = para.add_run("Directions: In the following questions, a statement of Assertion (A) "
                          "is followed by a statement of Reason (R). Choose the correct option.")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)
        run.font.italic = True

        # AR options
        options = [
            "(a) Both A and R are true and R is the correct explanation of A",
            "(b) Both A and R are true but R is NOT the correct explanation of A",
            "(c) A is true but R is false",
            "(d) A is false but R is true"
        ]
        for opt in options:
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(1)
            run = para.add_run(opt)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)

        for idx, q in enumerate(self.data.assertion_reason, 1):
            self._add_ar_question(idx, q)

        # AR answers
        self._add_ar_answers()

    def _add_ar_question(self, num: int, question):
        """Add a single AR question."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(9)

        run = para.add_run(f"{num}. Assertion: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True

        # Extract assertion and reason from question text
        q_text = question.question
        if 'Reason:' in q_text:
            parts = q_text.split('Reason:', 1)
            assertion = parts[0].replace('Assertion:', '').strip()
            reason = parts[1].strip()
        else:
            assertion = q_text
            reason = ""

        run = para.add_run(assertion)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)

        if reason:
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            run = para.add_run("Reason: ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True

            run = para.add_run(reason)
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

    def _add_ar_answers(self):
        """Add AR answer key."""
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)

        run = para.add_run("✓ Answers (A-R): ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

        answers_text = "  ".join([
            f"{idx}({q.answer})" for idx, q in enumerate(self.data.assertion_reason, 1)
            if q.answer
        ])

        run = para.add_run(answers_text)
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(10)

    def _add_source_based_section(self):
        """Add source-based questions section."""
        self._add_section_title("3. Source-Based Questions", len(self.data.source_based))

        for idx, item in enumerate(self.data.source_based, 1):
            self._add_source_based(idx, item)

    def _add_source_based(self, num: int, item: dict):
        """Add a single source-based question set."""
        # Source header
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)

        run = para.add_run(f"Source {chr(64+num)}: ")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Source text (quoted)
        source_text = item.get('source', '')
        para = self.document.add_paragraph()
        para.paragraph_format.left_indent = Inches(0.3)
        para.paragraph_format.space_after = Pt(6)

        run = para.add_run(f'"{source_text}"')
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(11)
        run.font.italic = True

        # Questions
        questions = item.get('questions', [])
        for i, q in enumerate(questions, 1):
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(3)

            run = para.add_run(f"({self._roman(i)}) ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True

            run = para.add_run(f"{q.get('question', '')} ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

            marks = q.get('marks', 1)
            run = para.add_run(f"[{marks}]")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

    def _add_case_study_section(self):
        """Add case study questions section."""
        self._add_section_title("4. Case Study Questions (NEW PATTERN)", len(self.data.case_study))

        for idx, item in enumerate(self.data.case_study, 1):
            self._add_case_study(idx, item)

    def _add_case_study(self, num: int, item: dict):
        """Add a single case study."""
        # Title
        title = item.get('title', f'Case Study {num}')
        para = self.document.add_paragraph()
        para.paragraph_format.space_before = Pt(12)

        run = para.add_run(f"Case Study: {title}")
        run.font.name = Fonts.PRIMARY
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = Colors.hex_to_rgb(Colors.HEADING_BLUE)

        # Passage (indented)
        passage = item.get('passage', '')
        para = self.document.add_paragraph()
        para.paragraph_format.left_indent = Inches(0.3)
        para.paragraph_format.space_after = Pt(6)
        DocxHelpers.add_formatted_text(para, passage)

        # Questions
        questions = item.get('questions', [])
        for i, q in enumerate(questions, 1):
            para = self.document.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.space_after = Pt(3)

            run = para.add_run(f"({self._roman(i)}) ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True

            run = para.add_run(f"{q.get('question', '')} ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)

            marks = q.get('marks', 1)
            run = para.add_run(f"[{marks}]")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(10)
            run.font.color.rgb = Colors.hex_to_rgb(Colors.ACCENT_RED)

    def _add_short_answer_section(self):
        """Add short answer questions section."""
        self._add_section_title("5. Short Answer Questions (3 Marks)", len(self.data.short_answer))
        self._add_question_list(self.data.short_answer)

    def _add_long_answer_section(self):
        """Add long answer questions section."""
        self._add_section_title("6. Long Answer Questions (5 Marks)", len(self.data.long_answer))
        self._add_question_list(self.data.long_answer)

    def _add_hots_section(self):
        """Add HOTS questions section."""
        self._add_section_title("7. HOTS (Higher Order Thinking Skills)", len(self.data.hots))
        self._add_question_list(self.data.hots)

    def _add_cbq_section(self):
        """Add Competency-Based Questions section."""
        self._add_section_title("8. Competency-Based Questions (CBQs)", len(self.data.competency_based))
        self._add_question_list(self.data.competency_based)

    def _add_value_based_section(self):
        """Add Value-Based Questions section."""
        self._add_section_title("9. Value-Based Questions", len(self.data.value_based))
        self._add_question_list(self.data.value_based)

    def _add_question_list(self, questions):
        """Add a list of questions with hints."""
        for idx, q in enumerate(questions, 1):
            para = self.document.add_paragraph()
            para.paragraph_format.space_before = Pt(6)

            run = para.add_run(f"{idx}. ")
            run.font.name = Fonts.PRIMARY
            run.font.size = Pt(11)
            run.font.bold = True

            DocxHelpers.add_formatted_text(para, q.question)

            # Hint if present - right-aligned, green, italic
            if q.hint:
                para = self.document.add_paragraph()
                para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                para.paragraph_format.space_after = Pt(3)

                run = para.add_run("💡 Hint: ")
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)
                run.font.bold = True
                run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

                run = para.add_run(q.hint)
                run.font.name = Fonts.PRIMARY
                run.font.size = Pt(10)
                run.font.italic = True
                run.font.color.rgb = Colors.hex_to_rgb(Colors.SUCCESS_GREEN)

    def _roman(self, num: int) -> str:
        """Convert number to roman numeral."""
        roman_map = [(1, 'i'), (4, 'iv'), (5, 'v'), (9, 'ix'), (10, 'x')]
        result = ''
        for value, numeral in reversed(roman_map):
            while num >= value:
                result += numeral
                num -= value
        return result
