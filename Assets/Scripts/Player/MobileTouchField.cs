using UnityEngine;
using UnityEngine.EventSystems;

namespace Kingmakers.Player
{
    /// <summary>
    /// Touch drag field for smooth mobile orbital camera look on Android.
    /// Eliminates camera jumps and provides smooth delta tracking.
    /// </summary>
    public class MobileTouchField : MonoBehaviour, IPointerDownHandler, IPointerUpHandler
    {
        [SerializeField] private float sensitivity = 0.2f;

        private Vector2 touchDist;
        private Vector2 pointerOld;
        private int pointerId;
        private bool isPressed;

        public Vector2 TouchDist => isPressed ? touchDist : Vector2.zero;

        private void Update()
        {
            if (isPressed)
            {
                if (pointerId >= 0 && pointerId < Input.touches.Length)
                {
                    touchDist = (Input.touches[pointerId].position - pointerOld) * sensitivity;
                    pointerOld = Input.touches[pointerId].position;
                }
                else
                {
                    Vector2 currentMousePos = new Vector2(Input.mousePosition.x, Input.mousePosition.y);
                    touchDist = (currentMousePos - pointerOld) * sensitivity;
                    pointerOld = currentMousePos;
                }
            }
            else
            {
                touchDist = Vector2.zero;
            }
        }

        public void OnPointerDown(PointerEventData eventData)
        {
            isPressed = true;
            pointerId = eventData.pointerId;
            pointerOld = eventData.position;
        }

        public void OnPointerUp(PointerEventData eventData)
        {
            isPressed = false;
        }
    }
}
