"""Convert all glTF/GLB files in subdirectories to STL format.

Applies the following transforms during conversion:
- Y-up to Z-up coordinate system rotation (glTF convention -> STL convention)
- 180° flip around X axis
- 1000x scale (glTF meters -> STL millimeters)
"""

import os
import glob

import numpy as np
import trimesh


def convert(src: str, dst: str) -> None:
    scene = trimesh.load(src)
    if isinstance(scene, trimesh.Scene):
        mesh = scene.to_mesh()
    else:
        mesh = scene

    # Y-up to Z-up
    rot = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])
    mesh.apply_transform(rot)

    # Flip upside-down
    flip = trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])
    mesh.apply_transform(flip)

    # Meters to millimeters
    scale = np.eye(4) * 1000
    scale[3, 3] = 1
    mesh.apply_transform(scale)

    mesh.export(dst)


def main() -> None:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    patterns = ["**/*.glb", "**/*.gltf"]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(repo_root, pattern), recursive=True))

    if not files:
        print("No glTF/GLB files found.")
        return

    for src in sorted(files):
        dst = os.path.splitext(src)[0] + ".stl"
        print(f"Converting {os.path.relpath(src, repo_root)} -> {os.path.relpath(dst, repo_root)}")
        convert(src, dst)

    print(f"Done. Converted {len(files)} file(s).")


if __name__ == "__main__":
    main()
