import {
  AlertCircle,
  FileText,
  Loader2,
  Play,
  RefreshCw,
  Sparkles,
  Trash2,
} from 'lucide-react';

const VideoCard = ({
  video,
  isAdmin,
  onDelete,
  onPlay,
  onShowSummary,
  onRetry,
}) => {
  const statusConfig = {
    pending: {
      color: 'bg-slate-700 text-slate-300',
      icon: null,
      text: '대기중',
    },
    queued: {
      color: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
      icon: <Loader2 size={12} className="animate-spin" />,
      text: '분석 대기',
    },
    processing: {
      color: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
      icon: <Loader2 size={12} className="animate-spin" />,
      text: 'AI 분석중',
    },
    completed: {
      color: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30',
      icon: <Sparkles size={12} />,
      text: '분석 완료',
    },
    failed: {
      color: 'bg-red-500/20 text-red-400 border-red-500/30',
      icon: <AlertCircle size={12} />,
      text: '분석 실패',
    },
  };

  const status = statusConfig[video.analysis_status] || statusConfig.pending;

  return (
    <div className="group relative bg-slate-900 rounded-2xl overflow-hidden border border-slate-800 hover:border-indigo-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-indigo-500/10 hover:-translate-y-1 flex flex-col h-full">
      <div className="aspect-video relative overflow-hidden bg-slate-950">
        <img
          src={video.thumbnail}
          alt={video.title}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105 opacity-80 group-hover:opacity-100"
          onError={(e) => {
            e.target.src =
              'https://placehold.co/640x360/1e293b/cbd5e1.png?text=No+Preview';
          }}
        />
        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center backdrop-blur-[2px]">
          <button
            onClick={() => onPlay(video)}
            className="transform scale-90 group-hover:scale-100 transition-transform duration-300 w-16 h-16 rounded-full bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center text-white hover:bg-white hover:text-black hover:border-white shadow-xl"
          >
            <Play fill="currentColor" size={24} className="ml-1" />
          </button>
        </div>
        <span className="absolute top-3 left-3 bg-black/60 backdrop-blur-md text-[10px] font-bold uppercase tracking-wider text-white px-2.5 py-1 rounded-md border border-white/10">
          {video.category}
        </span>
      </div>

      <div className="p-5 flex flex-col flex-1">
        <div className="mb-auto">
          <div className="flex justify-between items-start gap-4 mb-3">
            <h3 className="font-bold text-lg text-slate-100 line-clamp-1 group-hover:text-indigo-400 transition-colors">
              {video.title}
            </h3>
          </div>
          <p className="text-slate-400 text-sm line-clamp-2 leading-relaxed mb-4">
            {video.description}
          </p>
        </div>

        <div className="pt-4 mt-2 border-t border-slate-800 flex items-center justify-between">
          <div
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${status.color.includes('border') ? status.color : 'border-transparent ' + status.color}`}
          >
            {status.icon}
            <span>{status.text}</span>
          </div>

          <div className="flex items-center gap-2">
            {isAdmin && video.analysis_status === 'failed' && (
              <button
                onClick={() => onRetry(video.id)}
                className="p-2 text-slate-400 hover:text-yellow-400 hover:bg-yellow-500/10 rounded-lg transition-colors"
                title="분석 재시도"
              >
                <RefreshCw size={18} />
              </button>
            )}

            {video.analysis_status === 'completed' && (
              <button
                onClick={() => onShowSummary(video)}
                className="p-2 text-slate-400 hover:text-indigo-400 hover:bg-indigo-500/10 rounded-lg transition-colors"
                title="AI 요약 보기"
              >
                <FileText size={18} />
              </button>
            )}
            {isAdmin && (
              <button
                onClick={() => onDelete(video.id)}
                className="p-2 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                title="삭제"
              >
                <Trash2 size={18} />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoCard;
