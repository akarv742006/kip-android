using System;
using System.Collections.Generic;
using UnityEngine;

namespace Kingmakers.Dialogue
{
    [Serializable]
    public class DialogueNode
    {
        public int id;
        public string speakerNameKey;
        public string speakerNameFallback;
        public string dialogueTextKey;
        public string dialogueTextFallback;

        public List<DialogueOption> options = new List<DialogueOption>();
    }
}
