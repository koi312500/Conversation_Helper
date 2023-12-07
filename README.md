# Conversation_Helper
This program helps conversation for a person who lacks language.
It exchange complicated korean expression to easy expression and review complicated korean expression according to "Forgetting curve theory".


It uses socket to communicate with python program and processing program.

## How to run
1. Install python libraries to execute files.
    - `pip install -r requirements.txt` to install all libraries.
2. Edit `config.py` to your own opendict_KEY. (우리말샘 OPENAPI Key)
3. Edit `Conversation_Helper.pde`'s 10th line to your font
    - Edit this line. `mainFont = createFont("D2Coding", 16);`
    - Replace D2Coding to your installed font which support hangul.
4. Execute `main.py` and `Conversation_Helper.pde`
    - Execute `main.py` first. (Because python program is server.)
    - Execute `Conversation_Helper.pde` second. (Because processing program is client.)
