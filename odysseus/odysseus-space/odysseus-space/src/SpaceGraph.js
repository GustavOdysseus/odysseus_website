import React, { useState, useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Text, Stars, Html } from '@react-three/drei';
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing';
import { useSpring, animated } from '@react-spring/three';
import { useDrag } from '@use-gesture/react';
import { atom, useAtom, Provider as JotaiProvider } from 'jotai';
import * as THREE from 'three';

// Átomos Jotai para estado global
const divisionsAtom = atom([]);
const connectionsAtom = atom([]);
const selectedPlanetAtom = atom(null);
const connectionModeAtom = atom(false);
const tooltipAtom = atom(null);
const historyAtom = atom([]);
const visualSettingsAtom = atom({
  showLabels: true,
  connectionOpacity: 0.8,
  planetSize: 1,
  glowIntensity: 1.5,
});

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
  const lineRef = useRef();
  const [visualSettings] = useAtom(visualSettingsAtom);
  const { color, width, dash, glow } = connectionTypes[type];
  
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
            opacity={visualSettings.connectionOpacity * 0.5}
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
          opacity={visualSettings.connectionOpacity}
          transparent
        />
      </line>
    </group>
  );
};

// Planeta base
const Planet = ({ position, name, color, description, onHover, onClick, scale = 1 }) => {
  const [hovered, setHovered] = useState(false);
  const meshRef = useRef();
  const atmosphereRef = useRef();
  const [visualSettings] = useAtom(visualSettingsAtom);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.002;
    }
    if (atmosphereRef.current) {
      atmosphereRef.current.rotation.y -= 0.001;
    }
  });

  const handlePointerOver = () => {
    setHovered(true);
    onHover?.({ description, position });
  };

  const handlePointerOut = () => {
    setHovered(false);
    onHover?.(null);
  };

  return (
    <group position={position} scale={scale * visualSettings.planetSize}>
      <mesh ref={atmosphereRef} scale={hovered ? 1.6 : 1.5}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.1}
        />
      </mesh>

      <mesh
        ref={meshRef}
        onClick={onClick}
        onPointerOver={handlePointerOver}
        onPointerOut={handlePointerOut}
      >
        <sphereGeometry args={[1, 32, 32]} />
        <meshPhongMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.2}
          shininess={50}
        />
      </mesh>

      {visualSettings.showLabels && (
        <Text
          position={[0, 1.5, 0]}
          fontSize={0.5}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          {name}
        </Text>
      )}
    </group>
  );
};

// Planeta interativo
const DraggablePlanet = ({ position: initialPosition, ...props }) => {
  const { camera } = useThree();
  const [dragging, setDragging] = useState(false);
  const [divisions, setDivisions] = useAtom(divisionsAtom);
  const [connectionMode] = useAtom(connectionModeAtom);
  const [selectedPlanet, setSelectedPlanet] = useAtom(selectedPlanetAtom);
  const [connections, setConnections] = useAtom(connectionsAtom);

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
      const newPosition = spring.position.get();
      setDivisions(divisions.map(d => 
        d.name === props.name ? { ...d, position: newPosition } : d
      ));
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
      if (selectedPlanet && selectedPlanet !== props.name) {
        setConnections([...connections, {
          start: selectedPlanet,
          end: props.name,
          type: 'hierarchy'
        }]);
        setSelectedPlanet(null);
      } else {
        setSelectedPlanet(props.name);
      }
    }
  };

  return (
    <animated.group {...spring} {...bind()}>
      <Planet
        {...props}
        onClick={handleClick}
        scale={dragging ? 1.2 : 1}
      />
    </animated.group>
  );
};

// Interface de controle
const Controls = () => {
  const [connectionMode, setConnectionMode] = useAtom(connectionModeAtom);
  const [visualSettings, setVisualSettings] = useAtom(visualSettingsAtom);

  return (
    <div className="absolute top-4 left-4 space-y-2">
      <button
        className={`px-4 py-2 rounded-lg ${
          connectionMode ? 'bg-blue-600' : 'bg-gray-600'
        } text-white`}
        onClick={() => setConnectionMode(!connectionMode)}
      >
        {connectionMode ? 'Creating Connection' : 'Create Connection'}
      </button>
      <div className="space-y-2 mt-4">
        <label className="flex items-center space-x-2 text-white">
          <input
            type="checkbox"
            checked={visualSettings.showLabels}
            onChange={(e) => setVisualSettings({
              ...visualSettings,
              showLabels: e.target.checked
            })}
          />
          <span>Show Labels</span>
        </label>
        <div className="text-white">
          <span>Connection Opacity</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={visualSettings.connectionOpacity}
            onChange={(e) => setVisualSettings({
              ...visualSettings,
              connectionOpacity: parseFloat(e.target.value)
            })}
            className="w-full"
          />
        </div>
      </div>
    </div>
  );
};

// Componente principal
const SpaceGraph = () => {
  const [divisions] = useAtom(divisionsAtom);
  const [connections] = useAtom(connectionsAtom);
  const [tooltip] = useAtom(tooltipAtom);
  const [visualSettings] = useAtom(visualSettingsAtom);

  useEffect(() => {
    // Inicializar as divisões
    const initialDivisions = [
      { name: "Olimpos", position: [-8, 4, -5], color: "#ff9999", 
        description: "Conselho estratégico e governança adaptativa" },
      { name: "Prometeus", position: [-4, 6, -3], color: "#ff9999",
        description: "Inovação disruptiva e novos modelos de negócio" },
      // ... adicione outras divisões aqui
    ];
    setDivisionsAtom(initialDivisions);
  }, []);

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
            intensity={visualSettings.glowIntensity}
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

// Componente wrapper com provider
const SpaceGraphWrapper = () => {
  return (
    <JotaiProvider>
      <SpaceGraph />
    </JotaiProvider>
  );
};

export default SpaceGraphWrapper;