import {useAuth} from "@clerk/clerk-react";

export const useApi = () => {
    const {getToken} = useAuth();

    const makeRequest = async (endpoint, options = {}) => {
        const token = await getToken({});
        const defaultOptions = {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            }
        }

        const response = await fetch(`https://localhost:8000/${endpoint}`,
            {
                ...defaultOptions,
                ...options,
            }
        );
        if (!response.ok) {
            const errorData = await response.json().catch(() => null)
            if (response.status === 429) {
                throw new Error("Rate limit exceeded. Please try again later.");
            }
            throw new Error(errorData?.detail || 'An error occurred while making the request.');
        }
        return response.json();
    }

    return { makeRequest };
}