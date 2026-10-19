#if UNITY_EDITOR
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;
using System.IO;

namespace Kingmakers.Editor
{
    public static class Builder
    {
        [MenuItem("Kingmakers/Build Android AAA APK")]
        public static void BuildAndroidAPK()
        {
            string outputDir = "Builds/Android";
            if (!Directory.Exists(outputDir))
            {
                Directory.CreateDirectory(outputDir);
            }

            string apkPath = Path.Combine(outputDir, "Kingmakers_AAA.apk");

            Debug.Log("[Builder] Configuring AAA Android Player Settings...");

            // AAA Android Settings
            PlayerSettings.companyName = "KingmakersStudio";
            PlayerSettings.productName = "Kingmakers of Indian Politics";
            PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.Android, "com.kingmakers.politicalsim");
            
            // Android API and Architecture Target
            PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel26;
            PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevelAuto;
            PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
            PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;

            // Graphics APIs: Vulkan & OpenGLES3
            PlayerSettings.SetUseDefaultGraphicsAPIs(BuildTarget.Android, false);
            PlayerSettings.SetGraphicsAPIs(BuildTarget.Android, new UnityEngine.Rendering.GraphicsDeviceType[] {
                UnityEngine.Rendering.GraphicsDeviceType.Vulkan,
                UnityEngine.Rendering.GraphicsDeviceType.OpenGLES3
            });

            // Gather Scenes
            string[] scenes = new string[] {
                "Assets/Scenes/Main.unity"
            };

            // If Main scene does not exist yet, find any scenes in project
            var editorScenes = EditorBuildSettings.scenes;
            if (editorScenes != null && editorScenes.Length > 0)
            {
                scenes = new string[editorScenes.Length];
                for (int i = 0; i < editorScenes.Length; i++)
                {
                    scenes[i] = editorScenes[i].path;
                }
            }

            BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions
            {
                scenes = scenes,
                locationPathName = apkPath,
                target = BuildTarget.Android,
                options = BuildOptions.None
            };

            Debug.Log($"[Builder] Starting APK build to: {apkPath}");
            BuildReport report = BuildPipeline.BuildPlayer(buildPlayerOptions);
            BuildSummary summary = report.summary;

            if (summary.result == BuildResult.Succeeded)
            {
                Debug.Log($"[Builder] Android AAA APK build SUCCEEDED: {summary.totalSize} bytes at {apkPath}");
            }
            else if (summary.result == BuildResult.Failed)
            {
                Debug.LogError($"[Builder] Android AAA APK build FAILED with {summary.totalErrors} errors.");
            }
        }
    }
}
#endif
