from typing import List, Optional, Dict, Type
from .units import Unit, Pikeman, Archer, Knight
from .civilizations import Civilization
from .battle import BattleRecord, BattleSystem


class InsufficientGoldError(Exception):
    pass


class InsufficientUnitsError(Exception):
    pass


class InvalidTransformationError(Exception):
    pass


class Army:
    INITIAL_GOLD = 1000
    
    def __init__(self, civilization: Civilization):
        self._civilization = civilization
        self._gold = self.INITIAL_GOLD
        self._units: List[Unit] = []
        self._battle_history: List[BattleRecord] = []
        
        # Initialize units based on civilization
        self._initialize_units()
    
    @property
    def civilization(self) -> Civilization:
        return self._civilization
    
    @property
    def gold(self) -> int:
        return self._gold
    
    @property
    def units(self) -> List[Unit]:
        return self._units.copy()
    
    @property
    def battle_history(self) -> List[BattleRecord]:
        return self._battle_history.copy()
    
    @property
    def total_strength(self) -> int:
        return sum(unit.total_strength for unit in self._units)
    
    @property
    def unit_count(self) -> int:
        return len(self._units)
    
    def get_unit_counts(self) -> Dict[str, int]:
        counts = {"Pikeman": 0, "Archer": 0, "Knight": 0}
        for unit in self._units:
            counts[unit.__class__.__name__] += 1
        return counts
    
    def get_units_by_type(self, unit_type: Type[Unit]) -> List[Unit]:
        return [unit for unit in self._units if isinstance(unit, unit_type)]
    
    def train_unit(self, unit: Unit) -> None:
        if unit not in self._units:
            raise ValueError("Unit is not part of this army")
        
        cost = unit.get_training_cost()
        if self._gold < cost:
            raise InsufficientGoldError(
                f"Not enough gold for training. Need {cost}, have {self._gold}"
            )
        
        training_cost = unit.train()
        self._gold -= training_cost
    
    def train_all_units_of_type(self, unit_type: Type[Unit]) -> int:
        units_to_train = self.get_units_by_type(unit_type)
        if not units_to_train:
            return 0
        
        cost_per_unit = units_to_train[0].get_training_cost()
        total_cost = cost_per_unit * len(units_to_train)
        
        if self._gold < cost_per_unit:
            raise InsufficientGoldError(
                f"Not enough gold to train any {unit_type.__name__}. "
                f"Need {cost_per_unit}, have {self._gold}"
            )
        
        trained_count = 0
        for unit in units_to_train:
            if self._gold >= cost_per_unit:
                self.train_unit(unit)
                trained_count += 1
            else:
                break
        
        return trained_count
    
    def transform_unit(self, unit: Unit) -> Unit:
        if unit not in self._units:
            raise ValueError("Unit is not part of this army")
        
        transformation_cost = unit.get_transformation_cost()
        target_type = unit.get_transformation_target()
        
        if transformation_cost is None or target_type is None:
            raise InvalidTransformationError(
                f"{unit.__class__.__name__} cannot be transformed"
            )
        
        if self._gold < transformation_cost:
            raise InsufficientGoldError(
                f"Not enough gold for transformation. Need {transformation_cost}, have {self._gold}"
            )
        
        # Remove old unit and create new one
        self._units.remove(unit)
        # Create new unit based on target type
        if target_type == "Archer":
            new_unit = Archer(unit.age_in_years)
        elif target_type == "Knight":
            new_unit = Knight(unit.age_in_years)
        else:
            new_unit = Pikeman(unit.age_in_years)
        self._units.append(new_unit)
        self._gold -= transformation_cost
        
        return new_unit
    
    def attack(self, target_army: 'Army') -> None:
        BattleSystem.resolve_battle(self, target_army)
    
    def _initialize_units(self) -> None:
        config = self._civilization.config
        
        # Create pikemen
        for _ in range(config.pikemen):
            self._units.append(Pikeman())
        
        # Create archers
        for _ in range(config.archers):
            self._units.append(Archer())
        
        # Create knights
        for _ in range(config.knights):
            self._units.append(Knight())
    
    def _remove_strongest_units(self, count: int) -> int:
        if not self._units:
            return 0
        
        # Sort units by strength (descending) and remove the strongest ones
        self._units.sort(key=lambda u: u.total_strength, reverse=True)
        units_to_remove = min(count, len(self._units))
        
        for _ in range(units_to_remove):
            self._units.pop(0)
        
        return units_to_remove
    
    def __str__(self) -> str:
        unit_counts = self.get_unit_counts()
        return (f"{self._civilization} Army: "
                f"{unit_counts['Pikeman']} Pikemen, "
                f"{unit_counts['Archer']} Archers, "
                f"{unit_counts['Knight']} Knights "
                f"(Strength: {self.total_strength}, Gold: {self._gold})")
    
    def __repr__(self) -> str:
        return (f"Army(civilization={self._civilization}, "
                f"units={len(self._units)}, "
                f"strength={self.total_strength}, "
                f"gold={self._gold}, "
                f"battles={len(self._battle_history)})") 