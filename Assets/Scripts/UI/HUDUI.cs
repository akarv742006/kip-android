using UnityEngine;
using UnityEngine.UI;
using Kingmakers.Core;
using Kingmakers.Reputation;
using Kingmakers.Economy;
using Kingmakers.Party;
using Kingmakers.Localization;

namespace Kingmakers.UI
{
    public class HUDUI : MonoBehaviour
    {
        [Header("HUD Container")]
        [SerializeField] private GameObject hudPanel;

        [Header("Reputation Displays")]
        [SerializeField] private Text publicTrustText;
        [SerializeField] private Text integrityText;
        [SerializeField] private Text mediaImageText;

        [Header("Resource Displays")]
        [SerializeField] private Text personalMoneyText;
        [SerializeField] private Text campaignFundsText;

        [Header("Role Display")]
        [SerializeField] private Text currentRoleText;

        private void OnEnable()
        {
            EventBus.Subscribe<GameStateChangedEvent>(OnGameStateChanged);
            EventBus.Subscribe<ReputationChangedEvent>(OnReputationChanged);
            EventBus.Subscribe<ResourceChangedEvent>(OnResourceChanged);

            UpdateAllDisplays();
        }

        private void OnDisable()
        {
            EventBus.Unsubscribe<GameStateChangedEvent>(OnGameStateChanged);
            EventBus.Unsubscribe<ReputationChangedEvent>(OnReputationChanged);
            EventBus.Unsubscribe<ResourceChangedEvent>(OnResourceChanged);
        }

        private void OnGameStateChanged(GameStateChangedEvent evt)
        {
            hudPanel.SetActive(evt.NewState == GameState.Exploring || evt.NewState == GameState.DrivingVehicle);
        }

        [Header("AAA Netaji Phone Hub")]
        [SerializeField] private SmartPhoneUI smartPhone;

        public void OnPhoneButtonClicked()
        {
            if (smartPhone != null)
            {
                smartPhone.TogglePhone();
            }
        }

        private void OnReputationChanged(ReputationChangedEvent evt)
        {
            MobileHaptics.Trigger(HapticType.LightImpact);
            UpdateReputationDisplays();
        }

        private void OnResourceChanged(ResourceChangedEvent evt)
        {
            MobileHaptics.Trigger(HapticType.MediumImpact);
            UpdateResourceDisplays();
        }

        public void UpdateAllDisplays()
        {
            UpdateReputationDisplays();
            UpdateResourceDisplays();
            UpdateRoleDisplay();
        }

        private void UpdateReputationDisplays()
        {
            if (ServiceLocator.TryGet<ReputationSystem>(out var rep))
            {
                if (publicTrustText) publicTrustText.text = $"Trust: {rep.Get(ReputationType.PublicTrust)}";
                if (integrityText) integrityText.text = $"Integrity: {rep.Get(ReputationType.Integrity)}";
                if (mediaImageText) mediaImageText.text = $"Media: {rep.Get(ReputationType.MediaImage)}";
            }
        }

        private void UpdateResourceDisplays()
        {
            if (ServiceLocator.TryGet<EconomyManager>(out var eco))
            {
                if (personalMoneyText) personalMoneyText.text = $"Cash: ₹{eco.GetBalance(ResourceCategory.PersonalMoney):N0}";
                if (campaignFundsText) campaignFundsText.text = $"Funds: ₹{eco.GetBalance(ResourceCategory.CampaignFunds):N0}";
            }
        }

        private void UpdateRoleDisplay()
        {
            if (currentRoleText && ServiceLocator.TryGet<GovernmentSystem>(out var gov))
            {
                currentRoleText.text = $"Role: {gov.CurrentRole}";
            }
        }
    }
}
