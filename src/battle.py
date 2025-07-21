from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .army import Army


class BattleResult(Enum):
    WIN = "WIN"
    LOSS = "LOSS"
    TIE = "TIE"


@dataclass
class BattleRecord:
    opponent_civilization: str
    result: BattleResult
    own_strength: int
    opponent_strength: int
    gold_gained: int
    units_lost: int
    
    def __str__(self) -> str:
        return (f"Battle vs {self.opponent_civilization}: {self.result.value} "
                f"({self.own_strength} vs {self.opponent_strength}) "
                f"Gold: {self.gold_gained:+d}, Units lost: {self.units_lost}")


class BattleSystem:
    
    WINNER_GOLD_REWARD = 100
    UNITS_LOST_ON_DEFEAT = 2
    
    @classmethod
    def resolve_battle(cls, army1: 'Army', army2: 'Army') -> None:
        army1_strength = army1.total_strength
        army2_strength = army2.total_strength
        
        if army1_strength > army2_strength:
            cls._handle_victory(army1, army2, army1_strength, army2_strength)
        elif army2_strength > army1_strength:
            cls._handle_victory(army2, army1, army2_strength, army1_strength)
        else:
            cls._handle_tie(army1, army2, army1_strength)
    
    @classmethod
    def _handle_victory(cls, winner: 'Army', loser: 'Army', 
                       winner_strength: int, loser_strength: int) -> None:
        winner._gold += cls.WINNER_GOLD_REWARD
        
        units_lost = loser._remove_strongest_units(cls.UNITS_LOST_ON_DEFEAT)
        
        winner_record = BattleRecord(
            opponent_civilization=str(loser.civilization),
            result=BattleResult.WIN,
            own_strength=winner_strength,
            opponent_strength=loser_strength,
            gold_gained=cls.WINNER_GOLD_REWARD,
            units_lost=0
        )
        
        loser_record = BattleRecord(
            opponent_civilization=str(winner.civilization),
            result=BattleResult.LOSS,
            own_strength=loser_strength,
            opponent_strength=winner_strength,
            gold_gained=0,
            units_lost=units_lost
        )
        
        winner._battle_history.append(winner_record)
        loser._battle_history.append(loser_record)
    
    @classmethod
    def _handle_tie(cls, army1: 'Army', army2: 'Army', strength: int) -> None:
        units_lost_1 = army1._remove_strongest_units(1)
        units_lost_2 = army2._remove_strongest_units(1)
        
        army1_record = BattleRecord(
            opponent_civilization=str(army2.civilization),
            result=BattleResult.TIE,
            own_strength=strength,
            opponent_strength=strength,
            gold_gained=0,
            units_lost=units_lost_1
        )
        
        army2_record = BattleRecord(
            opponent_civilization=str(army1.civilization),
            result=BattleResult.TIE,
            own_strength=strength,
            opponent_strength=strength,
            gold_gained=0,
            units_lost=units_lost_2
        )
        
        army1._battle_history.append(army1_record)
        army2._battle_history.append(army2_record) 