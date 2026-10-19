using System;
using System.IO;
using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;
using Kingmakers.Reputation;
using Kingmakers.Economy;
using Kingmakers.Localization;
using Kingmakers.Party;

namespace Kingmakers.Persistence
{
    public class SaveSystem : MonoBehaviour
    {
        public static SaveSystem Instance { get; private set; }

        private string SaveFilePath => Path.Combine(Application.persistentDataPath, "kingmakers_save.json");

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<SaveSystem>(this);
        }

        public bool SaveGame()
        {
            try
            {
                SaveData data = new SaveData
                {
                    saveVersion = 1,
                    timestamp = DateTime.UtcNow.ToString("o")
                };

                // Position
                var player = GameObject.FindWithTag("Player");
                if (player != null)
                {
                    Vector3 pos = player.transform.position;
                    data.playerPosX = pos.x;
                    data.playerPosY = pos.y;
                    data.playerPosZ = pos.z;
                }

                // Role
                if (ServiceLocator.TryGet<GovernmentSystem>(out var gov))
                {
                    data.currentGovernmentRole = gov.CurrentRole.ToString();
                }

                // Reputation
                if (ServiceLocator.TryGet<ReputationSystem>(out var rep))
                {
                    var repDict = rep.ExportData();
                    foreach (var kvp in repDict)
                    {
                        data.reputationKeys.Add(kvp.Key);
                        data.reputationValues.Add(kvp.Value);
                    }
                }

                // Economy
                if (ServiceLocator.TryGet<EconomyManager>(out var eco))
                {
                    var ecoDict = eco.ExportData();
                    foreach (var kvp in ecoDict)
                    {
                        data.resourceKeys.Add(kvp.Key);
                        data.resourceValues.Add(kvp.Value);
                    }
                }

                // Story Flags
                if (ServiceLocator.TryGet<StoryFlagsManager>(out var flags))
                {
                    data.boolFlagKeys = flags.ExportBoolKeys();
                    data.boolFlagValues = flags.ExportBoolValues();
                    data.intFlagKeys = flags.ExportIntKeys();
                    data.intFlagValues = flags.ExportIntValues();
                }

                // Language
                if (ServiceLocator.TryGet<LocalizationManager>(out var loc))
                {
                    data.currentLanguageCode = loc.CurrentLanguage.ToCode();
                }

                string json = JsonUtility.ToJson(data, true);
                File.WriteAllText(SaveFilePath, json);

                Debug.Log($"[SaveSystem] Saved game successfully to {SaveFilePath}");
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Save game failed: {ex.Message}");
                return false;
            }
        }

        public bool LoadGame()
        {
            if (!HasSaveFile())
            {
                Debug.LogWarning("[SaveSystem] No save file found.");
                return false;
            }

            try
            {
                string json = File.ReadAllText(SaveFilePath);
                SaveData data = JsonUtility.FromJson<SaveData>(json);

                if (data == null) return false;

                // Position
                var player = GameObject.FindWithTag("Player");
                if (player != null)
                {
                    player.transform.position = new Vector3(data.playerPosX, data.playerPosY, data.playerPosZ);
                }

                // Role
                if (ServiceLocator.TryGet<GovernmentSystem>(out var gov))
                {
                    if (Enum.TryParse<GovernmentRole>(data.currentGovernmentRole, out var role))
                    {
                        gov.SetRoleDirect(role);
                    }
                }

                // Reputation
                if (ServiceLocator.TryGet<ReputationSystem>(out var rep))
                {
                    var repDict = new Dictionary<string, int>();
                    for (int i = 0; i < Math.Min(data.reputationKeys.Count, data.reputationValues.Count); i++)
                    {
                        repDict[data.reputationKeys[i]] = data.reputationValues[i];
                    }
                    rep.ImportData(repDict);
                }

                // Economy
                if (ServiceLocator.TryGet<EconomyManager>(out var eco))
                {
                    var ecoDict = new Dictionary<string, long>();
                    for (int i = 0; i < Math.Min(data.resourceKeys.Count, data.resourceValues.Count); i++)
                    {
                        ecoDict[data.resourceKeys[i]] = data.resourceValues[i];
                    }
                    eco.ImportData(ecoDict);
                }

                // Story Flags
                if (ServiceLocator.TryGet<StoryFlagsManager>(out var flags))
                {
                    flags.ImportFlags(data.boolFlagKeys, data.boolFlagValues, data.intFlagKeys, data.intFlagValues);
                }

                // Language
                if (ServiceLocator.TryGet<LocalizationManager>(out var loc))
                {
                    loc.LoadLanguage(LanguageExtensions.FromCode(data.currentLanguageCode));
                }

                Debug.Log("[SaveSystem] Loaded game state successfully.");
                return true;
            }
            catch (Exception ex)
            {
                Debug.LogError($"[SaveSystem] Load game failed: {ex.Message}");
                return false;
            }
        }

        public bool HasSaveFile()
        {
            return File.Exists(SaveFilePath);
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<SaveSystem>();
            }
        }
    }
}
