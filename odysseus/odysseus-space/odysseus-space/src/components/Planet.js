import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text } from '@react-three/drei';
import { useAtom } from 'jotai';
import { visualSettingsAtom } from '../context/atoms';

const Planet = React.memo(({ position, name, color, description, onHover, onClick, scale = 1 }) => {
  const [hovered, setHovered] = useState(false);
  const meshRef = useRef();
  const atmosphereRef = useRef();
  const [visualSettings] = useAtom(visualSettingsAtom);

  useFrame(() => {
    if (meshRef.current) meshRef.current.rotation.y += 0.002;
    if (atmosphereRef.current) atmosphereRef.current.rotation.y -= 0.001;
  });

  return (
    <group position={position} scale={scale * visualSettings.planetSize}>
      <mesh ref={atmosphereRef} scale={hovered ? 1.6 : 1.5}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshBasicMaterial color={color} transparent opacity={0.1} />
      </mesh>
      <mesh
        ref={meshRef}
        onClick={onClick}
        onPointerOver={() => {
          setHovered(true);
          onHover?.({ description, position });
        }}
        onPointerOut={() => {
          setHovered(false);
          onHover?.(null);
        }}
      >
        <sphereGeometry args={[1, 32, 32]} />
        <meshPhongMaterial color={color} emissive={color} emissiveIntensity={0.2} shininess={50} />
      </mesh>
      {visualSettings.showLabels && (
        <Text position={[0, 1.5, 0]} fontSize={0.5} color="white" anchorX="center" anchorY="middle">
          {name}
        </Text>
      )}
    </group>
  );
});

export default Planet;
