import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

export default function SpaceStation({ position = [0, 0, 0] }) {
  const group = useRef();

  useFrame((state, delta) => {
    // Add subtle rotation animation
    group.current.rotation.y += delta * 0.05;
  });

  return (
    <group ref={group} position={position}>
      {/* Central Hub */}
      <mesh>
        <sphereGeometry args={[2, 32, 32]} />
        <meshStandardMaterial color="#666666" metalness={0.8} roughness={0.2} />
      </mesh>

      {/* Ring Structure */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[4, 0.5, 16, 100]} />
        <meshStandardMaterial color="#444444" metalness={0.8} roughness={0.2} />
      </mesh>

      {/* Solar Panels */}
      <group rotation={[0, Math.PI / 4, 0]}>
        <mesh position={[5, 0, 0]}>
          <boxGeometry args={[4, 0.1, 1]} />
          <meshStandardMaterial color="#1E90FF" metalness={0.6} roughness={0.2} />
        </mesh>
        <mesh position={[-5, 0, 0]}>
          <boxGeometry args={[4, 0.1, 1]} />
          <meshStandardMaterial color="#1E90FF" metalness={0.6} roughness={0.2} />
        </mesh>
      </group>

      {/* Station Lights */}
      <pointLight position={[0, 5, 0]} intensity={1} color="#4090ff" distance={20} />
      <pointLight position={[0, -5, 0]} intensity={0.5} color="#4090ff" distance={15} />
    </group>
  );
}
