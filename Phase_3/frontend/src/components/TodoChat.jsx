import React, { useState, useEffect, useRef } from 'react';

/**
 * TodoChat Component - Conversational todo management with OpenAI Agents SDK backend
 * Uses clean React UI that calls the Phase 3 backend
 */
const TodoChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';

  // Add welcome message on component mount
  useEffect(() => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'Hello! I\'m your todo assistant. You can ask me to add, update, delete, or list your tasks. Try saying something like "Add buy milk to my list".',
        timestamp: new Date().toISOString()
      }
    ]);
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    // Add user message to the conversation
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const res = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue })
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to get response: ${res.status} - ${errorText}`);
      }

      const data = await res.json();

      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.message || 'I processed your request.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error processing message:', error);

      const errorMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="todo-chat-container">
      <div className="chat-header">
        <h2>Conversational Todo Assistant</h2>
      </div>

      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-content">
              {message.content}
            </div>
            <div className="message-timestamp">
              {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your todo command (e.g., 'Add buy milk to my list')..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  );
};

export default TodoChat;
