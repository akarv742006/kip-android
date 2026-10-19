using System;
using System.Collections.Generic;

namespace Kingmakers.Core
{
    public static class EventBus
    {
        private static readonly Dictionary<Type, List<Delegate>> EventListeners = new Dictionary<Type, List<Delegate>>();

        public static void Subscribe<T>(Action<T> listener)
        {
            Type type = typeof(T);
            if (!EventListeners.ContainsKey(type))
            {
                EventListeners[type] = new List<Delegate>();
            }
            EventListeners[type].Add(listener);
        }

        public static void Unsubscribe<T>(Action<T> listener)
        {
            Type type = typeof(T);
            if (EventListeners.ContainsKey(type))
            {
                EventListeners[type].Remove(listener);
            }
        }

        public static void Publish<T>(T eventArgs)
        {
            Type type = typeof(T);
            if (EventListeners.TryGetValue(type, out var listeners))
            {
                for (int i = listeners.Count - 1; i >= 0; i--)
                {
                    if (listeners[i] is Action<T> action)
                    {
                        action.Invoke(eventArgs);
                    }
                }
            }
        }

        public static void ClearAll()
        {
            EventListeners.Clear();
        }
    }

    // Common Event Payload Structures
    public struct GameStateChangedEvent
    {
        public GameState PreviousState;
        public GameState NewState;

        public GameStateChangedEvent(GameState prev, GameState next)
        {
            PreviousState = prev;
            NewState = next;
        }
    }

    public struct LanguageChangedEvent
    {
        public string LanguageCode;

        public LanguageChangedEvent(string lang)
        {
            LanguageCode = lang;
        }
    }

    public struct ReputationChangedEvent
    {
        public string Type;
        public int NewValue;
        public int Delta;

        public ReputationChangedEvent(string type, int newValue, int delta)
        {
            Type = type;
            NewValue = newValue;
            Delta = delta;
        }
    }

    public struct ResourceChangedEvent
    {
        public string Category;
        public long NewAmount;
        public long Delta;

        public ResourceChangedEvent(string category, long newAmount, long delta)
        {
            Category = category;
            NewAmount = newAmount;
            Delta = delta;
        }
    }
}
