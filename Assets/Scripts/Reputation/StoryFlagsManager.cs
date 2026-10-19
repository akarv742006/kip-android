using System;
using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.Reputation
{
    public class StoryFlagsManager : MonoBehaviour
    {
        public static StoryFlagsManager Instance { get; private set; }

        private readonly Dictionary<string, bool> boolFlags = new Dictionary<string, bool>();
        private readonly Dictionary<string, int> intFlags = new Dictionary<string, int>();

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<StoryFlagsManager>(this);
        }

        public void SetFlag(string flagName, bool value)
        {
            if (string.IsNullOrEmpty(flagName)) return;
            boolFlags[flagName] = value;
            Debug.Log($"[StoryFlagsManager] Flag '{flagName}' set to {value}");
        }

        public bool GetFlag(string flagName, bool defaultValue = false)
        {
            return boolFlags.TryGetValue(flagName, out bool val) ? val : defaultValue;
        }

        public void SetIntFlag(string flagName, int value)
        {
            if (string.IsNullOrEmpty(flagName)) return;
            intFlags[flagName] = value;
            Debug.Log($"[StoryFlagsManager] IntFlag '{flagName}' set to {value}");
        }

        public int GetIntFlag(string flagName, int defaultValue = 0)
        {
            return intFlags.TryGetValue(flagName, out int val) ? val : defaultValue;
        }

        public List<string> ExportBoolKeys() => new List<string>(boolFlags.Keys);
        public List<bool> ExportBoolValues() => new List<bool>(boolFlags.Values);

        public List<string> ExportIntKeys() => new List<string>(intFlags.Keys);
        public List<int> ExportIntValues() => new List<int>(intFlags.Values);

        public void ImportFlags(List<string> bKeys, List<bool> bVals, List<string> iKeys, List<int> iVals)
        {
            boolFlags.Clear();
            intFlags.Clear();

            if (bKeys != null && bVals != null)
            {
                for (int i = 0; i < Math.Min(bKeys.Count, bVals.Count); i++)
                {
                    boolFlags[bKeys[i]] = bVals[i];
                }
            }

            if (iKeys != null && iVals != null)
            {
                for (int i = 0; i < Math.Min(iKeys.Count, iVals.Count); i++)
                {
                    intFlags[iKeys[i]] = iVals[i];
                }
            }
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<StoryFlagsManager>();
            }
        }
    }
}
