import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, X, Minimize2 } from 'lucide-react';
import { ChatMessages } from './ChatMessages';
import { ChatInput } from './ChatInput';
import { useChat } from '../../hooks/useChat';

export const FloatingChatPanel = ({ onTasksUpdate }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const { messages, isLoading, sendMessage, messagesEndRef } = useChat(onTasksUpdate);

  const handleSendMessage = (message) => {
    sendMessage(message);
    if (!isOpen) {
      setUnreadCount(prev => prev + 1);
    }
  };

  const handleToggle = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setUnreadCount(0);
    }
  };

  return (
    <>
      {/* Floating Button - Mobile visible, Hidden on larger screens in open state */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0, rotate: -180, opacity: 0 }}
            animate={{ scale: 1, rotate: 0, opacity: 1 }}
            exit={{ scale: 0, rotate: 180, opacity: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleToggle}
            className="fixed bottom-6 right-6 z-40 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-full p-4 shadow-lg shadow-purple-500/50 flex items-center justify-center gap-2 group"
          >
            <MessageCircle className="w-6 h-6" />

            {/* Unread Badge */}
            <AnimatePresence>
              {unreadCount > 0 && (
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  exit={{ scale: 0 }}
                  className="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center"
                >
                  {unreadCount > 9 ? '9+' : unreadCount}
                </motion.span>
              )}
            </AnimatePresence>
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed bottom-6 transform -translate-x-1/2 w-full max-w-sm h-96 md:left-auto md:right-6 md:transform-none md:w-96 md:h-[32rem] flex flex-col rounded-2xl overflow-hidden glass-card shadow-glow-lg z-50"
          >
            {/* Header */}
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 border-b border-white/10 px-6 py-4 flex items-center justify-between"
            >
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                    <MessageCircle className="w-5 h-5 text-white" />
                  </div>
                  <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border border-white/20" />
                </div>

                <div>
                  <h3 className="text-sm font-semibold text-white">AI Assistant</h3>
                  <p className="text-xs text-slate-300">Always here to help</p>
                </div>
              </div>

              <div className="flex gap-2">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setIsOpen(false)}
                  className="btn-ghost p-2"
                  aria-label="Minimize"
                >
                  <Minimize2 className="w-4 h-4" />
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setIsOpen(false)}
                  className="btn-ghost p-2"
                  aria-label="Close"
                >
                  <X className="w-4 h-4" />
                </motion.button>
              </div>
            </motion.div>

            {/* Messages */}
            <ChatMessages messages={messages} messagesEndRef={messagesEndRef} isLoading={isLoading} />

            {/* Input */}
            <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
