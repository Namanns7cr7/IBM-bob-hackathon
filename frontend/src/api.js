import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadRepo = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload-repo', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const analyzeRepo = async (repoId, skillLevel, goal) => {
  const response = await api.post('/analyze', {
    repo_id: repoId,
    skill_level: skillLevel,
    goal: goal,
  });
  
  return response.data;
};

export const debugError = async (repoId, errorLog, skillLevel) => {
  const response = await api.post('/debug', {
    repo_id: repoId,
    error_log: errorLog,
    skill_level: skillLevel,
  });
  
  return response.data;
};

export const getDocs = async (concept) => {
  const response = await api.get(`/docs/${concept}`);
  return response.data;
};

export const listDocs = async () => {
  const response = await api.get('/docs');
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const getFeatureWalkthrough = async (repoId, featureName, skillLevel) => {
  const response = await api.post('/feature-walkthrough', {
    repo_id: repoId,
    feature_name: featureName,
    skill_level: skillLevel,
  });
  return response.data;
};

export const downloadReport = async (sessionId) => {
  const response = await api.get(`/download-report/${sessionId}`);
  return response.data;
};

export const getMemory = async (sessionId) => {
  const response = await api.get(`/memory/${sessionId}`);
  return response.data;
};

export const markConceptLearned = async (sessionId, conceptName) => {
  const response = await api.post('/memory/concept-learned', null, {
    params: {
      session_id: sessionId,
      concept_name: conceptName,
    },
  });
  return response.data;
};

export const getDocsCacheStats = async () => {
  const response = await api.get('/official-docs/cache-stats');
  return response.data;
};

export default api;

// Made with Bob
