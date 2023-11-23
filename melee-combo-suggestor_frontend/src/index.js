import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import HomePage from './Pages/HomePage/HomePage';
import ErrorPage from './Pages/ErrorPage/ErrorPage';
import Evaluator from './Pages/Evaluator/Evaluator';
import LoginPage from './Pages/LoginPage/LoginPage';
import { AuthProvider } from './AuthContext';
import LandingPage from './Pages/LandingPage/LandingPage';

const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage />, 
    errorElement: <ErrorPage />
  },
  {
    path: "/homepage",
    element: <HomePage />, 
    errorElement: <ErrorPage />
  },
  {
    path: "/evaluator",
    element: <Evaluator />, 
    errorElement: <ErrorPage />
  },
  {
    path: "/login",
    element: <LoginPage />, 
    errorElement: <ErrorPage />
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider>
      <div className="app-background">
        <div className="app-overlay"></div>
        <RouterProvider router={router} />
      </div>
    </AuthProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
