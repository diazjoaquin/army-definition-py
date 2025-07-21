from src import Army, Civilization, Pikeman, Archer, Knight, BattleResult


def print_separator(title: str):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")


def display_army_status(army: Army, title: str):
    print(f"\n{title}")
    print(f"  {army}")
    
    unit_counts = army.get_unit_counts()
    print(f"  Unit Details:")
    print(f"    - Pikemen: {unit_counts['Pikeman']}")
    print(f"    - Archers: {unit_counts['Archer']}")  
    print(f"    - Knights: {unit_counts['Knight']}")
    print(f"  Total Strength: {army.total_strength}")
    print(f"  Gold: {army.gold}")
    print(f"  Battles Fought: {len(army.battle_history)}")


def demonstrate_army_creation():
    print_separator("ARMY CREATION")
    
    # Create armies from each civilization
    chinese_army = Army(Civilization.CHINESE)
    english_army = Army(Civilization.ENGLISH)
    byzantine_army = Army(Civilization.BYZANTINE)
    
    display_army_status(chinese_army, "Chinese Army")
    display_army_status(english_army, "English Army")
    display_army_status(byzantine_army, "Byzantine Army")
    
    return chinese_army, english_army, byzantine_army


def demonstrate_training(army: Army):
    print_separator("TRAINING DEMONSTRATION")
    
    print(f"Initial army state:")
    display_army_status(army, "Before Training")
    
    # Train individual units
    pikemen = army.get_units_by_type(Pikeman)
    if pikemen:
        print(f"\nTraining first pikeman...")
        pikeman = pikemen[0]
        print(f"  Before: Strength {pikeman.total_strength}, Army Gold {army.gold}")
        army.train_unit(pikeman)
        print(f"  After:  Strength {pikeman.total_strength}, Army Gold {army.gold}")
    
    # Train all units of a type
    archers = army.get_units_by_type(Archer)
    if archers:
        print(f"\nTraining all archers...")
        print(f"  Before: {len(archers)} archers, Army Gold {army.gold}")
        trained_count = army.train_all_units_of_type(Archer)
        print(f"  After:  {trained_count} archers trained, Army Gold {army.gold}")
        
        # Show strength improvement
        trained_archers = army.get_units_by_type(Archer)
        if trained_archers:
            print(f"  Archer strength increased to: {trained_archers[0].total_strength}")
    
    display_army_status(army, "After Training")


def demonstrate_transformation(army: Army):
    print_separator("TRANSFORMATION DEMONSTRATION")
    
    display_army_status(army, "Before Transformations")
    
    # Transform pikeman to archer
    pikemen = army.get_units_by_type(Pikeman)
    if pikemen:
        print(f"\nTransforming pikeman to archer...")
        pikeman = pikemen[0]
        print(f"  Before: {army.get_unit_counts()}, Gold {army.gold}")
        new_archer = army.transform_unit(pikeman)
        print(f"  After:  {army.get_unit_counts()}, Gold {army.gold}")
        print(f"  New archer strength: {new_archer.total_strength}")
    
    # Transform archer to knight
    archers = army.get_units_by_type(Archer)
    if len(archers) > 1:  # Keep at least one archer
        print(f"\nTransforming archer to knight...")
        archer = archers[0]
        print(f"  Before: {army.get_unit_counts()}, Gold {army.gold}")
        new_knight = army.transform_unit(archer)
        print(f"  After:  {army.get_unit_counts()}, Gold {army.gold}")
        print(f"  New knight strength: {new_knight.total_strength}")
    
    # Try to transform knight (should fail)
    knights = army.get_units_by_type(Knight)
    if knights:
        print(f"\nAttempting to transform knight (should fail)...")
        knight = knights[0]
        try:
            army.transform_unit(knight)
        except Exception as e:
            print(f"  Expected error: {e}")
    
    display_army_status(army, "After Transformations")


def demonstrate_battles(army1: Army, army2: Army, army3: Army):
    print_separator("BATTLE DEMONSTRATION")
    
    print("Initial army strengths:")
    display_army_status(army1, army1.civilization.name.title() + " Army")
    display_army_status(army2, army2.civilization.name.title() + " Army")
    display_army_status(army3, army3.civilization.name.title() + " Army")
    
    # Battle 1: Strongest vs Weakest
    print(f"\n🗡️  BATTLE 1: {army3.civilization} vs {army1.civilization}")
    print(f"   {army3.civilization} Strength: {army3.total_strength}")
    print(f"   {army1.civilization} Strength: {army1.total_strength}")
    
    army3.attack(army1)
    
    print(f"   Result: {army3.battle_history[-1].result.value}")
    print(f"   {army3.civilization} Gold: {army3.gold} (+{army3.battle_history[-1].gold_gained})")
    print(f"   {army1.civilization} Units Lost: {army1.battle_history[-1].units_lost}")
    
    # Battle 2: Medium vs Weakened
    print(f"\n🗡️  BATTLE 2: {army2.civilization} vs {army1.civilization}")
    print(f"   {army2.civilization} Strength: {army2.total_strength}")
    print(f"   {army1.civilization} Strength: {army1.total_strength}")
    
    army2.attack(army1)
    
    print(f"   Result: {army2.battle_history[-1].result.value}")
    print(f"   {army2.civilization} Gold: {army2.gold} (+{army2.battle_history[-1].gold_gained})")
    print(f"   {army1.civilization} Units Lost: {army1.battle_history[-1].units_lost}")
    
    # Battle 3: Create a tie scenario
    print(f"\n🗡️  BATTLE 3: Creating a tie scenario...")
    
    # Create two identical armies for a tie
    tie_army1 = Army(Civilization.ENGLISH)
    tie_army2 = Army(Civilization.ENGLISH)
    
    print(f"   Both armies have strength: {tie_army1.total_strength}")
    
    tie_army1.attack(tie_army2)
    
    print(f"   Result: {tie_army1.battle_history[-1].result.value}")
    print(f"   Army 1 Units Lost: {tie_army1.battle_history[-1].units_lost}")
    print(f"   Army 2 Units Lost: {tie_army2.battle_history[-1].units_lost}")
    
    # Display final states
    print("\nFinal army states after battles:")
    display_army_status(army1, army1.civilization.name.title() + " Army")
    display_army_status(army2, army2.civilization.name.title() + " Army")
    display_army_status(army3, army3.civilization.name.title() + " Army")


def demonstrate_battle_history(armies):
    print_separator("BATTLE HISTORY")
    
    for army in armies:
        if army.battle_history:
            print(f"\n{army.civilization.name.title()} Army Battle History:")
            for i, battle in enumerate(army.battle_history, 1):
                print(f"  Battle {i}: {battle}")
        else:
            print(f"\n{army.civilization.name.title()} Army: No battles fought")


def demonstrate_error_handling():
    print_separator("ERROR HANDLING DEMONSTRATION")
    
    army = Army(Civilization.CHINESE)
    
    # Insufficient gold for training
    print("1. Testing insufficient gold for training:")
    army._gold = 5  # Less than pikeman training cost (10)
    pikemen = army.get_units_by_type(Pikeman)
    if pikemen:
        try:
            army.train_unit(pikemen[0])
        except Exception as e:
            print(f"   Expected error: {e}")
    
    # Reset gold
    army._gold = 1000
    
    # Invalid transformation
    print("\n2. Testing invalid transformation:")
    knights = army.get_units_by_type(Knight)
    if knights:
        try:
            army.transform_unit(knights[0])
        except Exception as e:
            print(f"   Expected error: {e}")
    
    # Training unit not in army
    print("\n3. Testing training unit not in army:")
    external_unit = Pikeman()
    try:
        army.train_unit(external_unit)
    except Exception as e:
        print(f"   Expected error: {e}")


def main():
    print("Army Modeling System - Complete Demonstration")
    print("This demonstrates all functionality of the army modeling system.")
    
    # Create armies
    chinese, english, byzantine = demonstrate_army_creation()
    
    # Demonstrate training (using Chinese army)
    demonstrate_training(chinese)
    
    # Demonstrate transformation (using English army)
    demonstrate_transformation(english)
    
    # Demonstrate battles
    demonstrate_battles(chinese, english, byzantine)
    
    # Show battle history
    demonstrate_battle_history([chinese, english, byzantine])
    
    # Demonstrate error handling
    demonstrate_error_handling()
    
    print_separator("DEMONSTRATION COMPLETE")
    print("All army modeling system features have been demonstrated!")
    print("The system successfully models:")
    print("  ✓ Multiple civilizations with different unit compositions")
    print("  ✓ Unit training to increase strength")
    print("  ✓ Unit transformation between types")
    print("  ✓ Battle resolution with proper win/lose/tie logic")
    print("  ✓ Battle history tracking")
    print("  ✓ Gold management")
    print("  ✓ Comprehensive error handling")


if __name__ == "__main__":
    main() 