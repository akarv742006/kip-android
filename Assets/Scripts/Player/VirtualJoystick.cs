using UnityEngine;
using UnityEngine.EventSystems;

namespace Kingmakers.Player
{
    /// <summary>
    /// AAA-grade floating/anchored virtual joystick for Android touchscreens.
    /// Supports multi-touch, touch drag, elastic return, and normalized output vector.
    /// </summary>
    public class VirtualJoystick : MonoBehaviour, IPointerDownHandler, IDragHandler, IPointerUpHandler
    {
        [Header("Joystick Settings")]
        [SerializeField] private RectTransform background;
        [SerializeField] private RectTransform handle;
        [SerializeField] private float handleRange = 64f;
        [SerializeField] private bool dynamicFloating = true;

        private Vector2 inputVector = Vector2.zero;
        private Canvas canvas;
        private Vector2 initialPosition;

        public Vector2 InputVector => inputVector;
        public float Horizontal => inputVector.x;
        public float Vertical => inputVector.y;

        private void Awake()
        {
            canvas = GetComponentInParent<Canvas>();
            if (background != null)
            {
                initialPosition = background.anchoredPosition;
            }
        }

        public void OnPointerDown(PointerEventData eventData)
        {
            if (dynamicFloating && background != null)
            {
                RectTransformUtility.ScreenPointToLocalPointInRectangle(
                    canvas.transform as RectTransform,
                    eventData.position,
                    canvas.worldCamera,
                    out Vector2 localPoint
                );
                background.anchoredPosition = localPoint;
            }

            OnDrag(eventData);
        }

        public void OnDrag(PointerEventData eventData)
        {
            if (background == null || handle == null) return;

            Vector2 position = RectTransformUtility.WorldToScreenPoint(canvas.worldCamera, background.position);
            Vector2 radius = background.sizeDelta / 2f;
            Vector2 rawInput = (eventData.position - position) / (radius * (canvas != null ? canvas.scaleFactor : 1f));

            inputVector = (rawInput.magnitude > 1f) ? rawInput.normalized : rawInput;
            handle.anchoredPosition = inputVector * handleRange;
        }

        public void OnPointerUp(PointerEventData eventData)
        {
            inputVector = Vector2.zero;
            if (handle != null)
            {
                handle.anchoredPosition = Vector2.zero;
            }

            if (dynamicFloating && background != null)
            {
                background.anchoredPosition = initialPosition;
            }
        }
    }
}
