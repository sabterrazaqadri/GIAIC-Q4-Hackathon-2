const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';

class APIClient {
  async request(endpoint, options = {}) {
    const url = `${BACKEND_URL}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    try {
      const response = await fetch(url, {
        ...defaultOptions,
        ...options,
        headers: {
          ...defaultOptions.headers,
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Request Failed:', error);
      throw error;
    }
  }

  async chat(message) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  async getHealth() {
    return this.request('/health', {
      method: 'GET',
    });
  }
}

export const api = new APIClient();
