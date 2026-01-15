import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Menu, X } from 'lucide-react';
import { useState } from 'react';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 glass-card backdrop-blur-lg border-b border-white/20"
    >
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo and Brand */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center space-x-3"
          >
            <div className="glass-card p-2 rounded-lg">
              <Brain className="w-6 h-6 text-purple-400" />
            </div>
            <h1 className="text-xl font-bold gradient-text bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              AI Powered Todo Task Manager
            </h1>
          </motion.div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#dashboard" className="text-slate-300 hover:text-white transition-colors">
              Dashboard
            </a>
            <a href="#tasks" className="text-slate-300 hover:text-white transition-colors">
              Tasks
            </a>
            <a href="#chat" className="text-slate-300 hover:text-white transition-colors">
              AI Chat
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden glass-card p-2 rounded-lg"
          >
            {isMenuOpen ? (
              <X className="w-5 h-5 text-white" />
            ) : (
              <Menu className="w-5 h-5 text-white" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden mt-4 pb-4"
          >
            <div className="flex flex-col space-y-3 pt-4">
              <a
                href="#dashboard"
                className="text-slate-300 hover:text-white transition-colors py-2"
                onClick={() => setIsMenuOpen(false)}
              >
                Dashboard
              </a>
              <a
                href="#tasks"
                className="text-slate-300 hover:text-white transition-colors py-2"
                onClick={() => setIsMenuOpen(false)}
              >
                Tasks
              </a>
              <a
                href="#chat"
                className="text-slate-300 hover:text-white transition-colors py-2"
                onClick={() => setIsMenuOpen(false)}
              >
                AI Chat
              </a>
            </div>
          </motion.div>
        )}
      </div>
    </motion.nav>
  );
};

export default Navbar;