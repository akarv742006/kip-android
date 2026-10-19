using System;
using System.Collections.Generic;
using UnityEngine;
using Kingmakers.Core;
using Kingmakers.Reputation;
using Kingmakers.Economy;

namespace Kingmakers.Dialogue
{
    public class DialogueManager : MonoBehaviour
    {
        public static DialogueManager Instance { get; private set; }

        public event Action<DialogueNode> OnDialogueNodeStarted;
        public event Action OnDialogueEnded;

        private DialogueData currentDialogue;
        private DialogueNode currentNode;

        public bool IsInDialogue => currentDialogue != null;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<DialogueManager>(this);
        }

        public void StartDialogue(DialogueData data)
        {
            if (data == null || data.nodes.Count == 0)
            {
                Debug.LogWarning("[DialogueManager] Invalid dialogue data provided.");
                return;
            }

            currentDialogue = data;
            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.SetGameState(GameState.InDialogue);
            }

            DisplayNode(data.GetNodeById(data.startNodeId));
        }

        public void SelectOption(int optionIndex)
        {
            if (currentNode == null || optionIndex < 0 || optionIndex >= currentNode.options.Count)
            {
                EndDialogue();
                return;
            }

            DialogueOption option = currentNode.options[optionIndex];

            // Apply Consequences
            if (option.reputationDelta != 0 && ServiceLocator.TryGet<ReputationSystem>(out var repSys))
            {
                repSys.Modify(option.reputationTypeToModify, option.reputationDelta);
            }

            if (option.resourceDelta != 0 && ServiceLocator.TryGet<EconomyManager>(out var ecoSys))
            {
                if (option.resourceDelta > 0)
                    ecoSys.Add(option.resourceToModify, option.resourceDelta);
                else
                    ecoSys.Spend(option.resourceToModify, -option.resourceDelta);
            }

            if (!string.IsNullOrEmpty(option.flagToSetOnSelect) && ServiceLocator.TryGet<StoryFlagsManager>(out var flagSys))
            {
                flagSys.SetFlag(option.flagToSetOnSelect, option.flagValueToSet);
            }

            if (option.targetNodeId >= 0 && currentDialogue != null)
            {
                DialogueNode nextNode = currentDialogue.GetNodeById(option.targetNodeId);
                if (nextNode != null)
                {
                    DisplayNode(nextNode);
                }
                else
                {
                    EndDialogue();
                }
            }
            else
            {
                EndDialogue();
            }
        }

        public bool IsOptionAvailable(DialogueOption option)
        {
            if (option == null) return false;

            if (!string.IsNullOrEmpty(option.requiredStoryFlag) && ServiceLocator.TryGet<StoryFlagsManager>(out var flagSys))
            {
                if (flagSys.GetFlag(option.requiredStoryFlag) != option.requiredFlagState)
                {
                    return false;
                }
            }

            if (option.requiredReputationValue > 0 && ServiceLocator.TryGet<ReputationSystem>(out var repSys))
            {
                if (repSys.Get(option.requiredReputationType) < option.requiredReputationValue)
                {
                    return false;
                }
            }

            return true;
        }

        private void DisplayNode(DialogueNode node)
        {
            currentNode = node;
            if (node == null)
            {
                EndDialogue();
                return;
            }

            OnDialogueNodeStarted?.Invoke(node);
        }

        public void EndDialogue()
        {
            currentDialogue = null;
            currentNode = null;

            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.SetGameState(GameState.Exploring);
            }

            OnDialogueEnded?.Invoke();
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<DialogueManager>();
            }
        }
    }
}
