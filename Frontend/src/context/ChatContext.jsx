import React, { createContext, useContext, useState, useEffect } from 'react';

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
    const [currentChatId, setCurrentChatId] = useState(null);
    const [chats, setChats] = useState([]);
    const [messages, setMessages] = useState([]);

    // Load chats from localStorage on mount
    useEffect(() => {
        const savedChats = localStorage.getItem('chatHistory');
        if (savedChats) {
            setChats(JSON.parse(savedChats));
        }
    }, []);

    // Save chats to localStorage whenever they change
    useEffect(() => {
        if (chats.length > 0) {
            localStorage.setItem('chatHistory', JSON.stringify(chats));
        }
    }, [chats]);

    const createNewChat = () => {
        const newChat = {
            id: Date.now(),
            title: 'New Chat',
            messages: [],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        setChats(prev => [newChat, ...prev]);
        setCurrentChatId(newChat.id);
        setMessages([]);
        return newChat.id;
    };

    const loadChat = (chatId) => {
        const chat = chats.find(c => c.id === chatId);
        if (chat) {
            setCurrentChatId(chatId);
            setMessages(chat.messages);
        }
    };

    const addMessage = (message) => {
        const newMessage = {
            ...message,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, newMessage]);

        // Update chat in the list
        setChats(prev => prev.map(chat => {
            if (chat.id === currentChatId) {
                const updatedMessages = [...chat.messages, newMessage];
                // Auto-generate title from first user message
                const title = chat.title === 'New Chat' && message.role === 'user'
                    ? message.content.substring(0, 40) + (message.content.length > 40 ? '...' : '')
                    : chat.title;

                return {
                    ...chat,
                    messages: updatedMessages,
                    title,
                    updatedAt: new Date().toISOString()
                };
            }
            return chat;
        }));
    };

    const renameChat = (chatId, newTitle) => {
        setChats(prev => prev.map(chat =>
            chat.id === chatId ? { ...chat, title: newTitle } : chat
        ));
    };

    const deleteChat = (chatId) => {
        setChats(prev => prev.filter(chat => chat.id !== chatId));
        if (currentChatId === chatId) {
            setCurrentChatId(null);
            setMessages([]);
        }
    };

    return (
        <ChatContext.Provider value={{
            currentChatId,
            chats,
            messages,
            createNewChat,
            loadChat,
            addMessage,
            renameChat,
            deleteChat
        }}>
            {children}
        </ChatContext.Provider>
    );
};

export const useChat = () => {
    const context = useContext(ChatContext);
    if (!context) {
        throw new Error('useChat must be used within ChatProvider');
    }
    return context;
};
