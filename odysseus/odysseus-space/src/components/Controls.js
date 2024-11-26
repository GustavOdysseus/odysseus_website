import React, { useEffect, useState } from 'react';
import { useAtom } from 'jotai';
import { connectionModeAtom, visualSettingsAtom } from '../context/atoms';
import { agentsAtom } from '../state/atoms';

const Controls = () => {
  const [connectionMode, setConnectionMode] = useAtom(connectionModeAtom);
  const [visualSettings, setVisualSettings] = useAtom(visualSettingsAtom);
  const [isAltPressed, setIsAltPressed] = useState(false);
  const [agents, setAgents] = useAtom(agentsAtom);

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

  const updateAgentBody = (agentId, param, value) => {
    setAgents(agents.map(agent => {
      if (agent.id === agentId) {
        return {
          ...agent,
          bodyParams: {
            ...agent.bodyParams,
            [param]: value
          }
        };
      }
      return agent;
    }));
  };

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
      <div className="absolute top-4 left-4 bg-black/80 text-white p-4 rounded-lg">
        <h2 className="text-xl font-bold mb-4">Agent Controls</h2>
        
        {agents.map(agent => (
          <div key={agent.id} className="mb-6">
            <h3 className="font-bold mb-2">{agent.name}</h3>
            
            <div className="space-y-2">
              <div>
                <label className="block text-sm">Height</label>
                <input
                  type="range"
                  min="1.5"
                  max="2.0"
                  step="0.01"
                  value={agent.bodyParams?.height || 1.75}
                  onChange={(e) => updateAgentBody(agent.id, 'height', parseFloat(e.target.value))}
                  className="w-full"
                />
                <div className="text-xs text-right">{agent.bodyParams?.height?.toFixed(2)}m</div>
              </div>

              <div>
                <label className="block text-sm">Neck Girth</label>
                <input
                  type="range"
                  min="0.3"
                  max="0.5"
                  step="0.01"
                  value={agent.bodyParams?.neckGirth || 0.35}
                  onChange={(e) => updateAgentBody(agent.id, 'neckGirth', parseFloat(e.target.value))}
                  className="w-full"
                />
                <div className="text-xs text-right">{agent.bodyParams?.neckGirth?.toFixed(2)}m</div>
              </div>

              <div>
                <label className="block text-sm">Chest Girth</label>
                <input
                  type="range"
                  min="0.8"
                  max="1.2"
                  step="0.01"
                  value={agent.bodyParams?.chestGirth || 0.9}
                  onChange={(e) => updateAgentBody(agent.id, 'chestGirth', parseFloat(e.target.value))}
                  className="w-full"
                />
                <div className="text-xs text-right">{agent.bodyParams?.chestGirth?.toFixed(2)}m</div>
              </div>

              <div>
                <label className="block text-sm">Waist Girth</label>
                <input
                  type="range"
                  min="0.6"
                  max="1.1"
                  step="0.01"
                  value={agent.bodyParams?.waistGirth || 0.8}
                  onChange={(e) => updateAgentBody(agent.id, 'waistGirth', parseFloat(e.target.value))}
                  className="w-full"
                />
                <div className="text-xs text-right">{agent.bodyParams?.waistGirth?.toFixed(2)}m</div>
              </div>

              <div>
                <label className="block text-sm">Hip Girth</label>
                <input
                  type="range"
                  min="0.7"
                  max="1.2"
                  step="0.01"
                  value={agent.bodyParams?.hipGirth || 0.9}
                  onChange={(e) => updateAgentBody(agent.id, 'hipGirth', parseFloat(e.target.value))}
                  className="w-full"
                />
                <div className="text-xs text-right">{agent.bodyParams?.hipGirth?.toFixed(2)}m</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Controls;
