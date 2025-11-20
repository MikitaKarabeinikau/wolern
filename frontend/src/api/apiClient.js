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

/**
 * Simple API call function that uses full URL
 * @param {string} url - The full API URL
 * @param {function} getToken - The Clerk `getToken` function
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {object} body - Request body
 * @returns {Promise<any>} - The JSON response from the API
 */
export const apiCall = async (url, getToken, method = "GET", body = null) => {
  try {
    const token = await getToken();
    
    console.log('Making API call:', { url, method, body });
    
    const response = await fetch(url, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      ...(body && { body: JSON.stringify(body) }),
    });
    
    console.log('API response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('API error:', errorText);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      const data = await response.json();
      console.log('API response data:', data);
      return data;
    }
    return;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};