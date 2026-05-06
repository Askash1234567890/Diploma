### Opera Automation Section

## clicker.py

Because Opera is a binary application, automating builds and simulations directly proved difficult. The solution is a **macro clicker** that simulates mouse and keyboard actions according to a predefined scenario, driving Opera through each simulation step automatically.

At the end of each iteration, the clicker calls [`get_harmonics.py`](https://github.com/Askash1234567890/Diploma/tree/main/scripts), which extracts the computed harmonics from Opera's output and appends them to the dataset.
