using System;
using System.Collections.Generic;
using UnityEngine;

namespace Kingmakers.Core
{
    public static class ServiceLocator
    {
        private static readonly Dictionary<Type, object> Services = new Dictionary<Type, object>();

        public static void Register<T>(T service)
        {
            Type type = typeof(T);
            if (Services.ContainsKey(type))
            {
                Debug.LogWarning($"[ServiceLocator] Service of type {type.Name} is being overwritten.");
            }
            Services[type] = service;
        }

        public static T Get<T>()
        {
            Type type = typeof(T);
            if (Services.TryGetValue(type, out var service))
            {
                return (T)service;
            }
            Debug.LogError($"[ServiceLocator] Service of type {type.Name} is not registered!");
            return default;
        }

        public static bool TryGet<T>(out T service)
        {
            Type type = typeof(T);
            if (Services.TryGetValue(type, out var obj))
            {
                service = (T)obj;
                return true;
            }
            service = default;
            return false;
        }

        public static void Unregister<T>()
        {
            Services.Remove(typeof(T));
        }

        public static void ResetAll()
        {
            Services.Clear();
        }
    }
}
