"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { User, api } from "@/lib/api";
import { LoginData, authService } from "@/services/auth.service";
import { useRouter } from "next/navigation";

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (data: LoginData) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    const fetchUser = async () => {
        const token = localStorage.getItem("token");
        if (token) {
            try {
                const userData = await api.users.me();
                setUser(userData);
            } catch (e) {
                console.error("Failed to fetch user", e);
                localStorage.removeItem("token");
                setUser(null);
            }
        } else {
            setUser(null);
        }
        setIsLoading(false);
    };

    useEffect(() => {
        fetchUser();
    }, []);

    const login = async (data: LoginData) => {
        setIsLoading(true);
        try {
            const response = await authService.login(data);
            localStorage.setItem("token", response.access_token);
            await fetchUser(); // Update state immediately
            router.push("/");
        } catch (error) {
            console.error("Login failed", error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
        router.push("/login");
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                isLoading,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}
