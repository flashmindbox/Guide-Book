"""
Tests for ProgressTracker.
"""

from core.models.base import ChapterData, ConceptItem, ModelAnswer, PYQItem, QuestionItem
from core.models.parts import PartManager
from core.progress import ProgressTracker


class TestProgressTracker:
    """Tests for ProgressTracker."""

    def create_tracker(self, chapter_data=None):
        """Helper to create a ProgressTracker."""
        if chapter_data is None:
            chapter_data = ChapterData()
        return ProgressTracker(chapter_data, PartManager())

    def test_initialization(self):
        """Test ProgressTracker initialization."""
        chapter = ChapterData()
        manager = PartManager()
        tracker = ProgressTracker(chapter, manager)

        assert tracker.data == chapter
        assert tracker.part_manager == manager

    def test_status_indicators(self):
        """Test status indicator constants."""
        tracker = self.create_tracker()

        assert tracker.STATUS_COMPLETE == '✅'
        assert tracker.STATUS_PARTIAL == '🔶'
        assert tracker.STATUS_EMPTY == '⬜'

    def test_get_status_indicator_complete(self):
        """Test status indicator for complete (>=80%)."""
        tracker = self.create_tracker()

        assert tracker.get_status_indicator(100) == '✅'
        assert tracker.get_status_indicator(80) == '✅'

    def test_get_status_indicator_partial(self):
        """Test status indicator for partial (1-79%)."""
        tracker = self.create_tracker()

        assert tracker.get_status_indicator(50) == '🔶'
        assert tracker.get_status_indicator(1) == '🔶'

    def test_get_status_indicator_empty(self):
        """Test status indicator for empty (<1%)."""
        tracker = self.create_tracker()

        assert tracker.get_status_indicator(0) == '⬜'
        assert tracker.get_status_indicator(0.5) == '⬜'

    def test_calculate_cover_progress_empty(self):
        """Test cover progress with empty data."""
        tracker = self.create_tracker()

        progress = tracker.calculate_cover_progress()
        # Empty chapter has default values for weightage, importance, pyq_frequency
        assert progress == 30  # 10 + 10 + 10 for default values

    def test_calculate_cover_progress_complete(self):
        """Test cover progress with complete data."""
        chapter = ChapterData(
            chapter_title="Test Chapter",
            learning_objectives="Learn about...",
            weightage="4-5 Marks",
            importance="High",
            pyq_frequency="Every Year"
        )
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_cover_progress()
        assert progress == 100

    def test_calculate_part_a_progress_empty(self):
        """Test Part A progress with no PYQ items."""
        tracker = self.create_tracker()

        progress = tracker.calculate_part_a_progress()
        assert progress == 10  # Only year range is set by default

    def test_calculate_part_a_progress_with_items(self):
        """Test Part A progress with PYQ items."""
        chapter = ChapterData(
            pyq_items=[
                PYQItem(question="Q1?"),
                PYQItem(question="Q2?"),
                PYQItem(question="Q3?"),
            ],
            pyq_prediction="Expected questions...",
            pyq_syllabus_note="Note about syllabus"
        )
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_a_progress()
        # 3 items * 10 = 30, prediction = 20, year range = 10, note = 10 = 70
        assert progress == 70

    def test_calculate_part_b_progress_empty(self):
        """Test Part B progress with no concepts."""
        chapter = ChapterData(concepts=[])
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_b_progress()
        assert progress == 0

    def test_calculate_part_b_progress_with_concepts(self):
        """Test Part B progress with concepts."""
        chapter = ChapterData(
            concepts=[
                ConceptItem(title="Concept 1", content="Content 1"),
                ConceptItem(title="Concept 2", content="Content 2", memory_trick="Trick"),
            ]
        )
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_b_progress()
        # 2 concepts * 14 = 28, 1 memory trick * 2 = 2 = 30
        assert progress == 30

    def test_calculate_part_c_progress_empty(self):
        """Test Part C progress with no model answers."""
        tracker = self.create_tracker()

        progress = tracker.calculate_part_c_progress()
        assert progress == 0

    def test_calculate_part_c_progress_with_answers(self):
        """Test Part C progress with model answers."""
        chapter = ChapterData(
            model_answers=[
                ModelAnswer(question="Q1", answer="A1"),
                ModelAnswer(question="Q2", answer="A2"),
            ],
            examiner_tips="Tips here"
        )
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_c_progress()
        # 2 answers * 20 = 40, tips = 10 = 50
        assert progress == 50

    def test_calculate_part_d_progress_empty(self):
        """Test Part D progress with no questions."""
        tracker = self.create_tracker()

        progress = tracker.calculate_part_d_progress()
        assert progress == 0

    def test_calculate_part_d_progress_with_questions(self):
        """Test Part D progress with various questions."""
        chapter = ChapterData(
            mcqs=[QuestionItem(question="MCQ1?")] * 10,  # 10%
            short_answer=[QuestionItem(question="SA?")] * 5,  # 10%
        )
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_d_progress()
        # 10 MCQs = 10, 5 SA * 2 = 10 = 20
        assert progress == 20

    def test_calculate_part_e_progress_na(self):
        """Test Part E progress when marked N/A."""
        chapter = ChapterData(map_work_na=True)
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_e_progress()
        assert progress == 100

    def test_calculate_part_e_progress_no_map_work(self):
        """Test Part E progress when map work is No."""
        chapter = ChapterData(map_work="No")
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_e_progress()
        assert progress == 100

    def test_calculate_part_e_progress_with_items(self):
        """Test Part E progress with map items."""
        chapter = ChapterData(
            map_work="Yes",
            map_items=["Location 1", "Location 2"],
            map_tips="Tips here"
        )
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_e_progress()
        # 2 items * 10 = 20, tips = 10 = 30
        assert progress == 30

    def test_calculate_part_f_progress_empty(self):
        """Test Part F progress with no revision content."""
        tracker = self.create_tracker()

        progress = tracker.calculate_part_f_progress()
        assert progress == 0

    def test_calculate_part_f_progress_with_content(self):
        """Test Part F progress with revision content."""
        chapter = ChapterData(
            revision_key_points=["Point 1", "Point 2"],  # 8%
            revision_key_terms=[{"term": "T1", "definition": "D1"}],  # 5%
        )
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_f_progress()
        # 2 points * 4 = 8, 1 term * 5 = 5 = 13
        assert progress == 13

    def test_calculate_part_g_progress_empty(self):
        """Test Part G progress with no strategy content."""
        tracker = self.create_tracker()

        progress = tracker.calculate_part_g_progress()
        assert progress == 0

    def test_calculate_part_g_progress_with_content(self):
        """Test Part G progress with strategy content."""
        chapter = ChapterData(
            time_allocation=[{"type": "MCQ", "marks": "10", "time": "15min"}],  # 25%
            examiner_pro_tips=["Tip 1", "Tip 2"],  # 10%
        )
        tracker = self.create_tracker(chapter)

        progress = tracker.calculate_part_g_progress()
        # time allocation = 25, 2 tips * 5 = 10 = 35
        assert progress == 35

    def test_get_progress_for_part(self):
        """Test getting progress for specific parts."""
        tracker = self.create_tracker()

        progress_a = tracker.get_progress_for_part('A')
        progress_b = tracker.get_progress_for_part('B')
        progress_invalid = tracker.get_progress_for_part('Z')

        assert isinstance(progress_a, (int, float))
        assert isinstance(progress_b, (int, float))
        assert progress_invalid == 0

    def test_get_all_progress(self):
        """Test getting all progress data."""
        tracker = self.create_tracker()

        all_progress = tracker.get_all_progress()

        assert 'cover' in all_progress
        assert 'part_a' in all_progress
        assert 'part_g' in all_progress

        # Check structure
        for key, data in all_progress.items():
            assert 'name' in data
            assert 'percentage' in data
            assert 'status' in data

    def test_get_overall_progress(self):
        """Test overall progress calculation."""
        tracker = self.create_tracker()

        overall = tracker.get_overall_progress()

        assert isinstance(overall, float)
        assert 0 <= overall <= 100

    def test_get_progress_summary(self):
        """Test progress summary."""
        tracker = self.create_tracker()

        summary = tracker.get_progress_summary()

        assert 'overall_percentage' in summary
        assert 'overall_status' in summary
        assert 'sections' in summary
        assert 'counts' in summary

        counts = summary['counts']
        assert 'total' in counts
        assert 'complete' in counts
        assert 'partial' in counts
        assert 'empty' in counts

    def test_get_sidebar_display(self):
        """Test sidebar display data."""
        tracker = self.create_tracker()

        display = tracker.get_sidebar_display()

        assert isinstance(display, list)
        assert len(display) > 0

        # Check structure of each item
        for name, status, percentage in display:
            assert isinstance(name, str)
            assert status in ['✅', '🔶', '⬜']
            assert isinstance(percentage, (int, float))
