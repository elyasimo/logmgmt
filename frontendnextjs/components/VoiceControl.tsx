"use client"

import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

const VoiceControl = () => {
  const [isListening, setIsListening] = useState(false)
  const router = useRouter()

  useEffect(() => {
    if (!('webkitSpeechRecognition' in window)) {
      console.log('Speech recognition not supported')
      return
    }

    const recognition = new (window as any).webkitSpeechRecognition()
    recognition.continuous = true
    recognition.interimResults = true

    recognition.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0])
        .map((result) => result.transcript)
        .join('')

      handleCommand(transcript.toLowerCase())
    }

    if (isListening) {
      recognition.start()
    } else {
      recognition.stop()
    }

    return () => {
      recognition.stop()
    }
  }, [isListening])

  const handleCommand = (command: string) => {
    if (command.includes('go to dashboard')) {
      router.push('/')
    } else if (command.includes('show logs')) {
      router.push('/logs')
    } else if (command.includes('open analytics')) {
      router.push('/analytics')
    } else if (command.includes('open settings')) {
      router.push('/settings')
    }
  }

  return (
    <div className="fixed top-4 right-4 z-50">
      <button
        onClick={() => setIsListening(!isListening)}
        className={`p-2 rounded-full ${
          isListening ? 'bg-neon-pink' : 'bg-neon-blue'
        } text-white`}
      >
        {isListening ? 'Stop Listening' : 'Start Voice Control'}
      </button>
    </div>
  )
}

export default VoiceControl

