import React, { useRef, useEffect, useState, useCallback, memo } from 'react';
import { useGLTF, Html } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useSpaceStore } from '../../state/store';
import { Agent } from '../../types';
import { crewAIService } from '../../services/crewAI';

const STATUS_COLORS = {
  active: new THREE.Color('#4CAF50'),
  inactive: new THREE.Color('#9E9E9E'),
} as const;

interface HumanAgentProps {
  agent: Agent;
  onClick?: () => void;
}

const HumanAgent: React.FC<HumanAgentProps> = memo(({ agent, onClick }) => {
  const group = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);
  const [interacting, setInteracting] = useState(false);
  const [response, setResponse] = useState('');

  // Load the base human model
  const { nodes, materials } = useGLTF('/models/human_male.glb');

  // Update mesh based on agent parameters
  useEffect(() => {
    if (!nodes?.HumanBody || !group.current) return;

    const mesh = nodes.HumanBody.clone();
    const positions = mesh.geometry.attributes.position.array;

    // Scale height
    for (let i = 0; i < positions.length; i += 3) {
      positions[i + 1] *= agent.bodyParams.height;
    }

    // Apply girths
    const applyGirth = (yMin: number, yMax: number, scale: number) => {
      for (let i = 0; i < positions.length; i += 3) {
        const y = positions[i + 1];
        if (y >= yMin && y <= yMax) {
          positions[i] *= scale;
          positions[i + 2] *= scale;
        }
      }
    };

    // Apply different girths to different body parts
    applyGirth(1.4, 1.6, agent.bodyParams.neckGirth);
    applyGirth(1.2, 1.4, agent.bodyParams.chestGirth);
    applyGirth(1.0, 1.2, agent.bodyParams.waistGirth);
    applyGirth(0.8, 1.0, agent.bodyParams.hipGirth);
    applyGirth(0.0, 0.8, agent.bodyParams.inseam);

    mesh.geometry.computeVertexNormals();
    
    // Clear existing mesh and add new one
    while (group.current.children.length) {
      group.current.remove(group.current.children[0]);
    }
    group.current.add(mesh);
  }, [agent.bodyParams, nodes]);

  // Handle interaction
  const handleInteraction = useCallback(async () => {
    if (interacting) return;
    
    setInteracting(true);
    try {
      const result = await crewAIService.getAgentResponse(agent.id, 'Tell me about your role');
      setResponse(result.response);
    } catch (error) {
      console.error('Error getting agent response:', error);
      setResponse('Sorry, I am unable to respond at the moment.');
    } finally {
      setInteracting(false);
    }
  }, [agent.id, interacting]);

  // Animation
  useFrame((state) => {
    if (!group.current) return;

    // Hover animation
    group.current.scale.y = THREE.MathUtils.lerp(
      group.current.scale.y,
      hovered ? 1.1 : 1,
      0.1
    );

    // Breathing animation
    group.current.position.y = Math.sin(state.clock.elapsedTime) * 0.01;
  });

  return (
    <group
      ref={group}
      position={agent.position}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
      onClick={(e) => {
        e.stopPropagation();
        handleInteraction();
        onClick?.();
      }}
    >
      {/* Status indicator */}
      <mesh position={[0, 2, 0]}>
        <sphereGeometry args={[0.1, 16, 16]} />
        <meshStandardMaterial
          color={STATUS_COLORS[agent.status]}
          emissive={STATUS_COLORS[agent.status]}
          emissiveIntensity={0.5}
        />
      </mesh>

      {/* Info panel */}
      {(hovered || interacting) && (
        <Html position={[0, 2.2, 0]} center>
          <div className="bg-black/80 text-white p-2 rounded-lg min-w-[200px]">
            <h3 className="font-bold">{agent.name}</h3>
            <p className="text-sm">{agent.role}</p>
            {response && (
              <p className="text-sm mt-2 italic">{response}</p>
            )}
          </div>
        </Html>
      )}
    </group>
  );
});

export default HumanAgent;
