import React from 'react';
import { Copy, Check } from 'lucide-react';

const ChatMessage = ({ message, isUser }) => {
    const [copied, setCopied] = React.useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(message.content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className={`message-wrapper ${isUser ? 'user-message-wrapper' : 'assistant-message-wrapper'}`}>
            <div className={`message ${isUser ? 'user-message' : 'assistant-message'}`}>
                <div className="message-header">
                    <span className="message-role">{isUser ? 'You' : 'AI Assistant'}</span>
                    {!isUser && (
                        <button
                            className="copy-button"
                            onClick={handleCopy}
                            title="Copy message"
                        >
                            {copied ? <Check size={16} /> : <Copy size={16} />}
                        </button>
                    )}
                </div>
                <div className="message-content">
                    {message.content}
                </div>
                {message.language && !isUser && (
                    <div className="message-meta">
                        <span className="language-badge">{message.language}</span>
                        <span className="timestamp">
                            {new Date(message.timestamp).toLocaleTimeString('en-US', {
                                hour: '2-digit',
                                minute: '2-digit'
                            })}
                        </span>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ChatMessage;
