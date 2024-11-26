import React, { useState, useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Stars, Html } from '@react-three/drei';
import * as THREE from 'three';

// Planeta individual com atmosfera e brilho
const Planet = ({ position, name, color, description, onHover }) => {
  const [hovered, setHovered] = useState(false);
  const meshRef = useRef();
  const atmosphereRef = useRef();

  // Rotação suave do planeta
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
    onHover({ description, position });
  };

  const handlePointerOut = () => {
    setHovered(false);
    onHover(null);
  };

  return (
    <group position={position}>
      {/* Atmosfera */}
      <mesh ref={atmosphereRef}
        scale={hovered ? 1.6 : 1.5}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.1}
        />
      </mesh>

      {/* Planeta principal */}
      <mesh
        ref={meshRef}
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

      {/* Nome do planeta */}
      <Text
        position={[0, 1.5, 0]}
        fontSize={0.5}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {name}
      </Text>
    </group>
  );
};

// Linha de conexão entre planetas
const Connection = ({ start, end }) => {
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

  return (
    <line>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={points.length}
          array={new Float32Array(points.flatMap(p => [p.x, p.y, p.z]))}
          itemSize={3}
        />
      </bufferGeometry>
      <lineBasicMaterial color="#ffffff" opacity={0.2} transparent />
    </line>
  );
};

// Componente principal
const SpaceGraph = () => {
  const [tooltip, setTooltip] = useState(null);

  const divisions = [
    { name: "Olimpos", position: [-8, 4, -5], color: "#ff9999", 
      description: "Conselho estratégico e governança adaptativa" },
    { name: "Prometeus", position: [-4, 6, -3], color: "#ff9999",
      description: "Inovação disruptiva e novos modelos de negócio" },
    { name: "Mercúrios", position: [0, 8, 0], color: "#99ff99",
      description: "Negociações e gestão de clientes" },
    { name: "Skaldos", position: [4, 6, 3], color: "#99ff99",
      description: "Comunicação estratégica e marketing" },
    { name: "Apolo", position: [8, 4, 5], color: "#99ff99",
      description: "Experiência do cliente e fidelização" },
    { name: "Mirmidões", position: [-6, 0, -8], color: "#9999ff",
      description: "Trading quantitativo e análise financeira" },
    { name: "Plutus", position: [-3, 0, -6], color: "#9999ff",
      description: "Gestão financeira e otimização de custos" },
    { name: "Vikings", position: [0, 0, -4], color: "#ffff99",
      description: "Exploração de mercados e tecnologias" },
    { name: "Dédalo", position: [3, 0, -2], color: "#ffff99",
      description: "Programação e arquitetura de soluções" },
    { name: "Athena", position: [0, 3, 0], color: "#ffb366",
      description: "Análise de dados e insights estratégicos" }
  ];

  const connections = [
    ["Olimpos", "Prometeus"],
    ["Prometeus", "Mercúrios"],
    ["Mercúrios", "Skaldos"],
    ["Skaldos", "Apolo"],
    ["Mirmidões", "Plutus"],
    ["Plutus", "Vikings"],
    ["Vikings", "Dédalo"],
    ["Athena", "Olimpos"],
    ["Athena", "Prometeus"],
    ["Athena", "Mercúrios"]
  ];

  return (
    <div className="w-full h-screen bg-black">
      <Canvas camera={{ position: [0, 5, 20], fov: 60 }}>
        <color attach="background" args={['#000000']} />
        
        {/* Iluminação */}
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        
        {/* Estrelas de fundo */}
        <Stars
          radius={100}
          depth={50}
          count={5000}
          factor={4}
          saturation={0}
          fade
        />
        
        {/* Controles de órbita */}
        <OrbitControls
          enableZoom={true}
          enablePan={true}
          enableRotate={true}
          zoomSpeed={0.6}
          panSpeed={0.5}
          rotateSpeed={0.4}
        />

        {/* Planetas */}
        {divisions.map((div) => (
          <Planet
            key={div.name}
            {...div}
            onHover={setTooltip}
          />
        ))}

        {/* Conexões */}
        {connections.map(([start, end], i) => {
          const startPos = divisions.find(d => d.name === start)?.position;
          const endPos = divisions.find(d => d.name === end)?.position;
          if (startPos && endPos) {
            return <Connection key={i} start={startPos} end={endPos} />;
          }
          return null;
        })}

        {/* Tooltip */}
        {tooltip && (
          <Html position={tooltip.position}>
            <div className="bg-gray-900 text-white px-4 py-2 rounded-lg shadow-lg border border-gray-700 text-sm">
              {tooltip.description}
            </div>
          </Html>
        )}
      </Canvas>
    </div>
  );
};

export default SpaceGraph;