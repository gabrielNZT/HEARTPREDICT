import { useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import styles from './ConversationalForm.module.css';

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
      className={`animate-fade-in ${styles.chatWindowContainer}`}
    >
      <div className="chatWindowGradientTop" />

      {messages.map((msg, idx) => (
        <MessageBubble 
          key={idx} 
          message={msg.text} 
          sender={msg.sender}
          isError={msg.error}
          isStructured={msg.isStructured}
          animationDelay={idx * 100}
        />
      ))}

      {children}

      <div className="chatWindowGradientBottom" />
    </div>
  );
}
