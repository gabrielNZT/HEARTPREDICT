import { useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';

export function ChatWindow({ messages, children }) {
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTo({
        top: chatRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [messages]);

  return (
    <div 
      ref={chatRef}
      className="animate-fade-in"
      style={{
        maxHeight: 'calc(100vh - 300px)',
        minHeight: '300px',
        overflowY: 'auto',
        padding: 'var(--space-4)',
        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
        borderRadius: 'var(--radius-xl)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        backdropFilter: 'blur(10px)',
        boxShadow: 'inset 0 2px 8px rgba(24, 144, 255, 0.1)',
        scrollbarWidth: 'thin',
        scrollbarColor: 'rgba(24, 144, 255, 0.3) transparent',
        position: 'relative'
      }}
    >
      {/* Gradiente sutil no topo */}
      <div style={{
        position: 'sticky',
        top: 0,
        height: '20px',
        background: 'linear-gradient(180deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%)',
        marginBottom: 'var(--space-2)',
        pointerEvents: 'none',
        borderRadius: 'var(--radius-xl) var(--radius-xl) 0 0'
      }} />

      {messages.map((msg, idx) => (
        <MessageBubble 
          key={idx} 
          message={msg.text} 
          sender={msg.sender}
          isError={msg.error}
          animationDelay={idx * 100}
        />
      ))}
      
      {children}

      {/* Gradiente sutil no bottom */}
      <div style={{
        position: 'sticky',
        bottom: 0,
        height: '20px',
        background: 'linear-gradient(0deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%)',
        marginTop: 'var(--space-2)',
        pointerEvents: 'none',
        borderRadius: '0 0 var(--radius-xl) var(--radius-xl)'
      }} />
    </div>
  );
}
