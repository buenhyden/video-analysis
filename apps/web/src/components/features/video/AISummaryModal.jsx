import { Sparkles } from 'lucide-react';
import Modal from '../../ui/Modal';

const AISummaryModal = ({ video, isOpen, onClose }) => {
  if (!isOpen || !video) return null;
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="AI Analysis Report"
      maxWidth="max-w-2xl"
    >
      <div className="p-6 max-h-[70vh] overflow-y-auto">
        <div className="flex items-center gap-3 mb-6 p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
          <div className="p-2 bg-indigo-500 rounded-lg">
            <Sparkles size={20} className="text-white" />
          </div>
          <div>
            <h5 className="font-bold text-indigo-300 text-sm">
              AI Video Analysis
            </h5>
            <p className="text-xs text-indigo-400/70">
              Vision Model(MiniCPM-V)과 LLM(Qwen3)이 영상을 분석한 결과입니다.
            </p>
          </div>
        </div>

        <div className="prose prose-invert prose-sm max-w-none">
          <div className="whitespace-pre-wrap leading-relaxed text-slate-300">
            {video.ai_summary || '요약 정보가 없습니다.'}
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default AISummaryModal;
