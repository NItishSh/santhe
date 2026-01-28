import { httpClient } from "@/lib/http-client";

export interface User {
    username: string;
    email: string;
    role: string;
    first_name?: string;
    last_name?: string;
    phone_number?: string;
    address?: string;
    date_of_birth?: string;
    payment_method_token?: string;
}

export const userService = {
    getMe: async (): Promise<User> => {
        return httpClient.get<User>('/users/me');
    }
};
