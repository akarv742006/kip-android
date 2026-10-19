using System;
using UnityEngine;

namespace Kingmakers.Party
{
    [CreateAssetMenu(fileName = "NewPartyData", menuName = "Kingmakers/Party Data")]
    public class PartyData : ScriptableObject
    {
        public string partyId;
        public string partyNameKey;
        public string partyNameFallback;
        public string ideologyKey;
        public Color primaryColor = Color.blue;
        public int currentSeatCount = 0;
        public bool isPlayerParty = false;
        public bool isInCoalition = false;
    }
}
