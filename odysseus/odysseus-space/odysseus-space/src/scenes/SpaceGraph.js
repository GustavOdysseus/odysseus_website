import React, { useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Html } from '@react-three/drei';
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing';
import { PerformanceMonitor } from '@react-three/drei';
import { useAtom } from 'jotai';
import { divisionsAtom, connectionsAtom, tooltipAtom, isDraggingAtom } from '../context/atoms';
import Controls from '../components/Controls';
import DraggablePlanet from '../components/DraggablePlanet';
import EnhancedConnection from '../components/EnhancedConnection';

const SpaceGraph = () => {
  const [divisions, setDivisions] = useAtom(divisionsAtom);
  const [connections] = useAtom(connectionsAtom);
  const [tooltip] = useAtom(tooltipAtom);
  const [isDragging, setIsDragging] = useAtom(isDraggingAtom);

  useEffect(() => {
    const initialDivisions = [
      { name: 'Olimpos', position: [0, 8, 0], color: '#ff9999', description: 'Descrição do Olimpos' },
      // Outros planetas...
    ];
    setDivisions(initialDivisions);
  }, [setDivisions]);

  return (
    <div className="relative w-full h-screen">
      <Controls />
      <Canvas camera={{ position: [0, 5, 20], fov: 60 }}>
        <PerformanceMonitor>
          {/* Configurações */}
          <color attach="background" args={['#000008']} />
          <ambientLight intensity={0.2} />
          <pointLight position={[10, 10, 10]} intensity={1} />
          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
          <OrbitControls enabled={!isDragging} />
          {/* Renderização dos planetas */}
          {divisions.map((div) => (
            <DraggablePlanet
              key={div.name}
              {...div}
              onDragStart={() => setIsDragging(true)}
              onDragEnd={() => setIsDragging(false)}
            />
          ))}
          {/* Renderização das conexões */}
          {connections.map((conn, i) => {
            const start = divisions.find((d) => d.name === conn.start)?.position;
            const end = divisions.find((d) => d.name === conn.end)?.position;
            if (start && end) {
              return <EnhancedConnection key={i} start={start} end={end} type={conn.type} />;
            }
            return null;
          })}
          {/* Pós-processamento */}
          <EffectComposer>
            <Bloom intensity={1.5} luminanceThreshold={0.1} luminanceSmoothing={0.9} />
            <ChromaticAberration offset={[0.0005, 0.0005]} />
          </EffectComposer>
          {/* Tooltip */}
          <Tooltip />
        </PerformanceMonitor>
      </Canvas>
    </div>
  );
};

export default SpaceGraph;
