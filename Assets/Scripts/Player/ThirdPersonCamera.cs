using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.Player
{
    public class ThirdPersonCamera : MonoBehaviour
    {
        [Header("Target")]
        [SerializeField] private Transform target;

        [Header("Distance & Angles")]
        [SerializeField] private float distance = 4.5f;
        [SerializeField] private float height = 1.8f;
        [SerializeField] private float mouseSensitivity = 3.0f;
        [SerializeField] private float rotationSmoothTime = 0.12f;

        private float yaw;
        private float pitch;
        private Vector3 currentVelocity;

        private void Start()
        {
            if (target == null)
            {
                var player = GameObject.FindWithTag("Player");
                if (player != null) target = player.transform;
            }
        }

        [Header("Mobile Touch Input (Optional)")]
        [SerializeField] private MobileTouchField touchField;

        private void LateUpdate()
        {
            if (target == null) return;

            if (ServiceLocator.TryGet<GameManager>(out var gm) && gm.CurrentState != GameState.Exploring)
            {
                return;
            }

            // Mouse look (Right Click or Editor)
            if (Input.GetMouseButton(1))
            {
                yaw += Input.GetAxis("Mouse X") * mouseSensitivity;
                pitch -= Input.GetAxis("Mouse Y") * mouseSensitivity;
            }

            // Touch Look (Mobile drag field)
            if (touchField != null && touchField.TouchDist.sqrMagnitude > 0.001f)
            {
                yaw += touchField.TouchDist.x * mouseSensitivity;
                pitch -= touchField.TouchDist.y * mouseSensitivity;
            }

            pitch = Mathf.Clamp(pitch, -10f, 60f);

            Vector3 targetPosition = target.position + Vector3.up * height;
            Quaternion rotation = Quaternion.Euler(pitch, yaw, 0f);
            Vector3 offset = rotation * new Vector3(0f, 0f, -distance);

            transform.position = Vector3.SmoothDamp(transform.position, targetPosition + offset, ref currentVelocity, rotationSmoothTime);
            transform.LookAt(targetPosition);
        }
    }
}
