"""
Unit tests for the civilizations module.
"""

import pytest
from src.civilizations import Civilization, CivilizationConfig


class TestCivilizationConfig:
    
    def test_creation(self):
        config = CivilizationConfig(pikemen=5, archers=10, knights=3)
        assert config.pikemen == 5
        assert config.archers == 10
        assert config.knights == 3
    
    def test_equality(self):
        config1 = CivilizationConfig(pikemen=5, archers=10, knights=3)
        config2 = CivilizationConfig(pikemen=5, archers=10, knights=3)
        config3 = CivilizationConfig(pikemen=4, archers=10, knights=3)
        
        assert config1 == config2
        assert config1 != config3


class TestCivilization:
    
    def test_all_civilizations_exist(self):
        expected_civs = ["CHINESE", "ENGLISH", "BYZANTINE"]
        actual_civs = [civ.name for civ in Civilization]
        
        for expected in expected_civs:
            assert expected in actual_civs
    
    def test_chinese_configuration(self):
        chinese = Civilization.CHINESE
        assert chinese.pikemen_count == 2
        assert chinese.archers_count == 25
        assert chinese.knights_count == 2
        
        config = chinese.config
        assert config.pikemen == 2
        assert config.archers == 25
        assert config.knights == 2
    
    def test_english_configuration(self):
        english = Civilization.ENGLISH
        assert english.pikemen_count == 10
        assert english.archers_count == 10
        assert english.knights_count == 10
        
        config = english.config
        assert config.pikemen == 10
        assert config.archers == 10
        assert config.knights == 10
    
    def test_byzantine_configuration(self):
        byzantine = Civilization.BYZANTINE
        assert byzantine.pikemen_count == 5
        assert byzantine.archers_count == 8
        assert byzantine.knights_count == 15
        
        config = byzantine.config
        assert config.pikemen == 5
        assert config.archers == 8
        assert config.knights == 15
    
    def test_get_all_civilizations(self):
        all_civs = Civilization.get_all_civilizations()
        
        assert len(all_civs) == 3
        assert "CHINESE" in all_civs
        assert "ENGLISH" in all_civs
        assert "BYZANTINE" in all_civs
        
        assert all_civs["CHINESE"] == Civilization.CHINESE
        assert all_civs["ENGLISH"] == Civilization.ENGLISH
        assert all_civs["BYZANTINE"] == Civilization.BYZANTINE
    
    def test_string_representation(self):
        chinese = Civilization.CHINESE
        assert str(chinese) == "Chinese"
        
        english = Civilization.ENGLISH
        assert str(english) == "English"
        
        byzantine = Civilization.BYZANTINE
        assert str(byzantine) == "Byzantine"
    
    def test_repr_representation(self):
        chinese = Civilization.CHINESE
        repr_str = repr(chinese)
        
        assert "Civilization.CHINESE" in repr_str
        assert "pikemen=2" in repr_str
        assert "archers=25" in repr_str
        assert "knights=2" in repr_str
    
    def test_civilization_uniqueness(self):
        civilizations = [Civilization.CHINESE, Civilization.ENGLISH, Civilization.BYZANTINE]
        configs = [civ.config for civ in civilizations]
        
        # Each configuration should be different
        for i, config1 in enumerate(configs):
            for j, config2 in enumerate(configs):
                if i != j:
                    assert config1 != config2
    
    def test_total_unit_counts(self):
        # Calculate total units for each civilization
        chinese_total = (Civilization.CHINESE.pikemen_count + 
                        Civilization.CHINESE.archers_count + 
                        Civilization.CHINESE.knights_count)
        
        english_total = (Civilization.ENGLISH.pikemen_count + 
                        Civilization.ENGLISH.archers_count + 
                        Civilization.ENGLISH.knights_count)
        
        byzantine_total = (Civilization.BYZANTINE.pikemen_count + 
                          Civilization.BYZANTINE.archers_count + 
                          Civilization.BYZANTINE.knights_count)
        
        # Verify expected totals
        assert chinese_total == 29  # 2 + 25 + 2
        assert english_total == 30  # 10 + 10 + 10
        assert byzantine_total == 28  # 5 + 8 + 15
        
        # All civilizations should have reasonable unit counts
        assert 25 <= chinese_total <= 35
        assert 25 <= english_total <= 35
        assert 25 <= byzantine_total <= 35 