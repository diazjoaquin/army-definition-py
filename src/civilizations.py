from enum import Enum
from dataclasses import dataclass
from typing import Dict


@dataclass
class CivilizationConfig:
    pikemen: int
    archers: int
    knights: int


class Civilization(Enum):
    
    CHINESE = CivilizationConfig(pikemen=2, archers=25, knights=2)
    ENGLISH = CivilizationConfig(pikemen=10, archers=10, knights=10)
    BYZANTINE = CivilizationConfig(pikemen=5, archers=8, knights=15)
    
    @property
    def config(self) -> CivilizationConfig:
        return self.value
    
    @property
    def pikemen_count(self) -> int:
        return self.value.pikemen
    
    @property
    def archers_count(self) -> int:
        return self.value.archers
    
    @property
    def knights_count(self) -> int:
        return self.value.knights
    
    @classmethod
    def get_all_civilizations(cls) -> Dict[str, 'Civilization']:
        return {civ.name: civ for civ in cls}
    
    def __str__(self) -> str:
        return self.name.title()
    
    def __repr__(self) -> str:
        config = self.config
        return (f"Civilization.{self.name}(pikemen={config.pikemen}, "
                f"archers={config.archers}, knights={config.knights})") 