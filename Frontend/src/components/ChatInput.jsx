import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

import React from 'react';
import { Send, Loader2 } from 'lucide-react';

const ChatInput = ({ onSend, disabled, loading }) => {
    const [input, setInput] = React.useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !disabled) {
            onSend(input.trim());
            setInput('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <form className="chat-input-container" onSubmit={handleSubmit}>
            <div className="input-wrapper">
                <textarea
                    className="chat-input"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask about real estate in Tamil Nadu... (Tamil/Tanglish/English)"
                    disabled={disabled}
                    rows={1}
                />
                <button
                    type="submit"
                    className="send-button"
                    disabled={disabled || !input.trim()}
                >
                    {loading ? (
                        <Loader2 size={20} className="spinner" />
                    ) : (
                        <Send size={20} />
                    )}
                </button>
            </div>
        </form>
    );
};

export default ChatInput;

