using UnityEngine;
using UnityEngine.UI;
using Kingmakers.Core;
using Kingmakers.Persistence;

namespace Kingmakers.UI
{
    public class PauseMenuUI : MonoBehaviour
    {
        [Header("Panels")]
        [SerializeField] private GameObject pauseMenuPanel;

        [Header("Buttons")]
        [SerializeField] private Button resumeButton;
        [SerializeField] private Button saveButton;
        [SerializeField] private Button loadButton;
        [SerializeField] private Button settingsButton;
        [SerializeField] private Button exitButton;

        [Header("Settings Sub-Menu")]
        [SerializeField] private SettingsUI settingsUI;

        private void Start()
        {
            if (resumeButton) resumeButton.onClick.AddListener(OnResumeClicked);
            if (saveButton) saveButton.onClick.AddListener(OnSaveClicked);
            if (loadButton) loadButton.onClick.AddListener(OnLoadClicked);
            if (settingsButton) settingsButton.onClick.AddListener(OnSettingsClicked);
            if (exitButton) exitButton.onClick.AddListener(OnExitClicked);

            HidePanel();
        }

        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.Escape))
            {
                if (ServiceLocator.TryGet<GameManager>(out var gm))
                {
                    if (gm.CurrentState == GameState.Exploring || gm.CurrentState == GameState.DrivingVehicle)
                    {
                        gm.PauseGame();
                        ShowPanel();
                    }
                    else if (gm.CurrentState == GameState.Paused)
                    {
                        gm.ResumeGame();
                        HidePanel();
                    }
                }
            }
        }

        private void OnResumeClicked()
        {
            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.ResumeGame();
            }
            HidePanel();
        }

        private void OnSaveClicked()
        {
            if (ServiceLocator.TryGet<SaveSystem>(out var saveSys))
            {
                saveSys.SaveGame();
            }
        }

        private void OnLoadClicked()
        {
            if (ServiceLocator.TryGet<SaveSystem>(out var saveSys))
            {
                saveSys.LoadGame();
            }
        }

        private void OnSettingsClicked()
        {
            if (settingsUI != null)
            {
                settingsUI.OpenSettings();
            }
        }

        private void OnExitClicked()
        {
            Application.Quit();
        }

        private void ShowPanel() => pauseMenuPanel.SetActive(true);
        private void HidePanel() => pauseMenuPanel.SetActive(false);
    }
}
