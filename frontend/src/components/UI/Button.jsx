import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../utils/cn';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  className,
  ...props
}) => {
  const baseClasses = "relative inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-primary/30";

  const variants = {
    primary: "bg-gradient-to-r from-primary to-secondary text-white hover:shadow-lg transform hover:scale-105",
    secondary: "bg-white text-primary border-2 border-primary hover:bg-primary hover:text-white",
    danger: "bg-gradient-to-r from-red-500 to-red-600 text-white hover:shadow-lg",
    ghost: "bg-transparent text-primary hover:bg-primary/10"
  };

  const sizes = {
    sm: "px-4 py-2 text-sm",
    md: "px-6 py-3",
    lg: "px-8 py-4 text-lg"
  };

  const handleClick = () => {
    if (!loading && !disabled && onClick) {
      onClick();
    }
  };

  return (
    <motion.button
      whileHover={loading || disabled ? {} : { scale: 1.02 }}
      whileTap={loading || disabled ? {} : { scale: 0.98 }}
      className={cn(
        baseClasses,
        variants[variant],
        sizes[size],
        (disabled || loading) && "opacity-50 cursor-not-allowed transform-none hover:scale-100",
        className
      )}
      onClick={handleClick}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <div className="mr-2">
          <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
        </div>
      )}
      {children}
    </motion.button>
  );
};

export default Button;
