using System;
using System.Collections.Generic;

namespace Kingmakers.Persistence
{
    [Serializable]
    public class SaveData
    {
        public int saveVersion = 1;
        public string timestamp;
        public string playerCharacterName;
        public string currentGovernmentRole;

        // Coordinates
        public float playerPosX;
        public float playerPosY;
        public float playerPosZ;

        // Dictionaries stored as serialized lists
        public List<string> reputationKeys = new List<string>();
        public List<int> reputationValues = new List<int>();

        public List<string> resourceKeys = new List<string>();
        public List<long> resourceValues = new List<long>();

        // Story Flags
        public List<string> boolFlagKeys = new List<string>();
        public List<bool> boolFlagValues = new List<bool>();

        public List<string> intFlagKeys = new List<string>();
        public List<int> intFlagValues = new List<int>();

        public string currentLanguageCode = "en";
    }
}
