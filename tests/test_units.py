"""
Unit tests for the units module.
"""

import pytest
from src.units import Unit, Pikeman, Archer, Knight


class TestPikeman:
    
    def test_creation(self):
        pikeman = Pikeman()
        assert pikeman.age_in_years == 0
        assert pikeman.total_strength == 5
        assert pikeman.additional_strength == 0
        
        old_pikeman = Pikeman(age_in_years=5)
        assert old_pikeman.age_in_years == 5
        assert old_pikeman.total_strength == 5
    
    def test_training(self):
        pikeman = Pikeman()
        initial_strength = pikeman.total_strength
        
        cost = pikeman.train()
        assert cost == 10
        assert pikeman.total_strength == initial_strength + 3
        assert pikeman.additional_strength == 3
        
        # Train again
        pikeman.train()
        assert pikeman.total_strength == initial_strength + 6
        assert pikeman.additional_strength == 6
    
    def test_transformation_properties(self):
        pikeman = Pikeman()
        assert pikeman.get_transformation_cost() == 30
        assert pikeman.get_transformation_target() == "Archer"
    
    def test_string_representation(self):
        pikeman = Pikeman(age_in_years=3)
        assert "Pikeman" in str(pikeman)
        assert "strength=5" in str(pikeman)
        assert "age=3" in str(pikeman)


class TestArcher:
    
    def test_creation(self):
        archer = Archer()
        assert archer.age_in_years == 0
        assert archer.total_strength == 10
        assert archer.additional_strength == 0
    
    def test_training(self):
        archer = Archer()
        initial_strength = archer.total_strength
        
        cost = archer.train()
        assert cost == 20
        assert archer.total_strength == initial_strength + 7
        assert archer.additional_strength == 7
    
    def test_transformation_properties(self):
        archer = Archer()
        assert archer.get_transformation_cost() == 40
        assert archer.get_transformation_target() == "Knight"


class TestKnight:
    
    def test_creation(self):
        knight = Knight()
        assert knight.age_in_years == 0
        assert knight.total_strength == 20
        assert knight.additional_strength == 0
    
    def test_training(self):
        knight = Knight()
        initial_strength = knight.total_strength
        
        cost = knight.train()
        assert cost == 30
        assert knight.total_strength == initial_strength + 10
        assert knight.additional_strength == 10
    
    def test_no_transformation(self):
        knight = Knight()
        assert knight.get_transformation_cost() is None
        assert knight.get_transformation_target() is None



class TestUnitPolymorphism:
    
    def test_all_units_have_required_methods(self):
        units = [Pikeman(), Archer(), Knight()]
        
        for unit in units:
            # Test required properties
            assert isinstance(unit.age_in_years, int)
            assert isinstance(unit.total_strength, int)
            assert isinstance(unit.additional_strength, int)
            
            # Test required methods
            assert isinstance(unit.get_training_cost(), int)
            assert isinstance(unit.get_training_strength_gain(), int)
            
            # Training should work
            initial_strength = unit.total_strength
            cost = unit.train()
            assert unit.total_strength > initial_strength
            assert cost > 0
    
    def test_strength_progression(self):
        pikeman = Pikeman()
        archer = Archer()
        knight = Knight()
        
        assert pikeman.total_strength == 5
        assert archer.total_strength == 10
        assert knight.total_strength == 20
        
        # Knights should be strongest, pikemen weakest
        assert knight.total_strength > archer.total_strength > pikeman.total_strength 