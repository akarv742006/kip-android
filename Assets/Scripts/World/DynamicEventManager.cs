using System;
using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.World
{
    [Serializable]
    public class WorldEvent
    {
        public string eventId;
        public string titleKey;
        public string fallbackTitle;
        public string descriptionKey;
        public string fallbackDescription;
        public bool isActive;
    }

    public class DynamicEventManager : MonoBehaviour
    {
        public static DynamicEventManager Instance { get; private set; }

        [SerializeField] private List<WorldEvent> worldEvents = new List<WorldEvent>();

        public List<WorldEvent> WorldEvents => worldEvents;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<DynamicEventManager>(this);

            RegisterDefaultEvents();
        }

        private void RegisterDefaultEvents()
        {
            worldEvents.Add(new WorldEvent
            {
                eventId = "evt_water_shortage",
                titleKey = "mission_civic_title",
                fallbackTitle = "Ward Water Shortage",
                descriptionKey = "mission_civic_desc",
                fallbackDescription = "Local water pipeline is broken in Ward 12.",
                isActive = true
            });
        }

        public void SetEventActive(string eventId, bool active)
        {
            WorldEvent evt = worldEvents.Find(e => e.eventId == eventId);
            if (evt != null)
            {
                evt.isActive = active;
                Debug.Log($"[DynamicEventManager] Event '{eventId}' set active: {active}");
            }
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<DynamicEventManager>();
            }
        }
    }
}
