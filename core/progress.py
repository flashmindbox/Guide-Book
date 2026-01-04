"""
Progress tracking for Guide Book Generator.
Calculates completion percentages for each section and overall.
"""

from typing import Dict, List, Tuple

from .models.base import ChapterData
from .models.parts import PartManager


class ProgressTracker:
    """
    Tracks completion progress for a chapter.
    Calculates per-section and overall completion percentages.
    """

    # Progress status indicators
    STATUS_COMPLETE = '✅'
    STATUS_PARTIAL = '🔶'
    STATUS_EMPTY = '⬜'

    # Thresholds for status
    THRESHOLD_COMPLETE = 80  # >= 80% is complete
    THRESHOLD_PARTIAL = 1    # >= 1% is partial

    def __init__(self, chapter_data: ChapterData, part_manager: PartManager):
        self.data = chapter_data
        self.part_manager = part_manager

    def calculate_cover_progress(self) -> float:
        """Calculate cover page completion percentage."""
        fields = [
            (self.data.chapter_title, 30),      # Title is important
            (self.data.learning_objectives, 40), # Objectives are important
            (self.data.weightage != "", 10),
            (self.data.importance != "", 10),
            (self.data.pyq_frequency != "", 10),
        ]

        total_weight = sum(weight for _, weight in fields)
        earned_weight = sum(weight for value, weight in fields if value)

        return (earned_weight / total_weight) * 100 if total_weight > 0 else 0

    def calculate_part_a_progress(self) -> float:
        """Calculate Part A (PYQ Analysis) completion percentage."""
        score = 0

        # PYQ items (60%)
        if self.data.pyq_items:
            non_empty = [p for p in self.data.pyq_items if not p.is_empty()]
            score += min(60, len(non_empty) * 10)  # 6 items = 60%

        # Prediction (20%)
        if self.data.pyq_prediction:
            score += 20

        # Year range set (10%)
        if self.data.pyq_year_range:
            score += 10

        # Syllabus note (10%)
        if self.data.pyq_syllabus_note:
            score += 10

        return min(100, score)

    def calculate_part_b_progress(self) -> float:
        """Calculate Part B (Key Concepts) completion percentage."""
        score = 0

        # Concepts (70%)
        non_empty_concepts = [c for c in self.data.concepts if not c.is_empty()]
        if non_empty_concepts:
            # 5+ concepts = full credit
            concept_score = min(70, len(non_empty_concepts) * 14)
            score += concept_score

        # Memory tricks (10%)
        concepts_with_tricks = [c for c in non_empty_concepts if c.memory_trick]
        if concepts_with_tricks:
            score += min(10, len(concepts_with_tricks) * 2)

        # Comparison tables (10%)
        if self.data.comparison_tables:
            score += 10

        # Common mistakes (5%)
        if self.data.common_mistakes:
            score += 5

        # Important dates (5%)
        if self.data.important_dates:
            score += 5

        return min(100, score)

    def calculate_part_c_progress(self) -> float:
        """Calculate Part C (Model Answers) completion percentage."""
        if not self.data.model_answers:
            return 0

        non_empty = [a for a in self.data.model_answers if not a.is_empty()]
        if not non_empty:
            return 0

        # 5 model answers = 100%
        base_score = min(100, len(non_empty) * 20)

        # Bonus for examiner tips
        if self.data.examiner_tips:
            base_score = min(100, base_score + 10)

        return base_score

    def calculate_part_d_progress(self) -> float:
        """Calculate Part D (Practice Questions) completion percentage."""
        score = 0

        # MCQs (20%)
        if self.data.mcqs:
            score += min(20, len(self.data.mcqs) * 1)  # 20 MCQs = 20%

        # Assertion-Reason (10%)
        if self.data.assertion_reason:
            score += min(10, len(self.data.assertion_reason) * 1.25)  # 8 AR = 10%

        # Short Answer (20%)
        if self.data.short_answer:
            score += min(20, len(self.data.short_answer) * 2)  # 10 SA = 20%

        # Long Answer (20%)
        if self.data.long_answer:
            score += min(20, len(self.data.long_answer) * 3.33)  # 6 LA = 20%

        # HOTS (10%)
        if self.data.hots:
            score += min(10, len(self.data.hots) * 2.5)  # 4 HOTS = 10%

        # Source/Case Based (10%)
        source_case = len(self.data.source_based) + len(self.data.case_study)
        if source_case:
            score += min(10, source_case * 5)  # 2 = 10%

        # CBQ/Value-based (10%)
        cbq_value = len(self.data.competency_based) + len(self.data.value_based)
        if cbq_value:
            score += min(10, cbq_value * 2.5)

        return min(100, score)

    def calculate_part_e_progress(self) -> float:
        """Calculate Part E (Map Work) completion percentage."""
        # If marked as N/A, it's complete
        if self.data.map_work_na:
            return 100

        # If no map work for this chapter
        if self.data.map_work == "No":
            return 100

        score = 0

        # Map items (60%)
        if self.data.map_items:
            score += min(60, len(self.data.map_items) * 10)

        # Map image (30%)
        if self.data.map_image_path:
            score += 30

        # Map tips (10%)
        if self.data.map_tips:
            score += 10

        return min(100, score)

    def calculate_part_f_progress(self) -> float:
        """Calculate Part F (Quick Revision) completion percentage."""
        score = 0

        # Key points (40%)
        if self.data.revision_key_points:
            score += min(40, len(self.data.revision_key_points) * 4)

        # Key terms (30%)
        if self.data.revision_key_terms:
            score += min(30, len(self.data.revision_key_terms) * 5)

        # Timeline (15%)
        if self.data.revision_timeline:
            score += min(15, len(self.data.revision_timeline) * 1.5)

        # Memory tricks (15%)
        if self.data.revision_memory_tricks:
            score += min(15, len(self.data.revision_memory_tricks) * 3)

        return min(100, score)

    def calculate_part_g_progress(self) -> float:
        """Calculate Part G (Exam Strategy) completion percentage."""
        score = 0

        # Time allocation table (25%)
        if self.data.time_allocation:
            score += 25

        # Common mistakes (25%)
        if self.data.common_mistakes_exam:
            score += min(25, len(self.data.common_mistakes_exam) * 3)

        # Pro tips (25%)
        if self.data.examiner_pro_tips:
            score += min(25, len(self.data.examiner_pro_tips) * 5)

        # Self-assessment checklist (25%)
        if self.data.self_assessment_checklist:
            score += min(25, len(self.data.self_assessment_checklist) * 6.25)

        return min(100, score)

    def get_progress_for_part(self, part_id: str) -> float:
        """Get progress for a specific part."""
        calculators = {
            'A': self.calculate_part_a_progress,
            'B': self.calculate_part_b_progress,
            'C': self.calculate_part_c_progress,
            'D': self.calculate_part_d_progress,
            'E': self.calculate_part_e_progress,
            'F': self.calculate_part_f_progress,
            'G': self.calculate_part_g_progress,
        }

        calculator = calculators.get(part_id.upper())
        if calculator:
            return calculator()
        return 0

    def get_status_indicator(self, percentage: float) -> str:
        """Get status indicator emoji based on percentage."""
        if percentage >= self.THRESHOLD_COMPLETE:
            return self.STATUS_COMPLETE
        elif percentage >= self.THRESHOLD_PARTIAL:
            return self.STATUS_PARTIAL
        else:
            return self.STATUS_EMPTY

    def get_all_progress(self) -> Dict[str, Dict]:
        """
        Get progress for all sections.
        Returns dict with section names as keys and progress info as values.
        """
        progress = {}

        # Cover page
        cover_pct = self.calculate_cover_progress()
        progress['cover'] = {
            'name': 'Cover Page',
            'percentage': cover_pct,
            'status': self.get_status_indicator(cover_pct),
        }

        # Parts
        enabled_parts = self.part_manager.get_enabled_parts()
        for part in enabled_parts:
            pct = self.get_progress_for_part(part.id)
            progress[f'part_{part.id.lower()}'] = {
                'name': f'Part {part.id}: {part.name}',
                'short_name': f'Part {part.id}',
                'percentage': pct,
                'status': self.get_status_indicator(pct),
            }

        return progress

    def get_overall_progress(self) -> float:
        """Calculate overall completion percentage."""
        all_progress = self.get_all_progress()

        if not all_progress:
            return 0

        total = sum(p['percentage'] for p in all_progress.values())
        return total / len(all_progress)

    def get_progress_summary(self) -> Dict:
        """Get a summary of progress including counts."""
        all_progress = self.get_all_progress()
        overall = self.get_overall_progress()

        complete_count = sum(1 for p in all_progress.values() if p['percentage'] >= self.THRESHOLD_COMPLETE)
        partial_count = sum(1 for p in all_progress.values()
                          if self.THRESHOLD_PARTIAL <= p['percentage'] < self.THRESHOLD_COMPLETE)
        empty_count = sum(1 for p in all_progress.values() if p['percentage'] < self.THRESHOLD_PARTIAL)

        return {
            'overall_percentage': overall,
            'overall_status': self.get_status_indicator(overall),
            'sections': all_progress,
            'counts': {
                'total': len(all_progress),
                'complete': complete_count,
                'partial': partial_count,
                'empty': empty_count,
            }
        }

    def get_sidebar_display(self) -> List[Tuple[str, str, float]]:
        """
        Get progress data formatted for sidebar display.
        Returns list of (name, status_emoji, percentage) tuples.
        """
        all_progress = self.get_all_progress()
        display = []

        # Cover page first
        if 'cover' in all_progress:
            p = all_progress['cover']
            display.append((p['name'], p['status'], p['percentage']))

        # Then parts in order
        enabled_parts = self.part_manager.get_enabled_parts()
        for part in enabled_parts:
            key = f'part_{part.id.lower()}'
            if key in all_progress:
                p = all_progress[key]
                display.append((p['short_name'], p['status'], p['percentage']))

        return display
