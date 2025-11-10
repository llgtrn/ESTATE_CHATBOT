import { useEffect, useRef } from 'react';
import { MessageItem } from '@/entities/message/ui/MessageItem';
import { Spinner } from '@/shared/ui';
import type { Message } from '@/entities/message/model/types';

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
  error?: Error | null;
}

export function MessageList({ messages, isLoading, error }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages.length]);

  if (error) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <p className="text-sm text-destructive">
            Error loading messages: {error.message}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="mt-2 text-sm text-primary-600 hover:underline"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (isLoading && messages.length === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center text-gray-500">
          <p className="text-sm">No messages yet</p>
          <p className="mt-1 text-xs">Start a conversation below</p>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="flex h-full flex-col gap-4 overflow-y-auto p-4 scrollbar-hide"
      data-testid="message-list"
    >
      {messages.map((message, index) => (
        <MessageItem
          key={message.message_id}
          message={message}
          isLatest={index === messages.length - 1}
        />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
