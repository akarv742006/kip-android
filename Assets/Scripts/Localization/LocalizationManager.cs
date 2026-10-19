using System;
using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.Localization
{
    [Serializable]
    public class LocalizationData
    {
        public List<LocalizationEntry> entries = new List<LocalizationEntry>();
    }

    [Serializable]
    public class LocalizationEntry
    {
        public string key;
        public string value;
    }

    public class LocalizationManager : MonoBehaviour
    {
        public static LocalizationManager Instance { get; private set; }

        private readonly Dictionary<string, string> localizedTable = new Dictionary<string, string>();
        private Language currentLanguage = Language.English;

        public Language CurrentLanguage => currentLanguage;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<LocalizationManager>(this);

            LoadLanguage(Language.English);
        }

        public void LoadLanguage(Language language)
        {
            currentLanguage = language;
            string code = language.ToCode();
            string resourcePath = $"Localization/{code}";

            TextAsset jsonFile = Resources.Load<TextAsset>(resourcePath);
            if (jsonFile == null)
            {
                Debug.LogError($"[LocalizationManager] Failed to load resource file: {resourcePath}");
                return;
            }

            localizedTable.Clear();
            try
            {
                LocalizationData data = JsonUtility.FromJson<LocalizationData>(jsonFile.text);
                if (data != null && data.entries != null)
                {
                    foreach (var entry in data.entries)
                    {
                        if (!string.IsNullOrEmpty(entry.key))
                        {
                            localizedTable[entry.key] = entry.value;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Debug.LogError($"[LocalizationManager] Json parse error for {code}: {ex.Message}");
            }

            Debug.Log($"[LocalizationManager] Loaded {localizedTable.Count} strings for {currentLanguage} ({code}).");
            EventBus.Publish(new LanguageChangedEvent(code));
        }

        public string GetString(string key, string fallback = "")
        {
            if (string.IsNullOrEmpty(key)) return fallback;

            if (localizedTable.TryGetValue(key, out string val))
            {
                return val;
            }

            Debug.LogWarning($"[LocalizationManager] Key missing: '{key}' for language {currentLanguage}");
            return string.IsNullOrEmpty(fallback) ? $"[{key}]" : fallback;
        }

        public string GetFormatString(string key, params object[] args)
        {
            string raw = GetString(key);
            try
            {
                return string.Format(raw, args);
            }
            catch (Exception ex)
            {
                Debug.LogError($"[LocalizationManager] Format error for key '{key}': {ex.Message}");
                return raw;
            }
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<LocalizationManager>();
            }
        }
    }
}
