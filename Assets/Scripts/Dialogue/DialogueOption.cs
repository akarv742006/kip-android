using System;
using UnityEngine;
using Kingmakers.Reputation;
using Kingmakers.Economy;

namespace Kingmakers.Dialogue
{
    [Serializable]
    public class DialogueOption
    {
        [Header("Display Text")]
        public string optionKey; // Localization Key
        public string fallbackText;

        [Header("Target Node")]
        public int targetNodeId = -1; // -1 ends dialogue

        [Header("Conditions")]
        public string requiredStoryFlag;
        public bool requiredFlagState = true;
        public ReputationType requiredReputationType;
        public int requiredReputationValue = 0;

        [Header("Consequences")]
        public ReputationType reputationTypeToModify;
        public int reputationDelta = 0;

        public ResourceCategory resourceToModify;
        public long resourceDelta = 0;

        public string flagToSetOnSelect;
        public bool flagValueToSet = true;
    }
}
