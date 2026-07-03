import { X } from 'lucide-react';

const Modal = ({ isOpen, onClose, title, children, maxWidth = 'max-w-md' }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div
        className={`bg-slate-900 border border-slate-800 w-full ${maxWidth} rounded-2xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200`}
      >
        <div className="flex justify-between items-center p-4 border-b border-slate-800 bg-slate-900/50">
          <h3 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            {title}
          </h3>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>
        <div className="p-0">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
