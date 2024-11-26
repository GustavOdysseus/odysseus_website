import React from 'react';
import { Html } from '@react-three/drei';
import { useAtom } from 'jotai';
import { tooltipAtom } from '../context/atoms';

const Tooltip = () => {
  const [tooltip] = useAtom(tooltipAtom);

  if (!tooltip) return null;

  return (
    <Html position={tooltip.position}>
      <div className="tooltip">
        {tooltip.description}
      </div>
    </Html>
  );
};

export default Tooltip;
