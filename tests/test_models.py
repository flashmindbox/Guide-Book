"""
Tests for core data models.
"""

from core.models.base import (
    ChapterData,
    ConceptItem,
    ModelAnswer,
    PYQItem,
    QuestionItem,
)


class TestConceptItem:
    """Tests for ConceptItem model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        concept = ConceptItem()
        assert concept.number == 1
        assert concept.title == ""
        assert concept.content == ""
        assert concept.ncert_line is None
        assert concept.memory_trick is None

    def test_is_empty_true(self):
        """Test is_empty returns True for empty concept."""
        concept = ConceptItem()
        assert concept.is_empty() is True

    def test_is_empty_false_with_title(self):
        """Test is_empty returns False when title is set."""
        concept = ConceptItem(title="Test Title")
        assert concept.is_empty() is False

    def test_is_empty_false_with_content(self):
        """Test is_empty returns False when content is set."""
        concept = ConceptItem(content="Test content here")
        assert concept.is_empty() is False

    def test_word_count_empty(self):
        """Test word_count returns 0 for empty content."""
        concept = ConceptItem()
        assert concept.word_count() == 0

    def test_word_count_with_content(self):
        """Test word_count returns correct count."""
        concept = ConceptItem(content="This is a test sentence")
        assert concept.word_count() == 5


class TestPYQItem:
    """Tests for PYQItem model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        pyq = PYQItem()
        assert pyq.question == ""
        assert pyq.marks == "3M"
        assert pyq.years == ""

    def test_get_year_count_empty(self):
        """Test year count returns 0 for empty years."""
        pyq = PYQItem()
        assert pyq.get_year_count() == 0

    def test_get_year_count_single(self):
        """Test year count for single year."""
        pyq = PYQItem(years="2023")
        assert pyq.get_year_count() == 1

    def test_get_year_count_multiple(self):
        """Test year count for multiple years."""
        pyq = PYQItem(years="2020, 2021, 2023")
        assert pyq.get_year_count() == 3

    def test_is_empty_true(self):
        """Test is_empty returns True for empty question."""
        pyq = PYQItem()
        assert pyq.is_empty() is True

    def test_is_empty_false(self):
        """Test is_empty returns False when question is set."""
        pyq = PYQItem(question="What is nationalism?")
        assert pyq.is_empty() is False


class TestQuestionItem:
    """Tests for QuestionItem model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        q = QuestionItem()
        assert q.question == ""
        assert q.marks == 1
        assert q.difficulty == "M"
        assert q.options is None
        assert q.answer is None

    def test_with_mcq_options(self):
        """Test MCQ with options."""
        q = QuestionItem(
            question="What is the capital of India?",
            options=["Mumbai", "Delhi", "Kolkata", "Chennai"],
            answer="Delhi"
        )
        assert len(q.options) == 4
        assert q.answer == "Delhi"

    def test_is_empty(self):
        """Test is_empty method."""
        assert QuestionItem().is_empty() is True
        assert QuestionItem(question="Test?").is_empty() is False


class TestModelAnswer:
    """Tests for ModelAnswer model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        ans = ModelAnswer()
        assert ans.question == ""
        assert ans.marks == 3
        assert ans.answer == ""
        assert ans.marking_points is None

    def test_is_empty_true(self):
        """Test is_empty returns True for empty answer."""
        ans = ModelAnswer()
        assert ans.is_empty() is True

    def test_is_empty_false_with_question(self):
        """Test is_empty returns False when question is set."""
        ans = ModelAnswer(question="Explain nationalism.")
        assert ans.is_empty() is False

    def test_is_empty_false_with_answer(self):
        """Test is_empty returns False when answer is set."""
        ans = ModelAnswer(answer="Nationalism is...")
        assert ans.is_empty() is False


class TestChapterData:
    """Tests for ChapterData model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        chapter = ChapterData()
        assert chapter.class_num == 10
        assert chapter.subject == "history"
        assert chapter.chapter_number == 1
        assert chapter.chapter_title == ""

    def test_class_num_validation(self):
        """Test class_num must be between 9 and 12."""
        chapter = ChapterData(class_num=9)
        assert chapter.class_num == 9

        chapter = ChapterData(class_num=12)
        assert chapter.class_num == 12

    def test_get_header_text(self):
        """Test get_header_text returns correct format."""
        chapter = ChapterData(class_num=10, subject="history")
        header = chapter.get_header_text()
        assert "CBSE Class 10" in header
        assert "History" in header

    def test_get_full_title(self):
        """Test get_full_title returns correct format."""
        chapter = ChapterData(chapter_number=1, chapter_title="Rise of Nationalism")
        title = chapter.get_full_title()
        assert title == "Chapter 1: Rise of Nationalism"

    def test_is_map_work_applicable_yes(self):
        """Test map work is applicable when enabled."""
        chapter = ChapterData(map_work="Yes", map_work_na=False)
        assert chapter.is_map_work_applicable() is True

    def test_is_map_work_applicable_no(self):
        """Test map work is not applicable when disabled."""
        chapter = ChapterData(map_work="No")
        assert chapter.is_map_work_applicable() is False

    def test_is_map_work_applicable_na(self):
        """Test map work is not applicable when marked N/A."""
        chapter = ChapterData(map_work="Yes", map_work_na=True)
        assert chapter.is_map_work_applicable() is False

    def test_get_enabled_part_ids_default(self):
        """Test default enabled parts."""
        chapter = ChapterData()
        parts = chapter.get_enabled_part_ids()
        assert parts == ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def test_to_autosave_dict(self):
        """Test conversion to autosave dict."""
        chapter = ChapterData(chapter_title="Test Chapter")
        data = chapter.to_autosave_dict()
        assert isinstance(data, dict)
        assert data['chapter_title'] == "Test Chapter"

    def test_from_autosave_dict(self):
        """Test creation from autosave dict."""
        data = {
            'class_num': 10,
            'subject': 'geography',
            'chapter_number': 2,
            'chapter_title': 'Resources',
        }
        chapter = ChapterData.from_autosave_dict(data)
        assert chapter.subject == 'geography'
        assert chapter.chapter_title == 'Resources'

    def test_calculate_completion_empty(self):
        """Test completion calculation for empty chapter."""
        chapter = ChapterData()
        completion = chapter.calculate_completion()
        assert 'cover' in completion
        assert 'overall' in completion
        assert completion['part_a'] == 0

    def test_calculate_completion_with_data(self):
        """Test completion calculation with some data."""
        chapter = ChapterData(
            chapter_title="Test Chapter",
            learning_objectives="Learn about history",
            pyq_items=[PYQItem(question="Test?")]
        )
        completion = chapter.calculate_completion()
        assert completion['cover'] == 100  # Both fields filled
        assert completion['part_a'] == 100  # Has PYQ items
