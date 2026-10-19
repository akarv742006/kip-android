using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using Kingmakers.Core;
using Kingmakers.Reputation;
using Kingmakers.Economy;

namespace Kingmakers.UI
{
    [System.Serializable]
    public struct ChirpPost
    {
        public string handle;
        public string content;
        public int likes;
        public bool isPositive;
    }

    /// <summary>
    /// AAA Feature: "Netaji Phone" In-Game Smartphone Hub.
    /// Provides live social media feed ("Chirp"), party memos, and polling intelligence.
    /// </summary>
    public class SmartPhoneUI : MonoBehaviour
    {
        [Header("Phone Panels")]
        [SerializeField] private GameObject phoneRoot;
        [SerializeField] private GameObject chirpAppPanel;
        [SerializeField] private GameObject pollAppPanel;

        [Header("Chirp App Widgets")]
        [SerializeField] private Transform chirpPostContainer;
        [SerializeField] private Text pollTrustText;
        [SerializeField] private Text pollMediaText;

        private bool isOpen = false;
        private List<ChirpPost> activeChirps = new List<ChirpPost>();

        private void Start()
        {
            if (phoneRoot != null) phoneRoot.SetActive(false);
            GenerateInitialChirps();
        }

        public void TogglePhone()
        {
            isOpen = !isOpen;
            if (phoneRoot != null) phoneRoot.SetActive(isOpen);

            if (isOpen)
            {
                MobileHaptics.Trigger(HapticType.LightImpact);
                RefreshDashboard();
            }
        }

        public void RefreshDashboard()
        {
            if (ServiceLocator.TryGet<ReputationSystem>(out var rep))
            {
                int trust = rep.Get(ReputationType.PublicTrust);
                int media = rep.Get(ReputationType.MediaImage);

                if (pollTrustText) pollTrustText.text = $"Public Approval: {trust}%";
                if (pollMediaText) pollMediaText.text = $"Media Sentiment: {media}%";

                // Update Chirp feed based on trust
                if (trust >= 60)
                {
                    AddChirp("@YouthForReform", "Inspiring rally today! Finally a leader who addresses water and jobs without empty promises! #FutureLeader", 450, true);
                }
                else if (trust <= 30)
                {
                    AddChirp("@TamilNaduWatch", "Protests erupt in Ward 4! Citizens demand accountability for stalled civic funds! #ResignNow", 1240, false);
                }
            }
        }

        public void AddChirp(string handle, string content, int likes, bool isPositive)
        {
            ChirpPost post = new ChirpPost
            {
                handle = handle,
                content = content,
                likes = likes,
                isPositive = isPositive
            };
            activeChirps.Insert(0, post);
        }

        private void GenerateInitialChirps()
        {
            AddChirp("@CauveryNews24", "Breaking: Election Commission announces local constituency election dates! Campaigning kicks off.", 890, true);
            AddChirp("@MaduraiVoter", "Hope this election brings real road repairs and cleaner drinking water.", 210, true);
            AddChirp("@StatePoliticalInsider", "Rumors of intense backdoor negotiations between senior alliance leaders.", 530, false);
        }
    }
}
