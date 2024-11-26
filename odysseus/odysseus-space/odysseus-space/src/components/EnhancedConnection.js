import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { useAtom } from 'jotai';
import { connectionTypes, visualSettingsAtom } from '../context/atoms';
import * as THREE from 'three';

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
              array={new Float32Array(points.flatMap((p) => [p.x, p.y, p.z]))}
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
            array={new Float32Array(points.flatMap((p) => [p.x, p.y, p.z]))}
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

export default EnhancedConnection;
