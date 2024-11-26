export interface Agent {
  id: string;
  name: string;
  role: string;
  status: 'active' | 'inactive';
  position: [number, number, number];
  bodyParams: {
    height: number;
    neckGirth: number;
    chestGirth: number;
    waistGirth: number;
    hipGirth: number;
    inseam: number;
  };
  skills: string[];
  expertise: number;
  backstory?: string;
}

export interface Task {
  id: string;
  name: string;
  description: string;
  status: 'pending' | 'in-progress' | 'completed' | 'failed';
  position: [number, number, number];
  assignedAgents: string[];
  priority: 'low' | 'medium' | 'high';
  dependencies?: string[];
  deadline?: Date;
  progress: number;
}

export interface Crew {
  id: string;
  name: string;
  agents: Agent[];
  tasks: Task[];
  objective: string;
  status: 'assembling' | 'active' | 'completed';
  createdAt: Date;
  completedAt?: Date;
}

export interface VisualSettings {
  ambientLightIntensity: number;
  pointLightIntensity: number;
  glowIntensity: number;
  bloomThreshold: number;
  bloomStrength: number;
  bloomRadius: number;
}

export interface CrewAIConfig {
  apiEndpoint: string;
  apiKey: string;
  modelName: string;
  temperature: number;
  maxTokens: number;
}
