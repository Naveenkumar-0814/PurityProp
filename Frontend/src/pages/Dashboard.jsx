import React from 'react';
import { useNavigate } from 'react-router-dom';
import PremiumInput from '../components/PremiumInput';
import { Home, FileText, Calculator, TrendingUp } from 'lucide-react';

const Dashboard = () => {
    const navigate = useNavigate();

    const suggestedPrompts = [
        {
            icon: '📋',
            title: 'Property Registration',
            description: 'Learn about the registration process and required documents',
            prompt: 'What documents do I need for property registration in Tamil Nadu?'
        },
        {
            icon: '💰',
            title: 'Stamp Duty Calculator',
            description: 'Calculate stamp duty and registration fees',
            prompt: 'How much is stamp duty for a property worth 50 lakhs?'
        },
        {
            icon: '📏',
            title: 'Land Measurements',
            description: 'Convert between cents, grounds, and square feet',
            prompt: 'How many square feet is 5 cents?'
        },
        {
            icon: '🏦',
            title: 'Bank Loans',
            description: 'Get information about home loans and eligibility',
            prompt: 'What are the eligibility criteria for a home loan?'
        }
    ];

    const handleSend = (message) => {
        // Navigate to chat with the message
        navigate('/chat', { state: { initialMessage: message } });
    };

    const handlePromptClick = (prompt) => {
        navigate('/chat', { state: { initialMessage: prompt } });
    };

    return (
        <div className="content-container fade-in">
            <div className="dashboard-welcome">
                <h1 className="welcome-headline">
                    What property are you working on?
                </h1>
                <p className="welcome-subtitle">
                    Your AI-powered assistant for Tamil Nadu real estate
                </p>

                <PremiumInput
                    onSend={handleSend}
                    placeholder="Ask about registration, documents, loans, or measurements..."
                />

                <div className="suggested-prompts">
                    {suggestedPrompts.map((prompt, index) => (
                        <div
                            key={index}
                            className="prompt-card"
                            onClick={() => handlePromptClick(prompt.prompt)}
                        >
                            <div className="prompt-icon">{prompt.icon}</div>
                            <div className="prompt-title">{prompt.title}</div>
                            <div className="prompt-description">{prompt.description}</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
