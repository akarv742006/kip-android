# SPEC.md --- Baseline Specification

**Status:** APPROVED BASELINE  
**Version:** 0.1  
**Platform Target:** Android  
**Engine:** Unity (C#)  
**Primary Mode:** Offline, single-player, third-person 3D political career simulator  
**Languages:** Tamil and English  

---

## 1. Product Vision
*Kingmakers of Indian Politics* is a fictional, open-world political career simulator set in a Tamil Nadu-inspired region, with a path into national politics. The player begins as a middle-class community activist solving local civic problems and can gradually become a party leader, MLA, state minister, Chief Minister, MP, Union Minister, Prime Minister, or party founder/president.

### Core Product Principles
1. **Player Agency:** Choices change relationships, reputation, story branches, and election conditions.
2. **Career Continuity:** Losing an election or making a mistake does not force a game over.
3. **Simulation-Driven Politics:** Votes and approval are driven by multi-factorial calculations.
4. **Open-World Presence:** Key interactions happen in the 3D world, backed by strategy menus.
5. **Offline-First:** Core gameplay and saves require no internet connection.
6. **Mobile Performance:** Adaptive crowd and rendering performance for mid-to-low Android hardware.
7. **Bilingual Accessibility:** Native support for Tamil and English.

---

## 2. Target Platform & Audience
- **Target OS:** Android
- **Graphics & View:** Realistic 3D environment, Third-person camera
- **Languages:** Tamil (`ta`) and English (`en`) with runtime switching
- **Scope:** Solo-developer modular architecture, offline single-player vertical slice first.

---

## 3. Core Systems Summary
1. **Movement & Camera:** Third-person character controller, vehicle interactables.
2. **Dialogue & Story:** Choice-based branching dialogue with condition evaluation and flag setting.
3. **Reputation Engine:** 5 dimensions (Public Trust, Integrity, Leadership, Party Loyalty, Media Image).
4. **Campaign & Election Simulation:** Demographic weightings, campaign effort, promise fulfillment, dynamic turnout, result breakdown.
5. **Economy:** Separation of Personal Money, Campaign Funds, Party Resources, and Political Influence.
6. **Localization:** Key-based lookup system supporting Tamil and English string tables.
7. **Offline Persistence:** Versioned JSON save state covering career progression and world flags.
