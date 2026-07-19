import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import Button from '../components/Button';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [vehicles, setVehicles] = useState([]);
  const [searchFilters, setSearchFilters] = useState({
    make: '',
    model: '',
    category: '',
    min_price: '',
    max_price: ''
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [restockQuantities, setRestockQuantities] = useState({});

  const fetchVehicles = async (filters = {}) => {
    setLoading(true);
    setError('');
    try {
      const activeFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, val]) => val !== '')
      );

      const queryStr = new URLSearchParams(activeFilters).toString();
      const endpoint = queryStr ? `/api/vehicles/search?${queryStr}` : '/api/vehicles';
      const response = await api.get(endpoint);
      setVehicles(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load vehicles.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVehicles();
  }, []);

  // const inventoryStats = useMemo(() => {
  //   const total = vehicles.length;
  //   const inStock = vehicles.filter((vehicle) => vehicle.quantity > 0).length;
  //   const outOfStock = total - inStock;
  //   const averagePrice = total
  //     ? vehicles.reduce((sum, vehicle) => sum + Number(vehicle.price || 0), 0) / total
  //     : 0;

  //   return { total, inStock, outOfStock, averagePrice };
  // }, [vehicles]);


  const inventoryStats = useMemo(() => {

    // Total vehicle models/listings
    const total = vehicles.length;


    // Total number of cars available
    // Example:
    // Toyota quantity 3
    // BMW quantity 5
    // Available Stock = 8

    const availableStock = vehicles.reduce(
      (sum, vehicle) => sum + Number(vehicle.quantity || 0),
      0
    );


    // Number of vehicle models which have no stock
    const outOfStock = vehicles.filter(
      (vehicle) => Number(vehicle.quantity) === 0
    ).length;



    const averagePrice = total
      ? vehicles.reduce(
        (sum, vehicle) => sum + Number(vehicle.price || 0),
        0
      ) / total
      : 0;


    return {
      total,
      availableStock,
      outOfStock,
      averagePrice
    };

  }, [vehicles]);


  const handleFilterChange = (e) => {
    setSearchFilters({ ...searchFilters, [e.target.name]: e.target.value });
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchVehicles(searchFilters);
  };

  const handleClearFilters = () => {
    const cleared = { make: '', model: '', category: '', min_price: '', max_price: '' };
    setSearchFilters(cleared);
    fetchVehicles(cleared);
  };

  const handlePurchase = async (id) => {
    setError('');
    setSuccess('');
    try {
      const response = await api.post(`/api/vehicles/${id}/purchase`);
      setVehicles((current) => current.map((vehicle) => (vehicle.id === id ? response.data : vehicle)));
      setSuccess('Vehicle purchased successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Purchase failed.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this vehicle?')) return;
    setError('');
    setSuccess('');
    try {
      await api.delete(`/api/vehicles/${id}`);
      setVehicles((current) => current.filter((vehicle) => vehicle.id !== id));
      setSuccess('Vehicle deleted successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Delete failed.');
    }
  };

  const handleRestockChange = (id, val) => {
    setRestockQuantities({ ...restockQuantities, [id]: val });
  };

  const handleRestockSubmit = async (id) => {
    setError('');
    setSuccess('');
    const quantity = parseInt(restockQuantities[id], 10);
    if (isNaN(quantity) || quantity <= 0) {
      setError('Restock quantity must be a positive number.');
      return;
    }
    try {
      const response = await api.post(`/api/vehicles/${id}/restock`, { quantity });
      setVehicles((current) => current.map((vehicle) => (vehicle.id === id ? response.data : vehicle)));
      setRestockQuantities({ ...restockQuantities, [id]: '' });
      setSuccess('Vehicle restocked successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Restock failed.');
    }
  };

  const isAdmin = user && user.role === 'ADMIN';

  // return (
  //   <div className="min-h-screen bg-transparent flex flex-col">
  //     <header className="border-b border-white/60 bg-white/80 backdrop-blur">
  //       <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8  ">
  //         <div className="flex items-center space-x-3">
  //           <div>
  //             <h1 className="text-xl font-semibold text-slate-900">Dealership Inventory System</h1>
  //           </div>
  //         </div>
  //         <div className="flex items-center space-x-4">
  //           <span className="hidden text-sm text-slate-600 sm:block">
  //             Welcome, <span className="font-semibold text-slate-800">{user?.username}</span>
  //             {isAdmin && <span className="ml-2 rounded-full bg-blue-100 px-2 py-0.5 text-xs font-semibold text-blue-800">Admin</span>}
  //           </span>
  //           <button
  //             onClick={logout}
  //             className="rounded-xl bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
  //           >
  //             Logout
  //           </button>
  //         </div>
  //       </div>
  //     </header>

  //     <main className="mx-auto flex-1 w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
  //       {success && (
  //         <div className="mb-4 rounded-2xl border border-green-200 bg-green-50 p-4 text-sm text-green-700 shadow-sm">
  //           {success}
  //         </div>
  //       )}
  //       {error && (
  //         <div className="mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 shadow-sm">
  //           {error}
  //         </div>
  //       )}
  //       {/* {isAdmin && (
  //         <div className="mb-6 rounded-[2rem] bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 p-6 text-white shadow-[0_30px_80px_-40px_rgba(15,23,42,0.9)]">
  //           <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
  //             <div>
  //               <p className="text-sm uppercase tracking-[0.3em] text-blue-200">Inventory command center</p>
  //               <h2 className="mt-2 text-2xl font-semibold sm:text-3xl">Manage your fleet with a calmer, smarter view.</h2>
  //               <p className="mt-2 max-w-2xl text-sm text-slate-300">
  //                 Track stock, restock quickly, and keep every listing polished for your customers.
  //               </p>
  //             </div>
  //             <div className="grid gap-3 sm:grid-cols-3">
  //               <div className="rounded-2xl border border-white/10 bg-white/10 p-3 backdrop-blur">
  //                 <p className="text-xs uppercase tracking-[0.2em] text-blue-100">Listings</p>
  //                 <p className="mt-1 text-xl font-semibold">{inventoryStats.total}</p>
  //               </div>
  //               <div className="rounded-2xl border border-white/10 bg-white/10 p-3 backdrop-blur">
  //                 <p className="text-xs uppercase tracking-[0.2em] text-blue-100">In stock</p>
  //                 <p className="mt-1 text-xl font-semibold">{inventoryStats.inStock}</p>
  //               </div>
  //               <div className="rounded-2xl border border-white/10 bg-white/10 p-3 backdrop-blur">
  //                 <p className="text-xs uppercase tracking-[0.2em] text-blue-100">Avg price</p>
  //                 <p className="mt-1 text-xl font-semibold">${inventoryStats.averagePrice.toLocaleString(undefined, { maximumFractionDigits: 0 })}</p>
  //               </div>
  //             </div>
  //           </div>
  //         </div>
  //       )} */}

  //       {isAdmin && (
  //         <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-4">

  //           <div className="border bg-white p-5 rounded-lg">
  //             <p className="text-sm text-gray-500">
  //               Total Vehicles
  //             </p>
  //             <h3 className="text-3xl font-bold">
  //               {inventoryStats.total}
  //             </h3>
  //           </div>


  //           <div className="border bg-white p-5 rounded-lg">
  //             <p className="text-sm text-gray-500">
  //               Available Stock
  //             </p>
  //             <h3 className="text-3xl font-bold text-green-600">
  //               {inventoryStats.inStock}
  //             </h3>
  //           </div>


  //           <div className="border bg-white p-5 rounded-lg">
  //             <p className="text-sm text-gray-500">
  //               Out Of Stock
  //             </p>
  //             <h3 className="text-3xl font-bold text-red-600">
  //               {inventoryStats.outOfStock}
  //             </h3>
  //           </div>


  //           <div className="border bg-white p-5 rounded-lg">
  //             <p className="text-sm text-gray-500">
  //               Average Price
  //             </p>
  //             <h3 className="text-2xl font-bold">
  //               ${inventoryStats.averagePrice.toLocaleString()}
  //             </h3>
  //           </div>

  //         </div>
  //       )}


  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      <header className="bg-white border-b border-gray-200">
        <div className="mx-auto max-w-7xl px-6 py-4 flex justify-between items-center">

          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              AutoHub Dealership
            </h1>

            <p className="text-sm text-gray-500">
              Vehicle Inventory Management System
            </p>
          </div>


          <div className="flex items-center gap-4">

            <div className="hidden sm:block text-right">

              <p className="text-sm text-gray-500">
                Welcome
              </p>

              <p className="font-semibold text-gray-800">
                {user?.username}

                {isAdmin && (
                  <span className="
                  ml-2
                  bg-black
                  text-white
                  text-xs
                  px-2
                  py-1
                  rounded
                  ">
                    ADMIN
                  </span>
                )}

              </p>

            </div>


            <button
              onClick={logout}
              className="
              border
              border-gray-300
              px-4
              py-2
              rounded-md
              text-sm
              hover:bg-gray-100
              transition
              "
            >
              Logout
            </button>

          </div>

        </div>
      </header>


      <main className="
      flex-1
      mx-auto
      w-full
      max-w-7xl
      px-6
      py-8
      ">


        {success && (
          <div className="
          mb-5
          bg-green-50
          border
          border-green-200
          text-green-700
          px-4
          py-3
          rounded-md
          ">
            {success}
          </div>
        )}


        {error && (
          <div className="
          mb-5
          bg-red-50
          border
          border-red-200
          text-red-700
          px-4
          py-3
          rounded-md
          ">
            {error}
          </div>
        )}



        {isAdmin && (

          <div className="
          grid
          grid-cols-1
          sm:grid-cols-2
          lg:grid-cols-4
          gap-5
          mb-8
          ">


            <div className="
            bg-white
            border
            border-gray-200
            p-5
            rounded-lg
            ">

              <p className="text-sm text-gray-500">
                Total Vehicles
              </p>

              <h2 className="
              mt-2
              text-3xl
              font-bold
              text-gray-900
              ">
                {inventoryStats.total}
              </h2>

            </div>



            <div className="
            bg-white
            border
            border-gray-200
            p-5
            rounded-lg
            ">

              <p className="text-sm text-gray-500">
                Available Stock
              </p>

              <h2 className="
              mt-2
              text-3xl
              font-bold
              text-green-600
              ">
                {inventoryStats.availableStock}
              </h2>

            </div>



            <div className="
            bg-white
            border
            border-gray-200
            p-5
            rounded-lg
            ">

              <p className="text-sm text-gray-500">
                Out Of Stock
              </p>

              <h2 className="
              mt-2
              text-3xl
              font-bold
              text-red-600
              ">
                {inventoryStats.outOfStock}
              </h2>

            </div>




            <div className="
            bg-white
            border
            border-gray-200
            p-5
            rounded-lg
            ">

              <p className="text-sm text-gray-500">
                Average Price
              </p>

              <h2 className="
              mt-2
              text-2xl
              font-bold
              text-gray-900
              ">
                ₹{inventoryStats.averagePrice.toLocaleString(
                  undefined,
                  { maximumFractionDigits: 0 }
                )}
              </h2>

            </div>


          </div>

        )}



        {/* <div className="flex flex-col gap-6 lg:flex-row">
          <aside className="soft-card h-fit w-full p-6 lg:w-72">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-slate-900">Search filters</h2>
            </div>
            <form onSubmit={handleSearchSubmit} className="space-y-4">
              <div>
                <label className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Make</label>
                <input
                  type="text"
                  name="make"
                  value={searchFilters.make}
                  onChange={handleFilterChange}
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="e.g. Toyota"
                />
              </div>
              <div>
                <label className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Model</label>
                <input
                  type="text"
                  name="model"
                  value={searchFilters.model}
                  onChange={handleFilterChange}
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="e.g. Camry"
                />
              </div>
              <div>
                <label className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Category</label>
                <input
                  type="text"
                  name="category"
                  value={searchFilters.category}
                  onChange={handleFilterChange}
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="e.g. Sedan"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Min</label>
                  <input
                    type="number"
                    name="min_price"
                    value={searchFilters.min_price}
                    onChange={handleFilterChange}
                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                    placeholder="Min"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Max</label>
                  <input
                    type="number"
                    name="max_price"
                    value={searchFilters.max_price}
                    onChange={handleFilterChange}
                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                    placeholder="Max"
                  />
                </div>
              </div>
              <div className="flex flex-col space-y-2 pt-2">
                <Button type="submit">Search</Button>
                <button
                  type="button"
                  onClick={handleClearFilters}
                  className="w-full rounded-xl bg-slate-100 px-3 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-200"
                >
                  Clear filters
                </button>
              </div>
            </form>
          </aside>

          <div className="flex-1">
            <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Vehicle inventory</h2>
                <p className="text-sm text-slate-500">{vehicles.length} vehicles currently listed</p>
              </div>
              {isAdmin && (
                <button
                  onClick={() => navigate('/admin/vehicle/new')}
                  className="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-700"
                >
                  + Add vehicle
                </button>
              )}
            </div>

            {loading ? (
              <div className="soft-card py-14 text-center">
                <div className="mx-auto mb-3 inline-block h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" role="status"></div>
                <p className="text-slate-500">Loading inventory...</p>
              </div>
            ) : vehicles.length === 0 ? (
              <div className="soft-card py-16 text-center">
                <p className="text-lg font-medium text-slate-700">Nothing matches that search yet.</p>
                <p className="mt-2 text-sm text-slate-500">Try relaxing the filters to view more inventory.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
                {vehicles.map((vehicle) => (
                  // <div key={vehicle.id} className="soft-card flex h-full flex-col overflow-hidden transition duration-200 hover:-translate-y-1">
                  <div key={vehicle.id} className="bg-white border rounded-xl overflow-hidden hover:shadow-md transition ">

                    <div className="relative flex h-48 items-center justify-center bg-gray-50">
                      {vehicle.image_url ? (
                        <img src={vehicle.image_url} alt={`${vehicle.make} ${vehicle.model}`} className="h-full w-full object-cover" />


                      ) : (
                        <div className="p-4 text-center text-slate-400">
                          <span className="mb-1 block text-4xl">🚗</span>
                          <span className="text-xs uppercase tracking-[0.3em]">{vehicle.category}</span>
                        </div>
                      )}
                      <span className="absolute right-3 top-3 rounded-full bg-white/90 px-2.5 py-1 text-xs font-semibold text-slate-700 shadow-sm">
                        {vehicle.year}
                      </span>
                    </div>

                    <div className="flex flex-1 flex-col justify-between p-5">
                      <div>
                        <div className="mb-2 flex items-start justify-between gap-3">
                          <h3 className="text-lg font-semibold leading-tight text-slate-900">
                            {vehicle.make} {vehicle.model}
                          </h3>
                          <span className="text-lg font-semibold text-blue-600">
                            ${Number(vehicle.price).toLocaleString()}
                          </span>
                        </div>
                        <div className="mb-4 flex flex-wrap gap-2">
                          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs text-slate-600">{vehicle.color}</span>
                          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs text-slate-600">{vehicle.fuel_type}</span>
                          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs text-slate-600">{vehicle.transmission}</span>
                          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs text-slate-600">{vehicle.mileage.toLocaleString()} mi</span>
                        </div>
                        {vehicle.description && <p className="mb-4 text-sm text-slate-500">{vehicle.description}</p>}
                      </div>

                      <div>
                        <div className="mb-4 flex items-center justify-between text-sm">
                          <span className="text-slate-500">Stock status</span>
                          {vehicle.quantity > 0 ? (
                            <span className="rounded-full bg-green-50 px-2.5 py-1 font-semibold text-green-700">
                              {vehicle.quantity} available
                            </span>
                          ) : (
                            <span className="rounded-full bg-red-50 px-2.5 py-1 font-semibold text-red-700">
                              Out of stock
                            </span>
                          )}
                        </div>

                        {!isAdmin && (
                          <button
                            onClick={() => handlePurchase(vehicle.id)}
                            disabled={vehicle.quantity <= 0}
                            className="mb-3 w-full rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:bg-slate-200 disabled:text-slate-400"
                          >
                            {vehicle.quantity > 0 ? "Purchase" : "Out of Stock"}
                          </button>
                        )}

                        {isAdmin && (
                          <div className="space-y-3 border-t border-slate-100 pt-4">
                            <div className="flex gap-2">
                              <button
                                onClick={() => navigate(`/admin/vehicle/edit/${vehicle.id}`)}
                                className="flex-1 rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => handleDelete(vehicle.id)}
                                className="flex-1 rounded-lg border border-red-200 px-3 py-2 text-xs font-semibold text-red-600 transition hover:bg-red-50"
                              >
                                Delete
                              </button>
                            </div>

                            <div className="flex items-center gap-2">
                              <input
                                type="number"
                                min="1"
                                placeholder="Qty"
                                value={restockQuantities[vehicle.id] || ''}
                                onChange={(e) => handleRestockChange(vehicle.id, e.target.value)}
                                className="w-16 rounded-lg border border-slate-200 px-2 py-2 text-xs outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/20"
                              />
                              <button
                                onClick={() => handleRestockSubmit(vehicle.id)}
                                className="rounded-lg bg-slate-800 px-3 py-2 text-xs font-semibold text-white transition hover:bg-slate-900"
                              >
                                Restock
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div> */}


        <div className="flex flex-col gap-8 lg:flex-row">


          {/* FILTER SIDEBAR */}

          <aside className="w-full lg:w-72 bg-white border border-gray-200 rounded-lg p-5 h-fit">

            <h2 className=" text-lg font-semibold text-gray-900 mb-5">
              Search Vehicles
            </h2>


            <form onSubmit={handleSearchSubmit} className="space-y-4">


              <div>
                <label className="text-sm text-gray-600"> Make</label>
                <input type="text" name="make" value={searchFilters.make}
                  onChange={handleFilterChange} placeholder="Toyota"
                  className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:border-black
"
                />

              </div>



              <div>
                <label className="text-sm text-gray-600">
                  Model
                </label>

                <input
                  type="text"
                  name="model"
                  value={searchFilters.model}
                  onChange={handleFilterChange}
                  placeholder="Camry"
                  className="
mt-1
w-full
border
border-gray-300
rounded-md
px-3
py-2
text-sm
focus:outline-none
focus:border-black
"
                />

              </div>




              <div>
                <label className="text-sm text-gray-600">
                  Category
                </label>

                <input
                  type="text"
                  name="category"
                  value={searchFilters.category}
                  onChange={handleFilterChange}
                  placeholder="SUV"
                  className="
mt-1
w-full
border
border-gray-300
rounded-md
px-3
py-2
text-sm
focus:outline-none
focus:border-black
"
                />

              </div>




              <div className="grid grid-cols-2 gap-3">

                <div>

                  <label className="text-sm text-gray-600">
                    Min Price
                  </label>

                  <input
                    type="number"
                    name="min_price"
                    value={searchFilters.min_price}
                    onChange={handleFilterChange}
                    className="
mt-1
w-full
border
rounded-md
px-3
py-2
text-sm
"
                  />

                </div>



                <div>

                  <label className="text-sm text-gray-600">
                    Max Price
                  </label>

                  <input
                    type="number"
                    name="max_price"
                    value={searchFilters.max_price}
                    onChange={handleFilterChange}
                    className="
mt-1
w-full
border
rounded-md
px-3
py-2
text-sm
"
                  />

                </div>


              </div>




              <button
                type="submit"
                className="
w-full
bg-black
text-white
py-2.5
rounded-md
text-sm
font-medium
hover:bg-gray-800
"
              >
                Search
              </button>



              <button
                type="button"
                onClick={handleClearFilters}
                className="
w-full
border
border-gray-300
py-2.5
rounded-md
text-sm
hover:bg-gray-100
"
              >
                Clear
              </button>


            </form>


          </aside>





          {/* VEHICLE SECTION */}

          <div className="flex-1">


            <div className="
flex
justify-between
items-center
mb-6
">


              <div>

                <h2 className="
text-2xl
font-bold
text-gray-900
">
                  Available Vehicles
                </h2>

                <p className="
text-sm
text-gray-500
">
                  {vehicles.length} vehicles found
                </p>

              </div>



              {isAdmin && (

                <button

                  onClick={() =>
                    navigate('/admin/vehicle/new')
                  }

                  className="
bg-black
text-white
px-4
py-2
rounded-md
text-sm
hover:bg-gray-800
"
                >

                  + Add Vehicle

                </button>

              )}


            </div>





            {loading ? (

              <div className="
bg-white
border
rounded-lg
p-10
text-center
">

                Loading vehicles...

              </div>


            ) : vehicles.length === 0 ? (


              <div className="
bg-white
border
rounded-lg
p-10
text-center
">

                <p className="font-semibold">
                  No vehicles found
                </p>

                <p className="text-sm text-gray-500 mt-2">
                  Try changing your filters
                </p>

              </div>



            ) : (



              <div className="
grid
grid-cols-1
md:grid-cols-2
xl:grid-cols-3
gap-6
">


                {vehicles.map((vehicle) => (


                  <div
                    key={vehicle.id}
                    className="
bg-white
border
border-gray-200
rounded-xl
overflow-hidden
hover:shadow-lg
transition
"
                  >



                    {/* IMAGE */}

                    <div className="
h-52
bg-gray-100
relative
">


                      {vehicle.image_url ? (

                        <img
                          src={vehicle.image_url}
                          alt={`${vehicle.make} ${vehicle.model}`}
                          className="
h-full
w-full
object-cover
"
                        />

                      ) : (


                        <div className="
h-full
flex
items-center
justify-center
text-5xl
">

                          🚗

                        </div>

                      )}



                      <span className="
absolute
top-3
right-3
bg-white
border
px-2
py-1
rounded
text-xs
">

                        {vehicle.year}

                      </span>


                    </div>





                    <div className="
p-5
">


                      <div className="
flex
justify-between
gap-3
mb-3
">


                        <h3 className="
font-bold
text-lg
">

                          {vehicle.make} {vehicle.model}

                        </h3>



                        <p className="
font-bold
text-blue-700
">

                          ₹{Number(vehicle.price).toLocaleString()}

                        </p>


                      </div>




                      <div className="
grid
grid-cols-2
gap-3
text-sm
mb-4
">


                        <div>
                          <p className="text-gray-400">
                            Fuel
                          </p>
                          <p>
                            {vehicle.fuel_type}
                          </p>
                        </div>


                        <div>
                          <p className="text-gray-400">
                            Transmission
                          </p>
                          <p>
                            {vehicle.transmission}
                          </p>
                        </div>



                        <div>
                          <p className="text-gray-400">
                            Mileage
                          </p>

                          <p>
                            {vehicle.mileage.toLocaleString()} mi
                          </p>

                        </div>



                        <div>
                          <p className="text-gray-400">
                            Color
                          </p>

                          <p>
                            {vehicle.color}
                          </p>

                        </div>


                      </div>




                      <div className="
border-t
pt-4
">


                        {vehicle.quantity > 0 ? (

                          <p className="
text-green-600
text-sm
font-medium
mb-3
">

                            {vehicle.quantity} available

                          </p>

                        ) : (


                          <p className="
text-red-600
text-sm
font-medium
mb-3
">

                            Out of stock

                          </p>

                        )}





                        {!isAdmin && (

                          <button
                            onClick={() => handlePurchase(vehicle.id)}
                            disabled={vehicle.quantity <= 0}

                            className="
w-full
bg-black
text-white
py-2.5
rounded-md
text-sm
disabled:bg-gray-300
"
                          >

                            {
                              vehicle.quantity > 0
                                ?
                                "Purchase Vehicle"
                                :
                                "Unavailable"
                            }

                          </button>

                        )}




                        {isAdmin && (

                          <div className="space-y-3">


                            <div className="flex gap-3">


                              <button
                                onClick={() =>
                                  navigate(`/admin/vehicle/edit/${vehicle.id}`)
                                }

                                className="
flex-1
border
py-2
rounded-md
text-sm
"
                              >
                                Edit
                              </button>



                              <button

                                onClick={() =>
                                  handleDelete(vehicle.id)
                                }

                                className="
flex-1
border
border-red-300
text-red-600
py-2
rounded-md
text-sm
"
                              >

                                Delete

                              </button>


                            </div>





                            <div className="flex gap-2">


                              <input

                                type="number"

                                min="1"

                                placeholder="Qty"

                                value={restockQuantities[vehicle.id] || ''}

                                onChange={(e) =>
                                  handleRestockChange(
                                    vehicle.id,
                                    e.target.value
                                  )
                                }

                                className="
w-20
border
rounded-md
px-2
"
                              />




                              <button

                                onClick={() =>
                                  handleRestockSubmit(vehicle.id)
                                }

                                className="
bg-gray-900
text-white
px-3
rounded-md
text-sm
"
                              >

                                Restock

                              </button>


                            </div>



                          </div>

                        )}



                      </div>


                    </div>


                  </div>



                ))}


              </div>


            )}


          </div>


        </div>
      </main>
    </div>
  );
};

export default Dashboard;
