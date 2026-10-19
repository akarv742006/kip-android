using UnityEngine;

namespace Kingmakers.Core
{
    public enum AAAQualityTier
    {
        BatterySaver,
        Balanced,
        HighFidelity,
        UltraCinema
    }

    /// <summary>
    /// AAA Graphics and Performance Manager optimized for Android.
    /// Manages 60/120 FPS high-refresh rate targets, thermal adaptation, and quality scaling.
    /// </summary>
    public class AAAGraphicsQualityManager : MonoBehaviour
    {
        public static AAAGraphicsQualityManager Instance { get; private set; }

        [Header("Frame Rate Control")]
        [SerializeField] private int targetFrameRate = 60;
        [SerializeField] private bool allow120Fps = true;

        [Header("Quality Tier")]
        [SerializeField] private AAAQualityTier currentTier = AAAQualityTier.HighFidelity;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            DontDestroyOnLoad(gameObject);

            InitializePerformanceSettings();
        }

        private void Start()
        {
            ApplyTier(currentTier);
        }

        public void InitializePerformanceSettings()
        {
            // Disable screen timeout during gameplay
            Screen.sleepTimeout = SleepTimeout.NeverSleep;

            // Unlock high refresh rate on modern Android displays (90Hz / 120Hz)
            if (allow120Fps && Screen.currentResolution.refreshRateRatio.value >= 90)
            {
                Application.targetFrameRate = Mathf.RoundToInt((float)Screen.currentResolution.refreshRateRatio.value);
            }
            else
            {
                Application.targetFrameRate = targetFrameRate;
            }

            QualitySettings.vSyncCount = 0; // Handled by targetFrameRate
            Debug.Log($"[AAAGraphicsQualityManager] Initialized. Target FPS: {Application.targetFrameRate}, Refresh Rate: {Screen.currentResolution.refreshRateRatio.value}Hz");
        }

        public void ApplyTier(AAAQualityTier tier)
        {
            currentTier = tier;

            switch (tier)
            {
                case AAAQualityTier.BatterySaver:
                    Application.targetFrameRate = 30;
                    QualitySettings.shadowDistance = 25f;
                    QualitySettings.shadowCascades = 1;
                    QualitySettings.shadowResolution = ShadowResolution.Low;
                    QualitySettings.antiAliasing = 0;
                    QualitySettings.lodBias = 0.8f;
                    break;

                case AAAQualityTier.Balanced:
                    Application.targetFrameRate = 60;
                    QualitySettings.shadowDistance = 45f;
                    QualitySettings.shadowCascades = 2;
                    QualitySettings.shadowResolution = ShadowResolution.Medium;
                    QualitySettings.antiAliasing = 2;
                    QualitySettings.lodBias = 1.0f;
                    break;

                case AAAQualityTier.HighFidelity:
                    Application.targetFrameRate = 60;
                    QualitySettings.shadowDistance = 80f;
                    QualitySettings.shadowCascades = 4;
                    QualitySettings.shadowResolution = ShadowResolution.High;
                    QualitySettings.antiAliasing = 4;
                    QualitySettings.lodBias = 1.4f;
                    break;

                case AAAQualityTier.UltraCinema:
                    Application.targetFrameRate = allow120Fps ? 120 : 60;
                    QualitySettings.shadowDistance = 120f;
                    QualitySettings.shadowCascades = 4;
                    QualitySettings.shadowResolution = ShadowResolution.VeryHigh;
                    QualitySettings.antiAliasing = 8;
                    QualitySettings.lodBias = 2.0f;
                    break;
            }

            Debug.Log($"[AAAGraphicsQualityManager] Applied Tier: {tier}");
        }

        public void ToggleFps(int fps)
        {
            targetFrameRate = fps;
            Application.targetFrameRate = fps;
        }
    }
}
