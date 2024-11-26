import React, { useState } from 'react';
import { useThree } from '@react-three/fiber';
import { useSpring, animated } from '@react-spring/three';
import { useDrag } from '@use-gesture/react';
import { useAtom } from 'jotai';
import { divisionsAtom, connectionModeAtom, selectedPlanetAtom, connectionsAtom } from '../context/atoms';
import Planet from './Planet'; // Importa o componente base do planeta
import { throttle } from 'lodash';

const DraggablePlanet = ({ position: initialPosition, ...props }) => {
  const { camera, gl } = useThree();
  const [dragging, setDragging] = useState(false);
  const [divisions, setDivisions] = useAtom(divisionsAtom);
  const [connectionMode] = useAtom(connectionModeAtom);
  const [selectedPlanet, setSelectedPlanet] = useAtom(selectedPlanetAtom);
  const [connections, setConnections] = useAtom(connectionsAtom);

  const [spring, api] = useSpring(() => ({
    position: initialPosition,
    scale: 1,
    config: { mass: 1, tension: 170, friction: 26 },
  }));

  const bind = useDrag(
    throttle(({ movement: [x, y], first, last, event }) => {
      if (!event.altKey || connectionMode) return;

      gl.domElement.style.cursor = first ? 'grabbing' : 'grab'; // Muda o cursor
      if (first) setDragging(true);
      if (last) {
        setDragging(false);
        gl.domElement.style.cursor = 'default'; // Reseta o cursor
        const newPosition = spring.position.get();
        setDivisions(
          divisions.map((d) =>
            d.name === props.name ? { ...d, position: newPosition } : d
          )
        );
      }

      const factor = camera.position.z / 10;
      const newX = initialPosition[0] + x / factor;
      const newY = initialPosition[1] - y / factor;

      api.start({
        position: [newX, newY, initialPosition[2]],
      });
    }, 16)
  );

  const handleClick = () => {
    if (connectionMode) {
      if (selectedPlanet && selectedPlanet !== props.name) {
        setConnections([
          ...connections,
          { start: selectedPlanet, end: props.name, type: 'hierarchy' },
        ]);
        setSelectedPlanet(null);
      } else {
        setSelectedPlanet(props.name);
      }
    }
  };

  return (
    <animated.group
      {...spring}
      {...bind()}
      onPointerDown={(e) => e.stopPropagation()} // Evita conflitos com OrbitControls
    >
      <Planet {...props} onClick={handleClick} scale={dragging ? 1.2 : 1} />
    </animated.group>
  );
};

export default DraggablePlanet;
