import pytest
from src.army import Army
from src.civilizations import Civilization
from src.battle import BattleSystem, BattleRecord, BattleResult
from src.units import Pikeman, Archer, Knight


class TestBattleRecord:
    
    def test_battle_record_creation(self):
        record = BattleRecord(
            opponent_civilization="English",
            result=BattleResult.WIN,
            own_strength=300,
            opponent_strength=250,
            gold_gained=100,
            units_lost=0
        )
        
        assert record.opponent_civilization == "English"
        assert record.result == BattleResult.WIN
        assert record.own_strength == 300
        assert record.opponent_strength == 250
        assert record.gold_gained == 100
        assert record.units_lost == 0
    
    def test_battle_record_string_representation(self):
        record = BattleRecord(
            opponent_civilization="Byzantine",
            result=BattleResult.LOSS,
            own_strength=200,
            opponent_strength=300,
            gold_gained=0,
            units_lost=2
        )
        
        str_repr = str(record)
        assert "Battle vs Byzantine: LOSS" in str_repr
        assert "(200 vs 300)" in str_repr
        assert "Gold: +0" in str_repr
        assert "Units lost: 2" in str_repr


class TestBattleSystem:
    
    def test_clear_victory(self):
        # Byzantine (405 strength) vs Chinese (300 strength)
        stronger_army = Army(Civilization.BYZANTINE)
        weaker_army = Army(Civilization.CHINESE)
        
        initial_stronger_gold = stronger_army.gold
        initial_weaker_units = weaker_army.unit_count
        
        BattleSystem.resolve_battle(stronger_army, weaker_army)
        
        # Winner should gain gold
        assert stronger_army.gold == initial_stronger_gold + 100
        
        # Loser should lose 2 strongest units
        assert weaker_army.unit_count == initial_weaker_units - 2
        
        # Check battle history
        stronger_history = stronger_army.battle_history
        weaker_history = weaker_army.battle_history
        
        assert len(stronger_history) == 1
        assert len(weaker_history) == 1
        
        assert stronger_history[0].result == BattleResult.WIN
        assert weaker_history[0].result == BattleResult.LOSS
        assert stronger_history[0].gold_gained == 100
        assert weaker_history[0].units_lost == 2
    
    def test_reverse_victory(self):
        # Chinese (300 strength) vs Byzantine (405 strength)
        weaker_army = Army(Civilization.CHINESE)
        stronger_army = Army(Civilization.BYZANTINE)
        
        initial_stronger_gold = stronger_army.gold
        initial_weaker_units = weaker_army.unit_count
        
        BattleSystem.resolve_battle(weaker_army, stronger_army)
        
        # Stronger army (second argument) should win
        assert stronger_army.gold == initial_stronger_gold + 100
        assert weaker_army.unit_count == initial_weaker_units - 2
        
        # Check battle history shows correct results
        weaker_history = weaker_army.battle_history
        stronger_history = stronger_army.battle_history
        
        assert weaker_history[0].result == BattleResult.LOSS
        assert stronger_history[0].result == BattleResult.WIN
    
    def test_tie_scenario(self):
        # Create two identical armies
        army1 = Army(Civilization.ENGLISH)
        army2 = Army(Civilization.ENGLISH)
        
        initial_units_1 = army1.unit_count
        initial_units_2 = army2.unit_count
        initial_gold_1 = army1.gold
        initial_gold_2 = army2.gold
        
        BattleSystem.resolve_battle(army1, army2)
        
        # Both armies should lose one unit each
        assert army1.unit_count == initial_units_1 - 1
        assert army2.unit_count == initial_units_2 - 1
        
        # Neither should gain gold
        assert army1.gold == initial_gold_1
        assert army2.gold == initial_gold_2
        
        # Check battle history
        history1 = army1.battle_history
        history2 = army2.battle_history
        
        assert len(history1) == 1
        assert len(history2) == 1
        assert history1[0].result == BattleResult.TIE
        assert history2[0].result == BattleResult.TIE
        assert history1[0].units_lost == 1
        assert history2[0].units_lost == 1
    
    def test_strongest_units_removed(self):
        army = Army(Civilization.CHINESE)
        
        # Train some units to make them stronger
        pikemen = army.get_units_by_type(Pikeman)
        archers = army.get_units_by_type(Archer)
        
        # Train a few archers to make them stronger (10 + 7 = 17 each)
        for i in range(3):
            army.train_unit(archers[i])
        
        # Get strength distribution before battle
        unit_strengths_before = [unit.total_strength for unit in army.units]
        unit_strengths_before.sort(reverse=True)
        
        # Simulate losing 2 strongest units
        army._remove_strongest_units(2)
        
        # Check that the 2 strongest units were removed
        unit_strengths_after = [unit.total_strength for unit in army.units]
        unit_strengths_after.sort(reverse=True)
        
        # The remaining strongest units should be weaker than the original 2nd strongest
        assert max(unit_strengths_after) <= unit_strengths_before[2]
    
    def test_multiple_battles_history(self):
        army1 = Army(Civilization.BYZANTINE)  # Stronger
        army2 = Army(Civilization.CHINESE)    # Weaker
        army3 = Army(Civilization.ENGLISH)    # Medium
        
        # First battle: army1 vs army2
        BattleSystem.resolve_battle(army1, army2)
        
        # Second battle: army1 vs army3
        BattleSystem.resolve_battle(army1, army3)
        
        # Army1 should have won both battles
        assert len(army1.battle_history) == 2
        assert all(record.result == BattleResult.WIN for record in army1.battle_history)
        assert army1.gold == 1000 + 200  # Won 2 battles, 100 gold each
        
        # Other armies should have one loss each
        assert len(army2.battle_history) == 1
        assert len(army3.battle_history) == 1
        assert army2.battle_history[0].result == BattleResult.LOSS
        assert army3.battle_history[0].result == BattleResult.LOSS
    
    def test_battle_record_accuracy(self):
        chinese = Army(Civilization.CHINESE)    # 300 strength
        english = Army(Civilization.ENGLISH)    # 350 strength
        
        BattleSystem.resolve_battle(chinese, english)
        
        # Check Chinese (loser) record
        chinese_record = chinese.battle_history[0]
        assert chinese_record.opponent_civilization == "English"
        assert chinese_record.result == BattleResult.LOSS
        assert chinese_record.own_strength == 300
        assert chinese_record.opponent_strength == 350
        assert chinese_record.gold_gained == 0
        assert chinese_record.units_lost == 2
        
        # Check English (winner) record
        english_record = english.battle_history[0]
        assert english_record.opponent_civilization == "Chinese"
        assert english_record.result == BattleResult.WIN
        assert english_record.own_strength == 350
        assert english_record.opponent_strength == 300
        assert english_record.gold_gained == 100
        assert english_record.units_lost == 0
    
    def test_army_attack_method(self):
        attacker = Army(Civilization.BYZANTINE)
        defender = Army(Civilization.CHINESE)
        
        initial_attacker_gold = attacker.gold
        initial_defender_units = defender.unit_count
        
        attacker.attack(defender)
        
        # Should work the same as BattleSystem.resolve_battle
        assert attacker.gold == initial_attacker_gold + 100
        assert defender.unit_count == initial_defender_units - 2
        assert len(attacker.battle_history) == 1
        assert len(defender.battle_history) == 1
    
    def test_empty_army_battle(self):
        normal_army = Army(Civilization.CHINESE)
        empty_army = Army(Civilization.ENGLISH)
        
        # Remove all units from empty army
        empty_army._units = []
        
        BattleSystem.resolve_battle(normal_army, empty_army)
        
        # Normal army should win easily
        assert normal_army.gold == 1100  # Gained 100 gold
        assert len(empty_army.units) == 0  # Still empty
        assert normal_army.battle_history[0].result == BattleResult.WIN
        assert empty_army.battle_history[0].result == BattleResult.LOSS
    
    def test_constants(self):
        assert BattleSystem.WINNER_GOLD_REWARD == 100
        assert BattleSystem.UNITS_LOST_ON_DEFEAT == 2 