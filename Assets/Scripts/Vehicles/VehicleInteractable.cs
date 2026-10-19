using UnityEngine;
using Kingmakers.Player;
using Kingmakers.Core;

namespace Kingmakers.Vehicles
{
    public class VehicleInteractable : MonoBehaviour, IInteractable
    {
        [SerializeField] private SimpleVehicleController vehicleController;
        [SerializeField] private Transform driverSeat;
        [SerializeField] private Transform exitSpot;

        private GameObject playerInstance;

        public string GetPromptKey() => "vehicle_enter_prompt";
        public string GetFallbackPrompt() => "Drive Vehicle";

        public void Interact()
        {
            playerInstance = GameObject.FindWithTag("Player");
            if (playerInstance == null || vehicleController == null) return;

            // Enter vehicle
            playerInstance.SetActive(false);
            vehicleController.EnableVehicle(this);

            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.SetGameState(GameState.DrivingVehicle);
            }
        }

        public void ExitVehicle()
        {
            if (playerInstance != null)
            {
                playerInstance.transform.position = exitSpot != null ? exitSpot.position : transform.position + Vector3.right * 2f;
                playerInstance.SetActive(true);
            }

            if (vehicleController != null)
            {
                vehicleController.DisableVehicle();
            }

            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                gm.SetGameState(GameState.Exploring);
            }
        }
    }
}
