using System;
using System.Collections.Generic;

namespace Kingmakers.Campaign
{
    [Serializable]
    public class ConstituencyData
    {
        public string constituencyId = "TN-101";
        public string constituencyName = "Chennai Central Ward";
        public int totalRegisteredVoters = 150000;
        public float baseExpectedTurnoutPercent = 68.5f;

        // Dynamic Issues Weights
        public float waterServiceWeight = 0.35f;
        public float roadInfrastructureWeight = 0.25f;
        public float employmentWeight = 0.20f;
        public float healthSanitationWeight = 0.20f;

        public List<CandidateData> candidates = new List<CandidateData>();
    }
}
