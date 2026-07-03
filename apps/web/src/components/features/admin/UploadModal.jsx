import { useState } from 'react';
import { useStore } from '../../../store/useStore';
import Button from '../../ui/Button';
import Input from '../../ui/Input';
import Modal from '../../ui/Modal';

const UploadModal = ({ isOpen, onClose }) =>
{
    const addVideo = useStore((state) => state.addVideo);
    const [form, setForm] = useState({ title: '', category: '', description: '', url: '', thumbnail: '' });

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        const videoData = {
            ...form,
            thumbnail: form.thumbnail || `https://source.unsplash.com/random/800x600?sig=${ Date.now() }`
        };
        await addVideo(videoData);
        setForm({ title: '', category: '', description: '', url: '', thumbnail: '' });
        onClose();
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} title="새 프로젝트 추가">
            <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                    label="프로젝트 제목"
                    value={form.title}
                    onChange={e => setForm({ ...form, title: e.target.value })}
                    required
                />
                <div className="grid grid-cols-2 gap-4">
                    <Input
                        label="카테고리"
                        value={form.category}
                        onChange={e => setForm({ ...form, category: e.target.value })}
                        placeholder="예: Commercial"
                        required
                    />
                    <Input
                        label="영상 URL"
                        value={form.url}
                        onChange={e => setForm({ ...form, url: e.target.value })}
                        placeholder="Youtube/Vimeo Link"
                    />
                </div>
                <Input
                    label="썸네일 이미지 URL"
                    value={form.thumbnail}
                    onChange={e => setForm({ ...form, thumbnail: e.target.value })}
                    placeholder="https://..."
                />
                <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">설명</label>
                    <textarea
                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 min-h-[80px]"
                        value={form.description}
                        onChange={e => setForm({ ...form, description: e.target.value })}
                    />
                </div>
                <Button type="submit" className="w-full">등록하기</Button>
            </form>
        </Modal>
    );
}

export default UploadModal;