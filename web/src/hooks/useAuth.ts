import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService, LoginData } from '@/services/auth.service';

export function useAuth() {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const router = useRouter();

    useEffect(() => {
        setIsAuthenticated(authService.isAuthenticated());
        setIsLoading(false);
    }, []);

    const login = async (data: LoginData) => {
        try {
            const response = await authService.login(data);
            localStorage.setItem('token', response.access_token);
            setIsAuthenticated(true);
            return response;
        } catch (error) {
            throw error;
        }
    };

    const logout = () => {
        authService.logout();
        setIsAuthenticated(false);
        router.push('/login');
    };

    return {
        isAuthenticated,
        isLoading,
        login,
        logout
    };
}
