import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send } from 'lucide-react';

export const ChatInput = ({ onSend, isLoading, placeholder = 'Ask me anything...' }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      onSubmit={handleSubmit}
      className="border-t border-white/10 p-4 bg-white/5 backdrop-blur-lg flex gap-2"
    >
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={placeholder}
        disabled={isLoading}
        className="input-field flex-1 text-sm"
      />

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        type="submit"
        disabled={isLoading || !input.trim()}
        className="btn-primary px-4 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Send className="w-4 h-4" />
      </motion.button>
    </motion.form>
  );
};
