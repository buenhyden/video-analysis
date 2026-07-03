import { AlertCircle, CheckCircle2 } from 'lucide-react';
import { useStore } from '../../store/useStore';

const Toast = () => {
  const { toast } = useStore();
  if (!toast.show) return null;

  const bgColors = {
    success: 'bg-emerald-500/90 text-white',
    error: 'bg-rose-500/90 text-white',
    info: 'bg-slate-700/90 text-white',
  };

  return (
    <div
      className={`fixed bottom-8 right-8 z-50 px-6 py-3 rounded-xl shadow-2xl backdrop-blur-md flex items-center gap-3 animate-in slide-in-from-bottom-5 fade-in duration-300 ${bgColors[toast.type]}`}
    >
      {toast.type === 'success' && <CheckCircle2 size={18} />}
      {toast.type === 'error' && <AlertCircle size={18} />}
      <span className="font-medium text-sm">{toast.message}</span>
    </div>
  );
};

export default Toast;
