using System;
using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.Economy
{
    public class EconomyManager : MonoBehaviour
    {
        public static EconomyManager Instance { get; private set; }

        private readonly Dictionary<ResourceCategory, long> balances = new Dictionary<ResourceCategory, long>();

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<EconomyManager>(this);

            ResetBalances();
        }

        public void ResetBalances()
        {
            balances[ResourceCategory.PersonalMoney] = 25000;      // 25,000 INR starting
            balances[ResourceCategory.CampaignFunds] = 100000;    // 100,000 INR
            balances[ResourceCategory.PartyResources] = 50;       // Volunteer capacity / units
            balances[ResourceCategory.PoliticalInfluence] = 10;   // Starting leverage
        }

        public long GetBalance(ResourceCategory category)
        {
            return balances.TryGetValue(category, out long val) ? val : 0;
        }

        public bool CanAfford(ResourceCategory category, long amount)
        {
            return GetBalance(category) >= amount;
        }

        public bool Spend(ResourceCategory category, long amount)
        {
            if (amount <= 0) return true;
            long current = GetBalance(category);
            if (current < amount)
            {
                Debug.LogWarning($"[EconomyManager] Insufficient {category}: Needs {amount}, Has {current}");
                return false;
            }

            balances[category] = current - amount;
            EventBus.Publish(new ResourceChangedEvent(category.ToString(), balances[category], -amount));
            return true;
        }

        public void Add(ResourceCategory category, long amount)
        {
            if (amount <= 0) return;
            long current = GetBalance(category);
            balances[category] = current + amount;
            EventBus.Publish(new ResourceChangedEvent(category.ToString(), balances[category], amount));
        }

        public Dictionary<string, long> ExportData()
        {
            var dict = new Dictionary<string, long>();
            foreach (var kvp in balances)
            {
                dict[kvp.Key.ToString()] = kvp.Value;
            }
            return dict;
        }

        public void ImportData(Dictionary<string, long> data)
        {
            if (data == null) return;
            foreach (var kvp in data)
            {
                if (Enum.TryParse<ResourceCategory>(kvp.Key, out var cat))
                {
                    balances[cat] = kvp.Value;
                }
            }
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<EconomyManager>();
            }
        }
    }
}
