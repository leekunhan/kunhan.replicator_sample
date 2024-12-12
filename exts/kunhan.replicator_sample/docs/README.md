# Replicator Sample Extension
Dynamic Shape Creation and Randomization for Omniverse Projects

---

## Overview
The Replicator Sample Extension provides a robust interface to create, randomize, and manage 3D primitives or imported USD models in the NVIDIA Omniverse. Users can define object semantics, apply randomized transformations, and generate synthetic data with Replicator functionality. This extension is highly customizable and includes support for annotators, camera creation, and output configuration.

---

## UI Overview

### Create
The Create section allows users to generate primitives or load USD files as objects in the scene, with configurable semantics and counts.

#### Shape Creation:
- Select from predefined shapes (cube, sphere, etc.).
- Assign semantic labels.
- Specify the number of instances to generate.

Example:
- Shape: Cube
- Semantic Label: Obstacle
- Count: 10

Result: Creates 10 cubes with the semantic label Obstacle.

#### USD Import:
- Import a USD file and assign it a semantic label and count.

Example:
- USD File: models/robot.usd
- Semantic Label: Robot
- Count: 5

Result: Creates 5 instances of the USD model with the semantic label Robot.

---

### Randomizer
The Randomizer section introduces random transformations to existing objects.

- Path Selector: Choose object paths from the stage.
- Position Randomization: Apply a uniform distribution within defined ranges for X, Y, and Z coordinates.
- Rotation Randomization: Apply a uniform distribution for rotation angles on X, Y, and Z axes.

Example Configurations:
- Position Min: (-10, -10, 0)
- Position Max: (10, 10, 5)
- Rotation Min: (0, 0, 0)
- Rotation Max: (360, 360, 0)

Click Register to apply these transformations to the selected objects.

---

### Writer
The Writer section enables users to define output settings for synthetic data generation.

- Annotators: Select data to export (e.g., RGB, bounding boxes, segmentation).
- Output Directory: Specify where data files will be stored.
- Preview/Run Controls:
  - Preview: Test configurations without writing data.
  - Run: Generate and export data files for each frame.

---

### Camera
The Camera section allows for camera creation and configuration:

- Name: Assign a unique name for the camera.
- Resolution: Define the X and Y resolution.
- Render Product: Generate a camera render product for annotations and data generation.

Example Configuration:
- Camera Name: MainCamera
- Resolution: 1920 x 1080

Click Create Camera to add the camera to the scene.

---

### Reset
Click the Reset button to remove all Replicator graphs and clear the current session.

---

## Technical Features

1. Shape Options:
   - Cube, Sphere, Cylinder, Cone, Torus, Plane.

2. Transformations:
   - Randomized position and rotation.

3. USD Support:
   - Load models directly from .usd, .usda, or .usdc files.

4. Annotations:
   - Options: RGB, bounding boxes, semantic segmentation, instance segmentation, normals.

5. Camera Integration:
   - Directly link the camera to synthetic data generation pipelines.

---

This extension provides a versatile toolset for creating dynamic environments, perfect for machine learning, simulation, and virtual world generation.
