# Changelog
[v 0.2.30] - Severe changes to the logic of how the code works, making it more reliable, faster and minimizing the 
chance of error in more complex transfer functions. [2024-06-24]

### 1.1 Refactoring the code on functions.py
- Transfer functions are now of type control.TransferFunction. In the previous version, the codes were being written
in a symbolic language (sympy). The change was made to minimize the chance of error when getting the answer in time;
- Refactored the code to improve readability and maintainability.
- The function ft_s is now named as ft_setter, the update;
- Correction on the name function root_locus, now it is root_locus;
- The function root_locus is now working with control.root_locus_map and control.root_locus_plot, due to better 
performance and stability;
- ft_t is working as expected, solving several errors happening in the previous version;

### 1.2 Controle.py—Main changes.
-  The time_f method is now called step, and will return the system's response when subjected to a unit step;
-  Now it's possible to calculate the system's response on a closed loop, using the method closed_loop;


