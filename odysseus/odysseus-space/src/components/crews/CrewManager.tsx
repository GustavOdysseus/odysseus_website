import React, { useState, useCallback } from 'react';
import { useSpaceStore } from '../../state/store';
import { Agent, Crew, Task } from '../../types';
import { crewAIService } from '../../services/crewAI';

interface CrewManagerProps {
  onCrewCreated?: (crew: Crew) => void;
  onError?: (error: Error) => void;
}

const CrewManager: React.FC<CrewManagerProps> = ({
  onCrewCreated,
  onError,
}) => {
  const [objective, setObjective] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  
  const agents = useSpaceStore((state) => state.agents);
  const addCrew = useSpaceStore((state) => state.createCrew);

  const handleCreateCrew = useCallback(async () => {
    if (!objective || selectedAgents.length === 0) {
      onError?.(new Error('Please provide an objective and select at least one agent'));
      return;
    }

    setLoading(true);
    try {
      // Optimize crew composition
      const optimization = await crewAIService.optimizeCrew(
        objective,
        agents.filter((a) => selectedAgents.includes(a.id))
      );

      // Generate suggested tasks
      const tasks = optimization.suggestedTasks;

      // Create the crew
      const crew: Crew = {
        id: `crew-${Date.now()}`,
        name: `Crew for ${objective.slice(0, 20)}...`,
        agents: agents.filter((a) => optimization.selectedAgents.includes(a.id)),
        tasks,
        objective,
        status: 'assembling',
        createdAt: new Date(),
      };

      // Add to global state
      addCrew(crew);
      onCrewCreated?.(crew);

      // Clear form
      setObjective('');
      setSelectedAgents([]);
    } catch (error) {
      console.error('Error creating crew:', error);
      onError?.(error instanceof Error ? error : new Error('Failed to create crew'));
    } finally {
      setLoading(false);
    }
  }, [objective, selectedAgents, agents, addCrew, onCrewCreated, onError]);

  return (
    <div className="bg-gray-900 p-4 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Create New Crew</h2>
      
      <div className="space-y-4">
        {/* Objective input */}
        <div>
          <label className="block text-sm font-medium mb-1">
            Objective
          </label>
          <textarea
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 rounded border border-gray-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            placeholder="Enter crew objective..."
            rows={3}
          />
        </div>

        {/* Agent selection */}
        <div>
          <label className="block text-sm font-medium mb-1">
            Select Agents
          </label>
          <div className="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto">
            {agents.map((agent) => (
              <label
                key={agent.id}
                className="flex items-center space-x-2 p-2 rounded bg-gray-800 cursor-pointer hover:bg-gray-700"
              >
                <input
                  type="checkbox"
                  checked={selectedAgents.includes(agent.id)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedAgents([...selectedAgents, agent.id]);
                    } else {
                      setSelectedAgents(
                        selectedAgents.filter((id) => id !== agent.id)
                      );
                    }
                  }}
                  className="rounded border-gray-600"
                />
                <div>
                  <p className="font-medium">{agent.name}</p>
                  <p className="text-sm text-gray-400">{agent.role}</p>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Create button */}
        <button
          onClick={handleCreateCrew}
          disabled={loading || !objective || selectedAgents.length === 0}
          className={`w-full py-2 px-4 rounded font-medium ${
            loading || !objective || selectedAgents.length === 0
              ? 'bg-gray-700 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {loading ? 'Creating...' : 'Create Crew'}
        </button>
      </div>
    </div>
  );
};

export default CrewManager;
