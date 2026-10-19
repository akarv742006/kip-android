using UnityEngine;
using UnityEngine.UI;
using Kingmakers.Core;

namespace Kingmakers.Localization
{
    public class LocalizedText : MonoBehaviour
    {
        [SerializeField] private string localizationKey;
        [SerializeField] private string fallbackText = "";

        private Text textComponent;

        public string Key
        {
            get => localizationKey;
            set
            {
                localizationKey = value;
                UpdateText();
            }
        }

        private void Awake()
        {
            textComponent = GetComponent<Text>();
        }

        private void OnEnable()
        {
            EventBus.Subscribe<LanguageChangedEvent>(OnLanguageChanged);
            UpdateText();
        }

        private void OnDisable()
        {
            EventBus.Unsubscribe<LanguageChangedEvent>(OnLanguageChanged);
        }

        private void OnLanguageChanged(LanguageChangedEvent evt)
        {
            UpdateText();
        }

        public void UpdateText()
        {
            if (textComponent == null) textComponent = GetComponent<Text>();
            if (textComponent == null) return;

            if (ServiceLocator.TryGet<LocalizationManager>(out var manager))
            {
                textComponent.text = manager.GetString(localizationKey, fallbackText);
            }
            else if (!string.IsNullOrEmpty(fallbackText))
            {
                textComponent.text = fallbackText;
            }
        }
    }
}
