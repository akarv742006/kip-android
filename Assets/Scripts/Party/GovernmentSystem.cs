using UnityEngine;
using Kingmakers.Core;

namespace Kingmakers.Party
{
    public enum GovernmentRole
    {
        Activist,
        PartyMember,
        Candidate,
        MLA,
        StateMinister,
        ChiefMinister,
        MP,
        UnionMinister,
        PrimeMinister,
        PartyPresident
    }

    public class GovernmentSystem : MonoBehaviour
    {
        public static GovernmentSystem Instance { get; private set; }

        [SerializeField] private GovernmentRole currentRole = GovernmentRole.Activist;

        public GovernmentRole CurrentRole => currentRole;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ServiceLocator.Register<GovernmentSystem>(this);
        }

        public void PromoteRole(GovernmentRole newRole)
        {
            if (newRole > currentRole)
            {
                GovernmentRole oldRole = currentRole;
                currentRole = newRole;
                Debug.Log($"[GovernmentSystem] PROMOTION! {oldRole} -> {newRole}");
            }
        }

        public void SetRoleDirect(GovernmentRole role)
        {
            currentRole = role;
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                ServiceLocator.Unregister<GovernmentSystem>();
            }
        }
    }
}
