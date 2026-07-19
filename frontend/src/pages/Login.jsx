// import React, { useState } from 'react';
// import { useNavigate, Link } from 'react-router-dom';
// import { useAuth } from '../context/AuthContext';
// import InputField from '../components/InputField';
// import Button from '../components/Button';

// const Login = () => {
//   const [formData, setFormData] = useState({ email: '', password: '' });
//   const [error, setError] = useState('');
//   const [loading, setLoading] = useState(false);
//   const { login } = useAuth();
//   const navigate = useNavigate();

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setError('');
//     setLoading(true);

//     try {
//       await login(formData.email, formData.password);
//       navigate('/dashboard');
//     } catch (err) {
//       if (err.response && err.response.data && err.response.data.detail) {
//         setError(err.response.data.detail);
//       } else {
//         setError('Invalid credentials. Please try again.');
//       }
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-[radial-gradient(circle_at_top_left,_rgba(59,130,246,0.18),_transparent_40%),linear-gradient(135deg,_#f8fbff_0%,_#eef4ff_100%)] px-4 py-12 sm:px-6 lg:px-8">
//       <div className="w-full max-w-6xl grid overflow-hidden rounded-[2rem] border border-slate-200/70 bg-white/80 shadow-[0_30px_90px_-30px_rgba(15,23,42,0.35)] backdrop-blur lg:grid-cols-[1.05fr_0.95fr]">
//         {/* <div className="auth-panel flex flex-col justify-between p-8 text-white lg:p-10">
//           <div>
//             <div className="inline-flex items-center rounded-full bg-white/15 px-3 py-1 text-sm font-medium backdrop-blur">
//               AutoMax control center
//             </div>
//             <h1 className="mt-6 text-3xl font-semibold leading-tight sm:text-4xl">
//               Welcome back to your dealership command center.
//             </h1>
//             <p className="mt-4 max-w-lg text-sm text-blue-100 sm:text-base">
//               Keep inventory fresh, restock fast, and deliver a smoother customer experience from one elegant dashboard.
//             </p>
//           </div>
//           <div className="mt-8 space-y-3 text-sm text-blue-50">
//             <div className="rounded-2xl border border-white/15 bg-white/10 p-3">• Live inventory updates across all vehicle listings</div>
//             <div className="rounded-2xl border border-white/15 bg-white/10 p-3">• Fast filters for quick browsing and ordering</div>
//             <div className="rounded-2xl border border-white/15 bg-white/10 p-3">• Admin tools for editing stock, pricing, and availability</div>
//           </div>
//         </div> */}

//         <div className="p-8 sm:p-10">
//           <div className="mb-8 text-center lg:text-left">
//             <h2 className="text-3xl font-semibold text-slate-900">Sign in</h2>
//           </div>

//           {error && (
//             <div className="mb-5 rounded-2xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
//               {error}
//             </div>
//           )}

//           <form className="space-y-5" onSubmit={handleSubmit}>
//             <InputField
//               label="Email Address"
//               id="email"
//               type="email"
//               value={formData.email}
//               onChange={handleChange}
//               placeholder="admin@dealership.com"
//               autoComplete="email"
//             />
//             <InputField
//               label="Password"
//               id="password"
//               type="password"
//               value={formData.password}
//               onChange={handleChange}
//               placeholder="••••••••"
//               autoComplete="current-password"
//             />

//             <Button type="submit" disabled={loading}>
//               {loading ? 'Signing in...' : 'Sign In'}
//             </Button>
//           </form>

//           <div className="mt-6 text-center text-sm text-slate-600">
//             Don’t have an account?{' '}
//             <Link to="/register" className="font-semibold text-blue-600 hover:text-blue-500">
//               Create one here
//             </Link>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default Login;


import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import InputField from "../components/InputField";
import Button from "../components/Button";

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(formData.email, formData.password);
      navigate("/dashboard");
    } catch (err) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Incorrect email or password.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md rounded-xl bg-white border border-gray-200 shadow-md p-8">

        {/* Logo */}
        <div className="text-center mb-8">


          <h1 className="mt-4 text-4xl font-bold text-gray-800">
            Sign In
          </h1>


        </div>

        {/* Heading */}
        <div className="mb-6">
          <p className="text-sm text-gray-500 mt-1">
            Sign in to continue to your dashboard.
          </p>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-5 rounded-md border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">

          <InputField
            label="Email Address"
            id="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
            autoComplete="email"
          />

          <div>
            <InputField
              label="Password"
              id="password"
              type={showPassword ? "text" : "password"}
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              autoComplete="current-password"
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="mt-2 text-sm text-blue-600 hover:text-blue-700"
            >
              {showPassword ? "Hide Password" : "Show Password"}
            </button>
          </div>

          <Button type="submit" disabled={loading}>
            {loading ? "Signing In..." : "Sign In"}
          </Button>
        </form>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-600">
          Don't have an account?{" "}
          <Link
            to="/register"
            className="font-semibold text-blue-600 hover:underline"
          >
            Create Account
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;