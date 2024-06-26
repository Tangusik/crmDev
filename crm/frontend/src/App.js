import React, { useEffect, useState } from 'react';
import { Routes, Route, useNavigate, useLocation, Navigate } from 'react-router-dom';
import Sign from './Sign';
import Colleagues from './Colleagues';
import Clients from './Clients';
import Schedule from './Schedule';
import Main from './Main';
import ClientPage from './ClientPage';
import { fetchGet } from "./api/get";

function RequireAuth({ children }) {
    const navigate = useNavigate();
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await fetchGet('check-auth');
                setIsAuthenticated(response.authenticated);

                if (!response.authenticated) {
                    navigate('/sign', { replace: true });
                }
            } catch (error) {
                console.error('Ошибка при проверке аутентификации:', error);
                setIsAuthenticated(false);
                navigate('/sign', { replace: true });
            }
        };

        checkAuth();
    }, [navigate]);

    if (isAuthenticated === null) {
        return <div>Загрузка...</div>;
    }

    return isAuthenticated ? children : null;
}

export const App = () => {
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await fetchGet('check-auth');
                setIsAuthenticated(response.authenticated);
            } catch (error) {
                console.error('Ошибка при проверке аутентификации:', error);
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, []);

    if (loading) {
        return <div>Загрузка...</div>;
    }

    return (
        <Routes>
            <Route path="/sign" element={<Sign />} />
            <Route
                path="/"
                element={
                    isAuthenticated ? <Navigate to="/main" /> : <Navigate to="/sign" />
                }
            />
            <Route
                path="colleagues"
                element={
                    <RequireAuth>
                        <Colleagues />
                    </RequireAuth>
                }
            />
            <Route
                path="clients"
                element={
                    <RequireAuth>
                        <Clients />
                    </RequireAuth>
                }
            />
            <Route
                path="schedule"
                element={
                    <RequireAuth>
                        <Schedule />
                    </RequireAuth>
                }
            />
            <Route
                path="main"
                element={
                    <RequireAuth>
                        <Main />
                    </RequireAuth>
                }
            />
            <Route
                path="client/:id"
                element={
                    <RequireAuth>
                        <ClientPage />
                    </RequireAuth>
                }
            />
        </Routes>
    );
};