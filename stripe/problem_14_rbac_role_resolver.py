"""
RBAC Role Resolver (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/c277ed4b-dff5-4e90-8190-375389b51c8d
Reference: Stripe docs on user roles + general RBAC literature.

Implement a role-based access control resolver. Given users, roles,
permissions, and the assignments between them, answer authorization queries.

================================================================================
DATA MODEL
================================================================================

users:        list of user IDs (strings).
roles:        list of role names.
permissions:  list of permission names.

assignments:
    role -> set of permissions       (which perms a role grants)
    user -> set of roles             (which roles a user has)

================================================================================
PART 1: Flat RBAC
================================================================================

A user has perm P iff any role they hold directly grants P.
If a user has multiple roles, effective permissions = UNION.

Function:
    can_part1(user, perm, user_roles, role_perms) -> bool

Example:
    user_roles = {
        "alice": ["editor"],
        "bob":   ["viewer", "auditor"],
        "carol": [],
    }
    role_perms = {
        "editor":  ["read", "write"],
        "viewer":  ["read"],
        "auditor": ["read", "audit"],
    }

    can_part1("alice", "read",    user_roles, role_perms) == True
    can_part1("alice", "write",   user_roles, role_perms) == True
    can_part1("alice", "audit",   user_roles, role_perms) == False
    can_part1("bob",   "audit",   user_roles, role_perms) == True   # via auditor
    can_part1("bob",   "write",   user_roles, role_perms) == False
    can_part1("carol", "read",    user_roles, role_perms) == False  # no roles
    can_part1("dave",  "read",    user_roles, role_perms) == False  # unknown user

================================================================================
PART 2: Role Hierarchy / Inheritance
================================================================================

Roles inherit from parent roles. Effective perms = own UNION transitive
parents. Detect cycles (raise or treat as no-op).

Function:
    can_part2(user, perm, user_roles, role_perms, role_parents) -> bool

Example:
    role_perms = {
        "viewer":      ["read"],
        "editor":      ["write"],
        "admin":       ["delete"],
        "super_admin": ["impersonate"],
    }
    role_parents = {
        # editor inherits from viewer; admin from editor; super_admin from admin
        "editor":      ["viewer"],
        "admin":       ["editor"],
        "super_admin": ["admin"],
    }
    user_roles = {
        "alice": ["super_admin"],
        "bob":   ["editor"],
    }

    can_part2("alice", "read",        user_roles, role_perms, role_parents) == True
        # super_admin -> admin -> editor -> viewer (read)
    can_part2("alice", "impersonate", user_roles, role_perms, role_parents) == True
    can_part2("bob",   "read",        user_roles, role_perms, role_parents) == True
        # editor inherits from viewer
    can_part2("bob",   "delete",      user_roles, role_perms, role_parents) == False
        # editor does NOT inherit upward to admin

    # Cycle detection:
    cyclic_parents = {"a": ["b"], "b": ["a"]}
    can_part2("x", "y", {"x": ["a"]}, {"a": []}, cyclic_parents)
        # Either raise ValueError or return False - confirm with source.

================================================================================
PART 3: Scoped / Resource-level Permissions
================================================================================

Permissions become (action, resource) pairs with wildcard support:
    ("read",  "invoice/*")     matches resource "invoice/123"
    ("write", "invoice/123")   exact match
    ("*",     "invoice/*")     any action on any invoice

Optional explicit DENY rules override allows.

Function:
    can_part3(user, action, resource, user_roles,
              role_perms, role_parents, deny_rules=None) -> bool

Example:
    role_perms = {
        "billing_admin": [("*",     "invoice/*")],
        "support":       [("read",  "invoice/*"), ("read", "customer/*")],
    }
    role_parents = {}
    user_roles = {
        "alice": ["billing_admin"],
        "bob":   ["support"],
    }

    can_part3("alice", "write", "invoice/123", user_roles, role_perms, role_parents) == True
    can_part3("alice", "read",  "customer/5",  user_roles, role_perms, role_parents) == False
    can_part3("bob",   "read",  "invoice/9",   user_roles, role_perms, role_parents) == True
    can_part3("bob",   "write", "invoice/9",   user_roles, role_perms, role_parents) == False

    # With deny rule:
    deny_rules = {"alice": [("write", "invoice/sensitive/*")]}
    can_part3("alice", "write", "invoice/sensitive/42",
              user_roles, role_perms, role_parents, deny_rules) == False
    can_part3("alice", "write", "invoice/123",
              user_roles, role_perms, role_parents, deny_rules) == True
"""


def can_part1(user: str, perm: str,
              user_roles: dict[str, list[str]],
              role_perms: dict[str, list[str]]) -> bool:
    pass


def can_part2(user: str, perm: str,
              user_roles: dict[str, list[str]],
              role_perms: dict[str, list[str]],
              role_parents: dict[str, list[str]]) -> bool:
    pass


def can_part3(*args, **kwargs) -> bool:
    pass


if __name__ == "__main__":
    pass
