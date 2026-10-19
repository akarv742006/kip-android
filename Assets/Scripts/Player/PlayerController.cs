using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.Player
{
    [RequireComponent(typeof(CharacterController))]
    [RequireComponent(typeof(PlayerStats))]
    public class PlayerController : MonoBehaviour
    {
        private CharacterController characterController;
        private PlayerStats stats;
        private Camera mainCamera;

        private Vector3 velocity;
        private bool isGrounded;
        private float gravity = -9.81f;

        private void Awake()
        {
            characterController = GetComponent<CharacterController>();
            stats = GetComponent<PlayerStats>();
            mainCamera = Camera.main;
        }

        private void Update()
        {
            if (ServiceLocator.TryGet<GameManager>(out var gm))
            {
                if (gm.CurrentState != GameState.Exploring)
                {
                    return;
                }
            }

            HandleMovement();
        }

        [Header("Mobile Touch Input (Optional)")]
        [SerializeField] private VirtualJoystick mobileJoystick;
        [SerializeField] private bool mobileSprintActive = false;

        public void SetMobileSprint(bool active) => mobileSprintActive = active;

        private void HandleMovement()
        {
            isGrounded = characterController.isGrounded;
            if (isGrounded && velocity.y < 0)
            {
                velocity.y = -2f;
            }

            // Read keyboard input as baseline
            float horizontal = Input.GetAxisRaw("Horizontal");
            float vertical = Input.GetAxisRaw("Vertical");
            bool isRunning = Input.GetKey(KeyCode.LeftShift) || mobileSprintActive;

            // Blend / override with mobile virtual joystick if touch input is active
            if (mobileJoystick != null && mobileJoystick.InputVector.sqrMagnitude > 0.01f)
            {
                horizontal = mobileJoystick.Horizontal;
                vertical = mobileJoystick.Vertical;
            }

            Vector3 direction = new Vector3(horizontal, 0f, vertical).normalized;

            if (direction.magnitude >= 0.1f)
            {
                float targetAngle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg;
                if (mainCamera != null)
                {
                    targetAngle += mainCamera.transform.eulerAngles.y;
                }

                float angle = Mathf.LerpAngle(transform.eulerAngles.y, targetAngle, Time.deltaTime * stats.rotationSpeed);
                transform.rotation = Quaternion.Euler(0f, angle, 0f);

                Vector3 moveDir = Quaternion.Euler(0f, targetAngle, 0f) * Vector3.forward;
                float currentSpeed = isRunning ? stats.runSpeed : stats.walkSpeed;

                characterController.Move(moveDir.normalized * (currentSpeed * Time.deltaTime));
            }

            velocity.y += gravity * Time.deltaTime;
            characterController.Move(velocity * Time.deltaTime);
        }
    }
}
