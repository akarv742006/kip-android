using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Kingmakers.Dialogue;
using Kingmakers.Localization;
using Kingmakers.Core;

namespace Kingmakers.UI
{
    public class DialogueUI : MonoBehaviour
    {
        [Header("UI Panels")]
        [SerializeField] private GameObject dialoguePanel;
        [SerializeField] private Text speakerNameText;
        [SerializeField] private Text dialogueText;
        [SerializeField] private Transform optionsContainer;
        [SerializeField] private GameObject optionButtonPrefab;

        private void OnEnable()
        {
            if (ServiceLocator.TryGet<DialogueManager>(out var diagMgr))
            {
                diagMgr.OnDialogueNodeStarted += DisplayNode;
                diagMgr.OnDialogueEnded += HidePanel;
            }

            HidePanel();
        }

        private void OnDisable()
        {
            if (ServiceLocator.TryGet<DialogueManager>(out var diagMgr))
            {
                diagMgr.OnDialogueNodeStarted -= DisplayNode;
                diagMgr.OnDialogueEnded -= HidePanel;
            }
        }

        private void DisplayNode(DialogueNode node)
        {
            if (node == null) return;

            dialoguePanel.SetActive(true);

            if (ServiceLocator.TryGet<LocalizationManager>(out var loc))
            {
                speakerNameText.text = loc.GetString(node.speakerNameKey, node.speakerNameFallback);
                dialogueText.text = loc.GetString(node.dialogueTextKey, node.dialogueTextFallback);
            }
            else
            {
                speakerNameText.text = node.speakerNameFallback;
                dialogueText.text = node.dialogueTextFallback;
            }

            // Clear old buttons
            foreach (Transform child in optionsContainer)
            {
                Destroy(child.gameObject);
            }

            // Populate Option Buttons
            for (int i = 0; i < node.options.Count; i++)
            {
                int index = i;
                DialogueOption option = node.options[i];

                if (!ServiceLocator.Get<DialogueManager>().IsOptionAvailable(option))
                {
                    continue;
                }

                GameObject btnObj = Instantiate(optionButtonPrefab, optionsContainer);
                Text btnText = btnObj.GetComponentInChildren<Text>();

                if (ServiceLocator.TryGet<LocalizationManager>(out var l))
                {
                    btnText.text = l.GetString(option.optionKey, option.fallbackText);
                }
                else
                {
                    btnText.text = option.fallbackText;
                }

                Button btn = btnObj.GetComponent<Button>();
                btn.onClick.AddListener(() =>
                {
                    ServiceLocator.Get<DialogueManager>().SelectOption(index);
                });
            }
        }

        private void HidePanel()
        {
            dialoguePanel.SetActive(false);
        }
    }
}
