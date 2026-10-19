using UnityEngine;
using UnityEngine.UI;
using Kingmakers.Localization;
using Kingmakers.Core;
using Kingmakers.World;

namespace Kingmakers.UI
{
    public class SettingsUI : MonoBehaviour
    {
        [Header("Panels")]
        [SerializeField] private GameObject settingsPanel;

        [Header("Dropdowns / Buttons")]
        [SerializeField] private Dropdown languageDropdown;
        [SerializeField] private Dropdown crowdQualityDropdown;
        [SerializeField] private Button closeButton;

        private void Start()
        {
            if (languageDropdown) languageDropdown.onValueChanged.AddListener(OnLanguageChanged);
            if (crowdQualityDropdown) crowdQualityDropdown.onValueChanged.AddListener(OnCrowdQualityChanged);
            if (closeButton) closeButton.onClick.AddListener(CloseSettings);

            HidePanel();
        }

        public void OpenSettings()
        {
            settingsPanel.SetActive(true);
        }

        private void OnLanguageChanged(int index)
        {
            Language selected = index == 1 ? Language.Tamil : Language.English;
            if (ServiceLocator.TryGet<LocalizationManager>(out var locMgr))
            {
                locMgr.LoadLanguage(selected);
            }
        }

        private void OnCrowdQualityChanged(int index)
        {
            TargetQualityLevel level = (TargetQualityLevel)index;
            var crowdMgr = FindObjectOfType<AdaptiveCrowdManager>();
            if (crowdMgr != null)
            {
                crowdMgr.SetQualityLevel(level);
            }
        }

        public void CloseSettings()
        {
            HidePanel();
        }

        private void HidePanel()
        {
            settingsPanel.SetActive(false);
        }
    }
}
