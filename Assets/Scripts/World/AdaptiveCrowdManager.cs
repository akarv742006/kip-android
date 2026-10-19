using System.Collections.Generic;
using UnityEngine;

namespace Kingmakers.World
{
    public enum TargetQualityLevel
    {
        Low,
        Medium,
        High
    }

    public class AdaptiveCrowdManager : MonoBehaviour
    {
        [SerializeField] private List<GameObject> crowdNPCs = new List<GameObject>();
        [SerializeField] private TargetQualityLevel qualityLevel = TargetQualityLevel.Medium;

        private void Start()
        {
            ApplyCrowdDensity();
        }

        public void SetQualityLevel(TargetQualityLevel level)
        {
            qualityLevel = level;
            ApplyCrowdDensity();
        }

        private void ApplyCrowdDensity()
        {
            float activePercent = qualityLevel switch
            {
                TargetQualityLevel.Low => 0.35f,
                TargetQualityLevel.Medium => 0.70f,
                TargetQualityLevel.High => 1.0f,
                _ => 0.7f
            };

            int activeCount = Mathf.RoundToInt(crowdNPCs.Count * activePercent);

            for (int i = 0; i < crowdNPCs.Count; i++)
            {
                if (crowdNPCs[i] != null)
                {
                    crowdNPCs[i].SetActive(i < activeCount);
                }
            }

            Debug.Log($"[AdaptiveCrowdManager] Crowd density set to {qualityLevel} ({activeCount}/{crowdNPCs.Count} active).");
        }
    }
}
