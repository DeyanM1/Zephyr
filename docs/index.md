![www](https://github.com/user-attachments/assets/621614f4-354e-4368-832e-184b75503e86)


## Introduction

Zephyr is a variable-based programming language designed for simplicity and efficiency. In Zephyr, all variables are lowercase, and the syntax is minimalistic, allowing you to define and manipulate variables, perform calculations, and structure your programs using loops, functions, and conditional logic.


### Vision and Purpose
Welcome to the Zephyr project! My goal is to create the world's first variable-based programming language, designed to provide an innovative and intuitive approach to understanding the inner workings of programming languages. This language is tailored for intermediate to professional developers who want to deepen their knowledge of how programming languages parse, compile, and execute code.

### Why This Language?
Programming languages often abstract away the low-level details of how they handle code, making it challenging for developers to fully grasp the mechanics of compilation and execution. With Zephyr, I aim to bridge this gap. By focusing on variables as a central concept, this language provides developers with a clear, hands-on perspective on how code is processed under the hood.

### Key Features
- Variable-Centric Design: A unique syntax and structure that revolve around variables as the primary building blocks of code.
- Educational Focus: Ideal for developers who want to learn or teach the concepts of parsing and compiling in a practical way.
- Comprehensive Documentation: The language comes with detailed, beginner-friendly, and well-organized documentation to help users understand its syntax, features, and concepts thoroughly.

### Who Is It For?
This language is intended for:

- Intermediate developers who want to expand their understanding of programming language design.
- Experienced professionals exploring innovative ways to teach or experiment with compilation processes.
- Curious learners interested in diving deeper into how programming languages work behind the scenes.




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