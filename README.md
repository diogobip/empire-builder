# empire-builder

## Project Technical Overview: Empire Simulation

This project is a turn-based strategy simulation designed with an object-oriented foundation and modular logic.

## 1. Core Architecture & Paradigms

* **Object-Oriented Programming (OOP):** The codebase utilizes **classes** (`Army`, `UnitType`, `Buildings`, `Economy`) to encapsulate data and state[cite: 5, 6, 7]. Each class instance acts as an object-container, allowing for efficient management of game entities like units and structures[cite: 5, 6, 7].

* **Data-Driven Design:** The project relies heavily on **dictionaries** for storing game state (e.g., `my_army.units`, `economy.resources`)[cite: 5, 7]. Dictionaries provide efficient key-value mapping for resources and unit counts, allowing for dynamic updates without hard-coding individual variables[cite: 5, 7].

## 2. Control Flow & Logic

* **Main Game Loop:** The engine operates via a **`while True:` infinite loop**, which governs turn progression, input collection, and the invocation of global game-state functions[cite: 8].

* **Modular Functionality:** The main file (`empire.py`) currently serves as a central controller, employing **if/elif/else conditional logic** to parse user input and route it to specific functions (e.g., `apply_job`, `save_game`)[cite: 8].

* **Iterative Processing:** **`for` loops** are used to traverse collections—specifically iterating over dictionary items (e.g., `my_army.units.items()`) to calculate total combat power or display status updates[cite: 5, 8].

## 3. State Management & Persistence

* **Serialization:** The project utilizes the `json` module to bridge the gap between volatile memory and persistent storage[cite: 8, 9].
  * **`json.dump`**: Encodes the game state (variables and objects) into a formatted JSON string for saving[cite: 8, 9].
  * **`json.load`**: Parses the JSON file back into Python-readable data structures for session restoration[cite: 8, 9].

* **Encapsulation:** By wrapping the `resources` dictionary within an `Economy` class, the architecture allows for safer state modification through dedicated methods rather than global variable manipulation[cite: 7].
