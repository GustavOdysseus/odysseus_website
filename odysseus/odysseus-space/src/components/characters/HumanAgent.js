import React, { useRef } from 'react';
import { Html } from '@react-three/drei';

export default function HumanAgent({ position, name, role, status, onClick }) {
  const group = useRef();

  return (
    <group ref={group} position={position} onClick={onClick}>
      {/* Temporary basic geometry instead of GLB model */}
      <group>
        {/* Body */}
        <mesh position={[0, 1, 0]}>
          <capsuleGeometry args={[0.3, 1, 4, 8]} />
          <meshStandardMaterial color="#4287f5" />
        </mesh>
        {/* Head */}
        <mesh position={[0, 2, 0]}>
          <sphereGeometry args={[0.25, 16, 16]} />
          <meshStandardMaterial color="#4287f5" />
        </mesh>
      </group>

      <Html position={[0, 2.5, 0]}>
        <div className="character-info bg-black/50 text-white p-2 rounded">
          <div className="font-bold">{name}</div>
          <div className="text-sm">{role}</div>
          <div className={`status ${status === 'active' ? 'text-green-500' : 'text-gray-400'}`}>
            {status}
          </div>
        </div>
      </Html>
    </group>
  );
}
