import { httpClient } from "@/lib/http-client";

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export interface RegisterData {
    username: string;
    email: string;
    password: string;
    role: string;
    first_name: string;
    last_name: string;
    phone_number: string;
    address: string;
    date_of_birth: string;
    payment_method_token: string;
}

export interface LoginData {
    username: string;
    password: string;
}

export const authService = {
    login: async (data: LoginData): Promise<AuthResponse> => {
        return httpClient.post<AuthResponse>('/auth/login', data);
    },

    register: async (data: RegisterData): Promise<any> => {
        return httpClient.post('/users/register', data);
    },

    logout: () => {
        localStorage.removeItem('token');
        // Optional: Call backend to invalidate token if supported
    },

    getToken: () => {
        if (typeof window !== 'undefined') {
            return localStorage.getItem('token');
        }
        return null;
    },

    isAuthenticated: () => {
        if (typeof window !== 'undefined') {
            return !!localStorage.getItem('token');
        }
        return false;
    }
};
