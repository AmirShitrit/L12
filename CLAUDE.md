# Guide

1. Use the uv virtual environment for managing packages and running the project.
2. Before modifying any files, show me your plan first and wait for my approval.
3. For every change/addition to the code behavior that involves pure logic (w/out side-effects), add a unit test first, and see that it fails.
   - If needed, make the code more testable by pushing side-effects to the edges using something like the Onion Architecture, or something simpler, when relevant.
4. When writing code:
   - Follow clean code and SOLID principles. 
   - Keep the code simple and readable.
   - Make the code self-explanatory using clear names.
     Avoid using comments, when possible.
   - Don't mix and match different levels of abstraction.
     Each function should stick to a single level of abstraction, delegating to sub-functions, if necessary.
   - The code should be efficient. For example, try to cache the results of repeated queries that don't change often.
5. Do not commit code. Only modify files and let me do the committing.
6. Output feedback on this file, prompts and the PRD.md file to FEEDBACK.md in the root folder of the project.