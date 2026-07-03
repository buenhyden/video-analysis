
const Input = ({ label, ...props }) => (
    <div className="flex flex-col gap-1.5">
        {label && <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{label}</label>}
        <input
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
            {...props}
        />
    </div>
);

export default Input;
