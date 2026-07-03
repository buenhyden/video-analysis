import Modal from '../../ui/Modal';

const VideoPlayerModal = ({ video, isOpen, onClose }) => {
  if (!isOpen || !video) return null;

  const getEmbedUrl = (url) => {
    const regExp =
      /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    const videoId = match && match[2].length === 11 ? match[2] : null;
    return videoId
      ? `https://www.youtube.com/embed/${videoId}?autoplay=1`
      : null;
  };

  const embedUrl = getEmbedUrl(video.url);

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={video.title}
      maxWidth="max-w-4xl"
    >
      <div className="aspect-video bg-black w-full">
        {embedUrl ? (
          <iframe
            src={embedUrl}
            className="w-full h-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        ) : (
          <div className="flex items-center justify-center h-full text-slate-500">
            지원되지 않는 동영상 URL입니다.
          </div>
        )}
      </div>
      <div className="p-6 bg-slate-900">
        <h4 className="font-bold text-white mb-2">{video.title}</h4>
        <p className="text-slate-400 text-sm">{video.description}</p>
      </div>
    </Modal>
  );
};

export default VideoPlayerModal;
