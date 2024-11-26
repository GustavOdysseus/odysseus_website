import React, { Suspense } from 'react';
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
import { useSpaceStore } from '../state/store';
import HumanAgent from '../components/characters/HumanAgent';
import SpaceStation from '../components/environment/SpaceStation';
import TaskModule from '../components/tasks/TaskModule';
import Controls from '../components/Controls';
import CrewManager from '../components/crews/CrewManager';

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
  const {
    agents,
    tasks,
    visualSettings,
    setSelectedEntity
  } = useSpaceStore();

  const handleAgentClick = (agent: any) => {
    setSelectedEntity({ type: 'agent', data: agent });
  };

  const handleTaskClick = (task: any) => {
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
          <pointLight
            position={[10, 10, 10]}
            intensity={visualSettings.pointLightIntensity}
          />
          <Stars
            radius={100}
            depth={50}
            count={5000}
            factor={4}
            saturation={0}
            fade
            speed={1}
          />

          {/* Space Station */}
          <SpaceStation position={[0, 0, 0]} />

          {/* Agents */}
          {agents.map((agent: any) => (
            <HumanAgent
              key={agent.id}
              agent={agent}
              onClick={() => handleAgentClick(agent)}
            />
          ))}

          {/* Tasks */}
          {tasks.map((task: any) => (
            <TaskModule
              key={task.id}
              task={task}
              onClick={() => handleTaskClick(task)}
            />
          ))}

          {/* Post Processing Effects */}
          <EffectComposer>
            <Bloom
              intensity={visualSettings.glowIntensity}
              luminanceThreshold={visualSettings.bloomThreshold}
              luminanceSmoothing={visualSettings.bloomRadius}
            />
            <ChromaticAberration offset={[0.002, 0.002]} />
          </EffectComposer>
        </Suspense>
      </Canvas>

      {/* UI Components */}
      <Controls />
      <CrewManager />
    </div>
  );
}
