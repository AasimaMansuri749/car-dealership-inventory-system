import React from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <button 
            onClick={handleLogout}
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none transition-colors"
          >
            Logout
          </button>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 flex items-center justify-center">
        <div className="px-4 py-6 sm:px-0 text-center">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center p-12 bg-white">
            <div>
              <h2 className="text-2xl font-semibold text-gray-800 mb-2">Welcome to Car Dealership Dashboard</h2>
              <p className="text-gray-500">Your authentication was successful. Vehicle management features coming soon!</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
