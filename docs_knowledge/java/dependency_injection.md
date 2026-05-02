# Dependency Injection in Spring

## What is Dependency Injection?

Dependency Injection (DI) is a design pattern where objects receive their dependencies from external sources rather than creating them internally.

## Why Use DI?

- **Loose Coupling**: Classes don't create their dependencies
- **Testability**: Easy to inject mock objects for testing
- **Flexibility**: Easy to swap implementations
- **Maintainability**: Changes in dependencies don't affect the class

## How Spring Does DI

Spring manages object creation and wiring through its IoC (Inversion of Control) container.

### @Autowired

The most common way to inject dependencies:

```java
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    // Spring automatically injects UserRepository
}
```

### Constructor Injection (Recommended)

```java
@Service
public class UserService {
    
    private final UserRepository userRepository;
    
    @Autowired  // Optional in Spring 4.3+
    public class UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

### Field Injection

```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
}
```

## Best Practices

1. **Prefer Constructor Injection**: Makes dependencies explicit and enables immutability
2. **Use Interfaces**: Inject interfaces, not concrete classes
3. **Avoid Circular Dependencies**: If A depends on B and B depends on A, redesign

## Example

```java
// Interface
public interface EmailService {
    void sendEmail(String to, String message);
}

// Implementation
@Service
public class GmailService implements EmailService {
    public void sendEmail(String to, String message) {
        // Send via Gmail
    }
}

// Usage
@Service
public class UserService {
    private final EmailService emailService;
    
    public UserService(EmailService emailService) {
        this.emailService = emailService;
    }
    
    public void registerUser(User user) {
        // Save user
        emailService.sendEmail(user.getEmail(), "Welcome!");
    }
}
```

Spring automatically finds GmailService and injects it into UserService!