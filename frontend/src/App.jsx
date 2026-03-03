import { useState } from 'react';
import EmployeeList from './components/EmployeeList';
import EmployeeForm from './components/EmployeeForm';
import './styles/App.css';

function App() {
  const [editingEmployee, setEditingEmployee] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleEdit = (employee) => {
    setEditingEmployee(employee);
    // Scroll to form
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSuccess = () => {
    setEditingEmployee(null);
    setRefreshTrigger(prev => prev + 1); // Trigger list refresh
  };

  const handleCancel = () => {
    setEditingEmployee(null);
  };

  return (
    <div className="app">
      <header>
        <h1>Employee Management System</h1>
      </header>
      
      <main>
        <EmployeeForm 
          employeeToEdit={editingEmployee}
          onSuccess={handleSuccess}
          onCancel={handleCancel}
        />
        
        <EmployeeList 
          onEdit={handleEdit}
          onRefresh={refreshTrigger}
        />
      </main>
    </div>
  );
}

export default App;