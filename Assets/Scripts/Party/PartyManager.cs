using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.Party
{
    public class PartyManager : MonoBehaviour
    {
        public static PartyManager Instance { get; private set; }

        [SerializeField] private List<PartyData> registeredParties = new List<PartyData>();

        public List<PartyData> RegisteredParties => registeredParties;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<PartyManager>(this);
        }

        public PartyData GetPartyById(string partyId)
        {
            return registeredParties.Find(p => p.partyId == partyId);
        }

        public PartyData GetPlayerParty()
        {
            return registeredParties.Find(p => p.isPlayerParty);
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<PartyManager>();
            }
        }
    }
}
