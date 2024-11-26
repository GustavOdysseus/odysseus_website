# 3D Models for Odysseus Space

This directory should contain the following GLB format 3D models:

1. `character.glb` - Base humanoid character model
2. `commander.glb` - Commander character model
3. `scientist.glb` - Scientist character model
4. `space_station.glb` - Space station model

## Model Requirements

### Character Models
- Should be humanoid models with basic animations (idle, walk, interact)
- Recommended poly count: 10k-15k triangles
- Required animations:
  - idle
  - walk
  - interact
- Texture resolution: 2048x2048 or lower

### Space Station Model
- Sci-fi style space station
- Recommended poly count: 50k-100k triangles
- Should include:
  - Docking areas
  - Living quarters
  - Research facilities
- Texture resolution: 4096x4096 or lower

## Recommended Sources for Models
1. Sketchfab
2. CGTrader
3. Turbosquid
4. Free3D

## Adding New Models
1. Export models in GLB format
2. Ensure proper scale (character height ~1.8 units)
3. Include all textures in the GLB file
4. Test animations before committing
5. Update the corresponding component code if adding new animations

## Note
The models should be optimized for web performance while maintaining visual quality. Consider using compressed textures and optimized geometry when possible.
