import React, { useState, useRef } from 'react';

export const TiltCard = ({ title, difficulty, description, techStack }) => {
  const cardRef = useRef(null);
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);

  const handleMouseMove = (e) => {
    if (!cardRef.current) return;
    const card = cardRef.current;
    const rect = card.getBoundingClientRect();
    
    const width = rect.width;
    const height = rect.height;
    const mouseX = e.clientX - rect.left - width / 2;
    const mouseY = e.clientY - rect.top - height / 2;

    // Scale rotation mapping (Max 15 degrees)
    const rY = (mouseX / (width / 2)) * 15;
    const rX = -(mouseY / (height / 2)) * 15;

    setRotateX(rX);
    setRotateY(rY);
  };

  const handleMouseLeave = () => {
    setRotateX(0);
    setRotateY(0);
  };

  return (
    <div style={{ perspective: 1000 }} className="w-full max-w-sm">
      <div
        ref={cardRef}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        style={{
          transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
          transition: 'transform 0.1s ease-out',
        }}
        className="relative group bg-slate-900/80 border border-cyan-500/30 rounded-lg p-6 backdrop-blur-md shadow-[0_0_15px_rgba(6,182,212,0.1)] hover:border-cyan-400 hover:shadow-[0_0_25px_rgba(6,182,212,0.3)] transition-colors duration-300 cursor-pointer"
      >
        <div className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-cyan-400" />
        <div className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2 border-cyan-400" />

        <div className="flex justify-between items-center mb-4">
          <span className="text-xs font-mono text-cyan-400 tracking-widest uppercase">Quest // Active</span>
          <span className="text-xs font-mono text-purple-400 border border-purple-500/30 px-2 py-0.5 rounded bg-purple-950/40">
            {difficulty}
          </span>
        </div>

        <h3 className="text-xl font-bold text-white tracking-wide group-hover:text-cyan-300 transition-colors duration-300 mb-2">
          {title}
        </h3>
        
        <p className="text-slate-400 text-sm font-sans mb-4 leading-relaxed">
          {description}
        </p>

        <div className="border-t border-slate-800 pt-3 flex flex-wrap gap-2">
          {techStack.map((tech) => (
            <span key={tech} className="text-xs font-mono text-slate-400 bg-slate-800/60 px-2 py-1 rounded">
              {tech}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};