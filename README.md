# ErrorVision 🛠️

**Beginner-Friendly Python Error Helper with Instant Fix Suggestions**

---

ErrorVision is a Python package that makes debugging **simple, clear, and beginner-friendly**. It enhances Python's default error messages by providing **easy-to-understand explanations** and **practical suggestions** for fixing common coding mistakes. Ideal for beginners, learners, and developers who want faster debugging.

---

## Features

- ✅ Converts complex Python errors into **simple explanations**.
- 💡 Suggests **practical fixes** for common errors like `SyntaxError`, `NameError`, `TypeError`, `IndexError`, `KeyError`, and more.
- 🖥️ Highlights the **exact line of code causing the error**.
- 🌐 Provides a **direct Google search link** for additional guidance.
- 🔹 Works with **threads** and handles uncaught exceptions globally.
- 🎨 Uses `rich` for **colorful, styled, and readable error output**.

---

## Installation

```bash
pip install errorvision
```

## Usage

Enable ErrorVision at the start of your Python script:

```bash
import errorvision.core as ev

ev.enable()

# Example code
print(undeclared_variable)  # Will trigger NameError
```

## Why Use ErrorVision?

- Speeds up learning for **Python beginners**.
- Makes debugging **less frustrating and more intuitive**.
- Provides **contextual guidance** without leaving your terminal.
- Works seamlessly in **scripts, notebooks, and threaded programs**.

---

## FAQ

**Q: Does it work with Python 2 and 3?**  
A: Designed for **Python 3.x**. Some features may not work in Python 2.

**Q: Can it handle multithreaded programs?**  
A: Yes! ErrorVision hooks into `threading.excepthook` for thread-safe error handling.

**Q: What if my code editor already highlights errors?**  
A: ErrorVision works in the **terminal or console**. It complements editor features and gives beginner-friendly explanations.

---

## Contributing

Contributions, suggestions, and bug reports are welcome! Please submit issues or pull requests on GitHub.

1. Fork the repository  
2. Create a new branch (`git checkout -b feature-name`)  
3. Make your changes  
4. Submit a pull request

---

## License

MIT License © 2026

## Author
Muhaiminul Islam Sadat