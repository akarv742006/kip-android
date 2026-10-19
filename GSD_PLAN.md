# GSD Execution & Milestone Plan --- Kingmakers of Indian Politics

## Milestone Roadmap

### Phase 1: Foundation & Core Services [COMPLETED]
- [x] Unity C# project structure and assembly definition (`KingmakersOfIndianPolitics`).
- [x] ServiceLocator & EventBus infrastructure for decoupled component communication.
- [x] GameState machine (`MainMenu`, `Exploring`, `InDialogue`, `InCampaignMenu`, `ElectionResults`, `DrivingVehicle`, `Paused`).
- [x] JSON-based bilingual localization system (`en`, `ta`) with runtime switching and event notification.

### Phase 2: Player Movement, Camera & Interactions [COMPLETED]
- [x] Third-person character controller with walk/run mechanics and gravity physics.
- [x] Smooth orbital camera controller with target tracking.
- [x] SphereCast-based interaction detector (`IInteractable` interface).
- [x] Vehicle enter/exit mechanics (`SimpleVehicleController`, `VehicleInteractable`).

### Phase 3: Dialogue, Reputation & Story Flags [COMPLETED]
- [x] Data-driven branching dialogue system using ScriptableObjects (`DialogueData`).
- [x] Independent 5-dimension reputation system (`PublicTrust`, `Integrity`, `Leadership`, `PartyLoyalty`, `MediaImage`).
- [x] Dynamic story flags manager (`bool` and `int` memory flags).

### Phase 4: Campaign, Elections & Government [COMPLETED]
- [x] Multi-factorial election simulator calculating voter turnout, candidate scores, victory margins, and seat rankings.
- [x] Campaign activities manager (`Rally`, `DoorToDoor`, `MediaInterview`) with campaign fund deductions.
- [x] Political role career progression (`Activist` -> `MLA` -> `Minister` -> `Chief Minister`).

### Phase 5: World Simulation & Adaptive Performance [COMPLETED]
- [x] Directional lighting day/night cycle.
- [x] Citizen NPC behaviors and dynamic world events (`DynamicEventManager`).
- [x] Performance-aware adaptive crowd density manager with quality levels (`Low`, `Medium`, `High`).

### Phase 6: Offline Persistence & UI Systems [COMPLETED]
- [x] Versioned JSON local device save/load system (`SaveSystem`, `SaveData`).
- [x] Complete UI suit: HUD, Dialogue UI, Campaign UI, Election Results UI, Settings UI, Pause Menu UI.
