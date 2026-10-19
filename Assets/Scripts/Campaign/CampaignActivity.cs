using System;
using Kingmakers.Economy;

namespace Kingmakers.Campaign
{
    public enum ActivityType
    {
        Rally,
        DoorToDoor,
        MediaInterview,
        VolunteerDrive,
        TownHall
    }

    [Serializable]
    public class CampaignActivity
    {
        public ActivityType type;
        public string titleKey;
        public string fallbackTitle;
        public long costInFunds;
        public int popularityGain;
        public int publicTrustGain;
        public int mediaImageGain;
    }
}
