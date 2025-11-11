const API_BASE_URL = "http://localhost:8000";

/**
 * A centralized function for making authenticated API requests.
 * @param {string} endpoint - The API endpoint (e.g., "/exercise/quota").
 * @param {function} getToken - The Clerk `getToken` function.
 * @param {object} options - Optional fetch options (method, body, etc.).
 * @returns {Promise<any>} - The JSON response from the API.
 */

export const apiClient = async (endpoint, getToken, options = {}) => {
  try {
    const token = await getToken();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Request failed with status ${response.status}`);
    }

    // Handle cases with no content in the response
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      return response.json();
    }
    return; // Return undefined for 204 No Content, etc.

  } catch (error) {
    console.error(`API Client Error: ${error.message}`);
    // Re-throw the error so the calling function can handle it
    throw error;
  }
};