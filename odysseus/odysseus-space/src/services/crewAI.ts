import axios from 'axios';
import { Agent, Task, Crew } from '../types';

const API_ENDPOINT = process.env.REACT_APP_CREWAI_API_ENDPOINT;
const API_KEY = process.env.REACT_APP_CREWAI_API_KEY;

if (!API_ENDPOINT || !API_KEY) {
  throw new Error('CrewAI API configuration missing. Please check your .env file.');
}

const api = axios.create({
  baseURL: API_ENDPOINT,
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
  },
});

class CrewAIService {
  async generateAgent(role: string, expertise: number): Promise<Agent> {
    try {
      const { data } = await api.post<Agent>('/agents/generate', {
        role,
        expertise,
        model: 'default',
        temperature: 0.5,
      });
      return data;
    } catch (error) {
      console.error('Error generating agent:', error);
      throw error;
    }
  }

  async suggestAgentSkills(role: string): Promise<string[]> {
    try {
      const { data } = await api.post<string[]>('/agents/suggest-skills', { role });
      return data;
    } catch (error) {
      console.error('Error suggesting agent skills:', error);
      throw error;
    }
  }

  async generateTask(objective: string, assignedAgents: string[]): Promise<Task> {
    try {
      const { data } = await api.post<Task>('/tasks/generate', {
        objective,
        assignedAgents,
      });
      return data;
    } catch (error) {
      console.error('Error generating task:', error);
      throw error;
    }
  }

  async analyzeTaskDependencies(tasks: Task[]): Promise<{ [taskId: string]: string[] }> {
    try {
      const { data } = await api.post<{ [taskId: string]: string[] }>('/tasks/analyze-dependencies', {
        tasks,
      });
      return data;
    } catch (error) {
      console.error('Error analyzing task dependencies:', error);
      throw error;
    }
  }

  async optimizeCrew(objective: string, availableAgents: Agent[]): Promise<{
    selectedAgents: string[];
    suggestedTasks: Task[];
  }> {
    try {
      const { data } = await api.post<{
        selectedAgents: string[];
        suggestedTasks: Task[];
      }>('/crews/optimize', {
        objective,
        availableAgents,
      });
      return data;
    } catch (error) {
      console.error('Error optimizing crew:', error);
      throw error;
    }
  }

  async simulateCrewExecution(crew: Crew): Promise<{
    success: boolean;
    estimatedCompletion: number;
    potentialIssues: string[];
    suggestions: string[];
  }> {
    try {
      const { data } = await api.post<{
        success: boolean;
        estimatedCompletion: number;
        potentialIssues: string[];
        suggestions: string[];
      }>('/crews/simulate', { crew });
      return data;
    } catch (error) {
      console.error('Error simulating crew execution:', error);
      throw error;
    }
  }

  async getAgentResponse(agentId: string, input: string): Promise<{
    response: string;
    confidence: number;
    suggestedActions?: string[];
  }> {
    try {
      const { data } = await api.post<{
        response: string;
        confidence: number;
        suggestedActions?: string[];
      }>('/agents/interact', {
        agentId,
        input,
      });
      return data;
    } catch (error) {
      console.error('Error getting agent response:', error);
      throw error;
    }
  }

  async analyzeTaskProgress(taskId: string, updates: string[]): Promise<{
    progress: number;
    status: Task['status'];
    nextSteps: string[];
  }> {
    try {
      const { data } = await api.post<{
        progress: number;
        status: Task['status'];
        nextSteps: string[];
      }>('/tasks/analyze-progress', {
        taskId,
        updates,
      });
      return data;
    } catch (error) {
      console.error('Error analyzing task progress:', error);
      throw error;
    }
  }

  async suggestCrewImprovements(crew: Crew): Promise<{
    agentSuggestions: { add: Agent[]; remove: string[] };
    taskOptimizations: { [taskId: string]: string[] };
    workflowSuggestions: string[];
  }> {
    try {
      const { data } = await api.post<{
        agentSuggestions: { add: Agent[]; remove: string[] };
        taskOptimizations: { [taskId: string]: string[] };
        workflowSuggestions: string[];
      }>('/crews/suggest-improvements', { crew });
      return data;
    } catch (error) {
      console.error('Error suggesting crew improvements:', error);
      throw error;
    }
  }
}

export const crewAIService = new CrewAIService();
