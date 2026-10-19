using UnityEngine;
using Kingmakers.Core;
using Kingmakers.Dialogue;

namespace Kingmakers.Player
{
    public interface IInteractable
    {
        string GetPromptKey();
        string GetFallbackPrompt();
        void Interact();
    }

    public class InteractionDetector : MonoBehaviour
    {
        [SerializeField] private float interactRadius = 2.5f;
        [SerializeField] private LayerMask interactableLayer;

        private IInteractable currentInteractable;

        public IInteractable CurrentInteractable => currentInteractable;

        private void Update()
        {
            if (ServiceLocator.TryGet<GameManager>(out var gm) && gm.CurrentState != GameState.Exploring)
            {
                currentInteractable = null;
                return;
            }

            DetectInteractables();

            if (currentInteractable != null && Input.GetKeyDown(KeyCode.E))
            {
                currentInteractable.Interact();
            }
        }

        private void DetectInteractables()
        {
            Collider[] colliders = Physics.OverlapSphere(transform.position, interactRadius, interactableLayer);
            IInteractable closest = null;
            float closestDist = float.MaxValue;

            foreach (var col in colliders)
            {
                if (col.TryGetComponent<IInteractable>(out var interactable))
                {
                    float dist = Vector3.Distance(transform.position, col.transform.position);
                    if (dist < closestDist)
                    {
                        closestDist = dist;
                        closest = interactable;
                    }
                }
            }

            currentInteractable = closest;
        }

        private void OnDrawGizmosSelected()
        {
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(transform.position, interactRadius);
        }
    }
}
