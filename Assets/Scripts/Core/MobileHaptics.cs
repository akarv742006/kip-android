using UnityEngine;

namespace Kingmakers.Core
{
    public enum HapticType
    {
        LightImpact,
        MediumImpact,
        HeavyImpact,
        SuccessNotification,
        WarningNotification,
        FailureNotification
    }

    /// <summary>
    /// AAA-grade mobile haptic tactile feedback engine.
    /// Utilizes Android's native Vibrator & VibrationEffect for subtle, premium physical feedback.
    /// </summary>
    public static class MobileHaptics
    {
        private static bool isInitialized = false;
        private static AndroidJavaObject vibrator;
        private static AndroidJavaClass vibrationEffectClass;
        private static int apiLevel = 0;

        public static void Initialize()
        {
            if (isInitialized) return;

#if UNITY_ANDROID && !UNITY_EDITOR
            try
            {
                using (var versionClass = new AndroidJavaClass("android.os.Build$VERSION"))
                {
                    apiLevel = versionClass.GetStatic<int>("SDK_INT");
                }

                using (var unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer"))
                using (var currentActivity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity"))
                {
                    vibrator = currentActivity.Call<AndroidJavaObject>("getSystemService", "vibrator");
                }

                if (apiLevel >= 26)
                {
                    vibrationEffectClass = new AndroidJavaClass("android.os.VibrationEffect");
                }

                isInitialized = true;
            }
            catch (System.Exception ex)
            {
                Debug.LogWarning($"[MobileHaptics] Failed to initialize Android vibrator: {ex.Message}");
            }
#else
            isInitialized = true;
#endif
        }

        public static void Trigger(HapticType type)
        {
            if (!isInitialized) Initialize();

#if UNITY_ANDROID && !UNITY_EDITOR
            if (vibrator == null) return;

            try
            {
                if (apiLevel >= 26 && vibrationEffectClass != null)
                {
                    int effectId = -1;
                    switch (type)
                    {
                        case HapticType.LightImpact:
                            // Small 20ms pulse
                            vibrator.Call("vibrate", vibrationEffectClass.CallStatic<AndroidJavaObject>("createOneShot", 20L, 80));
                            return;
                        case HapticType.MediumImpact:
                            vibrator.Call("vibrate", vibrationEffectClass.CallStatic<AndroidJavaObject>("createOneShot", 40L, 160));
                            return;
                        case HapticType.HeavyImpact:
                            vibrator.Call("vibrate", vibrationEffectClass.CallStatic<AndroidJavaObject>("createOneShot", 80L, 255));
                            return;
                        case HapticType.SuccessNotification:
                            long[] successPattern = new long[] { 0, 30, 60, 40 };
                            int[] successAmplitudes = new int[] { 0, 150, 0, 255 };
                            vibrator.Call("vibrate", vibrationEffectClass.CallStatic<AndroidJavaObject>("createWaveform", successPattern, successAmplitudes, -1));
                            return;
                        case HapticType.FailureNotification:
                            long[] failPattern = new long[] { 0, 50, 80, 50 };
                            int[] failAmplitudes = new int[] { 0, 200, 0, 200 };
                            vibrator.Call("vibrate", vibrationEffectClass.CallStatic<AndroidJavaObject>("createWaveform", failPattern, failAmplitudes, -1));
                            return;
                    }
                }
                else
                {
                    // Fallback for older API levels
                    vibrator.Call("vibrate", 35L);
                }
            }
            catch
            {
                // Graceful fallback
            }
#endif
        }
    }
}
