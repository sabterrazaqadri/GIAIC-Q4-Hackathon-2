import React from 'react';
import { motion } from 'framer-motion';
import { Heart } from 'lucide-react';

const Footer = () => {
  return (
    <motion.footer
      initial={{ y: 100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="glass-card backdrop-blur-lg border-t border-white/20 mt-16"
    >
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="text-slate-400 text-sm">
            © 2026 AI Powered Todo Task Manager. All rights reserved.
          </div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center space-x-2 mt-4 md:mt-0"
          >
            <span className="text-slate-300 text-sm">
              Made with
            </span>
            <Heart className="w-4 h-4 text-red-500 fill-current" />
            <span className="text-slate-300 text-sm">
              by sabter raza qadri
            </span>
          </motion.div>
        </div>
      </div>
    </motion.footer>
  );
};

export default Footer;