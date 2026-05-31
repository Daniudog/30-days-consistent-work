import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TiltCard } from './components/ui/TiltCard';

export default function App() {
  const [gameState, setGameState] = useState('START_SCREEN'); // START_SCREEN | IN_GAME

  return (
    <div className="relative min-h-screen w-full bg-slate-950 text-slate-100 overflow-x-hidden font-mono select-none">
      
      {/* Background Ambience Grid Layers */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_center,rgba(15,23,42,0.8)_0%,rgba(2,6,23,1)_100%)] z-0" />
      <div className="fixed inset-0 bg-[linear-gradient(to_right,#0f172a_1px,transparent_1px),linear-gradient(to_bottom,#0f172a_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-20 z-0" />

      <AnimatePresence mode="wait">
        {gameState === 'START_SCREEN' ? (
          /* MAIN MENU SCREEN */
          <motion.div
            key="main-menu"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, y: -50, scale: 1.05 }}
            transition={{ duration: 0.6, ease: 'easeInOut' }}
            className="relative z-10 flex flex-col items-center justify-center min-h-screen text-center px-4"
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mb-2"
            >
              <span className="text-xs font-mono tracking-[0.5em] text-cyan-500 uppercase">System Initializing... v1.0.4</span>
            </motion.div>

            <motion.h1 
              initial={{ letterSpacing: '0.1em' }}
              animate={{ letterSpacing: '0.25em' }}
              className="text-5xl md:text-7xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-200 to-slate-500 tracking-wider mb-8 uppercase drop-shadow-[0_5px_15px_rgba(0,0,0,0.5)]"
            >
              PORTFOLIO<span className="text-cyan-400">.OS</span>
            </motion.h1>

            <motion.button
              whileHover={{ scale: 1.05, boxShadow: '0 0 20px rgba(6,182,212,0.5)' }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setGameState('IN_GAME')}
              className="relative px-8 py-4 bg-cyan-500/10 border-2 border-cyan-400 rounded text-cyan-400 font-bold text-lg tracking-widest uppercase overflow-hidden transition-all duration-150 shadow-[0_0_10px_rgba(6,182,212,0.2)]"
            >
              <span className="relative z-10">Initialize Session</span>
              <div className="absolute inset-0 bg-cyan-400/10 opacity-0 hover:opacity-100 transition-opacity duration-300" />
            </motion.button>
          </motion.div>
        ) : (
          /* HUD & DASHBOARD LAYOUT */
          <motion.div
            key="dashboard"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
            className="relative z-10 min-h-screen p-6 md:p-12 flex flex-col items-center"
          >
            <header className="w-full max-w-6xl flex justify-between items-center border-b border-slate-800 pb-4 mb-12">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-cyan-500 animate-pulse" />
                <span className="font-bold tracking-wider text-sm">ARCHITECT_HP [100/100]</span>
              </div>
              <nav className="flex gap-6 text-sm text-slate-400">
                <button className="hover:text-cyan-400 transition-colors uppercase">// Quest Log</button>
                <button className="hover:text-cyan-400 transition-colors uppercase">// Skill Tree</button>
                <button 
                  onClick={() => setGameState('START_SCREEN')}
                  className="text-red-400 hover:text-red-300 transition-colors uppercase text-xs border border-red-500/20 px-2 py-0.5 rounded bg-red-950/20"
                >
                  Disconnect
                </button>
              </nav>
            </header>

            <main className="w-full max-w-6xl flex flex-col items-center">
              <div className="text-center mb-10">
                <h2 className="text-3xl font-extrabold text-white tracking-wide uppercase mb-2">Available Mission Objectives</h2>
                <p className="text-slate-400 text-sm">Select a deployment to view engineering files and architecture parameters.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full justify-items-center">
                <TiltCard 
                  title="Project: Overlord"
                  difficulty="LEGENDARY"
                  description="A decentralized cryptographic storage network with client-side zero-knowledge proofs."
                  techStack={['React', 'Rust', 'Wasm', 'Tailwind']}
                />
                <TiltCard 
                  title="Project: CyberSpace"
                  difficulty="ELITE"
                  description="Real-time WebGL financial data modeling pipeline with custom shader interpolation."
                  techStack={['Three.js', 'R3F', 'Zustand']}
                />
                <TiltCard 
                  title="Project: Nexus"
                  difficulty="NORMAL"
                  description="An automated Web3 developer infrastructure gateway orchestrating secure RPC connections."
                  techStack={['Next.js', 'TypeScript', 'Ethers.js']}
                />
              </div>
            </main>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}