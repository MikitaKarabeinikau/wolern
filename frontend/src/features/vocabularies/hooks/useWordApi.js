import { useAuth } from "@clerk/clerk-react";

export function useWordApi(onDataChange) {
  const { getToken } = useAuth();

  const fetchWithToken = async (url, options) => {
  const token = await getToken();
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  console.log("Response Status:", response.status);
  console.log("Response Headers:", response.headers);

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  // Handle 204 No Content responses
  if (response.status === 204) {
    return null; // No content to parse
  }

  // Check if the response has a JSON content type
  const contentType = response.headers.get("Content-Type");
  if (contentType && contentType.includes("application/json")) {
    return response.json(); // Parse JSON if available
  }

  return null; // Return null for non-JSON responses
};

const deleteItem = async (url) => {
  try {
    console.log("Delete request URL:", url);
    const response = await fetchWithToken(url, { method: "DELETE" });
    console.log("Item deleted successfully:", response); // Response will likely be null
    if (onDataChange) {
      onDataChange(); // Trigger state update
    }
  } catch (error) {
    console.error("Error deleting item:", error);
  }
};

  const updateItem = async (url, body) => {
    try {

      const response = await fetchWithToken(url, {
        method: "PUT",
        body: JSON.stringify(body),
      });

      console.log("Item updated successfully:", response);
      if (onDataChange) {
        onDataChange(); // Trigger state update
      }
    } catch (error) {
      console.error("Error updating item:", error);
    }
  };


  const addItem = async (url, body) => {
    try {
      await fetchWithToken(url, {
        method: "POST",
        body: JSON.stringify(body),
      });
      console.log("Item added successfully");
      onDataChange();
    } catch (error) {
      console.error("Error adding item:", error);
    }
  };

  return { deleteItem, updateItem, addItem };
}
