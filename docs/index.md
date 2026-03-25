# NEWPROJECTNAME

Insert project description here.

## Containers

```mermaid
C4Context
Person(user, User, "User with access to the application")
System_Boundary(proj, "NEWPROJECTNAME") {
    Container(proj_proxy, "Caddy proxy")
    Rel(user, proj_proxy, "Use system")
    Rel(proj_proxy, proj_be, "Forward requests")
    Container(proj_be, "FastAPI server", "uvicorn")
        BiRel(proj_be, app_db, "Read/Write data")
    System_Boundary(storage, "Storage"){
        SystemDb(app_db, "Application DB", "PostgreSQL")
    }
}
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")
```

## Technical challenges

Describe the technical challenges here.
