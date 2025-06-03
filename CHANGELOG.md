# Changelog
[0.2.1] - Corrections to fundamental class functions [2024-06-07]

## 1.1 Corrections -- Function utils
- Refinement of the ft_n and ft_t functions to correct errors with transfer functions with conincident roots;
- The ft_t function now uses control.info["FT"] directly, which corrects the problem of not calculating the points
of the graph for those with the same root solution.


### 1.2 Fixed -- Control Class
- Some properties of the class were not being updated correctly, now they are working as expected;
- Reanimate the function call. Control.time_function is now control.f_time;
- Bug fixes for Control.info is now working as expected;
- Improved graphics and colors parameters
### 1.3  Other Minor Changes
- Some changes to the documentation to make it clearer;
- Reliability improvements to the code and stability improvements.

### 1.4 Future Improvements
- Add test examples to the documentation;
- Impruve plotting options and controls;
- Documentation examples and updates;

### Thanks
- I would like to thank the community for their feedback and suggestions, which have been invaluable in improving
this package. If you have any other suggestions or problems, feel free to open an issue in the GitHub repository.
- If you have any suggestions, problems or bug reports, please send me an e-mail: d2020001214@unifei.edu.br