import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { userService, User } from '@/services/user.service';
import { useAuth } from './useAuth';

export function useUser() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { logout } = useAuth();
    const router = useRouter();

    const fetchUser = useCallback(async () => {
        try {
            setLoading(true);
            const userData = await userService.getMe();
            setUser(userData);
        } catch (err: any) {
            setError(err.message || 'Failed to load profile');
            // Check if unauthorized, then logout
            if (err.status === 401) {
                logout();
            }
        } finally {
            setLoading(false);
        }
    }, [logout]);

    useEffect(() => {
        // Only fetch if we have a token (simple check)
        const token = localStorage.getItem('token');
        if (!token) {
            setLoading(false);
            return;
        }
        fetchUser();
    }, [fetchUser]);

    return {
        user,
        loading,
        error,
        refetch: fetchUser
    };
}
