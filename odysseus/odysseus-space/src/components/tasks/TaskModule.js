import React, { useRef, useState, useCallback, memo } from 'react';
import { useSpring, animated } from '@react-spring/three';
import { Html } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Task } from '../../types';
import { useSpaceStore } from '../../state/store';
import { crewAIService } from '../../services/crewAI';

const STATUS_COLORS = {
  pending: '#9E9E9E',
  'in-progress': '#2196F3',
  completed: '#4CAF50',
  failed: '#F44336',
} as const;

interface TaskModuleProps {
  task: Task;
  onClick: () => void;
}

const TaskModule: React.FC<TaskModuleProps> = memo(({ task, onClick }) => {
  const group = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [progress, setProgress] = useState<{
    progress: number;
    nextSteps: string[];
  } | null>(null);

  const { scale } = useSpring({
    scale: hovered ? 1.2 : 1,
    config: { tension: 300, friction: 10 },
  });

  const fetchProgress = useCallback(async () => {
    try {
      const result = await crewAIService.analyzeTaskProgress(task.id, []);
      setProgress({
        progress: result.progress,
        nextSteps: result.nextSteps,
      });
    } catch (error) {
      console.error('Failed to fetch task progress:', error);
    }
  }, [task.id]);

  useFrame((state) => {
    if (group.current) {
      // Floating animation with position based on task priority
      const baseHeight = task.position[1];
      const priorityOffset = {
        high: 0.3,
        medium: 0.2,
        low: 0.1,
      }[task.priority];

      group.current.position.y =
        baseHeight +
        priorityOffset * Math.sin(state.clock.elapsedTime * 0.5) +
        (hovered ? 0.2 : 0);
    }
  });

  const handleClick = (e: THREE.Event) => {
    e.stopPropagation();
    onClick();
    setShowDetails((prev) => !prev);
    if (!progress) {
      fetchProgress();
    }
  };

  return (
    <animated.group
      ref={group}
      position={task.position}
      scale={scale}
      onClick={handleClick}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      {/* Task Module Visualization */}
      <mesh>
        <boxGeometry args={[2, 2, 2]} />
        <meshPhongMaterial
          color={STATUS_COLORS[task.status]}
          opacity={0.8}
          transparent
        />
      </mesh>

      {/* Progress Ring */}
      <mesh rotation={[0, 0, 0]} position={[0, 0, 1.1]}>
        <ringGeometry args={[0.8, 1, 32]} />
        <meshBasicMaterial
          color="#ffffff"
          opacity={0.3}
          transparent
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Progress Indicator */}
      <mesh rotation={[0, 0, 0]} position={[0, 0, 1.11]}>
        <ringGeometry args={[0.8, 1, 32, 1, 0, (task.progress / 100) * Math.PI * 2]} />
        <meshBasicMaterial
          color="#4CAF50"
          opacity={0.8}
          transparent
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Holographic Display */}
      <Html position={[0, 2.5, 0]}>
        <div className="task-info bg-black/70 text-white p-3 rounded-lg min-w-[250px] shadow-lg">
          <h3 className="text-lg font-bold mb-2">{task.name}</h3>
          <p className="text-sm mb-2">{task.description}</p>
          
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs text-gray-400">Status:</span>
            <span
              className={`text-xs px-2 py-1 rounded ${
                task.status === 'completed'
                  ? 'bg-green-500/30 text-green-300'
                  : task.status === 'in-progress'
                  ? 'bg-blue-500/30 text-blue-300'
                  : task.status === 'failed'
                  ? 'bg-red-500/30 text-red-300'
                  : 'bg-gray-500/30 text-gray-300'
              }`}
            >
              {task.status}
            </span>
          </div>

          <div className="flex justify-between items-center mb-2">
            <span className="text-xs text-gray-400">Priority:</span>
            <span
              className={`text-xs px-2 py-1 rounded ${
                task.priority === 'high'
                  ? 'bg-red-500/30 text-red-300'
                  : task.priority === 'medium'
                  ? 'bg-yellow-500/30 text-yellow-300'
                  : 'bg-green-500/30 text-green-300'
              }`}
            >
              {task.priority}
            </span>
          </div>

          <div className="mb-2">
            <div className="text-xs text-gray-400 mb-1">Progress:</div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-blue-500 rounded-full h-2 transition-all duration-300"
                style={{ width: `${task.progress}%` }}
              />
            </div>
          </div>

          {showDetails && (
            <>
              <div className="mt-3">
                <div className="text-xs text-gray-400 mb-1">Assigned Agents:</div>
                <div className="flex flex-wrap gap-1">
                  {task.assignedAgents.map((agentId) => (
                    <span
                      key={agentId}
                      className="text-xs bg-purple-500/30 px-2 py-1 rounded"
                    >
                      {agentId}
                    </span>
                  ))}
                </div>
              </div>

              {progress?.nextSteps && (
                <div className="mt-3">
                  <div className="text-xs text-gray-400 mb-1">Next Steps:</div>
                  <ul className="text-xs space-y-1">
                    {progress.nextSteps.map((step, index) => (
                      <li
                        key={index}
                        className="bg-black/30 p-2 rounded"
                      >
                        {step}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {task.deadline && (
                <div className="mt-3 text-xs">
                  <span className="text-gray-400">Deadline:</span>
                  <span className="ml-2">
                    {new Date(task.deadline).toLocaleDateString()}
                  </span>
                </div>
              )}
            </>
          )}
        </div>
      </Html>
    </animated.group>
  );
});

TaskModule.displayName = 'TaskModule';

export default TaskModule;
