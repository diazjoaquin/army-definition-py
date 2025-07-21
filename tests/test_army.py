import pytest
from src.army import Army, InsufficientGoldError, InsufficientUnitsError, InvalidTransformationError
from src.civilizations import Civilization
from src.units import Pikeman, Archer, Knight
from src.battle import BattleResult


class TestArmyCreation:

    def test_chinese_army_creation(self):
        army = Army(Civilization.CHINESE)
        
        assert army.civilization == Civilization.CHINESE
        assert army.gold == 1000
        assert army.unit_count == 29  # 2 + 25 + 2
        
        unit_counts = army.get_unit_counts()
        assert unit_counts["Pikeman"] == 2
        assert unit_counts["Archer"] == 25
        assert unit_counts["Knight"] == 2
    
    def test_english_army_creation(self):
        army = Army(Civilization.ENGLISH)
        
        assert army.civilization == Civilization.ENGLISH
        assert army.gold == 1000
        assert army.unit_count == 30  # 10 + 10 + 10
        
        unit_counts = army.get_unit_counts()
        assert unit_counts["Pikeman"] == 10
        assert unit_counts["Archer"] == 10
        assert unit_counts["Knight"] == 10
    
    def test_byzantine_army_creation(self):
        army = Army(Civilization.BYZANTINE)
        
        assert army.civilization == Civilization.BYZANTINE
        assert army.gold == 1000
        assert army.unit_count == 28  # 5 + 8 + 15
        
        unit_counts = army.get_unit_counts()
        assert unit_counts["Pikeman"] == 5
        assert unit_counts["Archer"] == 8
        assert unit_counts["Knight"] == 15
    
    def test_initial_strength_calculation(self):
        chinese = Army(Civilization.CHINESE)
        english = Army(Civilization.ENGLISH)
        byzantine = Army(Civilization.BYZANTINE)
        
        # Chinese: 2*5 + 25*10 + 2*20 = 10 + 250 + 40 = 300
        assert chinese.total_strength == 300
        
        # English: 10*5 + 10*10 + 10*20 = 50 + 100 + 200 = 350
        assert english.total_strength == 350
        
        # Byzantine: 5*5 + 8*10 + 15*20 = 25 + 80 + 300 = 405
        assert byzantine.total_strength == 405
    
    def test_empty_battle_history(self):
        army = Army(Civilization.CHINESE)
        assert len(army.battle_history) == 0


class TestArmyUnitManagement:
    
    def test_get_units_by_type(self):
        army = Army(Civilization.ENGLISH)  # 10 of each type
        
        pikemen = army.get_units_by_type(Pikeman)
        archers = army.get_units_by_type(Archer)
        knights = army.get_units_by_type(Knight)
        
        assert len(pikemen) == 10
        assert len(archers) == 10
        assert len(knights) == 10
        
        assert all(isinstance(unit, Pikeman) for unit in pikemen)
        assert all(isinstance(unit, Archer) for unit in archers)
        assert all(isinstance(unit, Knight) for unit in knights)
    
    def test_units_property_returns_copy(self):
        army = Army(Civilization.CHINESE)
        units_copy = army.units
        
        # Modifying the copy should not affect the original
        units_copy.append(Pikeman())
        assert len(army.units) == 29  # Original unchanged
        assert len(units_copy) == 30  # Copy is modified


class TestArmyTraining:
    
    def test_train_single_unit(self):
        army = Army(Civilization.CHINESE)
        pikemen = army.get_units_by_type(Pikeman)
        pikeman = pikemen[0]
        
        initial_gold = army.gold
        initial_strength = pikeman.total_strength
        
        army.train_unit(pikeman)
        
        assert army.gold == initial_gold - 10  # Pikeman training cost
        assert pikeman.total_strength == initial_strength + 3  # Pikeman training gain
    
    def test_train_unit_not_in_army(self):
        army = Army(Civilization.CHINESE)
        external_pikeman = Pikeman()
        
        with pytest.raises(ValueError, match="Unit is not part of this army"):
            army.train_unit(external_pikeman)
    
    def test_train_unit_insufficient_gold(self):
        army = Army(Civilization.CHINESE)
        pikemen = army.get_units_by_type(Pikeman)
        pikeman = pikemen[0]
        
        # Spend almost all gold
        army._gold = 5  # Less than pikeman training cost (10)
        
        with pytest.raises(InsufficientGoldError):
            army.train_unit(pikeman)
    
    def test_train_all_units_of_type(self):
        army = Army(Civilization.CHINESE)
        initial_gold = army.gold
        
        # Train all pikemen (2 units, 10 gold each)
        trained_count = army.train_all_units_of_type(Pikeman)
        
        assert trained_count == 2
        assert army.gold == initial_gold - 20  # 2 * 10
        
        # All pikemen should be stronger
        pikemen = army.get_units_by_type(Pikeman)
        for pikeman in pikemen:
            assert pikeman.total_strength == 8  # 5 + 3
    
    def test_train_all_units_partial_gold(self):
        army = Army(Civilization.ENGLISH)  # 10 pikemen
        army._gold = 25  # Only enough for 2.5 pikemen (10 gold each)
        
        trained_count = army.train_all_units_of_type(Pikeman)
        
        assert trained_count == 2  # Only 2 could be trained
        assert army.gold == 5  # 25 - 20
    
    def test_train_all_units_insufficient_gold(self):
        army = Army(Civilization.CHINESE)
        army._gold = 5  # Less than pikeman training cost (10)
        
        with pytest.raises(InsufficientGoldError):
            army.train_all_units_of_type(Pikeman)
    
    def test_train_all_units_no_units_of_type(self):
        army = Army(Civilization.CHINESE)
        # Remove all knights
        army._units = [u for u in army._units if not isinstance(u, Knight)]
        
        trained_count = army.train_all_units_of_type(Knight)
        assert trained_count == 0


class TestArmyTransformation:
    
    def test_transform_pikeman_to_archer(self):
        army = Army(Civilization.CHINESE)
        pikemen = army.get_units_by_type(Pikeman)
        pikeman = pikemen[0]
        
        initial_gold = army.gold
        initial_pikeman_count = len(army.get_units_by_type(Pikeman))
        initial_archer_count = len(army.get_units_by_type(Archer))
        
        new_archer = army.transform_unit(pikeman)
        
        assert isinstance(new_archer, Archer)
        assert army.gold == initial_gold - 30  # Transformation cost
        assert len(army.get_units_by_type(Pikeman)) == initial_pikeman_count - 1
        assert len(army.get_units_by_type(Archer)) == initial_archer_count + 1
        assert pikeman not in army.units
        assert new_archer in army.units
    
    def test_transform_archer_to_knight(self):
        army = Army(Civilization.CHINESE)
        archers = army.get_units_by_type(Archer)
        archer = archers[0]
        
        initial_gold = army.gold
        initial_archer_count = len(army.get_units_by_type(Archer))
        initial_knight_count = len(army.get_units_by_type(Knight))
        
        new_knight = army.transform_unit(archer)
        
        assert isinstance(new_knight, Knight)
        assert army.gold == initial_gold - 40  # Transformation cost
        assert len(army.get_units_by_type(Archer)) == initial_archer_count - 1
        assert len(army.get_units_by_type(Knight)) == initial_knight_count + 1
    
    def test_transform_knight_fails(self):
        army = Army(Civilization.CHINESE)
        knights = army.get_units_by_type(Knight)
        knight = knights[0]
        
        with pytest.raises(InvalidTransformationError):
            army.transform_unit(knight)
    
    def test_transform_unit_not_in_army(self):
        army = Army(Civilization.CHINESE)
        external_pikeman = Pikeman()
        
        with pytest.raises(ValueError, match="Unit is not part of this army"):
            army.transform_unit(external_pikeman)
    
    def test_transform_insufficient_gold(self):
        army = Army(Civilization.CHINESE)
        pikemen = army.get_units_by_type(Pikeman)
        pikeman = pikemen[0]
        
        army._gold = 20  # Less than transformation cost (30)
        
        with pytest.raises(InsufficientGoldError):
            army.transform_unit(pikeman)
    
    def test_transform_preserves_age(self):
        army = Army(Civilization.CHINESE)
        # Create an old pikeman
        old_pikeman = Pikeman(age_in_years=5)
        army._units.append(old_pikeman)
        
        new_archer = army.transform_unit(old_pikeman)
        assert new_archer.age_in_years == 5


class TestArmyStringRepresentation:
    
    def test_str_representation(self):
        army = Army(Civilization.CHINESE)
        str_repr = str(army)
        
        assert "Chinese Army" in str_repr
        assert "2 Pikemen" in str_repr
        assert "25 Archers" in str_repr
        assert "2 Knights" in str_repr
        assert "Strength: 300" in str_repr
        assert "Gold: 1000" in str_repr
    
    def test_repr_representation(self):
        army = Army(Civilization.CHINESE)
        repr_str = repr(army)
        
        assert "Army(" in repr_str
        assert "civilization=" in repr_str
        assert "units=29" in repr_str
        assert "strength=300" in repr_str
        assert "gold=1000" in repr_str
        assert "battles=0" in repr_str 