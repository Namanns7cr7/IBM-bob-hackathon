# React Basics

## What is React?

React is a JavaScript library for building user interfaces using reusable components.

## Components

Components are the building blocks of React apps. They can be functions or classes.

### Function Component

```javascript
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

### Using Components

```javascript
function App() {
  return (
    <div>
      <Welcome name="Alice" />
      <Welcome name="Bob" />
    </div>
  );
}
```

## JSX

JSX is a syntax extension that looks like HTML but is actually JavaScript.

```javascript
const element = <h1>Hello, world!</h1>;
const name = "Alice";
const greeting = <h1>Hello, {name}!</h1>;
```

## Props

Props (properties) are how you pass data from parent to child components.

```javascript
function UserCard(props) {
  return (
    <div>
      <h2>{props.name}</h2>
      <p>{props.email}</p>
    </div>
  );
}

// Usage
<UserCard name="Alice" email="alice@example.com" />
```

## State with useState

State is data that changes over time. Use `useState` hook to manage state.

```javascript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

## Side Effects with useEffect

Use `useEffect` for side effects like API calls, subscriptions, or DOM updates.

```javascript
import { useState, useEffect } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => setUser(data));
  }, [userId]); // Re-run when userId changes
  
  if (!user) return <div>Loading...</div>;
  
  return <div>{user.name}</div>;
}
```

## Event Handling

```javascript
function Button() {
  const handleClick = () => {
    alert('Button clicked!');
  };
  
  return <button onClick={handleClick}>Click me</button>;
}
```

## Conditional Rendering

```javascript
function Greeting({ isLoggedIn }) {
  if (isLoggedIn) {
    return <h1>Welcome back!</h1>;
  }
  return <h1>Please sign in.</h1>;
}
```

## Lists and Keys

```javascript
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

## Why React?

- **Component-Based**: Build encapsulated components
- **Declarative**: Describe what UI should look like
- **Learn Once, Write Anywhere**: Web, mobile (React Native), desktop
- **Large Ecosystem**: Tons of libraries and tools