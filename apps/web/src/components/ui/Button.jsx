import React from 'react';

const Button = ({ children, variant = 'primary', className = '', ...props }) =>
{
    const baseStyle = "px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50";
    const variants = {
        primary: "bg-indigo-600 text-white hover:bg-indigo-700 shadow-lg shadow-indigo-500/30",
        secondary: "bg-slate-800 text-slate-200 hover:bg-slate-700 border border-slate-700",
        danger: "bg-red-500/10 text-red-500 hover:bg-red-500/20",
        ghost: "text-slate-400 hover:text-white hover:bg-white/5"
    };
    return (
        <button className={`${ baseStyle } ${ variants[variant] } ${ className }`} {...props}>
            {children}
        </button>
    );
};

export default Button;
