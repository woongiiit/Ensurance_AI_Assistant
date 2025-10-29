'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Plus, MessageSquare, Menu, X, Settings } from 'lucide-react'
import Link from 'next/link'

interface Conversation {
  id: string
  title: string
  messages: Array<{id: string, role: 'user' | 'ai', content: string}>
  createdAt: Date
  updatedAt: Date
}

export default function ChatPage() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Array<{id: string, role: 'user' | 'ai', content: string}>>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // 자동 높이 조절
  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }

  useEffect(() => {
    adjustTextareaHeight()
  }, [input])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e as any)
    }
  }

  // 새 대화 시작
  const startNewConversation = () => {
    setCurrentConversationId(null)
    setMessages([])
    setInput('')
    setError(null)
    setSidebarOpen(false)
  }

  // 대화 로드
  const loadConversation = (conversationId: string) => {
    const conversation = conversations.find(c => c.id === conversationId)
    if (conversation) {
      setCurrentConversationId(conversationId)
      setMessages(conversation.messages)
      setInput('')
      setError(null)
      setSidebarOpen(false)
    }
  }

  // 대화 제목 생성 (첫 번째 사용자 메시지 기반)
  const generateConversationTitle = (firstMessage: string) => {
    return firstMessage.length > 30 ? firstMessage.substring(0, 30) + '...' : firstMessage
  }

  // 대화 저장
  const saveConversation = (messagesToSave: Array<{id: string, role: 'user' | 'ai', content: string}>) => {
    if (messagesToSave.length === 0) return

    const firstUserMessage = messagesToSave.find(m => m.role === 'user')
    if (!firstUserMessage) return

    const conversationId = currentConversationId || Date.now().toString()
    const title = generateConversationTitle(firstUserMessage.content)
    
    const conversation: Conversation = {
      id: conversationId,
      title,
      messages: messagesToSave,
      createdAt: currentConversationId ? 
        conversations.find(c => c.id === currentConversationId)?.createdAt || new Date() : 
        new Date(),
      updatedAt: new Date()
    }

    if (currentConversationId) {
      // 기존 대화 업데이트
      setConversations(prev => 
        prev.map(c => c.id === currentConversationId ? conversation : c)
      )
    } else {
      // 새 대화 추가
      setConversations(prev => [conversation, ...prev])
      setCurrentConversationId(conversationId)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    setError(null)
    setMessages(prev => [...prev, { id: Date.now().toString(), role: 'user', content: userMessage }])
    setIsLoading(true)

    const aiMessageId = (Date.now() + 1).toString()
    setMessages(prev => [...prev, { id: aiMessageId, role: 'ai', content: '' }])

    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      })

      if (response.ok) {
        const data = await response.json()
        const updatedMessages = messages.map(msg => 
          msg.id === aiMessageId 
            ? { ...msg, content: data.content || '응답을 받았지만 내용이 비어있습니다.' }
            : msg
        )
        setMessages(updatedMessages)
        // 대화 저장
        saveConversation(updatedMessages)
      } else {
        const errorText = await response.text()
        setError(`서버 오류 (${response.status}): ${errorText}`)
        const errorMessages = messages.map(msg => 
          msg.id === aiMessageId 
            ? { ...msg, content: '죄송합니다. 서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요.' }
            : msg
        )
        setMessages(errorMessages)
        // 에러 메시지도 저장
        saveConversation(errorMessages)
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      setError(`연결 오류: ${errorMessage}`)
      const errorMessages = messages.map(msg => 
        msg.id === aiMessageId 
          ? { ...msg, content: '네트워크 연결에 문제가 있습니다. 인터넷 연결을 확인하고 다시 시도해주세요.' }
          : msg
      )
      setMessages(errorMessages)
      // 에러 메시지도 저장
      saveConversation(errorMessages)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      {/* Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 flex-shrink-0`}>
        <div className="flex flex-col h-full min-h-0">
          {/* Sidebar Header */}
          <div className="flex items-center justify-between p-4 border-b flex-shrink-0">
            <h2 className="text-lg font-semibold text-gray-900">대화 내역</h2>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-1 rounded-md hover:bg-gray-100"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* New Chat Button */}
          <div className="p-4 flex-shrink-0">
            <button
              onClick={startNewConversation}
              className="w-full flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>새 대화</span>
            </button>
          </div>

          {/* Conversations List */}
          <div className="flex-1 overflow-y-auto px-4 pb-4 min-h-0">
            {conversations.length === 0 ? (
              <div className="text-center text-gray-500 py-8">
                <MessageSquare className="w-8 h-8 mx-auto mb-2 text-gray-400" />
                <p className="text-sm">아직 대화가 없습니다</p>
              </div>
            ) : (
              <div className="space-y-2">
                {conversations.map((conversation) => (
                  <button
                    key={conversation.id}
                    onClick={() => loadConversation(conversation.id)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      currentConversationId === conversation.id
                        ? 'bg-blue-50 text-blue-700 border border-blue-200'
                        : 'hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    <div className="font-medium text-sm truncate mb-1">
                      {conversation.title}
                    </div>
                    <div className="text-xs text-gray-500">
                      {conversation.updatedAt.toLocaleDateString('ko-KR')}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
        {/* Mobile Header */}
        <div className="lg:hidden flex items-center justify-between p-4 bg-white border-b flex-shrink-0">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 rounded-md hover:bg-gray-100"
          >
            <Menu className="w-5 h-5" />
          </button>
          <h1 className="text-lg font-semibold text-gray-900">보험 약관 AI 챗봇</h1>
          <Link
            href="/admin/login"
            className="p-2 rounded-md hover:bg-gray-100"
            title="관리자 로그인"
          >
            <Settings className="w-5 h-5 text-gray-600" />
          </Link>
        </div>

        <div className="flex-1 flex flex-col w-full p-4 sm:p-6 min-h-0 overflow-hidden">
          {/* Desktop Header */}
          <div className="hidden lg:block bg-white shadow-sm p-6 mb-6 flex-shrink-0">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                  보험 약관 AI 챗봇
                </h1>
                <p className="text-base text-gray-600">
                  보험 약관에 대해 궁금한 점을 물어보세요. AI가 문서를 기반으로 정확한 답변을 제공합니다.
                </p>
              </div>
              <Link
                href="/admin/login"
                className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Settings className="w-4 h-4" />
                <span>관리자 로그인</span>
              </Link>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 p-4 mb-6 flex-shrink-0">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">오류가 발생했습니다</h3>
                  <p className="mt-1 text-sm text-red-700">{error}</p>
                  <button
                    onClick={() => setError(null)}
                    className="mt-2 text-sm text-red-600 hover:text-red-500 underline"
                  >
                    닫기
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Chat Messages */}
          <div className="bg-white shadow-sm p-6 mb-6 flex-1 min-h-0 overflow-y-auto">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full text-gray-500">
                <div className="text-center px-4">
                  <Bot className="w-8 h-8 sm:w-12 sm:h-12 mx-auto mb-4 text-gray-400" />
                  <p className="text-sm sm:text-base">안녕하세요! 보험 약관에 대해 질문해주세요.</p>
                </div>
              </div>
            ) : (
              <div className="space-y-3 sm:space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`flex items-start space-x-2 sm:space-x-3 max-w-[90%] sm:max-w-[85%] ${
                        message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                      }`}
                    >
                      <div
                        className={`w-6 h-6 sm:w-8 sm:h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                          message.role === 'user'
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200 text-gray-600'
                        }`}
                      >
                        {message.role === 'user' ? (
                          <User className="w-3 h-3 sm:w-4 sm:h-4" />
                        ) : (
                          <Bot className="w-3 h-3 sm:w-4 sm:h-4" />
                        )}
                      </div>
                      <div
                        className={`px-3 py-2 sm:px-4 sm:py-3 rounded-lg text-sm sm:text-base ${
                          message.role === 'user'
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-100 text-gray-900'
                        }`}
                      >
                        <p className="whitespace-pre-wrap break-words">{message.content}</p>
                      </div>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="flex items-start space-x-2 sm:space-x-3 max-w-[90%] sm:max-w-[85%]">
                      <div className="w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center flex-shrink-0">
                        <Bot className="w-3 h-3 sm:w-4 sm:h-4" />
                      </div>
                      <div className="px-3 py-2 sm:px-4 sm:py-3 rounded-lg bg-gray-100 text-gray-900">
                        <div className="flex items-center space-x-2">
                          <span className="text-sm text-gray-600">AI가 답변을 생성하고 있습니다</span>
                          <div className="flex space-x-1">
                            <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gray-400 rounded-full animate-bounce"></div>
                            <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                            <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Chat Input */}
          <div className="bg-white shadow-sm p-6 flex-shrink-0">
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 sm:gap-4">
              <div className="flex-1 relative">
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => {
                    if (e.target.value.length <= 500) {
                      setInput(e.target.value)
                    }
                  }}
                  onKeyDown={handleKeyDown}
                  placeholder="보험 약관에 대해 질문해주세요... (Enter: 전송, Shift+Enter: 줄바꿈)"
                  className="w-full px-3 py-2 sm:px-4 sm:py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[44px] max-h-[120px] text-sm sm:text-base"
                  disabled={isLoading}
                  rows={1}
                />
                <div className={`absolute bottom-2 right-2 text-xs ${
                  input.length > 450 ? 'text-red-500' : 'text-gray-400'
                }`}>
                  {input.length}/500
                </div>
              </div>
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="px-4 py-2 sm:px-6 sm:py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 min-h-[44px] sm:min-h-[48px]"
              >
                <Send className="w-4 h-4" />
                <span className="hidden sm:inline">전송</span>
              </button>
            </form>
            <div className="mt-2 text-xs text-gray-500">
              💡 팁: Enter로 전송, Shift+Enter로 줄바꿈
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}