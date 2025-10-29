// API configuration
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const API_BASE_URL = `${API_URL}/api/v1`;

// Chat endpoints
export const chatEndpoint = `${API_BASE_URL}/chat`;

// Auth endpoints
export const authEndpoints = {
  login: `${API_BASE_URL}/auth/login`,
  initAdmin: `${API_BASE_URL}/auth/init-admin`,
};

// Admin endpoints
export const adminEndpoints = {
  chatHistory: `${API_BASE_URL}/admin/chat-history`,
  documents: `${API_BASE_URL}/admin/documents`,
  uploadDocument: `${API_BASE_URL}/admin/documents/upload`,
  deleteDocument: (docId: number) => `${API_BASE_URL}/admin/documents/${docId}`,
};

