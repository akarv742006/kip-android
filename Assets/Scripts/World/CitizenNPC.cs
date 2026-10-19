using UnityEngine;
using Kingmakers.Player;
using Kingmakers.Dialogue;
using Kingmakers.Core;

namespace Kingmakers.World
{
    public class CitizenNPC : MonoBehaviour, IInteractable
    {
        [SerializeField] private string npcName = "Local Resident";
        [SerializeField] private DialogueData npcDialogueData;
        [SerializeField] private string promptKey = "dialogue_interact_prompt";
        [SerializeField] private string fallbackPrompt = "Talk to Citizen";

        public string GetPromptKey() => promptKey;
        public string GetFallbackPrompt() => fallbackPrompt;

        public void Interact()
        {
            if (npcDialogueData == null)
            {
                Debug.LogWarning($"[CitizenNPC] {npcName} has no DialogueData assigned.");
                return;
            }

            if (ServiceLocator.TryGet<DialogueManager>(out var diagMgr))
            {
                diagMgr.StartDialogue(npcDialogueData);
            }
        }
    }
}
