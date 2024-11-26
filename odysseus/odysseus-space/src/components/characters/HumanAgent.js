import React, { useRef, useEffect, useState } from 'react';
import { useGLTF, Html } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function HumanAgent({ position, name, role, status, onClick }) {
  const group = useRef();
  const [bodyParams, setBodyParams] = useState({
    height: 1.75,
    neckGirth: 0.35,
    chestGirth: 0.9,
    waistGirth: 0.8,
    hipGirth: 0.9,
    inseam: 0.8
  });

  // Load the base human model
  const { nodes, materials } = useGLTF('/models/temp-models/models/human_male.obj');

  useEffect(() => {
    if (nodes && nodes.HumanBody) {
      // Apply body parameters to mesh
      const mesh = nodes.HumanBody;
      const positions = mesh.geometry.attributes.position.array;

      // Scale height
      for (let i = 0; i < positions.length; i += 3) {
        positions[i + 1] *= bodyParams.height;
      }

      // Apply girths (simplified example)
      const applyGirth = (yMin, yMax, scale) => {
        for (let i = 0; i < positions.length; i += 3) {
          const y = positions[i + 1];
          if (y >= yMin && y <= yMax) {
            positions[i] *= scale;
            positions[i + 2] *= scale;
          }
        }
      };

      // Apply different girths to different body sections
      applyGirth(1.5, 1.6, bodyParams.neckGirth);  // Neck
      applyGirth(1.2, 1.4, bodyParams.chestGirth); // Chest
      applyGirth(0.9, 1.1, bodyParams.waistGirth); // Waist
      applyGirth(0.6, 0.8, bodyParams.hipGirth);   // Hip

      mesh.geometry.attributes.position.needsUpdate = true;
      mesh.geometry.computeVertexNormals();
    }
  }, [nodes, bodyParams]);

  // Hover effect
  const [hovered, setHovered] = useState(false);
  const baseColor = new THREE.Color('#4287f5');
  const hoverColor = new THREE.Color('#42aff5');

  useFrame((state, delta) => {
    if (group.current) {
      // Subtle floating animation
      group.current.position.y = position[1] + Math.sin(state.clock.elapsedTime) * 0.1;
      
      // Color interpolation on hover
      if (materials && materials.HumanBody) {
        materials.HumanBody.color.lerp(
          hovered ? hoverColor : baseColor,
          delta * 4
        );
      }
    }
  });

  return (
    <group 
      ref={group} 
      position={position}
      onClick={onClick}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      {nodes && <primitive object={nodes.HumanBody} />}

      <Html position={[0, 2.5, 0]}>
        <div className="character-info bg-black/50 text-white p-2 rounded">
          <div className="font-bold">{name}</div>
          <div className="text-sm">{role}</div>
          <div className={`status ${status === 'active' ? 'text-green-500' : 'text-gray-400'}`}>
            {status}
          </div>
        </div>
      </Html>

      {/* Debug UI for body parameters */}
      {hovered && (
        <Html position={[1, 0, 0]}>
          <div className="bg-black/70 text-white p-2 rounded text-sm">
            <div>Height: {bodyParams.height.toFixed(2)}m</div>
            <div>Neck: {bodyParams.neckGirth.toFixed(2)}m</div>
            <div>Chest: {bodyParams.chestGirth.toFixed(2)}m</div>
            <div>Waist: {bodyParams.waistGirth.toFixed(2)}m</div>
            <div>Hip: {bodyParams.hipGirth.toFixed(2)}m</div>
          </div>
        </Html>
      )}
    </group>
  );
}

// Preload the model
useGLTF.preload('/models/temp-models/models/human_male.obj');
