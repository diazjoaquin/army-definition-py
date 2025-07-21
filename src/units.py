from abc import ABC, abstractmethod
from typing import Optional


class Unit(ABC):
    
    def __init__(self, age_in_years: int = 0):
        self._base_strength = self._get_base_strength()
        self._additional_strength = 0
        self._age_in_years = age_in_years
    
    @property
    def age_in_years(self) -> int:
        return self._age_in_years
    
    @property
    def total_strength(self) -> int:
        return self._base_strength + self._additional_strength
    
    @property
    def additional_strength(self) -> int:
        return self._additional_strength
    
    @abstractmethod
    def _get_base_strength(self) -> int:
        pass
    
    @abstractmethod
    def get_training_cost(self) -> int:
        pass
    
    @abstractmethod
    def get_training_strength_gain(self) -> int:
        pass
    
    @abstractmethod
    def get_transformation_cost(self) -> Optional[int]:
        pass
    
    @abstractmethod
    def get_transformation_target(self) -> Optional[str]:
        pass
    
    def train(self) -> int:
        cost = self.get_training_cost()
        self._additional_strength += self.get_training_strength_gain()
        return cost
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(strength={self.total_strength}, age={self.age_in_years})"
    
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(base_strength={self._base_strength}, "
                f"additional_strength={self._additional_strength}, age={self.age_in_years})")


class Pikeman(Unit):
    def _get_base_strength(self) -> int:
        return 5
    
    def get_training_cost(self) -> int:
        return 10
    
    def get_training_strength_gain(self) -> int:
        return 3
    
    def get_transformation_cost(self) -> Optional[int]:
        return 30
    
    def get_transformation_target(self) -> Optional[str]:
        return "Archer"


class Archer(Unit):
    
    def _get_base_strength(self) -> int:
        return 10
    
    def get_training_cost(self) -> int:
        return 20
    
    def get_training_strength_gain(self) -> int:
        return 7
    
    def get_transformation_cost(self) -> Optional[int]:
        return 40
    
    def get_transformation_target(self) -> Optional[str]:
        return "Knight"


class Knight(Unit):
    
    def _get_base_strength(self) -> int:
        return 20
    
    def get_training_cost(self) -> int:
        return 30
    
    def get_training_strength_gain(self) -> int:
        return 10
    
    def get_transformation_cost(self) -> Optional[int]:
        return None
    
    def get_transformation_target(self) -> Optional[str]:
        return None
