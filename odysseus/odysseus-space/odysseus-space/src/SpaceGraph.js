import React, { useState, useRef, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Text, Stars, Html, useGLTF } from '@react-three/drei';
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing';
import { create } from 'zustand';
import { useSpring, animated } from '@react-spring/three';
import { useDrag } from '@use-gesture/react';
import * as THREE from 'three';
import { atom, useAtom } from 'jotai';

// Store para gerenciar o estado global
const useStore = create((set) => ({
  divisions: [],
  connections: [],
  selectedPlanet: null,
  connectionMode: false,
  hierarchyLevels: {},
  addDivision: (division) => set((state) => ({
    divisions: [...state.divisions, division]
  })),
  addConnection: (connection, type) => set((state) => ({
    connections: [...state.connections, { ...connection, type }]
  })),
  updatePosition: (name, position) => set((state) => ({
    divisions: state.divisions.map(d => 
      d.name === name ? { ...d, position } : d
    )
  })),
  setSelectedPlanet: (name) => set({ selectedPlanet: name }),
  toggleConnectionMode: () => set((state) => ({ 
    connectionMode: !state.connectionMode 
  })),
}));

// Tipos de conexões e suas propriedades visuais
const connectionTypes = {
  hierarchy: {
    color: '#ff9966',
    width: 3,
    dash: false,
    glow: true
  },
  collaboration: {
    color: '#66ffff',
    width: 2,
    dash: true,
    glow: false
  },
  information: {
    color: '#9966ff',
    width: 1,
    dash: true,
    glow: false
  }
};

// Componente de linha melhorado
const EnhancedConnection = ({ start, end, type = 'hierarchy' }) => {
  const { color, width, dash, glow } = connectionTypes[type];
  const lineRef = useRef();
  
  const points = useMemo(() => {
    const curve = new THREE.QuadraticBezierCurve3(
      new THREE.Vector3(...start),
      new THREE.Vector3(
        (start[0] + end[0]) / 2,
        (start[1] + end[1]) / 2 + 2,
        (start[2] + end[2]) / 2
      ),
      new THREE.Vector3(...end)
    );
    return curve.getPoints(50);
  }, [start, end]);

  useFrame(({ clock }) => {
    if (dash && lineRef.current) {
      lineRef.current.material.dashOffset = clock.getElapsedTime() * 0.5;
    }
  });

  return (
    <group>
      {glow && (
        <line>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              count={points.length}
              array={new Float32Array(points.flatMap(p => [p.x, p.y, p.z]))}
              itemSize={3}
            />
          </bufferGeometry>
          <lineBasicMaterial
            color={color}
            transparent
            opacity={0.5}
            linewidth={width + 2}
          />
        </line>
      )}
      <line ref={lineRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={points.length}
            array={new Float32Array(points.flatMap(p => [p.x, p.y, p.z]))}
            itemSize={3}
          />
        </bufferGeometry>
        <lineDashedMaterial
          color={color}
          dashSize={dash ? 0.5 : 0}
          gapSize={dash ? 0.2 : 0}
          linewidth={width}
        />
      </line>
    </group>
  );
};

// Planeta interativo aprimorado
const DraggablePlanet = ({ position: initialPosition, name, color, description, onHover }) => {
  const { camera, size } = useThree();
  const [dragging, setDragging] = useState(false);
  const updatePosition = useStore((state) => state.updatePosition);
  const connectionMode = useStore((state) => state.connectionMode);
  const selectedPlanet = useStore((state) => state.selectedPlanet);
  const addConnection = useStore((state) => state.addConnection);

  const [spring, api] = useSpring(() => ({
    position: initialPosition,
    scale: 1,
    config: { mass: 1, tension: 170, friction: 26 }
  }));

  const bind = useDrag(({ movement: [x, y], first, last }) => {
    if (connectionMode) return;
    
    if (first) setDragging(true);
    if (last) {
      setDragging(false);
      updatePosition(name, spring.position.get());
    }

    const factor = camera.position.z / 10;
    const newX = initialPosition[0] + x / factor;
    const newY = initialPosition[1] - y / factor;
    
    api.start({
      position: [newX, newY, initialPosition[2]]
    });
  });

  const handleClick = () => {
    if (connectionMode) {
      if (selectedPlanet && selectedPlanet !== name) {
        addConnection({
          start: selectedPlanet,
          end: name
        }, 'hierarchy');
      }
    }
  };

  return (
    <animated.group {...spring} {...bind()}>
      <Planet
        name={name}
        color={color}
        description={description}
        onHover={onHover}
        onClick={handleClick}
        scale={dragging ? 1.2 : 1}
      />
    </animated.group>
  );
};

// Interface de controle
const Controls = () => {
  const toggleConnectionMode = useStore((state) => state.toggleConnectionMode);
  const connectionMode = useStore((state) => state.connectionMode);

  return (
    <div className="absolute top-4 left-4 space-y-2">
      <button
        className={`px-4 py-2 rounded-lg ${
          connectionMode ? 'bg-blue-600' : 'bg-gray-600'
        } text-white`}
        onClick={toggleConnectionMode}
      >
        {connectionMode ? 'Creating Connection' : 'Create Connection'}
      </button>
    </div>
  );
};

// Componente principal atualizado
const SpaceGraph = () => {
  const divisions = useStore((state) => state.divisions);
  const connections = useStore((state) => state.connections);
  const [tooltip, setTooltip] = useState(null);

  return (
    <div className="relative w-full h-screen">
      <Controls />
      <Canvas camera={{ position: [0, 5, 20], fov: 60 }}>
        <color attach="background" args={['#000008']} />
        
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        
        <Stars
          radius={100}
          depth={50}
          count={5000}
          factor={4}
          saturation={0}
          fade
          speed={1}
        />
        
        <OrbitControls
          enableZoom={true}
          enablePan={true}
          enableRotate={true}
          zoomSpeed={0.6}
          panSpeed={0.5}
          rotateSpeed={0.4}
        />

        {divisions.map((div) => (
          <DraggablePlanet
            key={div.name}
            {...div}
            onHover={setTooltip}
          />
        ))}

        {connections.map((conn, i) => {
          const start = divisions.find(d => d.name === conn.start)?.position;
          const end = divisions.find(d => d.name === conn.end)?.position;
          if (start && end) {
            return (
              <EnhancedConnection
                key={i}
                start={start}
                end={end}
                type={conn.type}
              />
            );
          }
          return null;
        })}

        <EffectComposer>
          <Bloom
            intensity={1.5}
            luminanceThreshold={0.1}
            luminanceSmoothing={0.9}
          />
          <ChromaticAberration offset={[0.0005, 0.0005]} />
        </EffectComposer>

        {tooltip && (
          <Html position={tooltip.position}>
            <div className="bg-gray-900/80 backdrop-blur-sm text-white px-4 py-2 rounded-lg shadow-lg border border-gray-700/50 text-sm">
              {tooltip.description}
            </div>
          </Html>
        )}
      </Canvas>
    </div>
  );
};

export default SpaceGraph;