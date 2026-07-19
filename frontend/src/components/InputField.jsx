import React from 'react';

const InputField = ({ label, id, type = 'text', value, onChange, placeholder, required = true, autoComplete }) => {
  return (
    <div className="mb-4">
      <label htmlFor={id} className="block text-sm font-medium text-slate-700 mb-2">
        {label}
      </label>
      <input
        type={type}
        id={id}
        name={id}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        autoComplete={autoComplete}
        className="w-full px-3.5 py-2.5 border border-slate-200 rounded-xl shadow-sm bg-slate-50/70 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
      />
    </div>
  );
};

export default InputField;
