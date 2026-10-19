using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Reputation;
using Kingmakers.Core;

namespace Kingmakers.Campaign
{
    [System.Serializable]
    public class ElectionResult
    {
        public string constituencyName;
        public int totalVotesCast;
        public float turnoutPercent;
        public CandidateData winner;
        public int victoryMarginVotes;
        public List<CandidateData> rankedCandidates = new List<CandidateData>();
    }

    public class ElectionSimulator : MonoBehaviour
    {
        public static ElectionSimulator Instance { get; private set; }

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<ElectionSimulator>(this);
        }

        public ElectionResult SimulateElection(ConstituencyData constituency)
        {
            if (constituency == null || constituency.candidates == null || constituency.candidates.Count == 0)
            {
                Debug.LogError("[ElectionSimulator] Cannot simulate election without constituency candidates!");
                return null;
            }

            // Sync Player candidate score with player reputation
            if (ServiceLocator.TryGet<ReputationSystem>(out var repSys))
            {
                foreach (var candidate in constituency.candidates)
                {
                    if (candidate.isPlayer)
                    {
                        int trust = repSys.Get(ReputationType.PublicTrust);
                        int integrity = repSys.Get(ReputationType.Integrity);
                        int media = repSys.Get(ReputationType.MediaImage);

                        candidate.basePopularity = (trust * 0.4f) + (integrity * 0.3f) + (media * 0.3f);
                    }
                }
            }

            // Calculate Turnout
            float noiseTurnout = UnityEngine.Random.Range(-2.0f, 2.0f);
            float finalTurnoutPct = Mathf.Clamp(constituency.baseExpectedTurnoutPercent + noiseTurnout, 40f, 95f);
            int totalCastVotes = Mathf.RoundToInt(constituency.totalRegisteredVoters * (finalTurnoutPct / 100f));

            float totalRawScore = 0f;
            List<float> rawScores = new List<float>();

            foreach (var cand in constituency.candidates)
            {
                // Multi-factorial candidate formula
                float score = (cand.basePopularity * 0.45f)
                            + (cand.campaignEffort * 0.30f)
                            + (cand.promiseFulfillmentScore * 0.15f)
                            + (cand.mediaImageScore * 0.10f);

                // Add deterministic noise factor (+/- 5%)
                float randomFactor = UnityEngine.Random.Range(0.95f, 1.05f);
                score *= randomFactor;

                rawScores.Add(score);
                totalRawScore += score;
            }

            if (totalRawScore <= 0.001f) totalRawScore = 1f;

            for (int i = 0; i < constituency.candidates.Count; i++)
            {
                var cand = constituency.candidates[i];
                float fraction = rawScores[i] / totalRawScore;
                cand.votePercentage = fraction * 100f;
                cand.totalVotesCalculated = Mathf.Round(totalCastVotes * fraction);
            }

            // Rank candidates
            List<CandidateData> ranked = new List<CandidateData>(constituency.candidates);
            ranked.Sort((a, b) => b.totalVotesCalculated.CompareTo(a.totalVotesCalculated));

            CandidateData winner = ranked[0];
            int margin = 0;
            if (ranked.Count > 1)
            {
                margin = Mathf.RoundToInt(ranked[0].totalVotesCalculated - ranked[1].totalVotesCalculated);
            }
            else
            {
                margin = Mathf.RoundToInt(ranked[0].totalVotesCalculated);
            }

            ElectionResult result = new ElectionResult
            {
                constituencyName = constituency.constituencyName,
                totalVotesCast = totalCastVotes,
                turnoutPercent = finalTurnoutPct,
                winner = winner,
                victoryMarginVotes = margin,
                rankedCandidates = ranked
            };

            Debug.Log($"[ElectionSimulator] Election complete in {constituency.constituencyName}! Winner: {winner.name} ({winner.partyName}) with margin {margin} votes.");
            return result;
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<ElectionSimulator>();
            }
        }
    }
}
