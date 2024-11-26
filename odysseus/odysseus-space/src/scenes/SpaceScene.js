import React, { Suspense, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import {
  Stars,
  OrbitControls,
  PerspectiveCamera,
  Environment,
  useProgress,
  Html
} from '@react-three/drei';
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing';
import { useAtom } from 'jotai';
import { agentsAtom, tasksAtom, visualSettingsAtom } from '../state/atoms';

import HumanAgent from '../components/characters/HumanAgent';
import SpaceStation from '../components/environment/SpaceStation';
import TaskModule from '../components/tasks/TaskModule';
import Controls from '../components/Controls';

function LoadingScreen() {
  const { progress } = useProgress();
  return (
    <Html center>
      <div className="loading-screen">
        <div className="text-white text-2xl">Loading Odysseus Space Station</div>
        <div className="progress-bar">
          <div className="progress" style={{ width: `${progress}%` }} />
        </div>
        <div className="text-white">{progress.toFixed(2)}%</div>
      </div>
    </Html>
  );
}

export default function SpaceScene() {
  const [agents] = useAtom(agentsAtom);
  const [tasks] = useAtom(tasksAtom);
  const [visualSettings] = useAtom(visualSettingsAtom);
  const [selectedEntity, setSelectedEntity] = useState(null);

  const handleAgentClick = (agent) => {
    setSelectedEntity({ type: 'agent', data: agent });
  };

  const handleTaskClick = (task) => {
    setSelectedEntity({ type: 'task', data: task });
  };

  return (
    <div className="w-full h-screen">
      <Canvas shadows>
        <Suspense fallback={<LoadingScreen />}>
          {/* Camera Setup */}
          <PerspectiveCamera makeDefault position={[0, 10, 20]} />
          <OrbitControls
            target={[0, 0, 0]}
            maxPolarAngle={Math.PI / 2}
            minDistance={5}
            maxDistance={50}
          />

          {/* Environment and Lighting */}
          <Environment preset="night" />
          <ambientLight intensity={visualSettings.ambientLightIntensity} />
          <pointLight position={[10, 10, 10]} intensity={visualSettings.pointLightIntensity} />
          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

          {/* Space Station */}
          <SpaceStation position={[0, 0, 0]} />

          {/* Agents */}
          {agents.map((agent) => (
            <HumanAgent
              key={agent.id}
              position={agent.position}
              name={agent.name}
              role={agent.role}
              status={agent.status}
              bodyParams={agent.bodyParams}
              onClick={() => handleAgentClick(agent)}
            />
          ))}

          {/* Tasks */}
          {tasks.map((task) => (
            <TaskModule
              key={task.id}
              position={task.position}
              task={task}
              status={task.status}
              assignedAgents={task.assignedAgents}
              onClick={() => handleTaskClick(task)}
            />
          ))}

          {/* Post Processing Effects */}
          <EffectComposer>
            <Bloom
              intensity={visualSettings.glowIntensity}
              luminanceThreshold={0.9}
              luminanceSmoothing={0.025}
            />
            <ChromaticAberration offset={[0.002, 0.002]} />
          </EffectComposer>
        </Suspense>
      </Canvas>

      {/* Controls */}
      <Controls />

      {/* Selected Entity Info */}
      {selectedEntity && (
        <div className="absolute top-4 right-4 bg-black/80 text-white p-4 rounded-lg max-w-md">
          <h2 className="text-xl font-bold mb-2">
            {selectedEntity.type === 'agent' ? 'Agent Details' : 'Task Details'}
          </h2>
          <pre className="text-sm overflow-auto">
            {JSON.stringify(selectedEntity.data, null, 2)}
          </pre>
          <button
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
            onClick={() => setSelectedEntity(null)}
          >
            Close
          </button>
        </div>
      )}
    </div>
  );
}
