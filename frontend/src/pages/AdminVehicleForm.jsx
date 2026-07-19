import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../api/axios';
import InputField from '../components/InputField';
import Button from '../components/Button';

const AdminVehicleForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditMode = !!id;

  const [formData, setFormData] = useState({
    make: '',
    model: '',
    category: '',
    price: '',
    quantity: '',
    description: '',
    year: new Date().getFullYear(),
    color: '',
    mileage: '',
    fuel_type: 'Petrol',
    transmission: 'Automatic',
    image_url: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [fetching, setFetching] = useState(isEditMode);

  useEffect(() => {
    if (isEditMode) {
      const fetchVehicle = async () => {
        try {
          const response = await api.get(`/api/vehicles/${id}`);
          const data = response.data;
          setFormData({
            make: data.make,
            model: data.model,
            category: data.category,
            price: data.price,
            quantity: data.quantity,
            description: data.description || '',
            year: data.year,
            color: data.color,
            mileage: data.mileage,
            fuel_type: data.fuel_type,
            transmission: data.transmission,
            image_url: data.image_url || ''
          });
        } catch (err) {
          setError('Failed to fetch vehicle details.');
        } finally {
          setFetching(false);
        }
      };
      fetchVehicle();
    }
  }, [id, isEditMode]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const payload = {
      ...formData,
      price: parseFloat(formData.price),
      quantity: parseInt(formData.quantity, 10),
      year: parseInt(formData.year, 10),
      mileage: parseInt(formData.mileage, 10)
    };

    try {
      if (isEditMode) {
        await api.put(`/api/vehicles/${id}`, payload);
      } else {
        await api.post('/api/vehicles', payload);
      }
      navigate('/dashboard');
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        if (Array.isArray(err.response.data.detail)) {
          setError(err.response.data.detail[0].msg);
        } else {
          setError(err.response.data.detail);
        }
      } else {
        setError('Operation failed. Please check form inputs and try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (fetching) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin inline-block w-8 h-8 border-4 border-current border-t-transparent text-blue-600 rounded-full" role="status"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-sm border border-gray-100">
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">
            {isEditMode ? 'Edit Vehicle Details' : 'Add New Vehicle'}
          </h2>
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="text-sm font-medium text-gray-600 hover:text-gray-900 bg-gray-100 hover:bg-gray-200 px-3 py-1.5 rounded transition"
          >
            Cancel
          </button>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <InputField label="Make" id="make" value={formData.make} onChange={handleChange} placeholder="e.g. Toyota" />
            <InputField label="Model" id="model" value={formData.model} onChange={handleChange} placeholder="e.g. Camry" />
            <InputField label="Category" id="category" value={formData.category} onChange={handleChange} placeholder="e.g. Sedan" />
            <InputField label="Year" id="year" type="number" value={formData.year} onChange={handleChange} placeholder="e.g. 2025" />
            <InputField label="Price (₹)" id="price" type="number" value={formData.price} onChange={handleChange} placeholder="e.g. 250000" />
            <InputField label="Quantity in Stock" id="quantity" type="number" value={formData.quantity} onChange={handleChange} placeholder="e.g. 5" />
            <InputField label="Color" id="color" value={formData.color} onChange={handleChange} placeholder="e.g. Black" />
            <InputField label="Mileage (mi)" id="mileage" type="number" value={formData.mileage} onChange={handleChange} placeholder="e.g. 15000" />

            <div>
              <label htmlFor="fuel_type" className="block text-sm font-medium text-gray-700 mb-1">Fuel Type</label>
              <select
                id="fuel_type"
                name="fuel_type"
                value={formData.fuel_type}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              >
                <option value="Petrol">Petrol</option>
                <option value="Diesel">Diesel</option>
                <option value="Electric">Electric</option>
                <option value="Hybrid">Hybrid</option>
              </select>
            </div>

            <div>
              <label htmlFor="transmission" className="block text-sm font-medium text-gray-700 mb-1">Transmission</label>
              <select
                id="transmission"
                name="transmission"
                value={formData.transmission}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              >
                <option value="Automatic">Automatic</option>
                <option value="Manual">Manual</option>
              </select>
            </div>
          </div>

          <InputField label="Image URL (Optional)" id="image_url" value={formData.image_url} onChange={handleChange} placeholder="https://example.com/image.jpg" required={false} />

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">Description (Optional)</label>
            <textarea
              id="description"
              name="description"
              rows="3"
              value={formData.description}
              onChange={handleChange}
              placeholder="Provide a description of the vehicle..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            ></textarea>
          </div>

          <div>
            <Button type="submit" disabled={loading}>
              {loading ? 'Saving details...' : isEditMode ? 'Update Vehicle' : 'Add Vehicle'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminVehicleForm;
