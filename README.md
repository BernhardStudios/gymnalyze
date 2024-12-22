# Gymnalyze

Python package designed to analyze videos of people training and assess their poses to help improve their movements. Utilizing MediaPipe, this package provides tools for pose estimation and analysis, making it easier for users to understand and enhance their physical performance.

## Installation
To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage
To use the gymnalyze package, you can follow these steps:

1. Import the necessary classes from the package:
   ```python
   from gymnalyze.analyzer import PoseAnalyzer
   from gymnalyze.pose_estimator import PoseEstimator
   ```

2. Load a video and analyze it:
   ```python
   analyzer = PoseAnalyzer()
   analyzer.analyze_video('path_to_video.mp4')
   ```

3. Assess the detected poses:
   ```python
   pose_data = ...  # obtained from the analysis
   results = analyzer.assess_pose(pose_data)
   ```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.