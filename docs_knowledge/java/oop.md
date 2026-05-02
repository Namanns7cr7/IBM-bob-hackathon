# Object-Oriented Programming in Java

## What is OOP?

Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects" which contain data (fields/attributes) and code (methods/functions).

## Key Concepts

### Classes and Objects

A **class** is a blueprint for creating objects. An **object** is an instance of a class.

```java
public class Car {
    // Fields (attributes)
    private String brand;
    private int year;
    
    // Constructor
    public Car(String brand, int year) {
        this.brand = brand;
        this.year = year;
    }
    
    // Method
    public void drive() {
        System.out.println("The " + brand + " is driving");
    }
}

// Creating an object
Car myCar = new Car("Toyota", 2023);
myCar.drive();
```

### Encapsulation

Encapsulation means hiding internal details and exposing only what's necessary through public methods.

- Use `private` for fields
- Use `public` getters and setters

### Inheritance

Inheritance allows a class to inherit properties and methods from another class.

```java
public class ElectricCar extends Car {
    private int batteryCapacity;
    
    public ElectricCar(String brand, int year, int batteryCapacity) {
        super(brand, year);
        this.batteryCapacity = batteryCapacity;
    }
}
```

### Polymorphism

Polymorphism allows objects of different classes to be treated as objects of a common parent class.

### Why OOP?

- **Modularity**: Code is organized into reusable classes
- **Maintainability**: Changes in one class don't affect others
- **Reusability**: Classes can be reused across projects
- **Flexibility**: Polymorphism allows flexible code design