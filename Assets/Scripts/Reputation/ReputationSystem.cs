using System;
using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.Reputation
{
    public class ReputationSystem : MonoBehaviour
    {
        public static ReputationSystem Instance { get; private set; }

        private readonly Dictionary<ReputationType, int> reputationValues = new Dictionary<ReputationType, int>();

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<ReputationSystem>(this);

            ResetReputation();
        }

        public void ResetReputation()
        {
            reputationValues[ReputationType.PublicTrust] = 50;
            reputationValues[ReputationType.Integrity] = 50;
            reputationValues[ReputationType.Leadership] = 40;
            reputationValues[ReputationType.PartyLoyalty] = 50;
            reputationValues[ReputationType.MediaImage] = 50;
        }

        public int Get(ReputationType type)
        {
            return reputationValues.TryGetValue(type, out int val) ? val : 50;
        }

        public void Modify(ReputationType type, int delta)
        {
            int current = Get(type);
            int updated = Mathf.Clamp(current + delta, 0, 100);
            reputationValues[type] = updated;

            Debug.Log($"[ReputationSystem] {type} adjusted by {delta}. New value: {updated}");
            EventBus.Publish(new ReputationChangedEvent(type.ToString(), updated, delta));
        }

        public Dictionary<string, int> ExportData()
        {
            var dict = new Dictionary<string, int>();
            foreach (var kvp in reputationValues)
            {
                dict[kvp.Key.ToString()] = kvp.Value;
            }
            return dict;
        }

        public void ImportData(Dictionary<string, int> data)
        {
            if (data == null) return;
            foreach (var kvp in data)
            {
                if (Enum.TryParse<ReputationType>(kvp.Key, out var type))
                {
                    reputationValues[type] = Mathf.Clamp(kvp.Value, 0, 100);
                }
            }
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<ReputationSystem>();
            }
        }
    }
}
