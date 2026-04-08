




Academic Life and Career Simulation Game


# Change History

           Date	                      Description	
	2026-03-10	Project initialization and requirements analysis	
    2026-03-25	Core game engine and player mechanics developed	 
	2026-04-02	Academic logic and JSON persistence integration	
	2026-04-08	Final architectural review and UML diagramming	 

## Table of Contents and List of Figures

Figure 1: Class Diagram (Section 5)

Figure 2: State Machine Diagram (Section 6)

Figure 3: Sequence Diagram (Section 6)

Figure 4: Component Diagram (Section 7)

Figure 5: Deployment Diagram (Section 8)

Figure 6: Use Case Diagram (Section 9)

## 1. Scope

This document outlines the architectural design of the Academic Life and Career Simulation Game. The goal of this project is to simulate a student's journey through university, balancing academic success, social life, and financial management. This report serves as a technical roadmap for understanding how the system is structured and how different components interact.

## 2. References

Kruchten, P. (1995). Architectural Blueprints—The “4+1” View Model of Software Architecture. IEEE Software, 12(6), 42-50. 

Pygame Association. Pygame Library Documentation (v2.x). Retrieved from https://www.pygame.org/docs/.

Python Software Foundation. JSON encoder and decoder documentation. Retrieved from https://docs.python.org/3/library/json.html.

UML Specification. Unified Modeling Language (UML) Resource Page. Object Management Group (OMG). https://www.uml.org/.

## 3. Software Architecture

To provide a clear and structured view of the system, we have adopted the 4+1 View Model proposed by Philippe Kruchten. This model allows us to describe the architecture through multiple concurrent views:

Logical View: Focuses on the object-oriented design (Class Diagrams).

Process View: Describes the dynamic behavior and synchronization (State & Sequence Diagrams).

Development View: Illustrates the software's static organization (Component Diagrams).

Physical View: Shows the deployment and hardware mapping (Deployment Diagrams).

Scenarios (+1): Ties the architecture together using use cases (Use Case Diagrams).

## 4. Architectural Goals & Constraints

The design is guided by several key objectives:

Modularity: Ensuring that the game logic (GPA calculation, exam systems) is separate from the rendering engine (Pygame).

Lightweight Persistence: Using JSON to store player data without the overhead of a full SQL database.

Platform Independence: Running as a standalone Python application on any desktop environment.

Constraint: The system must run locally and handle state transitions (Roaming to Quiz) without losing data.

## 5. Logical Architecture

![Class Diagram](class%20diagram.jpg)

The class diagram illustrates the internal structure of the system in more detail. The `Game` class acts as the core controller, coordinating all major components such as player management, quests, dialogues, and game progression.

The `Player` class represents the main character controlled by the user and stores attributes such as position, inventory, and movement.

The `Quiz` class manages the exam system, including question handling and scoring. It retrieves its data from the external `EXAM_BANK`, which is modeled as a dependency rather than a class.

The `StoryUI` class is responsible for presenting narrative elements and managing story progression, allowing interaction with the user interface.

The `DialogueBox` class handles communication between the player and NPCs, displaying dialogues retrieved from the `NPC_DIALOGUES` data source.

The `Building` class represents different locations in the game environment, enabling interactions such as attending classes or working.

The `EffectText` class provides visual feedback to the player, such as notifications about changes in game state.

External elements like `SaveData`, `QUESTS`, `EXAM_BANK`, and `NPC_DIALOGUES` are modeled as data sources and are connected via dependency relationships, since they provide data rather than behavior.

This design follows object-oriented principles such as separation of concerns and low coupling, ensuring that each component has a clear responsibility and can be maintained independently.

The relationships between classes are primarily composition-based, with the `Game` class aggregating and managing most system components, ensuring centralized control of the simulation.
## 6. Process Architecture

![State Machine Diagram](state%20machine%20diagram.png)
![Sequence Diagram](sequence%20diagram.jpg)

The simulation's runtime behavior is managed by a Finite State Machine (FSM) pattern. This architecture ensures that player movement and game-world updates are synchronized with user interactions.

State Control: The Game.update() loop checks boolean flags such as quiz.active, show_quests, and show_rels to determine which logic branch to execute.

Input Handling: When transitioning to the Interaction State, the standard movement input is suspended to allow the Quiz.answer() method to capture numeric keys for exam responses.

Time Management: The advance_time() process runs as a background service that updates the simulation clock and triggers state-dependent events like "New Day" or "Exam Results".

The sequence diagram represents the interaction flow during an exam scenario in the game.

The process starts when the player presses the interaction key (E). This input is captured by the main loop, which then calls the `interact()` method in the `Game` class.

If the condition `exam_ready == true` is satisfied, the `Game` class initiates the exam process by calling the `start(subject)` method of the `Quiz` class.

The `Quiz` class initializes the exam by selecting a set of questions from the `EXAM_BANK` data source and setting the state to "exam started".

A loop structure is then executed for each question. During this loop, the player submits answers by pressing input keys (1, 2, or 3). Each input is sent to the `Quiz` class through the `answer(choice)` method, where it is processed and evaluated.

After all questions are answered, the `Quiz` class calculates the final score and returns it to the `Game` class.

The `Game` class then handles the result using the `handle_quiz_result(score)` method, updating player statistics such as GPA and other attributes. It also updates the UI by displaying the result through a message system.

Throughout the process, the system maintains a clear control flow where the `Game` class acts as the central coordinator, ensuring that all interactions between components are properly managed.

This sequence demonstrates how user input is transformed into game logic execution and state updates in a structured and modular way.
## 7. Development Architecture

![Component Diagram](component%20diagram.png)

The component diagram visualizes how these modules are organized and interact within the system.
The system is built using a modular component-based architecture to separate game-state management from graphical rendering.

Core Module: Handles the event loop and state transitions.

Logic Module: Encapsulates the academic success formulas and student stat calculations.

External Dependencies: Utilizes the Pygame library for hardware abstraction (input/output) and the JSON module for data serialization.

The development architecture describes how the system is organized from a software engineering perspective.

The project is implemented in Python using the Pygame library. The codebase is structured into modular components, each responsible for a specific functionality such as game logic, UI rendering, and interaction handling.

The main entry point of the system is the `main.py` file, which initializes the game and runs the main loop. The `Game` class serves as the core module, managing state transitions and coordinating all other components.

Different classes such as `Player`, `Quiz`, `DialogueBox`, and `StoryUI` are separated into logical units to improve readability and maintainability.

Version control is managed using Git and hosted on GitHub. The development process follows a feature-branch workflow, where new features are implemented in separate branches and merged via pull requests.

This modular and layered structure ensures that the system is easy to extend, test, and maintain.
## 8. Physical Architecture

![Deployment Diagram](deployment%20diagram.png)

The simulation is designed as a standalone desktop application, ensuring a zero-dependency environment for the end-user.

Hardware Layer: The application executes on the client’s local CPU, utilizing standard system resources for rendering and logic processing.

Storage Layer: All persistence data is handled locally via the campus_life_save.json file. There are no external cloud requirements or database servers, making the application fully portable.

Deployment: The software is delivered as a Python-based executable or script, requiring only a compatible Python runtime and the Pygame library on the host machine.

The application runs locally on a single machine and does not require any server-side components. All game logic, rendering, and data processing are executed within a single runtime environment.

The system is developed using Python and the Pygame library, making it compatible with multiple operating systems such as Windows, macOS, and Linux.

Game data, including exam questions, NPC dialogues, and save files, are stored locally using JSON files. This allows easy data management and persistence.

This architecture ensures simplicity, portability, and ease of deployment.

## 9. Scenarios

![Use Case Diagram](use%20case%20diagram.png)

This view illustrates the core functionalities available to the user within the simulation environment.

Academic Journey: The player interacts with the school to take exams, where outcomes are determined by intelligence and study hours.

Resource Balancing: Players must perform daily actions to balance Intelligence, Energy, and Money to avoid simulation failure.

Persistence and Progress: The system supports saving and loading player statistics via a local JSON-based data management system.

## 10. Size and Performance

Memory Footprint: The application is lightweight, primarily using standard Python libraries and Pygame. It is designed to run efficiently on low-end hardware with minimal RAM usage.

Execution Speed: The game loop is capped at 60 FPS to ensure smooth UI transitions and consistent timing for the success algorithms.

Storage Size: The local data storage (JSON) is extremely compact, typically requiring less than 100 KB for full game state persistence.

## 11. Quality

Reliability: The state-machine architecture prevents logic errors by ensuring only one major interaction state is active at a time.

Maintainability: The use of object-oriented principles (classes for Players, NPCs, and Buildings) allows for easy expansion of game content without altering core engine logic.

Usability: The menu-based system provides a low learning curve, allowing players to focus on the decision-making aspect of the simulation.

## Appendices

### Acronyms and Abbreviations

GPA: Grade Point Average 

FSM: Finite State Machine 

UI: User Interface 

NPC: Non-Player Character 

UML: Unified Modeling Language

JSON: JavaScript Object Notation

### Definitions

Academic Simulation: A digital environment designed to replicate the essential processes of university life, including course attendance, examination systems, and personal resource management (budget, energy, etc.).

State Transition: The process by which the system switches from one operational mode (e.g., Roaming/Exploration) to another (e.g., Quiz Mode or Dialogue Interface) based on specific user triggers or game events.

Persistence: The capability of the system to store game-state data (player statistics, progress, and inventory) in local non-volatile storage, ensuring that information is retained even after the application is closed.

Orchestrator Class: A central design pattern where a single class (the Game class in this project) manages the instantiation, communication, and synchronization of all other subordinate entities and modules within the system.


### Design Principles

KISS (Keep It Simple, Stupid): Instead of complex and over-engineered systems, a manageable and modular structure was preferred. The development focused strictly on core mechanics (lectures, exams, and statistics) to avoid unnecessary feature bloat.

Encapsulation: Adhering to Object-Oriented Programming (OOP) principles, each class (Player, NPC, Building) manages its own internal data. For instance, the player's energy and intelligence levels are modified only through specific class methods, protecting the data from external interference.

Separation of Concerns (SoC): The graphical rendering logic (Pygame) and the academic success calculation logic (Success Algorithm) are decoupled. This ensures that changes made to the user interface do not affect the underlying game mechanics or vice versa.

DRY (Don't Repeat Yourself): To ensure a clean and sustainable codebase, repetitive code blocks were replaced with reusable functions and class methods, reducing redundancy and making the system easier to debug.
