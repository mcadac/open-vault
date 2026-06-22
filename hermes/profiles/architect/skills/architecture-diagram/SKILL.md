---
name: architecture-diagram
description: Create ASCII or Mermaid diagrams for system components, data flows, and API contracts
metadata:
  hermes:
    tags: [architecture, diagrams, documentation, mermaid]
---

# Architecture Diagram

Include a diagram in every ADR. A diagram communicates structure faster than prose.

## When to use

In the **Decision** or **Data Models** section of an ADR when:
- Multiple components interact
- Data flows through the system
- API contracts need visual clarification

## Mermaid (preferred)

Mermaid renders in GitHub, Obsidian, and most doc tools.

### Component diagram
```mermaid
graph TD
    Client -->|POST /auth/login| API
    API -->|verify| AuthService
    AuthService -->|query| UserDB
    AuthService -->|issue| TokenStore
    API -->|JWT| Client
```

### Sequence diagram
```mermaid
sequenceDiagram
    Client->>API: POST /auth/login {email, password}
    API->>AuthService: verify(email, password)
    AuthService->>UserDB: SELECT WHERE email=?
    UserDB-->>AuthService: user row
    AuthService-->>API: {userId, roles}
    API-->>Client: {token, refreshToken}
```

### Entity diagram
```mermaid
erDiagram
    USER {
        uuid id PK
        string email
        string password_hash
    }
    SESSION {
        uuid id PK
        uuid user_id FK
        timestamp expires_at
    }
    USER ||--o{ SESSION : "has"
```

## ASCII fallback

Use when Mermaid isn't supported:

```
[Client] --POST /login--> [API Gateway] --> [Auth Service] --> [User DB]
                                                    |
                                              [Token Store]
```

## Rules

- Label every arrow with the data or action it carries
- Show external systems (DB, third-party APIs) as distinct boxes
- Keep diagrams focused — one concern per diagram
- Don't include implementation details (no method names, no internal variables)
