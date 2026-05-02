# Spring Boot Basics

## What is Spring Boot?

Spring Boot is a framework that makes it easy to create production-ready Spring applications. It provides auto-configuration and eliminates boilerplate code.

## Core Concepts

### Controllers (@RestController)

Controllers handle HTTP requests and return responses.

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping
    public List<User> getAllUsers() {
        return userService.findAll();
    }
    
    @PostMapping
    public User createUser(@RequestBody User user) {
        return userService.save(user);
    }
}
```

### Service Layer (@Service)

Services contain business logic. They sit between controllers and repositories.

```java
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    public List<User> findAll() {
        return userRepository.findAll();
    }
    
    public User save(User user) {
        // Business logic here
        return userRepository.save(user);
    }
}
```

### Repository Layer (@Repository)

Repositories handle database operations.

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByEmail(String email);
}
```

### Entities (@Entity)

Entities represent database tables.

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String email;
    
    // Getters and setters
}
```

## Layered Architecture

```
Client Request
    ↓
Controller (HTTP handling)
    ↓
Service (Business logic)
    ↓
Repository (Data access)
    ↓
Database
```

## Why This Architecture?

- **Separation of Concerns**: Each layer has a specific responsibility
- **Testability**: Easy to test each layer independently
- **Maintainability**: Changes in one layer don't affect others
- **Reusability**: Services can be reused by multiple controllers