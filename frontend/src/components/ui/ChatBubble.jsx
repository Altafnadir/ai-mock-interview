import React from 'react';
import { Bot, User } from 'lucide-react';
import Avatar from './Avatar';

export default function ChatBubble({
  role = 'assistant', // user | assistant
  content = '',
  timestamp,
  userAvatar,
  userName,
  loading = false,
  className = '',
}) {
  const isUser = role === 'user';

  return (
    <div className={`flex gap-3 items-start ${isUser ? 'flex-row-reverse' : 'flex-row'} ${className}`}>
      {/* Avatar */}
      <div className="shrink-0 mt-0.5">
        {isUser ? (
          <Avatar name={userName || 'User'} size="sm" src={userAvatar} />
        ) : (
          <div className="w-8 h-8 rounded-full bg-indigo-600 dark:bg-indigo-500 text-white flex items-center justify-center shadow-sm">
            <Bot className="w-4 h-4" />
          </div>
        )}
      </div>

      {/* Bubble Content */}
      <div className={`max-w-[82%] sm:max-w-[75%] flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`px-4 py-3 rounded-2xl text-xs sm:text-sm leading-relaxed shadow-xs ${
            isUser
              ? 'bg-indigo-600 text-white rounded-tr-xs'
              : 'bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700 text-slate-800 dark:text-slate-100 rounded-tl-xs'
          }`}
        >
          {loading ? (
            <div className="flex items-center gap-1.5 py-1 px-1">
              <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: '0ms' }} />
              <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: '150ms' }} />
              <span className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          ) : (
            <div className="whitespace-pre-line space-y-1">
              {content}
            </div>
          )}
        </div>

        {timestamp && (
          <span className="text-[10px] text-slate-400 dark:text-slate-500 mt-1 px-1">
            {timestamp}
          </span>
        )}
      </div>
    </div>
  );
}
