using UnityEngine;

namespace Kingmakers.Player
{
    public class PlayerStats : MonoBehaviour
    {
        [Header("Profile")]
        public string characterName = "K. Anbarasan";
        public string background = "Community Activist";
        public string homeRegion = "Chennai Central";

        [Header("Movement Settings")]
        public float walkSpeed = 3.5f;
        public float runSpeed = 6.5f;
        public float rotationSpeed = 10f;
    }
}
