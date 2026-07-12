import React from 'react';

interface KavanLogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl' | number;
  showText?: boolean;
  textClassName?: string;
  roleBg?: string; // Optional role-specific accent background
}

export const KavanLogo: React.FC<KavanLogoProps> = ({ 
  size = 'md', 
  showText = false, 
  textClassName = '',
  roleBg
}) => {
  const sizeMap = {
    sm: 24,
    md: 32,
    lg: 48,
    xl: 64,
  };

  const pixelSize = typeof size === 'number' ? size : sizeMap[size] || 32;

  return (
    <div className="flex items-center gap-2.5 select-none">
      {/* KAVAN Shield Icon */}
      <div 
        className="relative flex items-center justify-center flex-shrink-0"
        style={{ width: pixelSize, height: pixelSize }}
      >
        <svg 
          viewBox="0 0 24 24" 
          className="w-full h-full drop-shadow-[0_2px_8px_rgba(239,68,68,0.25)] transition-transform hover:scale-105"
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="kavanShieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#ef4444" />
              <stop offset="100%" stopColor="#b91c1c" />
            </linearGradient>
          </defs>
          {/* Outer Shield with Red Gradient */}
          <path 
            d="M12 2L3 5.5v5.8c0 5.4 3.8 10.4 9 11.7 5.2-1.3 9-6.3 9-11.7V5.5L12 2z" 
            fill="url(#kavanShieldGrad)" 
            stroke="#ffffff"
            strokeWidth="1.25"
          />
          {/* Inner Shield Overlay for Depth */}
          <path 
            d="M12 4L5 6.7v4.6c0 4.3 3 8.3 7 9.4 4-1.1 7-5.1 7-9.4V6.7L12 4z" 
            fill="#090d16" 
            opacity="0.8"
          />
          {/* Subtle Inner Glow Border */}
          <path 
            d="M12 5L6 7.3v4c0 3.7 2.6 7.1 6 8 3.4-.9 6-4.3 6-8v-4L12 5z" 
            stroke="#ef4444" 
            strokeWidth="0.75" 
            strokeOpacity="0.4"
            fill="none"
          />
          {/* Brand letter 'K' styled elegantly inside the shield */}
          <text 
            x="12" 
            y="15.5" 
            fill="#ffffff" 
            fontSize="9" 
            fontWeight="900" 
            textAnchor="middle" 
            fontFamily="'Outfit', 'Inter', system-ui, sans-serif"
            className="animate-pulse"
            style={{ animationDuration: '3s' }}
          >
            K
          </text>
        </svg>
      </div>

      {/* KAVAN Typography */}
      {showText && (
        <div className={`flex flex-col ${textClassName}`}>
          <div className="flex items-center text-xl font-black tracking-tight leading-none">
            <span className="text-foreground">KAV</span>
            <span className="text-[#ef4444]">AN</span>
          </div>
          <span className="text-[9px] text-muted-foreground uppercase font-mono tracking-widest -mt-0.5">
            Enterprise RBAC
          </span>
        </div>
      )}
    </div>
  );
};

export default KavanLogo;
