# Army Definition (army-definition-py)

**Army Definition** is a Python project that models armies from different civilizations and simulates their behavior.  Each Army consists of units (Pikemen, Archers, Knights) with varying strengths and costs.  The system supports features like training units to increase their strength, transforming units between types, and resolving battles between armies.  The code was developed as an exercise in clean object-oriented design and is accompanied by example usage and unit tests.

## Features

- **Multiple Civilizations:** Armies are based on different civilizations (e.g. Chinese, English, Byzantine) with configurable unit compositions.
- **Unit Classes:** Implements `Pikeman`, `Archer`, and `Knight` unit types, each with its own strength and cost parameters.
- **Army Management:** Create and manage an `Army` object, track its units, total strength, gold reserves, and battle history.
- **Training Units:** Train individual units or all units of a given type. Training increases a unit’s strength at the cost of army gold.
- **Transforming Units:** Transform units to a higher class (e.g. Pikeman → Archer → Knight) with an associated cost.
- **Battle Resolution:** Simulate battles between two armies using a `BattleSystem`, yielding results (win, lose, tie) and recording battle outcomes.
- **Battle History:** Each Army keeps a history of battles fought, allowing analysis of past engagements.
- **Error Handling:** The system raises clear exceptions for invalid operations (e.g. insufficient gold or units), which the example script demonstrates.

## Technologies Used

- **Python 3.13.1:** The project is written in Python  3.13.1 and makes use of Python’s `typing` for clarity.
- **Built-in Libraries:** Uses standard libraries – no external dependencies are required.
- **Testing:** Includes unit tests for each module (Army, Battle, Units, Civilizations) to ensure correctness.

## Installation and Setup

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/diazjoaquin/army-definition-py.git
   cd army-definition-py
   ```

2. **Create virtual environment**
   
   On windows:
   
    ```bash
     python -m venv venv
     ./venv/Scripts/Activate
     ```
3. **Install the requirements**
   
   Python Version used: 3.13.1
   
   ```bash
   pip install -r requirements.txt
   ```

6. **Usage example**
7. 
   You can run the provided example script to see the system in action. From the project root directory.
   
   ```bash
   python example_usage.py
   ```
   
   This script will:
   - Create sample armies for different civilizations.
   - Display their initial unit counts, total strength, and gold.
   - Demonstrate training units (upgrading a unit’s strength).
   - Demonstrate transforming units between types.
   - Simulate several battles between the armies.
   - Print out battle results and the updated battle history.
   - Show error handling by attempting an invalid operation.
   - You should see output detailing each step (as illustrated in the example script). The code in example_usage.py shows how to call the key classes and methods (see code comments for guidance).

9. **Running Tests**
The repository includes unit tests to verify functionality. To run the tests:
```bash
   python -m pytest tests/ -v
```

This will run all tests in the tests/ directory (for Army, units, battle logic, etc.). All tests should pass if the system is working correctly.
