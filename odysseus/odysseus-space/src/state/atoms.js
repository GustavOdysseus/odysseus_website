import { atom } from 'jotai';

export const crewStateAtom = atom({
  name: 'Odysseus Crew',
  status: 'active',
  mission: 'AI Development Research',
});

export const agentsAtom = atom([
  {
    id: 1,
    name: 'Commander Sarah',
    role: 'Research Lead',
    status: 'active',
    specialty: 'AI Strategy',
    avatar: '/models/commander.glb',
  },
  {
    id: 2,
    name: 'Dr. Marcus',
    role: 'Data Scientist',
    status: 'active',
    specialty: 'Machine Learning',
    avatar: '/models/scientist.glb',
  },
  // Add more agents as needed
]);

export const tasksAtom = atom([
  {
    id: 1,
    name: 'Market Analysis',
    description: 'Analyze current AI market trends and opportunities',
    status: 'in-progress',
    assignedAgents: ['Commander Sarah', 'Dr. Marcus'],
    priority: 'high',
    deadline: '2024-03-01',
  },
  {
    id: 2,
    name: 'Technology Assessment',
    description: 'Evaluate emerging AI technologies and their potential impact',
    status: 'pending',
    assignedAgents: ['Dr. Marcus'],
    priority: 'medium',
    deadline: '2024-03-15',
  },
  // Add more tasks as needed
]);

export const selectedEntityAtom = atom(null);
