"""
Tests for PartManager.
"""

import pytest
from core.models.parts import Part, PartManager


class TestPart:
    """Tests for Part model."""

    def test_default_values(self):
        """Test Part default values."""
        part = Part(id='X', name='Test Part')
        assert part.id == 'X'
        assert part.name == 'Test Part'
        assert part.enabled is True
        assert part.removable is True
        assert part.order == 0
        assert part.is_custom is False

    def test_equality(self):
        """Test Part equality based on id."""
        part1 = Part(id='A', name='Part A')
        part2 = Part(id='A', name='Different Name')
        part3 = Part(id='B', name='Part B')

        assert part1 == part2  # Same ID
        assert part1 != part3  # Different ID

    def test_hash(self):
        """Test Part can be used in sets."""
        part1 = Part(id='A', name='Part A')
        part2 = Part(id='A', name='Different')

        parts_set = {part1, part2}
        assert len(parts_set) == 1  # Same ID, so only one in set


class TestPartManager:
    """Tests for PartManager."""

    def test_default_initialization(self):
        """Test PartManager initializes with default parts."""
        manager = PartManager()
        parts = manager.get_all_parts()

        assert len(parts) == 7
        part_ids = [p.id for p in parts]
        assert 'A' in part_ids
        assert 'G' in part_ids

    def test_get_all_parts_sorted(self):
        """Test parts are returned sorted by order."""
        manager = PartManager()
        parts = manager.get_all_parts()

        orders = [p.order for p in parts]
        assert orders == sorted(orders)

    def test_get_enabled_parts(self):
        """Test getting only enabled parts."""
        manager = PartManager()

        # All parts should be enabled by default
        enabled = manager.get_enabled_parts()
        assert len(enabled) == 7

    def test_get_part_by_id(self):
        """Test getting a part by ID."""
        manager = PartManager()

        part_a = manager.get_part_by_id('A')
        assert part_a is not None
        assert part_a.name == 'PYQ Analysis'

        part_none = manager.get_part_by_id('Z')
        assert part_none is None

    def test_enable_part(self):
        """Test enabling a part."""
        manager = PartManager()
        manager.disable_part('C')

        assert manager.get_part_by_id('C').enabled is False

        result = manager.enable_part('C')
        assert result is True
        assert manager.get_part_by_id('C').enabled is True

    def test_disable_part_removable(self):
        """Test disabling a removable part."""
        manager = PartManager()

        result = manager.disable_part('C')  # C is removable
        assert result is True
        assert manager.get_part_by_id('C').enabled is False

    def test_disable_part_non_removable(self):
        """Test disabling a non-removable part fails."""
        manager = PartManager()

        result = manager.disable_part('A')  # A is not removable
        assert result is False
        assert manager.get_part_by_id('A').enabled is True

    def test_toggle_part(self):
        """Test toggling a part's enabled state."""
        manager = PartManager()

        # Toggle C (removable) off
        new_state = manager.toggle_part('C')
        assert new_state is False

        # Toggle C back on
        new_state = manager.toggle_part('C')
        assert new_state is True

    def test_add_custom_part(self):
        """Test adding a custom part."""
        manager = PartManager()

        new_part = manager.add_custom_part(
            name='Custom Section',
            description='A custom section',
            icon='🔧'
        )

        assert new_part.id == 'H'  # Next available after A-G
        assert new_part.name == 'Custom Section'
        assert new_part.is_custom is True
        assert new_part.removable is True
        assert len(manager.get_all_parts()) == 8

    def test_remove_custom_part(self):
        """Test removing a custom part."""
        manager = PartManager()

        new_part = manager.add_custom_part(name='Custom')
        assert len(manager.get_all_parts()) == 8

        result = manager.remove_part(new_part.id)
        assert result is True
        assert len(manager.get_all_parts()) == 7

    def test_remove_standard_part_fails(self):
        """Test removing a standard part fails."""
        manager = PartManager()

        result = manager.remove_part('A')
        assert result is False
        assert len(manager.get_all_parts()) == 7

    def test_reorder_parts(self):
        """Test reordering parts."""
        manager = PartManager()

        # Reorder to put G first
        manager.reorder_parts(['G', 'A', 'B', 'C', 'D', 'E', 'F'])

        parts = manager.get_all_parts()
        assert parts[0].id == 'G'
        assert parts[1].id == 'A'

    def test_move_part_up(self):
        """Test moving a part up."""
        manager = PartManager()

        # B starts at order 2
        result = manager.move_part_up('B')
        assert result is True

        parts = manager.get_all_parts()
        part_ids = [p.id for p in parts]
        assert part_ids.index('B') < part_ids.index('A')

    def test_move_part_down(self):
        """Test moving a part down."""
        manager = PartManager()

        result = manager.move_part_down('A')
        assert result is True

        parts = manager.get_all_parts()
        part_ids = [p.id for p in parts]
        assert part_ids.index('A') > part_ids.index('B')

    def test_update_part_name(self):
        """Test updating a part's name."""
        manager = PartManager()

        result = manager.update_part_name('A', 'Previous Year Questions')
        assert result is True
        assert manager.get_part_by_id('A').name == 'Previous Year Questions'

    def test_update_part_description(self):
        """Test updating a part's description."""
        manager = PartManager()

        result = manager.update_part_description('A', 'New description')
        assert result is True
        assert manager.get_part_by_id('A').description == 'New description'

    def test_reset_to_defaults(self):
        """Test resetting to default configuration."""
        manager = PartManager()

        # Make some changes
        manager.disable_part('C')
        manager.add_custom_part(name='Custom')
        manager.update_part_name('A', 'Changed')

        # Reset
        manager.reset_to_defaults()

        parts = manager.get_all_parts()
        assert len(parts) == 7
        assert manager.get_part_by_id('A').name == 'PYQ Analysis'
        assert manager.get_part_by_id('C').enabled is True

    def test_to_dict(self):
        """Test converting to dictionary."""
        manager = PartManager()

        data = manager.to_dict()
        assert isinstance(data, list)
        assert len(data) == 7
        assert all(isinstance(d, dict) for d in data)

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = [
            {'id': 'X', 'name': 'Test', 'enabled': True, 'removable': True, 'order': 1, 'is_custom': False, 'description': '', 'icon': ''}
        ]

        manager = PartManager.from_dict(data)
        assert len(manager.get_all_parts()) == 1
        assert manager.get_part_by_id('X').name == 'Test'

    def test_get_enabled_part_ids(self):
        """Test getting list of enabled part IDs."""
        manager = PartManager()

        ids = manager.get_enabled_part_ids()
        assert ids == ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def test_get_part_count(self):
        """Test getting part counts."""
        manager = PartManager()
        manager.add_custom_part(name='Custom')
        manager.disable_part('C')

        counts = manager.get_part_count()
        assert counts['total'] == 8
        assert counts['enabled'] == 7  # One disabled
        assert counts['custom'] == 1
