"use client"

import { useState, useRef, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { User } from "@/lib/api"

interface UserMenuProps {
    user: User | null;
    onLogout: () => void;
}

export function UserMenu({ user, onLogout }: UserMenuProps) {
    const [isOpen, setIsOpen] = useState(false)
    const menuRef = useRef<HTMLDivElement>(null)
    const router = useRouter()

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setIsOpen(false)
            }
        }
        document.addEventListener("mousedown", handleClickOutside)
        return () => {
            document.removeEventListener("mousedown", handleClickOutside)
        }
    }, [menuRef])

    const handleNavigation = (path: string) => {
        router.push(path)
        setIsOpen(false)
    }

    return (
        <div className="relative" ref={menuRef}>
            <Button
                variant="ghost"
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 font-semibold"
            >
                {/* Simplified User Icon SVG */}
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
                {(user?.first_name && user?.last_name) ? `${user.first_name} ${user.last_name}` : (user?.username || "Account")}
            </Button>

            {isOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
                    <div className="py-1">
                        <div className="px-4 py-2 border-b">
                            <p className="text-sm font-medium text-gray-900 truncate">
                                {(user?.first_name && user?.last_name) ? `${user.first_name} ${user.last_name}` : user?.username}
                            </p>
                            <p className="text-xs text-gray-500 truncate">
                                {user?.email}
                            </p>
                        </div>

                        <button
                            onClick={() => handleNavigation('/profile')}
                            className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                            Profile
                        </button>

                        <button
                            onClick={() => handleNavigation('/orders')}
                            className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                            My Orders
                        </button>
                        <button
                            onClick={() => handleNavigation('/support')}
                            className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                            Support
                        </button>
                        <button
                            onClick={() => handleNavigation('/feedback')}
                            className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                            Feedback
                        </button>

                        <div className="border-t mt-1"></div>
                        <button
                            onClick={onLogout}
                            className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                        >
                            Log Out
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}
