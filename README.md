# Kingmakers of Indian Politics

*Kingmakers of Indian Politics* is an offline, single-player third-person 3D political career simulator set in a fictional Tamil Nadu-inspired region, built for Android using Unity (C#).

---

## 🌟 Key Features

- **3D Open World & Career Simulator:** Start as a middle-class activist and advance through local elections, ministerial portfolios, state leadership, and national office.
- **Multi-Factorial Election Engine:** Calculates election turnout and candidate support using public trust, integrity, media image, campaign effort, promise fulfillment, and demographic issue weightings.
- **Choice-Driven Dialogue & Branching Story:** Choice-based dialogue trees with condition checking, reputation adjustments, and story flags persistent across the player's career.
- **Independent Reputation System:** Tracks 5 distinct political dimensions (Public Trust, Integrity, Leadership, Party Loyalty, Media Image) rather than a single popularity score.
- **Resource Economy:** Strict separation between Personal Money, Campaign Funds, Party Resources, and Political Influence.
- **Bilingual Localization (Tamil & English):** Runtime language toggling for UI, dialogue, and campaign notifications with Tamil (`ta`) and English (`en`) JSON tables.
- **Offline Save / Load System:** Versioned JSON local device save system preserving position, reputation, economy, story flags, and government role.
- **Mobile Performance Adaptation:** Adaptive crowd density manager scaling NPC loads across Low, Medium, and High Android performance profiles.

---

## 🏗️ Project Architecture

```
Assets/
├── Scripts/
│   ├── Core/               # GameManager, GameState, ServiceLocator, EventBus
│   ├── Player/             # PlayerController, ThirdPersonCamera, PlayerStats, InteractionDetector
│   ├── Dialogue/           # DialogueManager, DialogueData, DialogueNode, DialogueOption
│   ├── Reputation/         # ReputationSystem, ReputationType, StoryFlagsManager
│   ├── Economy/            # EconomyManager, ResourceCategory
│   ├── Campaign/           # ElectionSimulator, CampaignManager, CandidateData, ConstituencyData
│   ├── Party/              # PartyManager, PartyData, GovernmentSystem
│   ├── Vehicles/           # SimpleVehicleController, VehicleInteractable
│   ├── World/              # DayNightCycle, CitizenNPC, DynamicEventManager, AdaptiveCrowdManager
│   ├── Localization/       # LocalizationManager, LocalizedText, Language
│   ├── Persistence/        # SaveSystem, SaveData
│   └── UI/                 # UIManager, HUDUI, DialogueUI, CampaignUI, ElectionResultsUI, SettingsUI, PauseMenuUI
└── Resources/
    └── Localization/
        ├── en.json         # English string dictionary
        └── ta.json         # Tamil string dictionary
```

---

## 📱 Android Setup & Build Instructions

1. **Unity Version:** Unity 2022.3 LTS or Unity 2023.2 LTS recommended.
2. **Modules Required:** Android Build Support (IL2CPP / ARM64), NDK, Android SDK & JDK.
3. **Open Project:** In Unity Hub, choose **Add project from disk** and select `E:/kip android`.
4. **Build Settings:**
   - Platform: **Android**
   - Scripting Backend: **IL2CPP**
   - Target Architectures: **ARM64**
   - Minimum API Level: **Android 8.0 (API level 26)**
5. **Build APK:** Click **Build and Run** or **Build APK**.
