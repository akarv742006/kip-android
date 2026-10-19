using System;

namespace Kingmakers.Campaign
{
    [Serializable]
    public class CandidateData
    {
        public string id;
        public string name;
        public string partyId;
        public string partyName;
        public bool isPlayer;

        public float basePopularity = 50f;
        public float campaignEffort = 0f;
        public float promiseFulfillmentScore = 50f;
        public float mediaImageScore = 50f;
        public float totalVotesCalculated = 0f;
        public float votePercentage = 0f;
    }
}
