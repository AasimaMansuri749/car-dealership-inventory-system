import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';
import InputField from '../components/InputField';
import Button from '../components/Button';

const Register = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [fieldErrors, setFieldErrors] = useState({});
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Username validation rules
  const validateUsername = (username) => {
    const errors = [];
    if (username.length < 3) {
      errors.push('Username must be at least 3 characters long');
    }
    if (!/^[a-zA-Z0-9_ ]+$/.test(username)) {
      errors.push('Username can only contain letters, numbers, underscores, and spaces');
    }
    return errors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    // Real-time validation for username
    if (name === 'username' && value) {
      const errors = validateUsername(value);
      setFieldErrors({ ...fieldErrors, username: errors });
    } else if (name === 'username') {
      setFieldErrors({ ...fieldErrors, username: [] });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validate username before submission
    const usernameErrors = validateUsername(formData.username);
    if (usernameErrors.length > 0) {
      setFieldErrors({ ...fieldErrors, username: usernameErrors });
      setError('Please fix the validation errors below');
      return;
    }

    setLoading(true);

    try {
      await api.post('/api/auth/register', formData);
      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        if (Array.isArray(err.response.data.detail)) {
          setError(err.response.data.detail[0].msg);
        } else {
          setError(err.response.data.detail);
        }
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center px-4 py-8">

      <div className="w-full max-w-md bg-white border border-gray-200 rounded-xl shadow-md p-8">

        {/* Logo */}
        <div className="text-center mb-7">


          <h1 className="mt-3 text-4xl font-bold text-gray-800">
            Create Account
          </h1>


        </div>


        {/* Title */}
        <div className="mb-6">


          <p className="mt-1 text-sm text-gray-500">
            Register to manage vehicle inventory.
          </p>
        </div>


        {/* Error Message */}
        {error && (
          <div className="mb-5 rounded-md border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error.replace("Value error, ", "")}
          </div>
        )}


        {/* Success Message */}
        {success && (
          <div className="mb-5 rounded-md border border-green-300 bg-green-50 px-4 py-3 text-sm text-green-700">
            {success}
          </div>
        )}


        <form className="space-y-5" onSubmit={handleSubmit}>

          {/* Username */}
          <div>
            <InputField
              label="Username"
              id="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter username"
              autoComplete="username"
            />

            {fieldErrors.username &&
              fieldErrors.username.length > 0 && (
                <div className="mt-2 text-sm text-red-600">
                  {fieldErrors.username.map((err, idx) => (
                    <div key={idx}>
                      • {err}
                    </div>
                  ))}
                </div>
              )}
          </div>


          {/* Email */}
          <InputField
            label="Email Address"
            id="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter email"
            autoComplete="email"
          />


          {/* Password */}
          <InputField
            label="Password"
            id="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Create password"
            autoComplete="new-password"
          />


          <Button type="submit" disabled={loading}>
            {loading ? "Creating account..." : "Register"}
          </Button>

        </form>


        {/* Login Link */}
        <div className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{" "}
          <Link
            to="/login"
            className="font-semibold text-blue-600 hover:text-blue-700"
          >
            Sign In
          </Link>
        </div>


      </div>

    </div>
  );
  // return (
  //   <div className="min-h-screen flex items-center justify-center bg-[radial-gradient(circle_at_top_right,_rgba(59,130,246,0.18),_transparent_40%),linear-gradient(135deg,_#f8fbff_0%,_#eef4ff_100%)] px-4 py-12 sm:px-6 lg:px-8">
  //     <div className="w-full max-w-3xl grid overflow-hidden rounded-[2rem] border border-slate-200/70 bg-white/80 shadow-[0_30px_90px_-30px_rgba(15,23,42,0.35)] backdrop-blur lg:grid-cols-[0.95fr_1.05fr]">
  //       {/* <div className="auth-panel flex flex-col justify-between p-8 text-white lg:p-10">
  //         <div>
  //           <div className="inline-flex items-center rounded-full bg-white/15 px-3 py-1 text-sm font-medium backdrop-blur">
  //             Start your workflow
  //           </div>
  //           <h1 className="mt-6 text-3xl font-semibold leading-tight sm:text-4xl">
  //             Build a polished inventory experience for your dealership.
  //           </h1>
  //           <p className="mt-4 max-w-lg text-sm text-blue-100 sm:text-base">
  //             Create an account to manage listings, track stock, and keep every vehicle ready for your customers.
  //           </p>
  //         </div>
  //         <div className="mt-8 rounded-2xl border border-white/15 bg-white/10 p-4 text-sm text-blue-50">
  //           Friendly, clear tools make daily operations simpler for admins and teams.
  //         </div>
  //       </div> */}

  //       <div className="p-8 sm:p-10">
  //         <div className="mb-8 text-center lg:text-left">
  //           <h2 className="text-3xl font-semibold text-slate-900">Create account</h2>

  //         </div>

  //         {error && (
  //           <div className="mb-5 rounded-2xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
  //             {error}
  //           </div>
  //         )}

  //         {success && (
  //           <div className="mb-5 rounded-2xl border border-green-200 bg-green-50 p-3 text-sm text-green-700">
  //             {success}
  //           </div>
  //         )}

  //         <form className="space-y-5" onSubmit={handleSubmit}>
  //           <div>
  //             <InputField
  //               label="Username"
  //               id="username"
  //               value={formData.username}
  //               onChange={handleChange}
  //               placeholder="johndoe"
  //               autoComplete="username"
  //             />
  //             {fieldErrors.username && fieldErrors.username.length > 0 && (
  //               <div className="mt-2 text-sm text-red-600">
  //                 {fieldErrors.username.map((err, idx) => (
  //                   <div key={idx}>• {err}</div>
  //                 ))}
  //               </div>
  //             )}
  //           </div>
  //           <InputField
  //             label="Email Address"
  //             id="email"
  //             type="email"
  //             value={formData.email}
  //             onChange={handleChange}
  //             placeholder="john@example.com"
  //             autoComplete="email"
  //           />
  //           <InputField
  //             label="Password"
  //             id="password"
  //             type="password"
  //             value={formData.password}
  //             onChange={handleChange}
  //             placeholder="••••••••"
  //             autoComplete="new-password"
  //           />

  //           <Button type="submit" disabled={loading}>
  //             {loading ? 'Creating account...' : 'Register'}
  //           </Button>
  //         </form>

  //         <div className="mt-6 text-center text-sm text-slate-600">
  //           Already have an account?{' '}
  //           <Link to="/login" className="font-semibold text-blue-600 hover:text-blue-500">
  //             Sign in here
  //           </Link>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
  // );
};

export default Register;
