using UnityEngine;

namespace Kingmakers.World
{
    public class DayNightCycle : MonoBehaviour
    {
        [SerializeField] private Light sunLight;
        [SerializeField] private float dayDurationInSeconds = 300f; // 5 minute days
        [Range(0f, 1f)] [SerializeField] private float currentTimeOfDay = 0.35f; // Morning

        public float CurrentTimeOfDay => currentTimeOfDay;

        private void Update()
        {
            currentTimeOfDay += (Time.deltaTime / dayDurationInSeconds);
            if (currentTimeOfDay >= 1f) currentTimeOfDay = 0f;

            UpdateSunLight();
        }

        private void UpdateSunLight()
        {
            if (sunLight == null) return;

            float sunAngle = (currentTimeOfDay * 360f) - 90f;
            sunLight.transform.rotation = Quaternion.Euler(sunAngle, 170f, 0f);

            // Light intensity mapping
            float intensityMultiplier = Mathf.Clamp01(Mathf.Sin(currentTimeOfDay * Mathf.PI * 2f));
            sunLight.intensity = Mathf.Lerp(0.1f, 1.2f, intensityMultiplier);
        }
    }
}
