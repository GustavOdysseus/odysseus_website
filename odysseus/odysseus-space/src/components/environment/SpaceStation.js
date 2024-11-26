import React, { useRef } from 'react';
import { useGLTF } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

export default function SpaceStation({ position = [0, 0, 0] }) {
  const group = useRef();
  // Note: You'll need to replace this with your actual space station model path
  const { nodes } = useGLTF('/models/space_station.glb');

  useFrame((state, delta) => {
    // Add subtle rotation animation
    group.current.rotation.y += delta * 0.05;
  });

  return (
    <group ref={group} position={position}>
      <primitive object={nodes.Scene} />
      <pointLight
        position={[0, 5, 0]}
        intensity={1}
        color="#4090ff"
        distance={20}
      />
    </group>
  );
}
