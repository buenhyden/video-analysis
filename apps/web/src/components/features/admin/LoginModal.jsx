import React, { useState } from 'react';
import { useStore } from '../../../store/useStore';
import Modal from '../../ui/Modal';
import Input from '../../ui/Input';
import Button from '../../ui/Button';

const LoginModal = ({ isOpen, onClose }) =>
{
    const login = useStore((state) => state.login);
    const error = useStore((state) => state.error);
    const [creds, setCreds] = useState({ username: '', password: '' });

    const handleSubmit = async (e) =>
    {
        e.preventDefault();
        const success = await login(creds.username, creds.password);
        if (success)
        {
            setCreds({ username: '', password: '' });
            onClose();
        }
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} title="관리자 로그인">
            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-lg p-3 mb-4">
                    <p className="text-xs text-indigo-300 text-center">
                        데모 계정: <strong>admin</strong> / <strong>1234</strong>
                    </p>
                </div>
                <Input
                    label="Username"
                    value={creds.username}
                    onChange={(e) => setCreds({ ...creds, username: e.target.value })}
                    placeholder="아이디 입력"
                />
                <Input
                    label="Password"
                    type="password"
                    value={creds.password}
                    onChange={(e) => setCreds({ ...creds, password: e.target.value })}
                    placeholder="비밀번호 입력"
                />
                {error && <p className="text-red-400 text-sm text-center">{error}</p>}
                <Button type="submit" className="w-full mt-2">로그인</Button>
            </form>
        </Modal>
    );
};

export default LoginModal;