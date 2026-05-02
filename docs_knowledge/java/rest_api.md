# REST API in Spring Boot

## What is REST?

REST (Representational State Transfer) is an architectural style for building web services using HTTP methods.

## HTTP Methods

- **GET**: Retrieve data
- **POST**: Create new data
- **PUT**: Update existing data
- **DELETE**: Delete data

## Spring Boot REST Annotations

### @RestController

Marks a class as a REST controller that returns JSON/XML instead of views.

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    // Methods here
}
```

### @GetMapping

Handle GET requests:

```java
@GetMapping
public List<Product> getAllProducts() {
    return productService.findAll();
}

@GetMapping("/{id}")
public Product getProductById(@PathVariable Long id) {
    return productService.findById(id);
}
```

### @PostMapping

Handle POST requests:

```java
@PostMapping
public Product createProduct(@RequestBody Product product) {
    return productService.save(product);
}
```

### @PutMapping

Handle PUT requests:

```java
@PutMapping("/{id}")
public Product updateProduct(@PathVariable Long id, @RequestBody Product product) {
    return productService.update(id, product);
}
```

### @DeleteMapping

Handle DELETE requests:

```java
@DeleteMapping("/{id}")
public void deleteProduct(@PathVariable Long id) {
    productService.delete(id);
}
```

## Path Variables and Request Parameters

```java
// Path variable: /api/users/123
@GetMapping("/{id}")
public User getUser(@PathVariable Long id) { }

// Query parameter: /api/users?email=test@example.com
@GetMapping
public User getUserByEmail(@RequestParam String email) { }
```

## Request Body

Use `@RequestBody` to receive JSON data:

```java
@PostMapping
public User createUser(@RequestBody User user) {
    return userService.save(user);
}
```

## Response Status

```java
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public User createUser(@RequestBody User user) {
    return userService.save(user);
}
```

## Best Practices

1. Use proper HTTP methods
2. Return appropriate status codes
3. Use meaningful URLs
4. Version your API (/api/v1/users)
5. Handle errors properly
6. Validate input data