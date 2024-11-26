import React, { useRef, useState } from 'react';
import { useSpring, animated } from '@react-spring/three';
import { Text, Html } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

export default function TaskModule({ position, task, status, assignedAgents, onClick }) {
  const group = useRef();
  const [hovered, setHovered] = useState(false);

  const { scale } = useSpring({
    scale: hovered ? 1.2 : 1,
    config: { tension: 300, friction: 10 },
  });

  useFrame((state, delta) => {
    // Add floating animation
    group.current.position.y += Math.sin(state.clock.elapsedTime) * 0.001;
  });

  return (
    <animated.group
      ref={group}
      position={position}
      scale={scale}
      onClick={onClick}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      {/* Task Module Visualization */}
      <mesh>
        <boxGeometry args={[2, 2, 2]} />
        <meshPhongMaterial
          color={status === 'completed' ? '#4CAF50' : status === 'in-progress' ? '#2196F3' : '#9E9E9E'}
          opacity={0.8}
          transparent
        />
      </mesh>

      {/* Holographic Display */}
      <Html position={[0, 2.5, 0]}>
        <div className="task-info bg-black/70 text-white p-3 rounded-lg min-w-[200px]">
          <h3 className="text-lg font-bold mb-2">{task.name}</h3>
          <p className="text-sm mb-2">{task.description}</p>
          <div className="text-xs">
            <div className="flex justify-between mb-1">
              <span>Status:</span>
              <span className={
                status === 'completed' ? 'text-green-400' :
                status === 'in-progress' ? 'text-blue-400' :
                'text-gray-400'
              }>{status}</span>
            </div>
            <div>
              <span>Assigned Agents:</span>
              <ul className="list-disc list-inside">
                {assignedAgents.map((agent, idx) => (
                  <li key={idx} className="text-blue-300">{agent}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </Html>

      {/* Energy Beam Effect */}
      <mesh position={[0, -1, 0]}>
        <cylinderGeometry args={[0.1, 0.1, 2, 16]} />
        <meshBasicMaterial color="#4fc3f7" opacity={0.3} transparent />
      </mesh>
    </animated.group>
  );
}
