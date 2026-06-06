![Zephyr](https://github.com/user-attachments/assets/621614f4-354e-4368-832e-184b75503e86)

## What is Zephyr?

Zephyr is a unique programming language designed around **variables as the primary concept**. Unlike traditional languages where functions and classes are the focus, Zephyr puts variables at the center of everything. This makes it perfect for learning how programming languages actually work under the hood.

All variables in Zephyr are lowercase, and the syntax is designed to be minimal yet powerful. You can use Zephyr to:
- Store and manipulate data
- Perform calculations
- Build logic with conditions and loops
- Create reusable code with functions
- Interact with files and hardware

## Why Learn Zephyr?

### For Learners
If you're interested in understanding **how programming languages work internally** - how they parse code, compile it, and execute it - Zephyr gives you hands-on experience with these concepts. By learning Zephyr, you'll develop a deeper understanding of programming fundamentals that applies to any language.

### For Educators
If you teach programming, Zephyr provides a fresh perspective on teaching core programming concepts. The variable-centric approach makes it easier to explain what happens "behind the scenes" when code runs.

### For Curious Developers
If you've always wondered how compilation and execution really work, Zephyr demystifies these processes with practical, working examples.

## Key Features

- **Variable-Centric Design**: Variables are not just containers for data - they're the foundation of the entire language structure
- **Educational Focus**: Every feature is designed to teach you something about how programming languages work
- **Simple Syntax**: Minimal, clear syntax means less time learning syntax rules and more time understanding concepts
- **Rich Documentation**: This guide includes plenty of examples to help you learn by doing

## Who Should Use This?

- **Intermediate developers** wanting to expand their understanding of programming language design
- **Experienced programmers** exploring innovative teaching approaches
- **Curious learners** interested in diving deeper into how languages work
- **Students and educators** looking for hands-on language learning experiences

## Getting Started

Ready to dive in? Head over to the [Getting Started Guide](overview.md) to write your first Zephyr program..



### Other

* Build .zim documentation:
```bash
mkdocs serve

docker run \
--network host \
  -v $(pwd)/docs:/output \
  ghcr.io/openzim/zimit \
    zimit \
      --seeds http://localhost:8000/Zephyr \
      --name ZephyrDocs.zim \
      --title "Zephyr Documentation" \
      --creator "DeyanM1" \
      --publisher "DeyanM1" \
      --lang "en" \
      --description "Full documentation of the Zephyr programming Language by DeyanM1"
```
