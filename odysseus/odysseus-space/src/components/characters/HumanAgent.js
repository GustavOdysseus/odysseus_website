import React, { useRef, useEffect } from 'react';
import { useGLTF, useAnimations } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

export default function HumanAgent({ position, name, role, status, onClick }) {
  const group = useRef();
  // Note: You'll need to replace this with your actual character model path
  const { nodes, materials, animations } = useGLTF('/models/character.glb');
  const { actions } = useAnimations(animations, group);

  useEffect(() => {
    // Play idle animation by default
    if (actions.idle) {
      actions.idle.play();
    }
  }, [actions]);

  return (
    <group ref={group} position={position} onClick={onClick}>
      <primitive object={nodes.Scene} />
      <Html position={[0, 2, 0]}>
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
