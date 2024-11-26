import { atom } from 'jotai';

// Estado da tripulação
export const crewStateAtom = atom({
  name: 'Odysseus Crew',
  status: 'active',
  mission: 'AI Development Research',
  location: 'Alpha Centauri Research Station',
});

// Estado dos agentes
export const agentsAtom = atom([
  {
    id: 1,
    name: 'Commander Sarah',
    role: 'Research Lead',
    status: 'active',
    specialty: 'AI Strategy',
    experience: 'Senior',
    avatar: '/models/commander.glb',
    position: [0, 0, 5],
  },
  {
    id: 2,
    name: 'Dr. Marcus',
    role: 'Data Scientist',
    status: 'active',
    specialty: 'Machine Learning',
    experience: 'Expert',
    avatar: '/models/scientist.glb',
    position: [5, 0, 0],
  },
  {
    id: 3,
    name: 'Engineer Alex',
    role: 'AI Engineer',
    status: 'active',
    specialty: 'Neural Networks',
    experience: 'Mid-Level',
    avatar: '/models/engineer.glb',
    position: [-5, 0, 0],
  },
]);

// Estado das tarefas
export const tasksAtom = atom([
  {
    id: 1,
    name: 'Market Analysis',
    description: 'Analyze current AI market trends and opportunities',
    status: 'in-progress',
    assignedAgents: ['Commander Sarah', 'Dr. Marcus'],
    priority: 'high',
    deadline: '2024-03-01',
    progress: 65,
    position: [0, 5, 5],
  },
  {
    id: 2,
    name: 'Technology Assessment',
    description: 'Evaluate emerging AI technologies and their potential impact',
    status: 'pending',
    assignedAgents: ['Dr. Marcus'],
    priority: 'medium',
    deadline: '2024-03-15',
    progress: 0,
    position: [5, 5, 0],
  },
  {
    id: 3,
    name: 'Neural Network Design',
    description: 'Design and implement new neural network architecture',
    status: 'completed',
    assignedAgents: ['Engineer Alex'],
    priority: 'high',
    deadline: '2024-02-28',
    progress: 100,
    position: [-5, 5, 0],
  },
]);

// Estado da entidade selecionada
export const selectedEntityAtom = atom(null);

// Estado das conexões entre agentes e tarefas
export const connectionsAtom = atom([
  { start: 'Commander Sarah', end: 'Market Analysis', type: 'assigned' },
  { start: 'Dr. Marcus', end: 'Market Analysis', type: 'assigned' },
  { start: 'Dr. Marcus', end: 'Technology Assessment', type: 'assigned' },
  { start: 'Engineer Alex', end: 'Neural Network Design', type: 'completed' },
]);

// Estado das configurações visuais
export const visualSettingsAtom = atom({
  showLabels: true,
  showConnections: true,
  connectionOpacity: 0.8,
  glowIntensity: 1.5,
  ambientLightIntensity: 0.2,
  pointLightIntensity: 1.0,
});
