import { motion } from 'framer-motion';
import { MessageCircle } from 'lucide-react';

export const ChatMessages = ({ messages, messagesEndRef, isLoading }) => {
  return (
    <div className="flex-1 overflow-y-auto space-y-4 p-4 no-scrollbar">
      {messages.map((message, index) => (
        <motion.div
          key={message.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-xs lg:max-w-md xl:max-w-lg ${
              message.role === 'user'
                ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-2xl rounded-tr-none'
                : message.isError
                ? 'bg-red-500/20 text-red-300 border border-red-500/30 rounded-2xl rounded-tl-none'
                : 'bg-white/10 text-slate-100 border border-white/20 rounded-2xl rounded-tl-none'
            } px-4 py-2.5 break-words`}
          >
            <p className="text-sm leading-relaxed">{message.content}</p>
            {message.timestamp && (
              <p className="text-xs opacity-50 mt-1">
                {new Date(message.timestamp).toLocaleTimeString('en-US', {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            )}
          </div>
        </motion.div>
      ))}

      {isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-start"
        >
          <div className="bg-white/10 text-slate-300 border border-white/20 rounded-2xl rounded-tl-none px-4 py-3 flex items-center gap-2">
            <MessageCircle className="w-4 h-4 animate-spin" />
            <span className="text-sm">AI is thinking...</span>
          </div>
        </motion.div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};
