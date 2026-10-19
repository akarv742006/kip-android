using UnityEngine;
using UnityEngine.UI;
using Kingmakers.Campaign;
using Kingmakers.Core;
using Kingmakers.Party;

namespace Kingmakers.UI
{
    public class ElectionResultsUI : MonoBehaviour
    {
        [Header("Panels")]
        [SerializeField] private GameObject resultsPanel;

        [Header("Texts")]
        [SerializeField] private Text constituencyTitleText;
        [SerializeField] private Text declaredWinnerText;
        [SerializeField] private Text marginText;
        [SerializeField] private Text turnoutText;
        [SerializeField] private Transform candidatesListContainer;
        [SerializeField] private GameObject candidateRowPrefab;

        [Header("Buttons")]
        [SerializeField] private Button continueButton;

        private void Start()
        {
            if (continueButton) continueButton.onClick.AddListener(OnContinueClicked);
            Hide();
        }

        public void DisplayResults(ElectionResult result)
        {
            if (result == null) return;

            resultsPanel.SetActive(true);
            constituencyTitleText.text = result.constituencyName;
            declaredWinnerText.text = $"Winner: {result.winner.name} ({result.winner.partyName})";
            marginText.text = $"Victory Margin: {result.victoryMarginVotes:N0} votes";
            turnoutText.text = $"Turnout: {result.turnoutPercent:F1}% ({result.totalVotesCast:N0} votes)";

            // Update role if player won
            if (result.winner.isPlayer && ServiceLocator.TryGet<GovernmentSystem>(out var gov))
            {
                gov.PromoteRole(GovernmentRole.MLA);
            }

            // Populate breakdown
            foreach (Transform child in candidatesListContainer)
            {
                Destroy(child.gameObject);
            }

            foreach (var candidate in result.rankedCandidates)
            {
                GameObject row = Instantiate(candidateRowPrefab, candidatesListContainer);
                Text rowText = row.GetComponentInChildren<Text>();
                rowText.text = $"{candidate.name} ({candidate.partyName}): {candidate.totalVotesCalculated:N0} votes ({candidate.votePercentage:F1}%)";
            }
        }

        private void OnContinueClicked()
        {
            Hide();
            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.SetGameState(GameState.Exploring);
            }
        }

        private void Hide()
        {
            resultsPanel.SetActive(false);
        }
    }
}
