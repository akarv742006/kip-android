using System.Collections.Generic;
using UnityEngine;

namespace Kingmakers.Dialogue
{
    [CreateAssetMenu(fileName = "NewDialogueData", menuName = "Kingmakers/Dialogue Data")]
    public class DialogueData : ScriptableObject
    {
        public string dialogueId;
        public int startNodeId = 0;
        public List<DialogueNode> nodes = new List<DialogueNode>();

        public DialogueNode GetNodeById(int id)
        {
            return nodes.Find(n => n.id == id);
        }
    }
}
