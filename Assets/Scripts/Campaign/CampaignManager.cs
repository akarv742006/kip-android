using System;
using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;
using Kingmakers.Economy;
using Kingmakers.Reputation;

namespace Kingmakers.Campaign
{
    public class CampaignManager : MonoBehaviour
    {
        public static CampaignManager Instance { get; private set; }

        [SerializeField] private ConstituencyData activeConstituency;

        public ConstituencyData ActiveConstituency => activeConstituency;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<CampaignManager>(this);

            InitializeDefaultConstituency();
        }

        private void InitializeDefaultConstituency()
        {
            activeConstituency = new ConstituencyData
            {
                constituencyId = "TN-101",
                constituencyName = "Chennai Central Assembly Ward",
                totalRegisteredVoters = 120000,
                baseExpectedTurnoutPercent = 72.0f,
                candidates = new List<CandidateData>
                {
                    new CandidateData
                    {
                        id = "cand_player",
                        name = "Player Activist",
                        partyId = "party_prm",
                        partyName = "People's Rights Movement",
                        isPlayer = true,
                        basePopularity = 50f,
                        campaignEffort = 30f,
                        promiseFulfillmentScore = 60f,
                        mediaImageScore = 50f
                    },
                    new CandidateData
                    {
                        id = "cand_rival",
                        name = "K. Ramanathan",
                        partyId = "party_ndp",
                        partyName = "National Democratic Progressive",
                        isPlayer = false,
                        basePopularity = 55f,
                        campaignEffort = 45f,
                        promiseFulfillmentScore = 40f,
                        mediaImageScore = 60f
                    }
                }
            };
        }

        public bool ExecuteCampaignActivity(CampaignActivity activity)
        {
            if (activity == null) return false;

            if (!ServiceLocator.TryGet<EconomyManager>(out var eco) || !eco.CanAfford(ResourceCategory.CampaignFunds, activity.costInFunds))
            {
                Debug.LogWarning("[CampaignManager] Cannot execute activity: Insufficient Campaign Funds.");
                return false;
            }

            eco.Spend(ResourceCategory.CampaignFunds, activity.costInFunds);

            CandidateData playerCand = activeConstituency.candidates.Find(c => c.isPlayer);
            if (playerCand != null)
            {
                playerCand.campaignEffort = Mathf.Clamp(playerCand.campaignEffort + activity.popularityGain, 0f, 100f);
            }

            if (ServiceLocator.TryGet<ReputationSystem>(out var rep))
            {
                if (activity.publicTrustGain != 0) rep.Modify(ReputationType.PublicTrust, activity.publicTrustGain);
                if (activity.mediaImageGain != 0) rep.Modify(ReputationType.MediaImage, activity.mediaImageGain);
            }

            Debug.Log($"[CampaignManager] Executed {activity.type}! Player campaign effort now {playerCand?.campaignEffort}");
            return true;
        }

        public ElectionResult RunElection()
        {
            if (!ServiceLocator.TryGet<ElectionSimulator>(out var sim))
            {
                Debug.LogError("[CampaignManager] ElectionSimulator not found!");
                return null;
            }

            ElectionResult result = sim.SimulateElection(activeConstituency);
            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.SetGameState(GameState.ElectionResults);
            }
            return result;
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<CampaignManager>();
            }
        }
    }
}
