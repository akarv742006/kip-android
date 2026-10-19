using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.UI
{
    public class UIManager : MonoBehaviour
    {
        public static UIManager Instance { get; private set; }

        [SerializeField] private HUDUI hudUI;
        [SerializeField] private DialogueUI dialogueUI;
        [SerializeField] private CampaignUI campaignUI;
        [SerializeField] private ElectionResultsUI electionResultsUI;
        [SerializeField] private PauseMenuUI pauseMenuUI;

        public HUDUI HUD => hudUI;
        public CampaignUI Campaign => campaignUI;
        public ElectionResultsUI ElectionResults => electionResultsUI;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<UIManager>(this);
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<UIManager>();
            }
        }
    }
}
