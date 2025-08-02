import React from 'react';
import { BarChart3, Users, Settings, Home } from 'lucide-react';

const Sidebar: React.FC = () => {
  const menuItems = [
    { icon: <Home className="h-5 w-5" />, label: 'Dashboard', active: true },
    { icon: <BarChart3 className="h-5 w-5" />, label: 'Analytics' },
    { icon: <Users className="h-5 w-5" />, label: 'Users' },
    { icon: <Settings className="h-5 w-5" />, label: 'Settings' }
  ];

  return (
    <div className="bg-gray-800 text-white w-64 flex-shrink-0">
      <div className="p-6">
        <h1 className="text-2xl font-bold">Analytics</h1>
      </div>
      
      <nav className="mt-6">
        <div className="px-4">
          {menuItems.map((item, index) => (
            <a
              key={index}
              href="#"
              className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                item.active
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <span className="mr-3">{item.icon}</span>
              {item.label}
            </a>
          ))}
        </div>
      </nav>
    </div>
  );
};

export default Sidebar; 