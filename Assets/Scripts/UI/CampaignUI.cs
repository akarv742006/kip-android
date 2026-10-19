using UnityEngine;
using UnityEngine.UI;
using Kingmakers.Campaign;
using Kingmakers.Core;
using Kingmakers.Localization;

namespace Kingmakers.UI
{
    public class CampaignUI : MonoBehaviour
    {
        [Header("Panels")]
        [SerializeField] private GameObject campaignMenuPanel;

        [Header("Constituency Info")]
        [SerializeField] private Text constituencyNameText;
        [SerializeField] private Text votersText;

        [Header("Buttons")]
        [SerializeField] private Button rallyButton;
        [SerializeField] private Button doorToDoorButton;
        [SerializeField] private Button runElectionButton;
        [SerializeField] private Button closeButton;

        private void Start()
        {
            if (rallyButton) rallyButton.onClick.AddListener(OnRallyClicked);
            if (doorToDoorButton) doorToDoorButton.onClick.AddListener(OnDoorToDoorClicked);
            if (runElectionButton) runElectionButton.onClick.AddListener(OnRunElectionClicked);
            if (closeButton) closeButton.onClick.AddListener(CloseMenu);

            HideMenu();
        }

        public void OpenMenu()
        {
            campaignMenuPanel.SetActive(true);
            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.SetGameState(GameState.InCampaignMenu);
            }

            if (ServiceLocator.TryGet<CampaignManager>(out var campMgr))
            {
                var constData = campMgr.ActiveConstituency;
                if (constData != null)
                {
                    constituencyNameText.text = constData.constituencyName;
                    votersText.text = $"Registered Voters: {constData.totalRegisteredVoters:N0}";
                }
            }
        }

        private void OnRallyClicked()
        {
            CampaignActivity activity = new CampaignActivity
            {
                type = ActivityType.Rally,
                titleKey = "campaign_rally_title",
                fallbackTitle = "Political Rally",
                costInFunds = 25000,
                popularityGain = 15,
                publicTrustGain = 5,
                mediaImageGain = 10
            };

            if (ServiceLocator.TryGet<CampaignManager>(out var mgr))
            {
                mgr.ExecuteCampaignActivity(activity);
            }
        }

        private void OnDoorToDoorClicked()
        {
            CampaignActivity activity = new CampaignActivity
            {
                type = ActivityType.DoorToDoor,
                titleKey = "campaign_door_to_door",
                fallbackTitle = "Door-to-Door Outreach",
                costInFunds = 5000,
                popularityGain = 8,
                publicTrustGain = 10,
                mediaImageGain = 2
            };

            if (ServiceLocator.TryGet<CampaignManager>(out var mgr))
            {
                mgr.ExecuteCampaignActivity(activity);
            }
        }

        private void OnRunElectionClicked()
        {
            if (ServiceLocator.TryGet<CampaignManager>(out var mgr))
            {
                mgr.RunElection();
                HideMenu();
            }
        }

        public void CloseMenu()
        {
            HideMenu();
            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.SetGameState(GameState.Exploring);
            }
        }

        private void HideMenu()
        {
            campaignMenuPanel.SetActive(false);
        }
    }
}
