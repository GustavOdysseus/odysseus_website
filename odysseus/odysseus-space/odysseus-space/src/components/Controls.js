import React, { useEffect, useState } from 'react';
import { useAtom } from 'jotai';
import { connectionModeAtom, visualSettingsAtom } from '../context/atoms';

const Controls = () => {
  const [connectionMode, setConnectionMode] = useAtom(connectionModeAtom);
  const [visualSettings, setVisualSettings] = useAtom(visualSettingsAtom);
  const [isAltPressed, setIsAltPressed] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e) => e.key === 'Alt' && setIsAltPressed(true);
    const handleKeyUp = (e) => e.key === 'Alt' && setIsAltPressed(false);

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

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
            onChange={(e) =>
              setVisualSettings({
                ...visualSettings,
                showLabels: e.target.checked,
              })
            }
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
            onChange={(e) =>
              setVisualSettings({
                ...visualSettings,
                connectionOpacity: parseFloat(e.target.value),
              })
            }
            className="w-full"
          />
        </div>
      </div>
      {isAltPressed && (
        <div className="text-white text-sm bg-gray-800 p-2 rounded shadow-md">
          Hold Alt to move planets
        </div>
      )}
    </div>
  );
};

export default Controls;
