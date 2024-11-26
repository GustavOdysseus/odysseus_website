import { create } from 'zustand';
import { Agent, Task, Crew, VisualSettings, CrewAIConfig } from '../types';

interface SpaceState {
  agents: Agent[];
  tasks: Task[];
  crews: Crew[];
  visualSettings: VisualSettings;
  crewAIConfig: CrewAIConfig;
  selectedEntity: { type: 'agent' | 'task' | 'crew'; data: Agent | Task | Crew } | null;
  
  // Actions
  addAgent: (agent: Agent) => void;
  updateAgent: (id: string, updates: Partial<Agent>) => void;
  removeAgent: (id: string) => void;
  
  addTask: (task: Task) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  removeTask: (id: string) => void;
  
  createCrew: (crew: Crew) => void;
  updateCrew: (id: string, updates: Partial<Crew>) => void;
  disbandCrew: (id: string) => void;
  
  setSelectedEntity: (entity: SpaceState['selectedEntity']) => void;
  updateVisualSettings: (settings: Partial<VisualSettings>) => void;
  updateCrewAIConfig: (config: Partial<CrewAIConfig>) => void;
}

export const useSpaceStore = create<SpaceState>((set) => ({
  agents: [],
  tasks: [],
  crews: [],
  selectedEntity: null,
  visualSettings: {
    ambientLightIntensity: 0.5,
    pointLightIntensity: 1.0,
    glowIntensity: 0.8,
    bloomThreshold: 0.9,
    bloomStrength: 1.5,
    bloomRadius: 0.4,
  },
  crewAIConfig: {
    apiEndpoint: 'http://localhost:8000',
    apiKey: '',
    modelName: 'gpt-4',
    temperature: 0.7,
    maxTokens: 1000,
  },

  // Agent actions
  addAgent: (agent) => set((state) => ({ 
    agents: [...state.agents, agent] 
  })),
  
  updateAgent: (id, updates) => set((state) => ({
    agents: state.agents.map((agent) =>
      agent.id === id ? { ...agent, ...updates } : agent
    ),
  })),
  
  removeAgent: (id) => set((state) => ({
    agents: state.agents.filter((agent) => agent.id !== id),
  })),

  // Task actions
  addTask: (task) => set((state) => ({ 
    tasks: [...state.tasks, task] 
  })),
  
  updateTask: (id, updates) => set((state) => ({
    tasks: state.tasks.map((task) =>
      task.id === id ? { ...task, ...updates } : task
    ),
  })),
  
  removeTask: (id) => set((state) => ({
    tasks: state.tasks.filter((task) => task.id !== id),
  })),

  // Crew actions
  createCrew: (crew) => set((state) => ({
    crews: [...state.crews, crew],
  })),
  
  updateCrew: (id, updates) => set((state) => ({
    crews: state.crews.map((crew) =>
      crew.id === id ? { ...crew, ...updates } : crew
    ),
  })),
  
  disbandCrew: (id) => set((state) => ({
    crews: state.crews.filter((crew) => crew.id !== id),
  })),

  // Other actions
  setSelectedEntity: (entity) => set({ selectedEntity: entity }),
  
  updateVisualSettings: (settings) => set((state) => ({
    visualSettings: { ...state.visualSettings, ...settings },
  })),
  
  updateCrewAIConfig: (config) => set((state) => ({
    crewAIConfig: { ...state.crewAIConfig, ...config },
  })),
}));
