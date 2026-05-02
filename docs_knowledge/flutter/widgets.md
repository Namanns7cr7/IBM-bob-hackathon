# Flutter Widgets

## What are Widgets?

In Flutter, everything is a widget. Widgets are the building blocks of Flutter apps.

## Stateless vs Stateful Widgets

### StatelessWidget

A widget that doesn't change over time.

```dart
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Text('Hello World');
  }
}
```

### StatefulWidget

A widget that can change over time.

```dart
class Counter extends StatefulWidget {
  @override
  _CounterState createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int count = 0;
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () {
            setState(() {
              count++;
            });
          },
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

## Common Widgets

### Container

A box that can contain other widgets:

```dart
Container(
  width: 200,
  height: 100,
  color: Colors.blue,
  child: Text('Hello'),
)
```

### Column and Row

Layout widgets for vertical and horizontal arrangement:

```dart
Column(
  children: [
    Text('First'),
    Text('Second'),
    Text('Third'),
  ],
)

Row(
  children: [
    Icon(Icons.star),
    Text('Rating'),
  ],
)
```

### ListView

Scrollable list of widgets:

```dart
ListView(
  children: [
    ListTile(title: Text('Item 1')),
    ListTile(title: Text('Item 2')),
    ListTile(title: Text('Item 3')),
  ],
)
```

### Stack

Overlay widgets on top of each other:

```dart
Stack(
  children: [
    Image.network('url'),
    Positioned(
      bottom: 10,
      right: 10,
      child: Text('Caption'),
    ),
  ],
)
```

## setState()

To update the UI, call `setState()`:

```dart
void incrementCounter() {
  setState(() {
    count++;
  });
}
```

## Widget Tree

Flutter builds a tree of widgets:

```
MaterialApp
  └─ Scaffold
      ├─ AppBar
      └─ Body
          └─ Column
              ├─ Text
              └─ Button
```

## Why Widgets?

- **Composable**: Build complex UIs from simple widgets
- **Reusable**: Create custom widgets and reuse them
- **Declarative**: Describe what the UI should look like
- **Fast**: Flutter renders widgets efficiently