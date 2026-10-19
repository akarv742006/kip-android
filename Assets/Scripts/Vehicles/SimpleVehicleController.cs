using UnityEngine;

namespace Kingmakers.Vehicles
{
    public class SimpleVehicleController : MonoBehaviour
    {
        [SerializeField] private float acceleration = 12f;
        [SerializeField] private float turnSpeed = 60f;
        [SerializeField] private float maxSpeed = 25f;

        private bool isBeingDriven = false;
        private VehicleInteractable activeInteractable;
        private Rigidbody rb;

        private void Awake()
        {
            rb = GetComponent<Rigidbody>();
        }

        public void EnableVehicle(VehicleInteractable interactable)
        {
            activeInteractable = interactable;
            isBeingDriven = true;
            if (rb != null) rb.isKinematic = false;
        }

        public void DisableVehicle()
        {
            isBeingDriven = false;
            activeInteractable = null;
            if (rb != null) rb.isKinematic = true;
        }

        private void Update()
        {
            if (!isBeingDriven) return;

            if (Input.GetKeyDown(KeyCode.F))
            {
                if (activeInteractable != null)
                {
                    activeInteractable.ExitVehicle();
                }
            }
        }

        private void FixedUpdate()
        {
            if (!isBeingDriven || rb == null) return;

            float moveInput = Input.GetAxis("Vertical");
            float turnInput = Input.GetAxis("Horizontal");

            if (Mathf.Abs(moveInput) > 0.05f)
            {
                Vector3 force = transform.forward * (moveInput * acceleration);
                if (rb.velocity.magnitude < maxSpeed)
                {
                    rb.AddForce(force, ForceMode.Acceleration);
                }
            }

            if (rb.velocity.magnitude > 0.5f)
            {
                float turn = turnInput * turnSpeed * Time.fixedDeltaTime * Mathf.Sign(moveInput);
                transform.Rotate(0f, turn, 0f);
            }
        }
    }
}
