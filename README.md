# SWE332-Academic-Life-and-Career-Simulation-Game
SWE332 Software Architecture Project - Academic Life Simulation Game

## Team Details
* İlayda Acarlar – 220513350 – GitHub: [@acarlarilayda](https://github.com/acarlarilayda)
* Renas Karabulut – 230513334 – GitHub: [@RenasKarabulut](https://github.com/RenasKarabulut)
* Ebrar Sena Kılıçkaya – 220513367 – GitHub: [@ebrarkilicikaya](https://github.com/ebrarkilicikaya)
  
## Project Introduction

Academic Life and Career Simulation Game is a 2D campus-life simulation developed in Python using Pygame.
The game represents the daily life of a university student and allows the player to manage academic, social, and financial responsibilities.

The player can move around the campus, interact with buildings and NPCs, take exams, study, work, rest, improve relationships, and complete quests.
The main purpose of the project is to simulate the balance between GPA, intelligence, energy, money, and social interaction in student life.

## Architecture Overview

This project follows the 4+1 architectural view model:
- Logical View: Class diagram representing system structure
- Process View: Sequence diagrams showing runtime behavior
- Development View: GitHub-based modular development
- Physical View: Deployment diagram of the system
- Scenarios: Use case and state machine diagrams
  
## Main Features

* 2D campus world exploration
* Player movement and interaction system
* Buildings with different purposes:

  * Home
  * School
  * Work
  * Cafe
  * Library
* Exam / quiz system
* Quest tracking system
* NPC interaction and dialogue system
* Relationship/friendship system
* Inventory and gift system
* Save / load system
* Auto-save support
* UI panels for quests, dialogue, and relationships

## Technologies Used

* Python
* Pygame
* JSON for save data
* Draw.io for UML diagrams
* GitHub for version control and collaboration

## How to Run

1. Make sure Python 3 is installed.
2. Install Pygame:

   ```bash
   pip install pygame
   ```
3. Download or clone the repository.
4. Run the game:

   ```bash
   python main.py
   ```

## Controls

* W / A / S / D or Arrow Keys → Move
* E → Interact
* ENTER → Continue dialogue
* TAB → Open/close quests
* Q → Open/close relationships
* G → Give gift
* F5 → Save
* F9 → Load

## Project Structure

* main.py → Main game logic and gameplay systems
* README.md → General project overview
* ARCHITECTURE.md → Detailed software architecture report
* class diagram.png → Logical architecture / class structure
* sequence diagram.jpg → Scenario flow
* component diagram.png → Major components of the system
* deployment diagram.png → Physical/deployment view
* state machine diagram.png → Player/game state transitions
* use case diagram.png → Main user interactions

## Architecture Link

See the architecture document here:
[Architecture Document](ARCHITECTURE.md)

## Contribution Summary

Each team member contributed through GitHub commits using feature branches and pull requests.
The project includes both technical development and architectural documentation contributions.

## Individual Contributions

- İlayda Acarlar:
  Implemented game logic, save/load system, and quest tracking system.

- Renas Karabulut:
  Developed core gameplay mechanics, NPC system, and player interactions.

- Ebrar Sena Kılıçkaya:
  Designed UI/UX elements, including dashboard, panels, and interface components.

## Course Requirement Note

This repository is public and prepared according to the SWE332 Software Architecture Project requirements, including Markdown documentation, a public GitHub repository, and visible team contributions in git history.
