import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import {
  OrbitControls,
  Stars,
  Environment,
  useGLTF,
} from '@react-three/drei';
import { useSpaceStore } from '../state/store';
import HumanAgent from '../components/characters/HumanAgent';
import TaskModule from '../components/tasks/TaskModule';
import CrewManager from '../components/crews/CrewManager';

const SpaceScene: React.FC = () => {
  const { agents, tasks, visualSettings } = useSpaceStore();

  return (
    <>
      <Canvas
        shadows
        camera={{ position: [0, 5, 10], fov: 75 }}
        style={{ width: '100vw', height: '100vh' }}
      >
        {/* Environment and Lighting */}
        <Environment preset="night" />
        <ambientLight intensity={visualSettings.ambientLightIntensity} />
        <pointLight
          position={[10, 10, 10]}
          intensity={visualSettings.pointLightIntensity}
        />
        
        {/* Background */}
        <Stars
          radius={100}
          depth={50}
          count={5000}
          factor={4}
          saturation={0}
          fade
        />

        {/* Controls */}
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={5}
          maxDistance={50}
        />

        {/* Scene Content */}
        <Suspense fallback={null}>
          {/* Agents */}
          {agents.map((agent) => (
            <HumanAgent
              key={agent.id}
              agent={agent}
              onClick={() => {
                useSpaceStore.setState({
                  selectedEntity: { type: 'agent', data: agent },
                });
              }}
            />
          ))}

          {/* Tasks */}
          {tasks.map((task) => (
            <TaskModule
              key={task.id}
              task={task}
              onClick={() => {
                useSpaceStore.setState({
                  selectedEntity: { type: 'task', data: task },
                });
              }}
            />
          ))}

          {/* Space Station */}
          <mesh position={[0, -2, 0]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[100, 100]} />
            <meshStandardMaterial
              color="#1a1a1a"
              metalness={0.8}
              roughness={0.4}
            />
          </mesh>
        </Suspense>
      </Canvas>

      {/* UI Overlay */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none">
        <div className="pointer-events-auto">
          <CrewManager
            onCrewCreated={(crew) => {
              console.log('New crew created:', crew);
            }}
            onError={(error) => {
              console.error('Error creating crew:', error);
            }}
          />
        </div>
      </div>
    </>
  );
};

export default SpaceScene;
