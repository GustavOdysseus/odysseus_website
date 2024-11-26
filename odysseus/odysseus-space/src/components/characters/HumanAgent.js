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
};

interface HumanAgentProps {
  agent: Agent;
  onClick: () => void;
}

const HumanAgent: React.FC<HumanAgentProps> = memo(({ agent, onClick }) => {
  const group = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);
  const [interacting, setInteracting] = useState(false);
  const [response, setResponse] = useState('');

  // Load the base human model
  const { nodes, materials } = useGLTF('/models/human_male.glb');

  useEffect(() => {
    let mounted = true;
    
    const updateMesh = () => {
      if (!mounted || !nodes?.HumanBody) return;
      
      const mesh = nodes.HumanBody;
      const positions = mesh.geometry.attributes.position.array;

      // Scale height
      for (let i = 0; i < positions.length; i += 3) {
        positions[i + 1] *= agent.bodyParams.height;
      }

      // Apply girths (simplified example)
      const applyGirth = (yMin: number, yMax: number, scale: number) => {
        for (let i = 0; i < positions.length; i += 3) {
          const y = positions[i + 1];
          if (y >= yMin && y <= yMax) {
            positions[i] *= scale;
            positions[i + 2] *= scale;
          }
        }
      };

      applyGirth(1.5, 1.6, agent.bodyParams.neckGirth);
      applyGirth(1.2, 1.4, agent.bodyParams.chestGirth);
      applyGirth(0.9, 1.1, agent.bodyParams.waistGirth);
      applyGirth(0.6, 0.8, agent.bodyParams.hipGirth);

      mesh.geometry.attributes.position.needsUpdate = true;
      mesh.geometry.computeVertexNormals();
    };

    updateMesh();
    return () => {
      mounted = false;
    };
  }, [nodes, agent.bodyParams]);

  const handleInteraction = useCallback(async () => {
    setInteracting(true);
    try {
      const result = await crewAIService.getAgentResponse(
        agent.id,
        'Tell me about your current task'
      );
      setResponse(result.response);
    } catch (error) {
      console.error('Failed to get agent response:', error);
      setResponse('Communication error...');
    }
    setInteracting(false);
  }, [agent.id]);

  useFrame((state, delta) => {
    if (group.current) {
      // Floating animation
      group.current.position.y = agent.position[1] + Math.sin(state.clock.elapsedTime) * 0.1;
      
      // Color interpolation on hover
      if (materials?.HumanBody) {
        materials.HumanBody.color.lerp(
          hovered ? new THREE.Color('#42aff5') : STATUS_COLORS[agent.status],
          delta * 4
        );
      }
    }
  });

  return (
    <group
      ref={group}
      position={agent.position}
      onClick={(e) => {
        e.stopPropagation();
        onClick();
      }}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      {nodes && <primitive object={nodes.HumanBody} />}

      <Html position={[0, 2.5, 0]}>
        <div className="character-info bg-black/50 text-white p-2 rounded-lg shadow-lg min-w-[200px]">
          <div className="font-bold text-lg">{agent.name}</div>
          <div className="text-sm text-gray-300">{agent.role}</div>
          <div className={`status ${
            agent.status === 'active' ? 'text-green-500' : 'text-gray-400'
          }`}>
            {agent.status}
          </div>
          
          {/* Skills */}
          <div className="mt-2">
            <div className="text-xs text-gray-400">Skills:</div>
            <div className="flex flex-wrap gap-1">
              {agent.skills.map((skill, index) => (
                <span
                  key={index}
                  className="text-xs bg-blue-500/30 px-1 rounded"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {/* Interaction */}
          <button
            onClick={handleInteraction}
            disabled={interacting}
            className={`mt-2 w-full px-2 py-1 rounded text-sm ${
              interacting
                ? 'bg-gray-600 cursor-wait'
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {interacting ? 'Thinking...' : 'Interact'}
          </button>

          {response && (
            <div className="mt-2 text-sm bg-black/30 p-2 rounded">
              {response}
            </div>
          )}
        </div>
      </Html>
    </group>
  );
});

HumanAgent.displayName = 'HumanAgent';

export default HumanAgent;

// Preload the model
useGLTF.preload('/models/human_male.glb');
