"""
Part management models for Guide Book Generator.
Handles dynamic part configuration (add/remove/reorder).
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Part(BaseModel):
    """Configuration for a single part."""
    id: str
    name: str
    enabled: bool = True
    removable: bool = True
    order: int = 0
    is_custom: bool = False
    description: str = ""
    icon: str = ""

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Part):
            return self.id == other.id
        return False


class PartManager:
    """
    Manages the parts for a chapter.
    Handles adding, removing, reordering, and enabling/disabling parts.
    """

    # Default parts configuration
    DEFAULT_PARTS = [
        Part(
            id='A',
            name='PYQ Analysis',
            enabled=True,
            removable=False,
            order=1,
            is_custom=False,
            description='10-year data with predictions and syllabus note',
            icon='📊'
        ),
        Part(
            id='B',
            name='Key Concepts',
            enabled=True,
            removable=False,
            order=2,
            is_custom=False,
            description='Core topics with memory tricks and exam-focused explanations',
            icon='📖'
        ),
        Part(
            id='C',
            name='Model Answers',
            enabled=True,
            removable=True,
            order=3,
            is_custom=False,
            description='Examiner-approved answers with marking scheme',
            icon='✅'
        ),
        Part(
            id='D',
            name='Practice Questions',
            enabled=True,
            removable=True,
            order=4,
            is_custom=False,
            description='MCQs, AR, SA, LA, HOTS, CBQs with answer hints',
            icon='📝'
        ),
        Part(
            id='E',
            name='Map Work',
            enabled=True,
            removable=True,
            order=5,
            is_custom=False,
            description='CBSE prescribed locations and marking tips',
            icon='🗺️'
        ),
        Part(
            id='F',
            name='Quick Revision',
            enabled=True,
            removable=True,
            order=6,
            is_custom=False,
            description='One-page summary, memory tricks compilation, key dates',
            icon='🔄'
        ),
        Part(
            id='G',
            name='Exam Strategy',
            enabled=True,
            removable=True,
            order=7,
            is_custom=False,
            description='Time management, marking scheme insights, last-minute tips',
            icon='🎯'
        ),
    ]

    def __init__(self, parts: Optional[List[Part]] = None):
        """Initialize with parts or use defaults."""
        if parts is None:
            self.parts = [p.model_copy() for p in self.DEFAULT_PARTS]
        else:
            self.parts = parts

    def get_all_parts(self) -> List[Part]:
        """Get all parts sorted by order."""
        return sorted(self.parts, key=lambda p: p.order)

    def get_enabled_parts(self) -> List[Part]:
        """Get only enabled parts sorted by order."""
        return sorted([p for p in self.parts if p.enabled], key=lambda p: p.order)

    def get_part_by_id(self, part_id: str) -> Optional[Part]:
        """Get a part by its ID."""
        for part in self.parts:
            if part.id == part_id:
                return part
        return None

    def enable_part(self, part_id: str) -> bool:
        """Enable a part by ID. Returns True if successful."""
        part = self.get_part_by_id(part_id)
        if part:
            part.enabled = True
            return True
        return False

    def disable_part(self, part_id: str) -> bool:
        """Disable a part by ID. Returns True if successful."""
        part = self.get_part_by_id(part_id)
        if part and part.removable:
            part.enabled = False
            return True
        return False

    def toggle_part(self, part_id: str) -> bool:
        """Toggle a part's enabled state. Returns new state."""
        part = self.get_part_by_id(part_id)
        if part:
            if part.enabled and part.removable:
                part.enabled = False
            else:
                part.enabled = True
            return part.enabled
        return False

    def add_custom_part(self, name: str, description: str = "", icon: str = "📌") -> Part:
        """Add a custom part. Returns the new part."""
        # Generate next available ID (H, I, J, ...)
        existing_ids = {p.id for p in self.parts}
        next_id = None
        for char in 'HIJKLMNOPQRSTUVWXYZ':
            if char not in existing_ids:
                next_id = char
                break

        if next_id is None:
            # Fallback to numbered custom parts
            custom_count = len([p for p in self.parts if p.is_custom])
            next_id = f'CUSTOM_{custom_count + 1}'

        # Get next order
        max_order = max(p.order for p in self.parts) if self.parts else 0

        new_part = Part(
            id=next_id,
            name=name,
            enabled=True,
            removable=True,
            order=max_order + 1,
            is_custom=True,
            description=description,
            icon=icon
        )

        self.parts.append(new_part)
        return new_part

    def remove_part(self, part_id: str) -> bool:
        """Remove a part by ID. Only custom parts can be removed. Returns True if successful."""
        part = self.get_part_by_id(part_id)
        if part and part.is_custom:
            self.parts.remove(part)
            return True
        return False

    def reorder_parts(self, part_ids: List[str]) -> None:
        """Reorder parts based on the provided list of IDs."""
        for index, part_id in enumerate(part_ids):
            part = self.get_part_by_id(part_id)
            if part:
                part.order = index + 1

    def move_part_up(self, part_id: str) -> bool:
        """Move a part up in the order. Returns True if successful."""
        sorted_parts = self.get_all_parts()
        for i, part in enumerate(sorted_parts):
            if part.id == part_id and i > 0:
                # Swap orders
                sorted_parts[i].order, sorted_parts[i-1].order = (
                    sorted_parts[i-1].order, sorted_parts[i].order
                )
                return True
        return False

    def move_part_down(self, part_id: str) -> bool:
        """Move a part down in the order. Returns True if successful."""
        sorted_parts = self.get_all_parts()
        for i, part in enumerate(sorted_parts):
            if part.id == part_id and i < len(sorted_parts) - 1:
                # Swap orders
                sorted_parts[i].order, sorted_parts[i+1].order = (
                    sorted_parts[i+1].order, sorted_parts[i].order
                )
                return True
        return False

    def update_part_name(self, part_id: str, new_name: str) -> bool:
        """Update a part's name. Returns True if successful."""
        part = self.get_part_by_id(part_id)
        if part:
            part.name = new_name
            return True
        return False

    def update_part_description(self, part_id: str, new_description: str) -> bool:
        """Update a part's description. Returns True if successful."""
        part = self.get_part_by_id(part_id)
        if part:
            part.description = new_description
            return True
        return False

    def reset_to_defaults(self) -> None:
        """Reset parts to default configuration."""
        self.parts = [p.model_copy() for p in self.DEFAULT_PARTS]

    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert parts to list of dictionaries."""
        return [p.model_dump() for p in self.parts]

    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> 'PartManager':
        """Create PartManager from list of dictionaries."""
        parts = [Part.model_validate(d) for d in data]
        return cls(parts=parts)

    def get_enabled_part_ids(self) -> List[str]:
        """Get list of enabled part IDs in order."""
        return [p.id for p in self.get_enabled_parts()]

    def get_part_count(self) -> Dict[str, int]:
        """Get counts of total, enabled, and custom parts."""
        return {
            'total': len(self.parts),
            'enabled': len([p for p in self.parts if p.enabled]),
            'custom': len([p for p in self.parts if p.is_custom]),
        }
