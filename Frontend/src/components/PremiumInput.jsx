import React, { useState } from 'react';
import { ArrowUp } from 'lucide-react';

const PremiumInput = ({ onSend, disabled, placeholder = "Ask anything..." }) => {
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (message.trim() && !disabled) {
            onSend(message);
            setMessage('');
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <div className="premium-input-container">
            <form onSubmit={handleSubmit}>
                <div className="premium-input-wrapper">
                    <textarea
                        className="premium-input"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder={placeholder}
                        disabled={disabled}
                        rows={1}
                        style={{
                            height: 'auto',
                            minHeight: '24px',
                            maxHeight: '200px',
                        }}
                        onInput={(e) => {
                            e.target.style.height = 'auto';
                            e.target.style.height = e.target.scrollHeight + 'px';
                        }}
                    />

                    <button
                        type="submit"
                        className="send-button-circle"
                        disabled={disabled || !message.trim()}
                        title="Send message"
                    >
                        <ArrowUp size={18} />
                    </button>
                </div>
            </form>
        </div>
    );
};

export default PremiumInput;
