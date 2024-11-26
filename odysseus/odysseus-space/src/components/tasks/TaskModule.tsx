import React, { useRef, useState, useEffect, memo } from 'react';
import { Html } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Task } from '../../types';
import { crewAIService } from '../../services/crewAI';

const PRIORITY_COLORS = {
  low: new THREE.Color('#2196F3'),
  medium: new THREE.Color('#FF9800'),
  high: new THREE.Color('#F44336'),
} as const;

const STATUS_COLORS = {
  pending: new THREE.Color('#9E9E9E'),
  'in-progress': new THREE.Color('#2196F3'),
  completed: new THREE.Color('#4CAF50'),
  failed: new THREE.Color('#F44336'),
} as const;

interface TaskModuleProps {
  task: Task;
  onClick?: () => void;
}

const TaskModule: React.FC<TaskModuleProps> = memo(({ task, onClick }) => {
  const group = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);
  const [analysis, setAnalysis] = useState<{
    progress: number;
    nextSteps: string[];
  } | null>(null);

  // Update task analysis
  useEffect(() => {
    const updateAnalysis = async () => {
      try {
        const result = await crewAIService.analyzeTaskProgress(task.id, []);
        setAnalysis({
          progress: result.progress,
          nextSteps: result.nextSteps,
        });
      } catch (error) {
        console.error('Error analyzing task:', error);
      }
    };

    updateAnalysis();
  }, [task.id, task.status]);

  // Animation
  useFrame((state) => {
    if (!group.current) return;

    // Hover animation
    group.current.scale.setScalar(
      THREE.MathUtils.lerp(
        group.current.scale.x,
        hovered ? 1.1 : 1,
        0.1
      )
    );

    // Status pulse animation
    if (task.status === 'in-progress') {
      const pulse = (Math.sin(state.clock.elapsedTime * 2) + 1) / 2;
      group.current.children[0].scale.setScalar(1 + pulse * 0.1);
    }
  });

  return (
    <group
      ref={group}
      position={task.position}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
      onClick={(e) => {
        e.stopPropagation();
        onClick?.();
      }}
    >
      {/* Task visualization */}
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial
          color={STATUS_COLORS[task.status]}
          emissive={PRIORITY_COLORS[task.priority]}
          emissiveIntensity={0.5}
          transparent
          opacity={0.8}
        />
      </mesh>

      {/* Progress indicator */}
      <mesh position={[0, -0.6, 0]}>
        <boxGeometry args={[1, 0.1, 0.1]} />
        <meshStandardMaterial
          color={STATUS_COLORS[task.status]}
          emissive={STATUS_COLORS[task.status]}
          emissiveIntensity={0.5}
        />
      </mesh>
      <mesh
        position={[
          -0.5 + (task.progress / 100) * 0.5,
          -0.6,
          0,
        ]}
      >
        <boxGeometry
          args={[task.progress / 100, 0.1, 0.1]}
        />
        <meshStandardMaterial
          color={STATUS_COLORS['completed']}
          emissive={STATUS_COLORS['completed']}
          emissiveIntensity={0.5}
        />
      </mesh>

      {/* Info panel */}
      {hovered && (
        <Html position={[0, 1.2, 0]} center>
          <div className="bg-black/80 text-white p-2 rounded-lg min-w-[200px]">
            <h3 className="font-bold">{task.name}</h3>
            <p className="text-sm">{task.description}</p>
            <div className="mt-2">
              <div className="flex justify-between text-sm">
                <span>Status:</span>
                <span className={`capitalize ${
                  task.status === 'completed'
                    ? 'text-green-400'
                    : task.status === 'failed'
                    ? 'text-red-400'
                    : 'text-blue-400'
                }`}>
                  {task.status}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Priority:</span>
                <span className={`capitalize ${
                  task.priority === 'high'
                    ? 'text-red-400'
                    : task.priority === 'medium'
                    ? 'text-orange-400'
                    : 'text-blue-400'
                }`}>
                  {task.priority}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Progress:</span>
                <span>{task.progress}%</span>
              </div>
            </div>
            {analysis?.nextSteps && analysis.nextSteps.length > 0 && (
              <div className="mt-2">
                <p className="text-sm font-bold">Next Steps:</p>
                <ul className="text-xs list-disc list-inside">
                  {analysis.nextSteps.slice(0, 3).map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </Html>
      )}
    </group>
  );
});

export default TaskModule;
